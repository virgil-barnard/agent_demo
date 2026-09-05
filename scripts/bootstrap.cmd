@echo off
setlocal

cd /d "%~dp0.."
set "PIP_REQUIRE_VIRTUALENV=true"
set "VENV_PYTHON=%CD%\.venv\Scripts\python.exe"

if not exist "%VENV_PYTHON%" (
    echo Creating .venv with the default Python 3 interpreter...
    py -3 -m venv .venv || exit /b 1
)

if not exist "%VENV_PYTHON%" (
    echo ERROR: Virtual environment creation failed: "%VENV_PYTHON%" was not found.
    exit /b 1
)

"%VENV_PYTHON%" -c "import sys; assert sys.prefix != sys.base_prefix; print(f'Venv Python: {sys.executable}')" || exit /b 1
"%VENV_PYTHON%" -m pip install -e ".[dev]" || exit /b 1
"%VENV_PYTHON%" -m pip check || exit /b 1

echo Environment ready. Run scripts\check.cmd to validate it.
exit /b 0

