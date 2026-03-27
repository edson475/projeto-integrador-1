# Sistema de Cadastro de Assistência Social - Web

Aplicação web para cadastro e gestão de beneficiários da Assistência Social, desenvolvida com **Flask** e **Supabase**.

Este é o repositório do Projeto Integrador 1 - Univesp.

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
| Database Password | `SuaSenha` |

### Passo 4: Criar Tabelas no Banco de Dados

1. No Supabase, clique em **"SQL Editor"**
2. Execute o script em `scripts/criar_tabelas.sql`.

### Passo 5: Rodar Localmente

```bash
pip install -r requirements.txt
python app.py
```
