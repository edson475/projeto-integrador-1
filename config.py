import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """Configurações da aplicação"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave-padrao-mude-em-producao')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Validações
    MAX_UPLOAD_SIZE = 16 * 1024 * 1024  # 16MB
    
    @classmethod
    def validate(cls):
        """Valida se todas as configurações necessárias estão presentes"""
        errors = []
        
        if not cls.SUPABASE_URL:
            errors.append("SUPABASE_URL não configurada")
        elif not cls.SUPABASE_URL.startswith('https://'):
            errors.append("SUPABASE_URL deve começar com https://")
            
        if not cls.SUPABASE_KEY:
            errors.append("SUPABASE_KEY não configurada")
        elif len(cls.SUPABASE_KEY) < 20:
            errors.append("SUPABASE_KEY parece inválida")
            
        return errors
