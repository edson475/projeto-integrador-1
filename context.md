# Contexto do Projeto - Sistema Web de Cadastro (Flask + Supabase)

## Visão Geral

Migração do sistema desktop de Cadastro de Assistência Social para uma aplicação web moderna, utilizando **Flask** como backend e **Supabase** como banco de dados na nuvem.

---

## Motivação da Migração

| Sistema Antigo (Desktop) | Novo Sistema (Web) |
|--------------------------|-------------------|
| Excel como banco de dados | Supabase (PostgreSQL) |
| CustomTkinter (desktop) | Flask + HTML/CSS/JS |
| Single-user | Multi-user via web |
| Dados locais | Dados na nuvem |
| Instalação local | Acesso via navegador |

---

## Arquitetura do Novo Sistema

### Stack Tecnológico

```
┌─────────────────────────────────────────────────┐
│              Navegador (Browser)                │
│         Chrome, Firefox, Edge, etc.             │
│  ┌─────────────────────────────────────────┐    │
│  │     Frontend: HTML5 + CSS3 + JS         │    │
│  │     Bootstrap 5 (UI Framework)          │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
                        ↕ HTTP/HTTPS
┌─────────────────────────────────────────────────┐
│              Backend: Flask (Python)            │
│  ┌─────────────────────────────────────────┐    │
│  │  Rotas: app.py                          │    │
│  │  Validações: validadores.py             │    │
│  │  Config: config.py                      │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
                        ↕ PostgreSQL
┌─────────────────────────────────────────────────┐
│         Supabase (Banco de Dados Cloud)         │
│  ┌─────────────────────────────────────────┐    │
│  │  Tabela: cadastros                      │    │
│  │  Tabela: membros_familia                │    │
│  │  API REST + Realtime                    │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### Tecnologias

| Camada | Tecnologia |
|--------|------------|
| Backend | Python 3.10+ com Flask 3.x |
| Frontend | HTML5, CSS3, JavaScript |
| UI Framework | Bootstrap 5.3 |
| Banco de Dados | Supabase (PostgreSQL 15) |
| ORM | Supabase-py (cliente oficial) |
| Templates | Jinja2 |
| Servidor | Flask Development Server / Gunicorn |

---

## Estrutura de Arquivos do Projeto

```
sistema-web-supabase/
├── app.py                      # Aplicação Flask principal
├── config.py                   # Configurações do sistema
├── database.py                 # Conexão com Supabase
├── models.py                   # Modelos de dados
├── validadores.py              # Validações (CPF, NIS, etc.)
├── requirements.txt            # Dependências Python
├── .env                        # Variáveis de ambiente (não versionar)
├── .env.example                # Exemplo de .env
├── .gitignore                  # Ignorar arquivos do Git
│
├── templates/                  # Templates HTML
│   ├── base.html               # Layout base
│   ├── index.html              # Página inicial
│   ├── login.html              # Tela de autenticação e bloqueio
│   ├── cadastro.html           # Formulário de cadastro
│   ├── pesquisa.html           # Busca de cadastros
│   ├── lista.html              # Listagem completa
│   └── familia.html            # Composição familiar
│
├── static/                     # Arquivos estáticos
│   ├── css/
│   │   └── style.css           # Estilos personalizados
│   └── js/
│       └── main.js             # JavaScript do frontend
│
├── scripts/                    # Scripts SQL e utilitários
│   └── criar_tabelas.sql       # SQL para criar tabelas no Supabase
│
└── README.md                   # Documentação completa
```

---

## Estrutura do Banco de Dados (Supabase)

### Tabela: usuarios (Acesso Restrito)

```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);
```

### Tabela: cadastros

```sql
CREATE TABLE cadastros (
    id SERIAL PRIMARY KEY,
    ref_id INTEGER UNIQUE NOT NULL,
    nome VARCHAR(200) NOT NULL,
    data_ref TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    nis VARCHAR(15),
    rg VARCHAR(20),
    endereco VARCHAR(200),
    numero VARCHAR(10),
    complemento VARCHAR(50),
    bairro VARCHAR(100),
    cidade TEXT,
    estado TEXT,
    cep VARCHAR(10),
    telefone VARCHAR(20),
    cpf VARCHAR(14),
    data_nascimento DATE,
    email VARCHAR(100),
    prioritario BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: membros_familia

```sql
CREATE TABLE membros_familia (
    id SERIAL PRIMARY KEY,
    ref_id INTEGER REFERENCES cadastros(ref_id) ON DELETE CASCADE,
    nome VARCHAR(200) NOT NULL,
    data_nascimento DATE,
    vinculo VARCHAR(50),
    titular BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Política de Acesso e RLS (Row Level Security)
Para habilitar que a API leia as tabelas corretamente, especialmente a `usuarios`, configuramos exceções de bloqueio RLS.
```sql
ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Acesso total a usuarios" ON usuarios FOR ALL USING (true) WITH CHECK (true);
```

### Índices

```sql
CREATE INDEX idx_cadastros_nome ON cadastros(nome);
CREATE INDEX idx_cadastros_cpf ON cadastros(cpf);
CREATE INDEX idx_cadastros_nis ON cadastros(nis);
CREATE INDEX idx_cadastros_ref ON cadastros(ref_id);
CREATE INDEX idx_membros_ref ON membros_familia(ref_id);
CREATE INDEX idx_membros_nome ON membros_familia(nome);
```

---

## Configuração do Supabase

### Passo a Passo Supabase

1. **Criar conta**: https://supabase.com
2. **Criar novo projeto**:
   - Nome: `cadastro-assistencia`
   - Senha do banco: (guardar em local seguro)
   - Região: `East US (N. Virginia)` - mais próxima do Brasil
3. **Aguardar criação**: ~2 minutos
4. **Obter credenciais**:
   - Settings → API
   - Project URL: `https://xxxxx.supabase.co`
   - API Key (anon/public): `eyJhbG...`

### Executar SQL no Supabase

1. No painel do Supabase, ir para **SQL Editor**
2. Clicar em **New Query**
3. Copiar e colar o conteúdo de `scripts/criar_tabelas.sql`
4. Clicar em **Run**

---

## Variáveis de Ambiente (.env)

```env
# Configurações do Flask
SECRET_KEY=sua-chave-secreta-aqui
FLASK_ENV=development
FLASK_DEBUG=True

# Configurações do Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=sua-chave-api-anon-aqui
```

---

## Rotas da Aplicação (Flask)

| Rota | Método | Descrição |
|------|--------|-----------|
| `/` | GET | Página inicial |
| `/login` | GET/POST | Tela de autenticação e form de Entrada |
| `/logout` | GET | Destroi a sessão atual com servidor |
| `/cadastro` | GET | Formulário de novo cadastro |
| `/cadastro/salvar` | POST | Salvar novo cadastro |
| `/cadastro/<ref_id>` | GET | Visualizar cadastro |
| `/cadastro/<ref_id>/editar` | GET/POST | Editar cadastro |
| `/cadastro/<ref_id>/excluir` | POST | Excluir cadastro |
| `/pesquisa` | GET/POST | Buscar cadastros |
| `/lista` | GET | Listar todos os cadastros |
| `/familia/<ref_id>` | GET/POST | Gerenciar composição familiar |
| `/api/cep/<cep>` | GET | Buscar CEP na ViaCEP |

---

## Funcionalidades Implementadas

### Segurança e Acesso
- [x] Login e controle restrito de Sistema.
- [x] Ocultação proativa de menu no front-end baseado em `flask.session`.
- [x] Criptografia de senhas padrão no Supabase utilizando `werkzeug.security` (padrão scrypt).
- [x] Botão alternador de olho mágico do campo senha com puro JS (visibility toggle).

### Cadastro
- [x] Novo cadastro com REF automático
- [x] Validação de CPF e NIS
- [x] Máscaras de entrada (JavaScript)
- [x] Busca automática de CEP (preenchendo endereço, bairro, cidade e estado)
- [x] Campo prioritário (Sim/Não)

### Composição Familiar
- [x] Adicionar membros
- [x] Remover membros
- [x] Definir vínculo familiar
- [x] Identificar titular

### Pesquisa
- [x] Buscar por nome
- [x] Buscar por CPF
- [x] Buscar por NIS
- [x] Buscar por REF
- [x] Buscar por membro da família

### Lista
- [x] Exibir todos os cadastros
- [x] Ordenação por colunas
- [x] Paginação (se necessário)

---

## Dependências Python (requirements.txt)

```
Flask==3.0.0
supabase==2.0.3
python-dotenv==1.0.0
requests==2.31.0
validate-docbr==1.10.0
```

---

## Instalação e Configuração

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Conta no Supabase (gratuita)

### Passos de Instalação

```bash
# 1. Criar pasta do projeto
mkdir sistema-web-supabase
cd sistema-web-supabase

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Criar arquivo .env
copy .env.example .env
# Editar .env com suas credenciais do Supabase

# 6. Executar aplicação
python app.py
```

### Acessar a Aplicação

Após iniciar, acessar: **http://127.0.0.1:5000**

---

## Diferenças: Sistema Antigo vs Novo

| Aspecto | Desktop (Excel) | Web (Supabase) |
|---------|-----------------|----------------|
| Armazenamento | Arquivo local | Nuvem (PostgreSQL) |
| Acesso | Single-user | Multi-user |
| Interface | CustomTkinter | Bootstrap 5 |
| Validação | Python (local) | Python + JS |
| CEP | ViaCEP API | ViaCEP API |
| Backup | Manual | Automático (Supabase) |
| Deploy | Executável | Hospedagem web |

---

## Próximos Passos (Melhorias Futuras)

- [x] Autenticação de usuários (login/senha)
- [ ] Controle de permissões
- [ ] Exportação para PDF/Excel
- [ ] Dashboard com estatísticas
- [ ] Upload de documentos
- [ ] Histórico de alterações
- [ ] API REST completa
- [ ] Deploy em produção (Render, Railway, etc.)

---

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'flask'"
**Solução**: Ativar ambiente virtual e instalar dependências:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Erro: "Invalid API key"
**Solução**: Verificar se as credenciais no `.env` estão corretas

### Erro: "Table does not exist"
**Solução**: Executar o SQL de criação das tabelas no Supabase

### Erro: "Port 5000 already in use"
**Solução**: Alterar porta no `app.py` ou fechar outro Flask rodando

---

## Links Úteis

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [ViaCEP API](https://viacep.com.br/)
- [validate-docbr](https://github.com/validate-docbr/validate-docbr)
