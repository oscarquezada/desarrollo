@echo off

REM Paso 1: Activar entorno virtual
call .\env\Scripts\activate

REM Paso 2: Instalar paquetes desde requirements.txt
pip install -r requirements.txt

REM Paso 3: Navegar al directorio de backend (donde está manage.py)
cd backend

REM Paso 4: Ejecutar el servidor de Django en el puerto 8000 en todas las interfaces
python manage.py runserver 0.0.0.0:8000 --insecure

REM Paso 5: Abrir el navegador en la URL 0.0.0.0:8000
start chrome  http://localhost:8000 
