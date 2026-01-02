#!/usr/bin/env python3
"""
verificar_entorno.py

Verifica:
1. Versión de Python (recomendada y mínima)
2. Uso de entorno virtual
3. Dependencias instaladas (requirements.txt)
"""

import sys
import os
import subprocess
from pathlib import Path


# ===============================
# CONFIGURACIÓN
# ===============================
PREFERRED_PYTHON = (3, 11)   # versión recomendada
MIN_PYTHON = (3, 10)         # versión mínima aceptada
REQUIREMENTS_FILE = "requirements.txt"


# ===============================
# UTILIDADES
# ===============================
def python_version():
    return sys.version_info


def in_virtualenv():
    if hasattr(sys, "real_prefix"):
        return True
    if sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        return True
    return "CONDA_PREFIX" in os.environ


def get_installed_packages():
    try:
        output = subprocess.check_output(
            [sys.executable, "-m", "pip", "freeze"],
            universal_newlines=True
        )
        return {line.split("==")[0].lower() for line in output.splitlines()}
    except Exception:
        return set()


def load_requirements(path):
    if not Path(path).exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [
            line.strip().lower()
            for line in f
            if line.strip() and not line.startswith("#")
        ]


# ===============================
# MAIN
# ===============================
def main():
    print("\n=== Verificación del entorno del proyecto ===\n")

    # -------------------------------------------------
    # 1. Verificar versión de Python
    # -------------------------------------------------
    version = python_version()
    print(f"Python detectado: {version.major}.{version.minor}.{version.micro}")

    if version < MIN_PYTHON:
        print("\n❌ Versión de Python NO compatible.")
        print(f"Se requiere al menos Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}")
        print("\n👉 Instrucciones para Windows:")
        print("1. Ve a: https://www.python.org/downloads/windows/")
        print("2. Descarga Python 3.11.x")
        print("3. Marca la opción: 'Add Python to PATH'")
        print("4. Finaliza la instalación")
        print("5. Verifica con: python --version")
        sys.exit(2)

    elif (version.major, version.minor) != PREFERRED_PYTHON:
        print("⚠️  Versión aceptable, pero no recomendada.")
        print(f"   Recomendado: Python {PREFERRED_PYTHON[0]}.{PREFERRED_PYTHON[1]}")
        print("   Tu versión puede funcionar, pero podrían surgir incompatibilidades.\n")
    else:
        print("✔ Versión recomendada de Python detectada.")

    # -------------------------------------------------
    # 2. Entorno virtual
    # -------------------------------------------------
    if in_virtualenv():
        print("✔ Entorno virtual detectado.")
    else:
        print("⚠️  No se detectó un entorno virtual.")
        print("   Se recomienda usar uno:")
        print("   python -m venv .venv")
        print("   .\\.venv\\Scripts\\activate  (Windows)")
        print("   source .venv/bin/activate  (Linux/Mac)")

    # -------------------------------------------------
    # 3. Dependencias
    # -------------------------------------------------
    print("\nVerificando dependencias...")
    required = load_requirements(REQUIREMENTS_FILE)
    installed = get_installed_packages()

    if not required:
        print("⚠️ No se encontró requirements.txt")
    else:
        missing = [pkg for pkg in required if pkg.split("==")[0] not in installed]

        if not missing:
            print("✔ Todas las dependencias están instaladas.")
        else:
            print("❌ Faltan las siguientes dependencias:")
            for m in missing:
                print(f"   - {m}")

            print("\nPara instalarlas ejecuta:")
            print("   pip install -r requirements.txt")

    print("\n✔ Verificación finalizada.\n")


if __name__ == "__main__":
    main()
