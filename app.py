from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from functools import wraps
from werkzeug.security import check_password_hash
from config import Config
from database import db
from validadores import Validadores
from datetime import datetime

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY


# =====================================================
# DECORADOR DE AUTENTICAÇÃO
# =====================================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Por favor, faça login para acessar o sistema.', 'error')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# =====================================================
# ROTAS DE AUTENTICAÇÃO
# =====================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Tela de login"""
    # Se já estiver logado, vai pra home
    if 'usuario_id' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')
        
        usuario = db.buscar_usuario_por_email(email)
        
        if usuario and check_password_hash(usuario.get('senha_hash', ''), senha):
            session['usuario_id'] = usuario['id']
            session['usuario_nome'] = usuario['nome']
            
            proxima_pagina = request.args.get('next')
            return redirect(proxima_pagina or url_for('index'))
            
        flash('E-mail ou senha incorretos.', 'error')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Encerra a sessão"""
    session.clear()
    flash('Sessão encerrada com sucesso.', 'success')
    return redirect(url_for('login'))


# =====================================================
# ROTAS PRINCIPAIS
# =====================================================

@app.route('/')
@login_required
def index():
    """Página inicial"""
    return render_template('index.html')


# =====================================================
# ROTAS DE CADASTRO
# =====================================================

@app.route('/cadastro')
@login_required
def cadastro():
    """Formulário de novo cadastro"""
    proximo_ref = db.obter_proximo_ref()
    return render_template('cadastro.html', cadastro=None, proximo_ref=proximo_ref)


@app.route('/cadastro/salvar', methods=['POST'])
@login_required
def salvar_cadastro():
    """Salva novo cadastro"""
    try:
        # Obter dados do formulário
        dados = {
            'nome': request.form.get('nome', '').strip().upper(),
            'cpf': Validadores.apenas_numeros(request.form.get('cpf', '')),
            'rg': request.form.get('rg', '').strip(),
            'nis': Validadores.apenas_numeros(request.form.get('nis', '')),
            'data_nascimento': request.form.get('data_nascimento', '').strip(),
            'email': request.form.get('email', '').strip().lower(),
            'telefone': request.form.get('telefone', '').strip(),
            'cep': Validadores.apenas_numeros(request.form.get('cep', '')),
            'endereco': request.form.get('endereco', '').strip().upper(),
            'numero': request.form.get('numero', '').strip(),
            'complemento': request.form.get('complemento', '').strip().upper(),
            'bairro': request.form.get('bairro', '').strip().upper(),
            'cidade': request.form.get('cidade', '').strip().upper(),
            'estado': request.form.get('estado', '').strip().upper(),
            'prioritario': request.form.get('prioritario') == 'on'
        }
        
        # Validações
        erros = []
        
        if not dados['nome']:
            erros.append('Nome é obrigatório')
        
        if dados['cpf'] and not Validadores.validar_cpf(dados['cpf']):
            erros.append('CPF inválido')

        if dados['rg'] and not Validadores.validar_rg(dados['rg']):
            erros.append('RG inválido.')
        
        if dados['nis'] and not Validadores.validar_nis(dados['nis']):
            erros.append('NIS inválido')
        
        if dados['data_nascimento'] and not Validadores.validar_data(dados['data_nascimento']):
            erros.append('Data de nascimento inválida. Use DD/MM/YYYY')
        
        if dados['email'] and not Validadores.validar_email(dados['email']):
            erros.append('E-mail inválido')
        
        if erros:
            for erro in erros:
                flash(erro, 'error')
            return redirect(url_for('cadastro'))
        
        # Salvar no banco
        ref_id, sucesso = db.inserir_cadastro(dados)
        
        if sucesso:
            flash(f'Cadastro salvo com sucesso! REF: {ref_id}', 'success')
            return redirect(url_for('visualizar_cadastro', ref_id=ref_id))
        else:
            flash('Erro ao salvar cadastro. Tente novamente.', 'error')
            return redirect(url_for('cadastro'))
            
    except Exception as e:
        flash(f'Erro inesperado: {str(e)}', 'error')
        return redirect(url_for('cadastro'))


@app.route('/cadastro/<int:ref_id>')
@login_required
def visualizar_cadastro(ref_id):
    """Visualiza cadastro existente"""
    cadastro = db.buscar_cadastro(ref_id)
    
    if not cadastro:
        flash('Cadastro não encontrado', 'error')
        return redirect(url_for('lista'))
    
    membros = db.obter_membros_familia(ref_id)
    return render_template('cadastro.html', cadastro=cadastro, membros=membros, edicao=False)


@app.route('/cadastro/<int:ref_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_cadastro(ref_id):
    """Edita cadastro existente"""
    if request.method == 'GET':
        cadastro = db.buscar_cadastro(ref_id)
        
        if not cadastro:
            flash('Cadastro não encontrado', 'error')
            return redirect(url_for('lista'))
        
        return render_template('cadastro.html', cadastro=cadastro, edicao=True)
    
    else:  # POST
        try:
            # Obter dados do formulário
            dados = {
                'nome': request.form.get('nome', '').strip().upper(),
                'cpf': Validadores.apenas_numeros(request.form.get('cpf', '')),
                'rg': request.form.get('rg', '').strip(),
                'nis': Validadores.apenas_numeros(request.form.get('nis', '')),
                'data_nascimento': request.form.get('data_nascimento', '').strip(),
                'email': request.form.get('email', '').strip().lower(),
                'telefone': request.form.get('telefone', '').strip(),
                'cep': Validadores.apenas_numeros(request.form.get('cep', '')),
                'endereco': request.form.get('endereco', '').strip().upper(),
                'numero': request.form.get('numero', '').strip(),
                'complemento': request.form.get('complemento', '').strip().upper(),
                'bairro': request.form.get('bairro', '').strip().upper(),
                'cidade': request.form.get('cidade', '').strip().upper(),
                'estado': request.form.get('estado', '').strip().upper(),
                'prioritario': request.form.get('prioritario') == 'on'
            }
            
            # Validações
            erros = []
            
            if not dados['nome']:
                erros.append('Nome é obrigatório')
            
            if dados['cpf'] and not Validadores.validar_cpf(dados['cpf']):
                erros.append('CPF inválido')

            if dados['rg'] and not Validadores.validar_rg(dados['rg']):
                erros.append('RG inválido.')
            
            if dados['nis'] and not Validadores.validar_nis(dados['nis']):
                erros.append('NIS inválido')
            
            if dados['data_nascimento'] and not Validadores.validar_data(dados['data_nascimento']):
                erros.append('Data de nascimento inválida. Use DD/MM/YYYY')
            
            if erros:
                for erro in erros:
                    flash(erro, 'error')
                return redirect(url_for('editar_cadastro', ref_id=ref_id))
            
            # Atualizar no banco
            sucesso = db.atualizar_cadastro(ref_id, dados)
            
            if sucesso:
                flash('Cadastro atualizado com sucesso!', 'success')
                return redirect(url_for('visualizar_cadastro', ref_id=ref_id))
            else:
                flash('Erro ao atualizar cadastro.', 'error')
                return redirect(url_for('editar_cadastro', ref_id=ref_id))
                
        except Exception as e:
            flash(f'Erro inesperado: {str(e)}', 'error')
            return redirect(url_for('editar_cadastro', ref_id=ref_id))


@app.route('/cadastro/<int:ref_id>/excluir', methods=['POST'])
@login_required
def excluir_cadastro(ref_id):
    """Exclui cadastro"""
    try:
        sucesso = db.excluir_cadastro(ref_id)
        
        if sucesso:
            flash('Cadastro excluído com sucesso!', 'success')
        else:
            flash('Erro ao excluir cadastro.', 'error')
            
    except Exception as e:
        flash(f'Erro ao excluir: {str(e)}', 'error')
    
    return redirect(url_for('lista'))


# =====================================================
# ROTAS DE PESQUISA
# =====================================================

@app.route('/pesquisa', methods=['GET', 'POST'])
@login_required
def pesquisa():
    """Pesquisa de cadastros"""
    resultados = []
    termo = ''
    
    if request.method == 'POST':
        termo = request.form.get('termo', '').strip()
        
        if termo:
            # Buscar no cadastro principal
            resultados = db.buscar_cadastros(termo)
            
            # Se não encontrou, buscar por membro da família
            if not resultados:
                resultados = db.buscar_por_membro_familia(termo)
            
            if not resultados:
                flash('Nenhum resultado encontrado', 'info')
    
    return render_template('pesquisa.html', resultados=resultados, termo=termo)


# =====================================================
# ROTAS DE LISTA
# =====================================================

@app.route('/lista')
@login_required
def lista():
    """Lista todos os cadastros"""
    cadastros = db.buscar_cadastros()
    return render_template('lista.html', cadastros=cadastros)


# =====================================================
# ROTAS DE FAMÍLIA
# =====================================================

@app.route('/familia/<int:ref_id>', methods=['GET', 'POST'])
@login_required
def gerenciar_familia(ref_id):
    """Gerencia composição familiar"""
    cadastro = db.buscar_cadastro(ref_id)
    
    if not cadastro:
        flash('Cadastro não encontrado', 'error')
        return redirect(url_for('lista'))
    
    if request.method == 'POST':
        # Adicionar membro
        nome = request.form.get('nome_membro', '').strip().upper()
        data_nascimento = request.form.get('data_nascimento_membro', '').strip()
        vinculo = request.form.get('vinculo', '').strip()
        titular = request.form.get('titular') == 'on'
        
        if not nome:
            flash('Nome do membro é obrigatório', 'error')
        elif not Validadores.validar_data(data_nascimento):
            flash('Data de nascimento inválida', 'error')
        else:
            sucesso = db.adicionar_membro_familia(ref_id, nome, data_nascimento, vinculo, titular)
            
            if sucesso:
                flash('Membro adicionado com sucesso!', 'success')
            else:
                flash('Erro ao adicionar membro', 'error')
        
        return redirect(url_for('gerenciar_familia', ref_id=ref_id))
    
    # GET - exibir formulário
    membros = db.obter_membros_familia(ref_id)
    return render_template('familia.html', cadastro=cadastro, membros=membros)


@app.route('/familia/membro/<int:membro_id>/excluir', methods=['POST'])
@login_required
def excluir_membro(membro_id):
    """Exclui membro da família"""
    try:
        # Precisamos obter o ref_id para redirecionar depois
        # Vamos buscar todos os membros e encontrar o ref_id
        sucesso = db.remover_membro_familia(membro_id)
        
        if sucesso:
            flash('Membro removido com sucesso!', 'success')
        else:
            flash('Erro ao remover membro', 'error')
            
    except Exception as e:
        flash(f'Erro ao remover: {str(e)}', 'error')
    
    # Redirecionar de volta para a página de família
    # Precisamos passar o ref_id, vamos buscar no banco
    return redirect(url_for('lista'))  # Simplificado - volta para lista


# =====================================================
# ROTAS DE PRONTUÁRIO
# =====================================================

@app.route('/prontuario/<int:ref_id>')
@login_required
def prontuario(ref_id):
    """Visualiza e manipula o dossiê Prontuário SUAS"""
    cadastro = db.buscar_cadastro(ref_id)
    if not cadastro:
        flash('Cadastro não encontrado', 'error')
        return redirect(url_for('lista'))
        
    prontuario = db.buscar_prontuario_por_cadastro(ref_id)
    
    if not prontuario:
        # Família sem prontuário, mostra opção para abrir
        return render_template('prontuario.html', cadastro=cadastro, prontuario=None)
        
    # Busca atendimentos e encaminhamentos
    atendimentos = db.obter_atendimentos_do_prontuario(prontuario['id'])
    
    for at in atendimentos:
        at['encaminhamentos'] = db.obter_encaminhamentos_do_atendimento(at['id'])
        
    return render_template('prontuario.html', cadastro=cadastro, prontuario=prontuario, atendimentos=atendimentos)

@app.route('/prontuario/<int:ref_id>/abrir', methods=['POST'])
@login_required
def abrir_prontuario(ref_id):
    servico = request.form.get('servico_vinculado', '')
    motivo = request.form.get('motivo_procura', '')
    
    dados = {
        'cadastro_ref_id': ref_id,
        'tecnico_id': session.get('usuario_id'),
        'servico_vinculado': servico,
        'motivo_procura': motivo,
        'data_abertura': datetime.now().strftime('%Y-%m-%d')
    }
    
    p_id, sucesso = db.criar_prontuario(dados)
    if sucesso:
        flash('Prontuário aberto com sucesso!', 'success')
    else:
        flash('Erro ao abrir prontuário.', 'error')
        
    return redirect(url_for('prontuario', ref_id=ref_id))

@app.route('/prontuario/<int:prontuario_id>/atendimento/novo', methods=['GET', 'POST'])
@login_required
def novo_atendimento(prontuario_id):
    prontuario = db.buscar_prontuario(prontuario_id)
    if not prontuario:
        flash('Prontuário não encontrado', 'error')
        return redirect(url_for('lista'))
        
    cadastro = db.buscar_cadastro(prontuario['cadastro_ref_id'])
    
    if request.method == 'POST':
        tipo = request.form.get('tipo_atendimento')
        demanda = request.form.get('demanda')
        descricao = request.form.get('descricao')
        gerar_encaminhamento = request.form.get('gerar_encaminhamento') == 'on'
        
        dados = {
            'prontuario_id': prontuario_id,
            'tecnico_id': session.get('usuario_id'),
            'tipo_atendimento': tipo,
            'demanda': demanda,
            'descricao': descricao,
            'data_atendimento': datetime.now().strftime('%Y-%m-%d')
        }
        
        atendente_id, sucesso = db.registrar_atendimento(dados)
        
        if sucesso:
            flash('Atendimento registrado com sucesso', 'success')
            if gerar_encaminhamento:
                return redirect(url_for('novo_encaminhamento', atendimento_id=atendente_id))
            return redirect(url_for('prontuario', ref_id=prontuario['cadastro_ref_id']))
        else:
            flash('Erro ao registrar atendimento', 'error')
            
    return render_template('novo_atendimento.html', prontuario=prontuario, cadastro=cadastro)

@app.route('/atendimento/<int:atendimento_id>/encaminhamento/novo', methods=['GET', 'POST'])
@login_required
def novo_encaminhamento(atendimento_id):
    atendimento = db.buscar_atendimento(atendimento_id)
    if not atendimento:
        flash('Atendimento não encontrado', 'error')
        return redirect(url_for('lista'))
        
    prontuario = db.buscar_prontuario(atendimento['prontuario_id'])
    cadastro = db.buscar_cadastro(prontuario['cadastro_ref_id'])
    
    if request.method == 'POST':
        servico = request.form.get('servico_destino')
        motivo = request.form.get('motivo')
        
        dados = {
            'atendimento_id': atendimento_id,
            'servico_destino': servico,
            'motivo': motivo,
            'status': 'Pendente'
        }
        
        _, sucesso = db.registrar_encaminhamento(dados)
        
        if sucesso:
            flash('Encaminhamento registrado com sucesso', 'success')
        else:
            flash('Erro ao registrar encaminhamento', 'error')
            
        return redirect(url_for('prontuario', ref_id=prontuario['cadastro_ref_id']))
        
    historico = db.obter_encaminhamentos_do_prontuario(prontuario['id'])
        
    return render_template('novo_encaminhamento.html', atendimento=atendimento, prontuario=prontuario, cadastro=cadastro, historico=historico)

@app.route('/encaminhamento/<int:enc_id>/concluir', methods=['POST'])
@login_required
def concluir_encaminhamento(enc_id):
    encaminhamento = db.buscar_encaminhamento(enc_id)
    if not encaminhamento:
        flash('Encaminhamento não encontrado', 'error')
        return redirect(url_for('lista'))
        
    atendimento = db.buscar_atendimento(encaminhamento['atendimento_id'])
    prontuario = db.buscar_prontuario(atendimento['prontuario_id'])
    
    sucesso = db.concluir_encaminhamento(enc_id)
    if sucesso:
        flash('Encaminhamento marcado como Realizado', 'success')
    else:
        flash('Erro ao atualizar encaminhamento', 'error')
        
    return redirect(url_for('prontuario', ref_id=prontuario['cadastro_ref_id']))


# =====================================================
# API DE CEP
# =====================================================

@app.route('/api/cep/<cep>')
def buscar_cep(cep):
    """Busca CEP na ViaCEP"""
    import requests
    
    cep_limpo = Validadores.apenas_numeros(cep)
    
    if len(cep_limpo) != 8:
        return jsonify({'erro': 'CEP inválido'})
    
    try:
        response = requests.get(f'https://viacep.com.br/ws/{cep_limpo}/json/')
        dados = response.json()
        
        if 'erro' not in dados:
            return jsonify({
                'cep': dados.get('cep', ''),
                'logradouro': dados.get('logradouro', ''),
                'bairro': dados.get('bairro', ''),
                'localidade': dados.get('localidade', ''),
                'uf': dados.get('uf', '')
            })
        else:
            return jsonify({'erro': 'CEP não encontrado'})
            
    except Exception as e:
        return jsonify({'erro': str(e)})


# =====================================================
# CONFIGURAÇÃO E INICIALIZAÇÃO
# =====================================================

@app.context_processor
def injetar_configuracoes():
    """Injeta variáveis nos templates"""
    return {
        'app_name': 'Sistema de Cadastro',
        'ano': datetime.now().year,
        'usuario_logado': session.get('usuario_nome')
    }


if __name__ == '__main__':
    # Validar configurações antes de iniciar
    erros_config = Config.validate()
    
    if erros_config:
        print("\n" + "="*50)
        print("ERROS DE CONFIGURAÇÃO:")
        for erro in erros_config:
            print(f"  ✗ {erro}")
        print("="*50)
        print("\nCopie o arquivo .env.example para .env e preencha as configurações do Supabase.")
        print("Veja o README.md para instruções detalhadas.\n")
    else:
        print("\n" + "="*50)
        print("SISTEMA DE CADASTRO - ASSISTÊNCIA SOCIAL")
        print("="*50)
        print("Iniciando servidor...")
        print("Acesse: http://127.0.0.1:5001")
        print("="*50 + "\n")
        
        app.run(host='0.0.0.0', port=5001, debug=Config.FLASK_DEBUG)
