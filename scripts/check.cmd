@echo off
setlocal

cd /d "%~dp0.."
set "PIP_REQUIRE_VIRTUALENV=true"
set "VENV_PYTHON=%CD%\.venv\Scripts\python.exe"

if not exist "%VENV_PYTHON%" (
    echo ERROR: Missing .venv. Run scripts\bootstrap.cmd first.
    exit /b 1
)

"%VENV_PYTHON%" -c "import sys; assert sys.prefix != sys.base_prefix; print(f'Using: {sys.executable}')" || exit /b 1
"%VENV_PYTHON%" -m pip check || exit /b 1
"%VENV_PYTHON%" -m ruff format --check . || exit /b 1
"%VENV_PYTHON%" -m ruff check . || exit /b 1
"%VENV_PYTHON%" -m pytest || exit /b 1
"%VENV_PYTHON%" -m compileall -q src tests || exit /b 1

echo All repository checks passed.
exit /b 0

