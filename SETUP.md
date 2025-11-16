# 🚀 Guía de Configuración - CHATBOT-IA

> **Nota:** Esta guía está optimizada para Windows. Todo el equipo trabaja en este sistema operativo.

---

## ⚙️ Requisitos Previos

- ✅ Python 3.10 o superior instalado
- ✅ Git instalado
- ✅ Proyecto ya clonado en tu computadora

---

## 🔧 Configuración Inicial (Solo la primera vez)

### Paso 1: Abrir PowerShell o CMD en la carpeta del proyecto

**Opción A - Desde el Explorador de Archivos:**
1. Abre la carpeta `CHATBOT-IA`
2. En la barra de dirección escribe `cmd` o `powershell` y presiona Enter

**Opción B - Desde la terminal:**
```powershell
cd C:\ruta\a\tu\proyecto\CHATBOT-IA
```

### Paso 2: Crear el entorno virtual

```powershell
py -m venv .venv
```

⏱️ Esto tomará unos segundos. Verás que se crea una carpeta `.venv` en el proyecto.

### Paso 3: Activar el entorno virtual

**Si usas PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

**Si usas CMD:**
```cmd
.venv\Scripts\activate.bat
```

✅ **Verificación:** Deberías ver `(.venv)` al inicio de tu línea de comando:
```
(.venv) PS C:\...\CHATBOT-IA>
```

### Paso 4: Instalar las dependencias

```powershell
pip install -r requirements.txt
```

⏱️ Esto tomará unos minutos. Verás cómo se descargan e instalan las librerías.

### Paso 5: Verificar que todo funciona

```powershell
python verificar_entorno.py
```

**Salida esperada:**
```
Verificando entorno...
Python: 3.X.X ...
✅ sentence_transformers - OK
✅ faiss - OK
✅ numpy - OK
🎉 ¡Entorno configurado correctamente!
```

---

## 💻 Uso Diario (Cada vez que trabajes en el proyecto)

### 1. Abre tu terminal en la carpeta del proyecto

```powershell
cd C:\ruta\a\tu\proyecto\CHATBOT-IA
```

### 2. Activa el entorno virtual

**PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

**CMD:**
```cmd
.venv\Scripts\activate.bat
```

✅ Verifica que veas `(.venv)` al inicio de la línea.

### 3. Trabaja normalmente

```powershell
python tu_script.py
```

### 4. Al terminar (opcional)

```powershell
deactivate
```

---

## 🆘 Solución de Problemas

### ❌ Error: "No se puede ejecutar Activate.ps1"

**Error completo:**
```
Activate.ps1 no se puede cargar porque la ejecución de scripts está deshabilitada...
```

**Solución:**

1. Abre PowerShell **como Administrador**:
   - Presiona `Windows + X`
   - Selecciona "Windows PowerShell (Administrador)"

2. Ejecuta este comando:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. Escribe `S` (Sí) cuando te pregunte

4. Cierra PowerShell y abre uno normal (sin administrador)

5. Intenta activar nuevamente:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

**Alternativa rápida:** Usa CMD en lugar de PowerShell (no requiere cambiar permisos).

---

### ❌ Error: "python no se reconoce como comando"

**Solución:**

Usa `py` en lugar de `python`:

```powershell
py -m venv .venv
py verificar_entorno.py
```

---

### ❌ Error al instalar faiss-cpu

**Síntoma:** Error de compilación o falla al instalar `faiss-cpu`.

**Solución 1 - Versión específica:**
```powershell
pip install faiss-cpu==1.7.4
```

**Solución 2 - Usar conda (si tienes Anaconda/Miniconda instalado):**
```powershell
conda install -c conda-forge faiss-cpu
pip install sentence-transformers numpy
```

---

### ❌ La carpeta .venv ya existe pero no funciona

**Solución:** Elimínala y créala de nuevo:

```powershell
# Eliminar la carpeta
rmdir /s .venv

# Crear nuevamente
py -m venv .venv

# Activar
.venv\Scripts\Activate.ps1

# Reinstalar dependencias
pip install -r requirements.txt
```

---

## 📋 Comandos de Referencia Rápida

| Acción | Comando PowerShell | Comando CMD |
|--------|-------------------|-------------|
| Crear entorno | `py -m venv .venv` | `py -m venv .venv` |
| Activar entorno | `.venv\Scripts\Activate.ps1` | `.venv\Scripts\activate.bat` |
| Desactivar entorno | `deactivate` | `deactivate` |
| Instalar dependencias | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Verificar instalación | `python verificar_entorno.py` | `python verificar_entorno.py` |
| Ver librerías instaladas | `pip list` | `pip list` |

---

## ⚠️ Recordatorios Importantes

### ✅ **SIEMPRE activa el entorno virtual antes de trabajar**

Si no ves `(.venv)` al inicio de tu línea de comando, las librerías no estarán disponibles.

### ✅ **NO elimines la carpeta `.venv`**

Es tu entorno local. Si la eliminas por error, solo repite los pasos de configuración inicial.

### ✅ **NO modifiques archivos dentro de `.venv`**

Esa carpeta se gestiona automáticamente. Solo trabaja en las carpetas del proyecto (`app/`, `data/`, etc.).

### ✅ **Actualiza tu entorno si hay cambios en `requirements.txt`**

Si alguien del equipo agregó nuevas librerías:

```powershell
# Con el entorno activado
pip install -r requirements.txt
```

---

## 📞 ¿Necesitas Ayuda?

Si después de seguir esta guía sigues teniendo problemas:

1. Verifica que Python esté instalado: `py --version`
2. Asegúrate de estar en la carpeta correcta del proyecto
3. Revisa que el archivo `requirements.txt` exista
4. Contacta al equipo del proyecto

---

## 🎯 Resumen Ultra Rápido

```powershell
# Primera vez
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python verificar_entorno.py

# Cada día
cd C:\ruta\proyecto\CHATBOT-IA
.venv\Scripts\Activate.ps1
python tu_script.py
```

¡Listo para trabajar! 🚀