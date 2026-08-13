@echo off
setlocal

title X Scraper

echo.
echo ==========================================
echo             X SCRAPER
echo ==========================================
echo.

REM Ir a la carpeta donde esta este archivo
cd /d "%~dp0"

echo [1/3] Abriendo Microsoft Edge...
echo.

start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" ^
    --remote-debugging-port=9222 ^
    --user-data-dir="C:\EdgeDebug" ^
    "https://x.com"

echo.
echo [2/3] Esperando a que Edge este listo...
echo.

timeout /t 3 /nobreak >nul

echo Edge iniciado.
echo.

echo [3/3] Iniciando X Scraper...
echo.

REM Iniciar Streamlit en segundo plano
start "" /b python -m streamlit run app.py --server.headless true

echo.
echo Esperando a que Streamlit este listo...
echo.

REM Esperar unos segundos para que Streamlit arranque
timeout /t 5 /nobreak >nul

REM Abrir automaticamente la aplicacion
start "" "http://localhost:8501"

echo.
echo ==========================================
echo           X SCRAPER ESTA LISTO
echo ==========================================
echo.
echo La aplicacion se ha abierto en el navegador.
echo.
echo Puedes cerrar esta ventana cuando termines.
echo.

pause

endlocal