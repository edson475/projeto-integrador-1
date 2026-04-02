from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import Config
from database import db
from validadores import Validadores
from datetime import datetime

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY


# =====================================================
# ROTAS PRINCIPAIS
# =====================================================

@app.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')


# =====================================================
# ROTAS DE CADASTRO
# =====================================================

@app.route('/cadastro')
def cadastro():
    """Formulário de novo cadastro"""
    proximo_ref = db.obter_proximo_ref()
    return render_template('cadastro.html', cadastro=None, proximo_ref=proximo_ref)


@app.route('/cadastro/salvar', methods=['POST'])
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
def visualizar_cadastro(ref_id):
    """Visualiza cadastro existente"""
    cadastro = db.buscar_cadastro(ref_id)
    
    if not cadastro:
        flash('Cadastro não encontrado', 'error')
        return redirect(url_for('lista'))
    
    membros = db.obter_membros_familia(ref_id)
    return render_template('cadastro.html', cadastro=cadastro, membros=membros, edicao=False)


@app.route('/cadastro/<int:ref_id>/editar', methods=['GET', 'POST'])
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
def lista():
    """Lista todos os cadastros"""
    cadastros = db.buscar_cadastros()
    return render_template('lista.html', cadastros=cadastros)


# =====================================================
# ROTAS DE FAMÍLIA
# =====================================================

@app.route('/familia/<int:ref_id>', methods=['GET', 'POST'])
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
        'ano': datetime.now().year
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
        print("Acesse: http://127.0.0.1:5000")
        print("="*50 + "\n")
        
        app.run(host='0.0.0.0', port=5000, debug=Config.FLASK_DEBUG)
