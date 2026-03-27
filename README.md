# Sistema de Cadastro de Assistência Social - Web

Aplicação web para cadastro e gestão de beneficiários da Assistência Social, desenvolvida com **Flask** e **Supabase**.

---

## 📋 Pré-requisitos

Antes de começar, você precisa ter instalado:

- ✅ **Python 3.10 ou superior**
- ✅ **pip** (gerenciador de pacotes Python)
- ✅ **Conta no Supabase** (gratuita)

---

## 🚀 Passo a Passo de Instalação

Siga estes passos **na ordem** para não errar:

### Passo 1: Verificar Python Instalado

Abra o **Prompt de Comando** (cmd) e digite:

```bash
python --version
```

Se aparecer a versão (ex: `Python 3.13.x`), continue. Se não, instale o Python em: https://python.org

### Passo 2: Criar Conta no Supabase

1. Acesse **https://supabase.com**
2. Clique em **"Start your project"** ou **"Sign In"**
3. Crie conta com GitHub, Google ou e-mail
4. Após login, clique em **"New Project"**

### Passo 3: Configurar Projeto no Supabase

Preencha as informações:

| Campo | Valor Sugerido |
|-------|---------------|
| Name | `cadastro-assistencia` |
| Database Password | `Senha123!@#` (GUARDE ESTA SENHA!) |
| Region | `East US (N. Virginia)` |

Clique em **"Create new project"** e aguarde ~2 minutos.

### Passo 4: Obter Credenciais da API

1. No painel do Supabase, clique em **"Settings"** (engrenagem no menu lateral)
2. Clique em **"API"**
3. Copie as seguintes informações:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **API Key (anon/public)**: `eyJhbG...` (chave longa)

Guarde essas duas informações!

### Passo 5: Criar Tabelas no Banco de Dados

1. No Supabase, clique em **"SQL Editor"** no menu lateral
2. Clique em **"New Query"**
3. Abra o arquivo `scripts/criar_tabelas.sql` deste projeto
4. Copie **TODO** o conteúdo do arquivo
5. Cole no SQL Editor do Supabase
6. Clique em **"Run"** (ou pressione Ctrl+Enter)

Você deve ver a mensagem "Success. No rows returned"

### Passo 6: Navegar até a Pasta do Projeto

Abra o **Prompt de Comando** e digite:

```bash
cd "c:\Users\User\Documents\Univesp\4º Semestre\PI1 VS Code\CadastroAssistencia\sistema-web-supabase"
```

### Passo 7: Criar Ambiente Virtual

No prompt de comando, na pasta do projeto:

```bash
python -m venv venv
```

Isso criará uma pasta `venv` no projeto.

### Passo 8: Ativar Ambiente Virtual

**No Windows:**

```bash
venv\Scripts\activate
```

Você verá `(venv)` no início da linha do comando.

### Passo 9: Instalar Dependências

Com o ambiente virtual ativado:

```bash
pip install -r requirements.txt
```

Aguarde a instalação de todos os pacotes.

### Passo 10: Configurar Arquivo .env

1. Na pasta do projeto, abra o arquivo `.env` com o Bloco de Notas
2. Substitua os valores:

```env
SECRET_KEY=qualquer-coisa-aqui-123456
FLASK_ENV=development
FLASK_DEBUG=True
SUPABASE_URL=https://SEU-PROJETO.supabase.co
SUPABASE_KEY=eyJhbG... (sua chave completa)
```

3. Salve o arquivo

### Passo 11: Executar a Aplicação

Ainda no prompt com o ambiente ativado:

```bash
python app.py
```

Você verá:

```
==================================================
SISTEMA DE CADASTRO - ASSISTÊNCIA SOCIAL
==================================================
Iniciando servidor...
Acesse: http://127.0.0.1:5000
==================================================
```

### Passo 12: Acessar o Sistema

Abra seu navegador e acesse:

**http://127.0.0.1:5000**

🎉 **Pronto! Sistema rodando!**

---

## 📁 Estrutura do Projeto

```
sistema-web-supabase/
├── app.py                      # Aplicação principal (Flask)
├── config.py                   # Configurações
├── database.py                 # Conexão com Supabase
├── models.py                   # Modelos de dados
├── validadores.py              # Validações (CPF, NIS, etc.)
├── requirements.txt            # Dependências Python
├── .env                        # Variáveis de ambiente
│
├── templates/                  # HTMLs
│   ├── base.html
│   ├── index.html
│   ├── cadastro.html
│   ├── pesquisa.html
│   ├── lista.html
│   └── familia.html
│
├── static/                     # Arquivos estáticos
│   ├── css/style.css
│   └── js/main.js
│
└── scripts/
    └── criar_tabelas.sql       # SQL para Supabase
```

---

## 🔧 Comandos Úteis

### Iniciar o sistema

```bash
cd "c:\Users\User\Documents\Univesp\4º Semestre\PI1 VS Code\CadastroAssistencia\sistema-web-supabase"
venv\Scripts\activate
python app.py
```

### Parar o servidor

Pressione **Ctrl + C** no prompt de comando.

### Verificar se há erros

Se aparecer erro de importação:

```bash
pip install -r requirements.txt --force-reinstall
```

---

## 🌐 Funcionalidades

| Funcionalidade | Descrição |
|---------------|-----------|
| **Novo Cadastro** | Cadastra nova família com REF automático |
| **Editar Cadastro** | Modifica dados de cadastro existente |
| **Excluir Cadastro** | Remove cadastro e família (com confirmação) |
| **Pesquisa** | Busca por nome, CPF, NIS, REF ou membro da família |
| **Lista Completa** | Exibe todos os cadastros em tabela |
| **Composição Familiar** | Gerencia membros da família |
| **CEP Automático** | Busca endereço via ViaCEP |
| **Validações** | CPF, NIS, data, e-mail |

---

## 🔍 Troubleshooting (Problemas Comuns)

### Erro: "ModuleNotFoundError: No module named 'flask'"

**Solução:** Ative o ambiente virtual e reinstale:

```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Erro: "Invalid API key" ou "Connection error"

**Solução:** Verifique no `.env`:
- SUPABASE_URL começa com `https://`
- SUPABASE_KEY está completa (copia errada é comum)

### Erro: "Table does not exist"

**Solução:** Execute o SQL no Supabase novamente:
1. Vá em SQL Editor no Supabase
2. Execute o conteúdo de `scripts/criar_tabelas.sql`

### Erro: "Port 5000 already in use"

**Solução:** Outro Flask está rodando. Feche-o ou altere a porta no `app.py`:

```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Sistema não carrega / Tela em branco

**Solução:** 
1. Pressione F12 no navegador
2. Veja o erro no Console
3. Verifique se o Flask está rodando

---

## 📊 Banco de Dados

### Tabelas Criadas

**cadastros:**
- ref_id (chave única)
- nome, cpf, rg, nis
- endereco, numero, complemento, bairro, cep
- telefone, email, data_nascimento
- prioritario, data_ref

**membros_familia:**
- ref_id (vínculo com cadastro)
- nome, data_nascimento, vinculo, titular

---

## 🔐 Segurança

**Importante:** Este sistema é para **demonstração/estudos**. Para produção:

1. Altere `FLASK_DEBUG=False`
2. Use uma `SECRET_KEY` forte e única
3. Configure políticas RLS no Supabase
4. Use HTTPS em produção
5. Adicione autenticação de usuários

---

## 📝 Links Úteis

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [Bootstrap 5](https://getbootstrap.com/)
- [ViaCEP API](https://viacep.com.br/)

---

## 👨‍💻 Desenvolvimento

### Tecnologias

| Camada | Tecnologia |
|--------|------------|
| Backend | Python 3 + Flask 3 |
| Frontend | HTML5 + CSS3 + JavaScript |
| UI | Bootstrap 5.3 |
| Banco | Supabase (PostgreSQL) |

---

## ✅ Checklist de Instalação

Marque cada item conforme for completando:

- [ ] Python instalado e funcionando
- [ ] Conta no Supabase criada
- [ ] Projeto criado no Supabase
- [ ] Tabelas criadas (SQL executado)
- [ ] Credenciais copiadas (URL e Key)
- [ ] Ambiente virtual criado (`venv`)
- [ ] Dependências instaladas
- [ ] Arquivo `.env` configurado
- [ ] Sistema rodando (`python app.py`)
- [ ] Acesso no navegador (`http://127.0.0.1:5000`)
- [ ] Primeiro cadastro realizado

---

## 🎯 Próximos Passos

Após o sistema estar rodando:

1. **Teste todas as funcionalidades**
2. **Cadastre algumas famílias de exemplo**
3. **Teste a pesquisa por nome/CPF**
4. **Adicione membros às famílias**
5. **Explore o banco no Supabase**

---

**Dúvidas?** Consulte o arquivo `context.md` para mais detalhes sobre a arquitetura.
