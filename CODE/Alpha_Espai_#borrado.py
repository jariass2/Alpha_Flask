#########################################################################
## Borra los ficheros de los directorios                               ##
## POC/PyG_mes                                                         ##
## POC/SUMAS_Y_SALDOS/FINAL_RESULT                                     ##
## POC/SUMAS_Y_SALDOS/INTERMEDIATE                                     ##
#########################################################################

import os

# Definir las rutas base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_BASE = os.path.join(BASE_DIR, 'POC')
DIR_RESULTADOS_FINALES = os.path.join(RUTA_BASE, 'SUMAS_Y_SALDOS', 'FINAL_RESULT')
DIR_SALIDA = os.path.join(RUTA_BASE, 'PyG_mes')
DIR_INTERMEDIATE = os.path.join(RUTA_BASE, 'SUMAS_Y_SALDOS', 'INTERMEDIATE')

def crear_directorio_si_no_existe(directorio):
    """
    Crea un directorio si no existe.
    """
    if not os.path.exists(directorio):
        os.makedirs(directorio)
        print(f"Directorio creado: {directorio}")

def borrar_archivos_directorio(directorio):
    """
    Elimina todos los archivos dentro de un directorio dado.
    """
    try:
        # Asegurarse de que el directorio existe
        crear_directorio_si_no_existe(directorio)
        
        archivos_encontrados = False
        for archivo in os.listdir(directorio):
            ruta_archivo = os.path.join(directorio, archivo)
            if os.path.isfile(ruta_archivo):
                os.remove(ruta_archivo)
                print(f"Archivo eliminado: {ruta_archivo}")
                archivos_encontrados = True
        
        if not archivos_encontrados:
            print(f"No se encontraron archivos para eliminar en: {directorio}")
            
    except Exception as e:
        print(f"Error al borrar archivos de {directorio}: {e}")

print("Iniciando proceso de eliminación de archivos...")
print(f"Ruta base: {RUTA_BASE}")

# Crear directorios si no existen
crear_directorio_si_no_existe(RUTA_BASE)
crear_directorio_si_no_existe(os.path.join(RUTA_BASE, 'SUMAS_Y_SALDOS'))
crear_directorio_si_no_existe(DIR_RESULTADOS_FINALES)
crear_directorio_si_no_existe(DIR_SALIDA)
crear_directorio_si_no_existe(DIR_INTERMEDIATE)

# Borrar los archivos de los directorios especificados
print("\nBorrando archivos...")
borrar_archivos_directorio(DIR_RESULTADOS_FINALES)
borrar_archivos_directorio(DIR_SALIDA)
borrar_archivos_directorio(DIR_INTERMEDIATE)
borrar_archivos_directorio(DIR_SALIDA)

print("\nProceso de eliminación de archivos completado.")
