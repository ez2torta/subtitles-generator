import shutil
import os

def clean_output(project=None):
    # Limpiar fuentes que no sean 'Regular'
    fonts_dir = 'fonts'
    if os.path.exists(fonts_dir):
        for fname in os.listdir(fonts_dir):
            if fname.endswith('.ttf') and 'Regular' not in fname:
                fpath = os.path.join(fonts_dir, fname)
                os.remove(fpath)
                print(f"Fuente eliminada: {fpath}")
    output_dir = 'output'
    if project:
        # Buscar y eliminar archivos y carpetas relacionados al proyecto
        found = False
        for root, dirs, files in os.walk(output_dir, topdown=False):
            # Eliminar archivos de subtítulos del proyecto
            for f in files:
                if f.startswith(f"subtitle_{project}_") and f.endswith(".png"):
                    fpath = os.path.join(root, f)
                    os.remove(fpath)
                    print(f"Archivo eliminado: {fpath}")
                    found = True
            # Eliminar carpetas vacías
            for d in dirs:
                dir_path = os.path.join(root, d)
                if not os.listdir(dir_path):
                    shutil.rmtree(dir_path)
                    print(f"Carpeta vacía eliminada: {dir_path}")
        if not found:
            print(f"No se encontraron archivos de proyecto '{project}' en '{output_dir}'.")
    else:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            print(f"Directorio '{output_dir}' eliminado.")
        else:
            print(f"No existe el directorio '{output_dir}'. Nada que limpiar.")

if __name__ == "__main__":
    import sys
    project = sys.argv[1] if len(sys.argv) > 1 else None
    clean_output(project)
