@echo off
title Entrenamiento Juan - App
echo ======================================
echo  🏋️ Iniciando app de entrenamiento...
echo ======================================
echo.

:: Cambiar al directorio donde está el proyecto
cd /d "C:\Users\juan\Desktop\app_entrenamiento"

:: Activar el entorno virtual
call venv\Scripts\activate

:: Ejecutar Streamlit
echo.
echo 🚀 Lanzando Streamlit...
streamlit run app.py

:: Pausa para ver mensajes de error
pause