import shutil
import sys
import subprocess
import platform
from app import create_app

def instalar_graphviz():
    """
    Intenta instalar Graphviz automáticamente según el sistema operativo.
    """
    os_name = platform.system()
    try:
        if os_name == "Linux":
            print("Instalando Graphviz en Linux...")
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "graphviz"], check=True)
        elif os_name == "Windows":
            print("Por favor, instala Graphviz manualmente desde: https://graphviz.gitlab.io/download/")
            print("Deteniendo ejecución...")
            sys.exit(1)
        elif os_name == "Darwin":  # macOS
            print("Instalando Graphviz en macOS...")
            subprocess.run(["brew", "install", "graphviz"], check=True)
        else:
            print(f"Sistema operativo no reconocido: {os_name}. No se puede instalar Graphviz automáticamente.")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error durante la instalación de Graphviz. Por favor, instálalo manualmente.")
        sys.exit(1)

def verificar_o_instalar_graphviz():
    """
    Verifica si Graphviz está instalado. Si no, intenta instalarlo.
    """
    if not shutil.which("dot"):
        print("Graphviz no está instalado. Intentando instalar...")
        instalar_graphviz()
    else:
        print("Graphviz está instalado.")

verificar_o_instalar_graphviz()

app = create_app()

if __name__ == '__main__':
    app.run()
