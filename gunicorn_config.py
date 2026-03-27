# Configuração do Gunicorn para Produção

# Bind: 127.0.0.1 ou use unix socket para segurança interna
bind = "unix:projeto.sock"

# Número de processos (geralmente (2 x cores) + 1)
workers = 3

# Timeout para requisições longas
timeout = 120

# Log de erros
errorlog = "logs/gunicorn_error.log"

# Permissões do socket
umask = 0o007