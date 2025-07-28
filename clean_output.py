import shutil
import os

def clean_output():
    # Limpiar fuentes que no sean 'Regular'
    fonts_dir = 'fonts'
    if os.path.exists(fonts_dir):
        for fname in os.listdir(fonts_dir):
            if fname.endswith('.ttf') and 'Regular' not in fname:
                fpath = os.path.join(fonts_dir, fname)
                os.remove(fpath)
                print(f"Fuente eliminada: {fpath}")
    output_dir = 'output'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print(f"Directorio '{output_dir}' eliminado.")
    else:
        print(f"No existe el directorio '{output_dir}'. Nada que limpiar.")

if __name__ == "__main__":
    clean_output()
