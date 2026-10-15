@echo off
chcp 65001 >nul
title Atlas Access - Sistema Baseado em Conhecimento (Prolog e Python)
cls

:MENU
echo ===============================================================================
echo     ATLAS ACCESS - CONTROLE DE ACESSO (PROJETO SENAI SA01)
echo     Equipe: Fábio, Fabi, Jonas Poli, Luciano
echo ===============================================================================
echo.
echo  --- PROLOG NATIVO (SWI-Prolog) ---
echo  [1] Abrir SWI-Prolog com a Base Principal (prolog\atlas_access.pl)
echo  [2] Abrir Apresentação no SWI-Prolog (prolog\apresentacao_slides.pl)
echo  [3] Executar Testes Automatizados em SWI-Prolog (prolog\test_casos.pl)
echo.
echo  --- PYTHON (Interpretador e Simulador) ---
echo  [4] Ensaiar Slides do Jonas (python\apresentacao_jonas.py)
echo  [5] Menu Geral do Sistema e Matriz Cruzada (python\main.py)
echo  [6] Executar Testes Automatizados em Python (12 testes)
echo.
echo  --- VISUALIZADOR DE SLIDES (Navegador) ---
echo  [7] Abrir Visualizador de Slides no Navegador (Copiar para Google Slides)
echo.
echo  [0] Sair
echo ===============================================================================
set /p opt="Digite o número da opção desejada [0-7]: "

if "%opt%"=="1" goto PROLOG_BASE
if "%opt%"=="2" goto PROLOG_SLIDES
if "%opt%"=="3" goto PROLOG_TESTS
if "%opt%"=="4" goto PY_JONAS
if "%opt%"=="5" goto PY_MAIN
if "%opt%"=="6" goto PY_TESTS
if "%opt%"=="7" goto OPEN_SLIDES
if "%opt%"=="0" exit /b

echo Opção inválida!
pause
goto MENU

:PROLOG_BASE
echo Iniciando SWI-Prolog com a base principal...
start swipl prolog\atlas_access.pl
goto MENU

:PROLOG_SLIDES
echo Iniciando SWI-Prolog com os slides...
start swipl prolog\apresentacao_slides.pl
goto MENU

:PROLOG_TESTS
echo Executando testes em Prolog...
swipl -s prolog\test_casos.pl -g run_tests -t halt
pause
goto MENU

:PY_JONAS
python python\apresentacao_jonas.py
pause
goto MENU

:PY_MAIN
python python\main.py
pause
goto MENU

:PY_TESTS
python -m unittest python\tests\test_suite.py
pause
goto MENU

:OPEN_SLIDES
start slides_html\apresentacao_slides_jonas.html
goto MENU

