"""
Models do sistema - Definições de estrutura de dados

Este arquivo contém as classes que representam as estruturas
de dados usadas no sistema, mapeando para as tabelas do Supabase.
"""

from datetime import datetime


class Cadastro:
    """Modelo de Cadastro"""
    
    def __init__(self, dados=None):
        self.id = None
        self.ref_id = None
        self.nome = ""
        self.data_ref = ""
        self.nis = ""
        self.rg = ""
        self.endereco = ""
        self.numero = ""
        self.complemento = ""
        self.bairro = ""
        self.cidade = ""
        self.estado = ""
        self.cep = ""
        self.telefone = ""
        self.cpf = ""
        self.data_nascimento = ""
        self.email = ""
        self.prioritario = False
        self.created_at = None
        self.updated_at = None
        
        if dados:
            self.carregar(dados)
    
    def carregar(self, dados):
        """Carrega dados do dicionário"""
        self.id = dados.get('id')
        self.ref_id = dados.get('ref_id')
        self.nome = dados.get('nome', '')
        self.data_ref = dados.get('data_ref', '')
        self.nis = dados.get('nis', '')
        self.rg = dados.get('rg', '')
        self.endereco = dados.get('endereco', '')
        self.numero = dados.get('numero', '')
        self.complemento = dados.get('complemento', '')
        self.bairro = dados.get('bairro', '')
        self.cidade = dados.get('cidade', '')
        self.estado = dados.get('estado', '')
        self.cep = dados.get('cep', '')
        self.telefone = dados.get('telefone', '')
        self.cpf = dados.get('cpf', '')
        self.data_nascimento = dados.get('data_nascimento', '')
        self.email = dados.get('email', '')
        self.prioritario = dados.get('prioritario', False)
        self.created_at = dados.get('created_at')
        self.updated_at = dados.get('updated_at')
    
    def para_dict(self):
        """Converte para dicionário"""
        return {
            'ref_id': self.ref_id,
            'nome': self.nome,
            'nis': self.nis,
            'rg': self.rg,
            'endereco': self.endereco,
            'numero': self.numero,
            'complemento': self.complemento,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'estado': self.estado,
            'cep': self.cep,
            'telefone': self.telefone,
            'cpf': self.cpf,
            'data_nascimento': self.data_nascimento,
            'email': self.email,
            'prioritario': self.prioritario
        }
    
    def nome_formatado(self):
        """Retorna nome formatado"""
        return self.nome.upper() if self.nome else ""
    
    def __repr__(self):
        return f"Cadastro(REF={self.ref_id}, Nome={self.nome})"


class MembroFamilia:
    """Modelo de Membro da Família"""
    
    def __init__(self, dados=None):
        self.id = None
        self.ref_id = None
        self.nome = ""
        self.data_nascimento = ""
        self.vinculo = ""
        self.titular = False
        self.created_at = None
        
        if dados:
            self.carregar(dados)
    
    def carregar(self, dados):
        """Carrega dados do dicionário"""
        self.id = dados.get('id')
        self.ref_id = dados.get('ref_id')
        self.nome = dados.get('nome', '')
        self.data_nascimento = dados.get('data_nascimento', '')
        self.vinculo = dados.get('vinculo', '')
        self.titular = dados.get('titular', False)
        self.created_at = dados.get('created_at')
    
    def para_dict(self):
        """Converte para dicionário"""
        return {
            'ref_id': self.ref_id,
            'nome': self.nome,
            'data_nascimento': self.data_nascimento,
            'vinculo': self.vinculo,
            'titular': self.titular
        }
    
    def vinculo_formatado(self):
        """Retorna vínculo formatado"""
        return self.vinculo.capitalize() if self.vinculo else ""
    
    def __repr__(self):
        return f"Membro(Nome={self.nome}, Vínculo={self.vinculo})"


class Prontuario:
    """Modelo de Prontuário SUAS"""
    
    def __init__(self, dados=None):
        self.id = None
        self.cadastro_ref_id = None
        self.tecnico_id = None
        self.data_abertura = ""
        self.servico_vinculado = ""
        self.motivo_procura = ""
        self.status = "Ativo"
        self.created_at = None
        
        # Campos populados por Join
        self.tecnico_nome = ""
        
        if dados:
            self.carregar(dados)

    def carregar(self, dados):
        self.id = dados.get('id')
        self.cadastro_ref_id = dados.get('cadastro_ref_id')
        self.tecnico_id = dados.get('tecnico_id')
        self.data_abertura = dados.get('data_abertura', '')
        self.servico_vinculado = dados.get('servico_vinculado', '')
        self.motivo_procura = dados.get('motivo_procura', '')
        self.status = dados.get('status', 'Ativo')
        self.created_at = dados.get('created_at')
        
        # Tratar o Join vindo do Supabase
        if 'usuarios' in dados and isinstance(dados['usuarios'], dict):
            self.tecnico_nome = dados['usuarios'].get('nome', '')

    def para_dict(self):
        return {
            'cadastro_ref_id': self.cadastro_ref_id,
            'tecnico_id': self.tecnico_id,
            'data_abertura': self.data_abertura,
            'servico_vinculado': self.servico_vinculado,
            'motivo_procura': self.motivo_procura,
            'status': self.status
        }
        

class Atendimento:
    """Modelo de Atendimento do Prontuário"""
    
    def __init__(self, dados=None):
        self.id = None
        self.prontuario_id = None
        self.tecnico_id = None
        self.data_atendimento = ""
        self.tipo_atendimento = ""
        self.demanda = ""
        self.descricao = ""
        self.created_at = None
        
        self.tecnico_nome = ""
        self.encaminhamentos = []
        
        if dados:
            self.carregar(dados)

    def carregar(self, dados):
        self.id = dados.get('id')
        self.prontuario_id = dados.get('prontuario_id')
        self.tecnico_id = dados.get('tecnico_id')
        self.data_atendimento = dados.get('data_atendimento', '')
        self.tipo_atendimento = dados.get('tipo_atendimento', '')
        self.demanda = dados.get('demanda', '')
        self.descricao = dados.get('descricao', '')
        self.created_at = dados.get('created_at')
        
        if 'usuarios' in dados and isinstance(dados['usuarios'], dict):
            self.tecnico_nome = dados['usuarios'].get('nome', '')

    def para_dict(self):
        return {
            'prontuario_id': self.prontuario_id,
            'tecnico_id': self.tecnico_id,
            'data_atendimento': self.data_atendimento,
            'tipo_atendimento': self.tipo_atendimento,
            'demanda': self.demanda,
            'descricao': self.descricao
        }


class Encaminhamento:
    """Modelo de Encaminhamento"""
    
    def __init__(self, dados=None):
        self.id = None
        self.atendimento_id = None
        self.servico_destino = ""
        self.motivo = ""
        self.status = "Pendente"
        self.retorno = ""
        self.created_at = None
        
        if dados:
            self.carregar(dados)

    def carregar(self, dados):
        self.id = dados.get('id')
        self.atendimento_id = dados.get('atendimento_id')
        self.servico_destino = dados.get('servico_destino', '')
        self.motivo = dados.get('motivo', '')
        self.status = dados.get('status', 'Pendente')
        self.retorno = dados.get('retorno', '')
        self.created_at = dados.get('created_at')

    def para_dict(self):
        return {
            'atendimento_id': self.atendimento_id,
            'servico_destino': self.servico_destino,
            'motivo': self.motivo,
            'status': self.status,
            'retorno': self.retorno
        }
