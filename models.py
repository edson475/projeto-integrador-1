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
