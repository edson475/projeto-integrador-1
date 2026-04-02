# Sistema de Cadastro de Assistência Social - Web

Aplicação web para cadastro e gestão de beneficiários da Assistência Social, desenvolvida como Projeto Integrador 1 da Univesp. O projeto utiliza **Flask** no backend e o **Supabase** (PostgreSQL na nuvem) como banco de dados.

---

## 📋 Pré-requisitos

Para executar este sistema em sua máquina local, certifique-se de ter os seguintes itens instalados:

- ✅ **Python 3.10** ou superior
- ✅ **pip** (Gerenciador de pacotes do Python)
- ✅ **Git** (Opcional, mas recomendado para baixar o repositório)

---

## 🚀 Como Instalar e Rodar Localmente

Siga o passo a passo abaixo para colocar a aplicação no ar em seu computador.

### 1. Obter o Código Fonte

Abra o terminal (ou Prompt de Comando) e clone este repositório:
```bash
git clone https://github.com/edson475/projeto-integrador-1.git
cd projeto-integrador-1
```
*(Caso não possua o Git, você pode baixar o arquivo `.zip` clicando em "Code" > "Download ZIP" na página do repositório no GitHub).*

### 2. Criar e Ativar um Ambiente Virtual (Recomendado)

O ambiente virtual isola as dependências do projeto para não interferir no seu sistema.

**No Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**No Linux ou Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

Com o ambiente ativado, instale as bibliotecas necessárias contidas no arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente (.env)

O sistema exige uma comunicação direta com o servidor do Supabase na nuvem. Por questões de segurança, as credenciais não ficam salvas no código fonte. 

Você deve criar um arquivo `.env` baseado no arquivo de exemplo existente.

1. Faça uma cópia do arquivo `.env.example` e renomeie-o para `.env`. Pode usar o navegador de arquivos ou rodar o comando abaixo:
   - No Windows: `copy .env.example .env`
   - Linux/Mac: `cp .env.example .env`
2. Abra o novo arquivo `.env` em qualquer editor de texto.

> ⚠️ **ATENÇÃO: CHAVES DO SUPABASE**
> Para que o sistema funcione e acesse os cadastros reais, você precisará preencher as variáveis `SUPABASE_URL` e `SUPABASE_KEY` dentro do arquivo `.env`. 
> **Estas informações são estritamente confidenciais e devem ser solicitadas diretamente com o Administrador do Sistema (responsável pela conta principal do Supabase).**

Seu arquivo `.env` deve ficar parecido com isto:
```env
# Configurações do Flask
SECRET_KEY=uma-chave-secreta-qualquer-aqui
FLASK_ENV=development
FLASK_DEBUG=True

# Credenciais do Supabase (Solicitar ao Administrador)
SUPABASE_URL=https://[ID].supabase.co
SUPABASE_KEY=eyJhb...
```

### 5. Iniciar a Aplicação

Para finalmente ligar o servidor da aplicação na sua máquina, execute:
```bash
python app.py
```
Se as configurações estiverem corretas, você verá uma mensagem informando que o servidor inciou com sucesso.

Acesse o sistema diretamente no seu navegador, no endereço: **http://127.0.0.1:5000/**

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python e Flask
- **Frontend:** HTML5, CSS3, e Bootstrap 5
- **Banco de Dados:** Supabase (PostgreSQL 15)
- **Integração Externa:** API ViaCEP para endereços
