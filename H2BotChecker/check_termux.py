#!/usr/bin/env python3
"""
Script de verificación para Termux
Verifica que todas las dependencias estén instaladas correctamente
"""

import sys
import os

def check_python_version():
    """Verifica la versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 o superior es requerido")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True

def check_module(module_name, package_name=None):
    """Verifica si un módulo está instalado"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✅ {package_name} - OK")
        return True
    except ImportError:
        print(f"❌ {package_name} - NO INSTALADO")
        print(f"   Instala con: pip install {package_name}")
        return False

def check_file(file_path):
    """Verifica si un archivo existe"""
    if os.path.exists(file_path):
        print(f"✅ {file_path} - Existe")
        return True
    else:
        print(f"❌ {file_path} - NO ENCONTRADO")
        return False

def main():
    print("=" * 50)
    print("🔍 Verificación de Dependencias para Termux")
    print("=" * 50)
    print()
    
    all_ok = True
    
    # Verificar Python
    print("📦 Verificando Python...")
    if not check_python_version():
        all_ok = False
    print()
    
    # Verificar módulos principales
    print("📦 Verificando módulos principales...")
    modules = [
        ("pyrogram", "pyrogram"),
        ("tgcrypto", "tgcrypto"),
        ("dotenv", "python-dotenv"),
        ("httpx", "httpx"),
        ("faker", "faker"),
        ("requests", "requests"),
        ("aiohttp", "aiohttp"),
        ("names", "names"),
        ("sqlite3", None),  # Viene con Python
        ("asyncio", None),  # Viene con Python
    ]
    
    for module, package in modules:
        if package:
            if not check_module(module, package):
                all_ok = False
        else:
            if not check_module(module):
                all_ok = False
    print()
    
    # Verificar archivos importantes
    print("📁 Verificando archivos del bot...")
    files = [
        "main.py",
        "requirements.txt",
        "plugins/command/start.py",
        "plugins/tools/cmds.py",
    ]
    
    for file in files:
        if not check_file(file):
            all_ok = False
    print()
    
    # Verificar sistema operativo
    print("💻 Información del sistema...")
    print(f"   Sistema: {os.name}")
    if os.name == 'posix':
        print("   ✅ Sistema compatible con Termux (Linux/Unix)")
    elif os.name == 'nt':
        print("   ⚠️  Sistema Windows detectado (esto es para Termux)")
    print()
    
    # Resultado final
    print("=" * 50)
    if all_ok:
        print("✅ ¡Todo está listo! El bot debería funcionar correctamente.")
        print()
        print("Para ejecutar el bot:")
        print("  python main.py")
    else:
        print("❌ Hay problemas que deben resolverse antes de ejecutar el bot.")
        print()
        print("Instala las dependencias faltantes con:")
        print("  pip install -r requirements.txt")
    print("=" * 50)

if __name__ == "__main__":
    main()

