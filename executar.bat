@echo off
title Sistema de Cadastro Web - Flask + Supabase
cd /d "%~dp0"

echo ==================================================
echo  SISTEMA DE CADASTRO - ASSISTENCIA SOCIAL (WEB)
echo  Flask + Supabase
echo ==================================================
echo.

REM Verificar se o ambiente virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo.
    echo Execute os seguintes comandos para criar:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Ativar ambiente virtual
echo [1/2] Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Verificar se o arquivo .env existe
if not exist ".env" (
    echo.
    echo [ATENCAO] Arquivo .env nao encontrado!
    echo Copie .env.example para .env e preencha as configuracoes do Supabase.
    echo.
    pause
    exit /b 1
)

REM Iniciar aplicacao
echo [2/2] Iniciando aplicacao...
echo.
echo ==================================================
echo  Acesse: http://127.0.0.1:5000
echo  Para parar: Pressione Ctrl+C
echo ==================================================
echo.

python app.py

pause
