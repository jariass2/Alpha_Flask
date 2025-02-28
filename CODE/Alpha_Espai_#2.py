#########################################################################
## Generamos los datos derivados los ficheros provenientes de la       ##
## contabilidad.                                                       ##
## Coloca los csv en directorio PyG_mes                                ##
#########################################################################

import os
import pandas as pd
import locale
import re

# --- Configuration ---
RUTA_BASE = 'POC/'
RUTA_MASTERFILE = os.path.join(RUTA_BASE, 'MASTERFILES', 'Masterfile_PyG.csv')
DIR_RESULTADOS_FINALES = os.path.join(RUTA_BASE, 'SUMAS_Y_SALDOS', 'FINAL_RESULT')
DIR_SALIDA = os.path.join(RUTA_BASE, 'PyG_mes')

def establecer_locale():
    """Establece el locale a español si es posible."""
    try:
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')  # Para Windows
        except locale.Error:
            print("No se pudo establecer el locale español. Usando el locale por defecto.")

def cargar_masterfile(ruta: str) -> pd.DataFrame:
    """Cargar el archivo Masterfile."""
    df = pd.read_csv(ruta)
    df['imeapu'] = None  # Initialize 'imeapu'
    return df

def obtener_archivos_csv(directorio: str) -> list:
    """Obtener lista de archivos CSV en el directorio."""
    return [f for f in os.listdir(directorio) if f.endswith('.csv')]

def procesar_archivo_csv(df_masterfile: pd.DataFrame, archivo_csv: str, dir_resultados_finales: str) -> pd.DataFrame:
    """Procesar un archivo CSV y actualizar el Masterfile."""
    ruta_csv_actual = os.path.join(dir_resultados_finales, archivo_csv)
    df_csv_actual = pd.read_csv(ruta_csv_actual)

    columnas_requeridas = ['CUEAPU', 'total_IMEAPU']
    if not all(columna in df_csv_actual.columns for columna in columnas_requeridas):
        print(f"Advertencia: Faltan columnas {columnas_requeridas} en {archivo_csv}. Saltando.")
        return df_masterfile

    df_masterfile['imeapu'] = pd.to_numeric(df_masterfile['imeapu'], errors='coerce')

    for indice, fila in df_masterfile.iterrows():
        codigos = [
            str(int(codigo)) for codigo in fila.iloc[:2].values
            if pd.notna(codigo) and isinstance(codigo, (int, float)) and len(str(int(codigo))) == 7
        ]

        valores_imeapu = [
            df_csv_actual.loc[df_csv_actual['CUEAPU'] == int(codigo), 'total_IMEAPU'].sum()
            for codigo in codigos
        ]

        if valores_imeapu:
            df_masterfile.at[indice, 'imeapu'] = sum(valores_imeapu)

    return df_masterfile

def formatear_numero_europeo(x):
    """Formatear número en estilo europeo."""
    if pd.isna(x):
        return None
    try:
        return locale.format_string('%.2f', float(x), grouping=True)
    except (ValueError, TypeError):
        return None

def guardar_masterfile(df_masterfile: pd.DataFrame, archivo_csv: str, dir_salida: str):
    """Guardar el Masterfile actualizado."""
    # --- Removed the conditional check ---
    print(f"Saving output for {archivo_csv}")  # Always print
    encabezado = ['codigo_1', 'codigo_2', 'concepto', 'imeapu']
    nombre_base_archivo = os.path.splitext(archivo_csv)[0]
    ruta_salida_csv = os.path.join(dir_salida, f"{nombre_base_archivo}_PyG.csv")
    ruta_salida_excel = os.path.join(dir_salida, f"{nombre_base_archivo}_PyG.xlsx")

    # Apply formatting to the main DataFrame
    df_masterfile['imeapu'] = df_masterfile['imeapu'].apply(formatear_numero_europeo)

    # Save to CSV
    df_masterfile.to_csv(ruta_salida_csv, index=False, header=encabezado)

    # Save to XLSX (no extra formatting needed)
    df_masterfile.to_excel(ruta_salida_excel, index=False, header=encabezado, sheet_name=obtener_nombre_hoja(archivo_csv))


def obtener_nombre_hoja(archivo_csv: str) -> str:
    """Extraer el mes del nombre del archivo CSV."""
    match = re.search(r"_(\d{1,2})\.csv$", archivo_csv)
    if match:
        mes = match.group(1).zfill(2)
        return f"{mes}_PyG"
    return "SinMes_PyG"


def main():
    """Función principal."""
    os.makedirs(DIR_SALIDA, exist_ok=True)
    establecer_locale()

    df_masterfile = cargar_masterfile(RUTA_MASTERFILE)
    archivos_csv = obtener_archivos_csv(DIR_RESULTADOS_FINALES)

    for archivo_csv in archivos_csv:
        print(f"Procesando archivo: {archivo_csv}")
        # Reset 'imeapu' *before* processing each file
        df_masterfile['imeapu'] = None
        df_masterfile = procesar_archivo_csv(df_masterfile, archivo_csv, DIR_RESULTADOS_FINALES)
        guardar_masterfile(df_masterfile, archivo_csv, DIR_SALIDA) # Always save

    print("Proceso completado.")

if __name__ == "__main__":
    main()