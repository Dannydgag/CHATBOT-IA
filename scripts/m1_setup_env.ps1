#este script crea el entorno virtual y lo activa, luego instala las dependencias necesarias
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt