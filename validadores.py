from validate_docbr import CPF, PIS
import re
from datetime import datetime


class Validadores:
    """Classe com validadores e formatadores"""
    
    @staticmethod
    def validar_cpf(cpf):
        """Valida CPF com ou sem máscara"""
        if not cpf:
            return True  # CPF vazio é válido (opcional)
        cpf_obj = CPF()
        cpf_limpo = re.sub(r'\D', '', cpf)
        if len(cpf_limpo) != 11:
            return False
        if cpf_limpo == '00000000000':
            return True
        return cpf_obj.validate(cpf_limpo)

    @staticmethod
    def formatar_cpf(cpf):
        """Formata CPF com máscara"""
        cpf_limpo = re.sub(r'\D', '', cpf)
        if len(cpf_limpo) == 11:
            return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
        return cpf

    @staticmethod
    def validar_rg(rg):
        """Valida RG (padrão SP com dígito verificador)"""
        if not rg:
            return True  # RG vazio é válido
        rg_limpo = re.sub(r'[^0-9xX]', '', str(rg)).upper()
        if len(rg_limpo) != 9:
            return False
            
        # Calcula o dígito verificador do RG (SP)
        soma = 0
        multiplicadores = [2, 3, 4, 5, 6, 7, 8, 9]
        
        for i in range(8):
            soma += int(rg_limpo[i]) * multiplicadores[i]
            
        resto = soma % 11
        dv_esperado = str(11 - resto)
        
        if dv_esperado == '10':
            dv_esperado = 'X'
        elif dv_esperado == '11':
            dv_esperado = '0'
            
        return rg_limpo[8] == dv_esperado

    @staticmethod
    def validar_nis(nis):
        """Valida NIS/PIS"""
        if not nis:
            return True  # NIS vazio é válido (opcional)
        pis_obj = PIS()
        nis_limpo = re.sub(r'\D', '', nis)
        if len(nis_limpo) != 11:
            return False
        if nis_limpo == '00000000000':
            return True
        return pis_obj.validate(nis_limpo)

    @staticmethod
    def formatar_nis(nis):
        """Formata NIS com máscara"""
        nis_limpo = re.sub(r'\D', '', nis)
        if len(nis_limpo) == 11:
            return f"{nis_limpo[:3]}.{nis_limpo[3:8]}.{nis_limpo[8:10]}-{nis_limpo[10:]}"
        return nis

    @staticmethod
    def formatar_cep(cep):
        """Formata CEP com máscara"""
        cep_limpo = re.sub(r'\D', '', cep)
        if len(cep_limpo) == 8:
            return f"{cep_limpo[:5]}-{cep_limpo[5:]}"
        return cep

    @staticmethod
    def formatar_telefone(telefone):
        """Formata telefone"""
        tel_limpo = re.sub(r'\D', '', telefone)
        if len(tel_limpo) == 11:
            return f"({tel_limpo[:2]}) {tel_limpo[2:7]}-{tel_limpo[7:]}"
        elif len(tel_limpo) == 10:
            return f"({tel_limpo[:2]}) {tel_limpo[2:6]}-{tel_limpo[6:]}"
        return telefone

    @staticmethod
    def formatar_cnpj(cnpj):
        """Formata CNPJ com máscara"""
        cnpj_limpo = re.sub(r'\D', '', cnpj)
        if len(cnpj_limpo) == 14:
            return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
        return cnpj

    @staticmethod
    def validar_data(data_str):
        """Valida data no formato DD/MM/YYYY"""
        if not data_str:
            return True  # Data vazia é válida (opcional)
        try:
            datetime.strptime(data_str, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    @staticmethod
    def validar_email(email):
        """Valida e-mail"""
        if not email:
            return True  # E-mail vazio é válido (opcional)
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(padrao, email))

    @staticmethod
    def limpar_string(texto):
        """Remove caracteres especiais de uma string"""
        if not texto:
            return ""
        return re.sub(r'\s+', ' ', texto).strip()

    @staticmethod
    def apenas_numeros(texto):
        """Retorna apenas os números de uma string"""
        if not texto:
            return ""
        return re.sub(r'\D', '', texto)
