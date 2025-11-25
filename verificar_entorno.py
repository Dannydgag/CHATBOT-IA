import sys

def verificar_libreria(nombre):
    try:
        __import__(nombre)
        print(f"✅ {nombre} - OK")
        return True
    except ImportError:
        print(f"❌ {nombre} - NO INSTALADO")
        return False

print("Verificando entorno...\n")
print(f"Python: {sys.version}\n")

librerias = ['sentence_transformers', 'faiss', 'numpy']
resultados = [verificar_libreria(lib) for lib in librerias]

if all(resultados):
    print("\n🎉 ¡Entorno configurado correctamente!")
else:
    print("\n⚠️  Algunas librerías faltan. Ejecuta: pip install -r requirements.txt")
###```
"""
## 📊 Tu estructura ideal debería ser:
```
CHATBOT-IA/
├── 📁 .git/
├── 📁 .github/          (opcional - para GitHub Actions)
├── 📁 .venv/           ❌ NO SUBIR (debe estar en .gitignore)
├── 📁 app/             ✅ Tu aplicación
├── 📁 data/            ✅ Tus datos
├── 📁 docs/            ✅ Documentación
├── 📁 index/           ✅ (¿índices de búsqueda?)
├── 📁 models/          ✅ Tus modelos
│
├── 📄 .gitignore       ⭐ AGREGAR (crítico)
├── 📄 SETUP.md         ⭐ AGREGAR (instrucciones)
├── 📄 README.md        ✅ Ya tienes
├── 📄 requirements.txt ✅ Ya tienes
├── 📄 importante.txt   ✅ Ya tienes
└── 📄 verificar_entorno.py  ⭐ AGREGAR (verificación)"""