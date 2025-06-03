@echo off
echo Instalando pacotes do requirements.txt...
pip install -r requirements.txt

echo Executando o script Python...
python "teste final.py"

echo.
echo Encerrado. Deseja desinstalar os pacotes? (S/N)
set /p resp=

if /I "%resp%"=="S" (
    for /F "usebackq tokens=*" %%p in ("requirements.txt") do (
        echo Desinstalando %%p...
        pip uninstall -y %%p
    )
    echo Todos os pacotes foram desinstalados.
) else (
    echo Os pacotes foram mantidos.
)

pause
