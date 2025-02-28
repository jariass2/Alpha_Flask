#########################################################################
## Añade worksheets desde ficheros mensuales PyG_mes a                 ##
## fichero existente en PyG_anual si existe                            ##
## A principio de aó deberia generarse un fichero vacio con nombre     ##
## Nombre Comercio_Codigo Comercio_Año                                 ##
#########################################################################

import os
import pandas as pd
import re
import xlsxwriter

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_BASE = os.path.join(BASE_DIR, 'POC')
DIR_ENTRADA = os.path.join(RUTA_BASE, 'PyG_mes')
DIR_SALIDA = os.path.join(RUTA_BASE, 'PyG_anual')

def crear_directorio_si_no_existe(directorio):
    if not os.path.exists(directorio):
        os.makedirs(directorio)
        print(f"Directorio creado: {directorio}")
    else:
        print(f"Directorio existente: {directorio}")

def extraer_nombre_base(nombre_archivo: str) -> str:
    match = re.search(r"(.*)_\d{1,2}_PyG\.xlsx$", nombre_archivo)
    if match:
        return match.group(1)
    return None

def obtener_archivos_salida_existentes():
    archivos_salida = set()
    for archivo in os.listdir(DIR_SALIDA):
        if archivo.endswith('_PyG.xlsx'):
            nombre_base = archivo[:-9]  # Remove '_PyG.xlsx'
            archivos_salida.add(nombre_base)
    return archivos_salida

def obtener_nombre_hoja(archivo_entrada):
    # Extract sheet name assuming format "XX_PyG" where XX is month
    parts = archivo_entrada.split('_')
    if len(parts) >= 2:
        return f"{parts[-2]}_PyG"
    return None

def main():
    try:
        print("\nIniciando proceso de copia de hojas de cálculo...")
        
        # Create directories if they don't exist
        crear_directorio_si_no_existe(DIR_ENTRADA)
        crear_directorio_si_no_existe(DIR_SALIDA)
        
        print(f"\nDirectorio de entrada: {DIR_ENTRADA}")
        print(f"Directorio de salida: {DIR_SALIDA}")

        # Get existing base names in output directory
        nombres_base_salida = obtener_archivos_salida_existentes()
        print(f"\nArchivos existentes en salida: {nombres_base_salida}")

        archivos_procesados = 0
        # Process all input files
        for archivo_entrada in os.listdir(DIR_ENTRADA):
            if archivo_entrada.endswith('.xlsx'):
                nombre_base_entrada = extraer_nombre_base(archivo_entrada)
                if not nombre_base_entrada:
                    continue  # Skip if base name not extracted correctly
                
                print(f"\nProcesando archivo: {archivo_entrada}")
                
                # Check if there's a corresponding output file
                if nombre_base_entrada in nombres_base_salida:
                    ruta_archivo_entrada = os.path.join(DIR_ENTRADA, archivo_entrada)
                    ruta_archivo_salida = os.path.join(DIR_SALIDA, f"{nombre_base_entrada}_PyG.xlsx")
                    
                    # Read all sheets from input file with decimal comma
                    df_input = pd.read_excel(ruta_archivo_entrada, sheet_name=None, decimal=',')
                    
                    # Read existing sheets from output file if it exists
                    if os.path.exists(ruta_archivo_salida):
                        df_output = pd.read_excel(ruta_archivo_salida, sheet_name=None, decimal=',')
                    else:
                        df_output = {}
                    
                    # Update output sheets with input sheets
                    for hoja_nombre, data in df_input.items():
                        # Standardize column names to lowercase
                        data.columns = data.columns.str.lower()
                        # Convert 'imeapu' column to numeric
                        if 'imeapu' in data.columns:
                            data['imeapu'] = pd.to_numeric(data['imeapu'], errors='coerce')
                        df_output[hoja_nombre] = data  # Overwrite if exists
                    
                    # Write all sheets to output file with XlsxWriter
                    with pd.ExcelWriter(ruta_archivo_salida, engine='xlsxwriter') as writer:
                        for hoja_nombre, data in df_output.items():
                            data.to_excel(writer, sheet_name=hoja_nombre, index=False)
                            worksheet = writer.sheets[hoja_nombre]
                            
                            # Check if 'imeapu' column exists and apply formatting
                            if 'imeapu' in data.columns:
                                imeapu_col_idx = data.columns.get_loc('imeapu')
                                
                                # Create a format for numbers with commas as decimal separators
                                number_format = writer.book.add_format({'num_format': '#,##0.00'})
                                
                                # Apply the format to the 'imeapu' column
                                worksheet.set_column(imeapu_col_idx, imeapu_col_idx, None, number_format)
                    
                    print(f"✅ Procesado exitosamente: {archivo_entrada}")
                    archivos_procesados += 1
                else:
                    print(f"⚠️ Ignorando {archivo_entrada}: No existe archivo correspondiente en el directorio de salida")
        
        print(f"\nProceso completado. Archivos procesados: {archivos_procesados}")

    except Exception as e:
        print(f"\n❌ Error en el proceso principal: {str(e)}")
        raise

if __name__ == "__main__":
    main()