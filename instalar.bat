@echo off
title Instalando Dependencias - Sistema Web
cd /d "%~dp0"

echo ==================================================
echo  INSTALACAO DE DEPENDENCIAS
echo  Sistema de Cadastro Web - Flask + Supabase
echo ==================================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Instale o Python 3.10 ou superior em: https://python.org
    echo.
    pause
    exit /b 1
)

echo [1/3] Python encontrado!
python --version
echo.

REM Criar ambiente virtual se nao existir
if not exist "venv" (
    echo [2/3] Criando ambiente virtual...
    python -m venv venv
) else (
    echo [2/3] Ambiente virtual ja existe.
)
echo.

REM Ativar ambiente virtual
echo [3/3] Instalando dependencias...
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo ==================================================
echo  Instalacao concluida!
echo.
echo  Proximos passos:
echo  1. Copie .env.example para .env
echo  2. Preencha com suas credenciais do Supabase
echo  3. Execute executar.bat
echo ==================================================
echo.

pause
