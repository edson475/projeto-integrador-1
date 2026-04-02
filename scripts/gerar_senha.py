from werkzeug.security import generate_password_hash

senha = "univesp321"
hash_senha = generate_password_hash(senha)

print("="*50)
print("GERADOR DE HASH PARA A TABELA USUÁRIOS")
print("="*50)
print(f"Senha original: {senha}")
print(f"Hash p/ Banco: {hash_senha}")
print("="*50)
print("Abra o Supabase > SQL Editor e insira o primeiro usuário usando este código:")
print(f"INSERT INTO usuarios (nome, email, senha_hash) VALUES ('Administrador', 'email@gmail.com', '{hash_senha}');")
