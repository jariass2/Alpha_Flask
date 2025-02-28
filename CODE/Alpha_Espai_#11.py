#######################################################################
##                   Cálculo MARGEN DE GESTION                       ##
##                                                                   ##
##                                                                   ##
#######################################################################


import os
import pandas as pd
from datetime import datetime
import re

# Configurar Pandas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '{:.2f}'.format)

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_BASE = os.path.join(BASE_DIR, 'POC')
DIR_VENTAS_BRUTAS = os.path.join(RUTA_BASE, 'VENTAS_BRUTAS')
DIR_COMPRAS_MERCANCIAS = os.path.join(RUTA_BASE, 'COMPRAS_MERCANCIAS')
DIR_PYG_MES = os.path.join(RUTA_BASE, 'PYG_MES')
DIR_MARGEN_CAJA = os.path.join(RUTA_BASE, 'MARGEN_CAJA')
DIR_MASTERFILE = os.path.join(RUTA_BASE, 'MASTERFILES')

# Índices de inicio para las columnas de mes en los archivos Excel
COLUMNA_VENTAS_MES_START_INDEX = 6
COLUMNA_COMPRAS_MES_START_INDEX = 10

# Verify directories
if not os.path.exists(DIR_MARGEN_CAJA):
    raise FileNotFoundError(f"El directorio {DIR_MARGEN_CAJA} no existe.")
if not os.path.exists(DIR_MASTERFILE):
    raise FileNotFoundError(f"El directorio {DIR_MASTERFILE} no existe.")
if not os.path.exists(DIR_PYG_MES):
    raise FileNotFoundError(f"El directorio {DIR_PYG_MES} no existe.")

# Get the correct Excel file
archivo_excel = next(
    (f for f in os.listdir(DIR_MARGEN_CAJA) if f.startswith('Margen_Demarca') and f.endswith('.xlsx')),
    None
)
if not archivo_excel:
    raise FileNotFoundError(f"No se encontró ningún archivo Excel con el patrón 'Margen_Demarca*.xlsx' en {DIR_MARGEN_CAJA}.")

ruta_excel = os.path.join(DIR_MARGEN_CAJA, archivo_excel)

# Get the current month and determine up to which month to process
mes_actual = datetime.now().month

##########################################################################
## FORZAR MES ACTUAL PARA PRUEBAS ##
# mes_actual = 10  # Set to 10 for testing up to September (previous month)
##########################################################################

meses_base = [
    "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
    "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
]
meses_a_procesar = meses_base[:mes_actual - 1]

# --- REVISED Data Aggregation (Single Pass) ---
def aggregate_data(ruta_excel, meses_a_procesar):
    """Aggregates Margen, Ventas, and Compras in a single pass."""
    aggregated_data = {}  # Dictionary to store all aggregated data

    with pd.ExcelFile(ruta_excel) as xls:
        for mes_base in meses_a_procesar:
            hojas_disponibles = xls.sheet_names
            hoja_encontrada = next((h for h in hojas_disponibles if h.upper().startswith(mes_base)), None)

            print(f"Procesando mes: {mes_base}")

            if not hoja_encontrada:
                print(f"⚠️ No se encontró ninguna hoja correspondiente a {mes_base}.")
                continue

            try:
                df = pd.read_excel(xls, sheet_name=hoja_encontrada, header=None)
                if len(df.columns) > 8:  # Check for sufficient columns
                    df_filtrado = df[df[8] == "Total"]
                else:
                    print(f"⚠️ La hoja {hoja_encontrada} no tiene suficientes columnas para procesar.")
                    continue

                for _, row in df_filtrado.iterrows():
                    atica_code = str(row[0]) if len(row) > 0 else None
                    if pd.isna(atica_code):  # Skip rows with missing ATICA
                        continue
                    atica_code = atica_code.strip() # Clean the ATICA code

                    # Initialize dictionary for the ATICA code if it doesn't exist
                    if atica_code not in aggregated_data:
                        aggregated_data[atica_code] = {
                            "Margen Gestión": 0.0,
                            "Ventas": 0.0,
                            "Compras": 0.0
                        }

                    # Extract and add values, handling potential errors
                    try:
                        margen = float(row[28]) if len(row) > 28 and pd.notna(row[28]) else 0.0
                        ventas = float(row[24]) if len(row) > 24 and pd.notna(row[24]) else 0.0
                        compras = float(row[26]) if len(row) > 26 and pd.notna(row[26]) else 0.0

                        aggregated_data[atica_code]["Margen Gestión"] += margen
                        aggregated_data[atica_code]["Ventas"] += ventas
                        aggregated_data[atica_code]["Compras"] += compras
                    except (ValueError, TypeError) as e:
                        print(f"⚠️ Error reading values for ATICA {atica_code} in sheet {hoja_encontrada}: {e}")
                        #  Could log this to a file for later review.

            except KeyError:
                print(f"⚠️ La hoja {hoja_encontrada} no existe en el archivo Excel.")
            except Exception as e:
                print(f"⚠️ Error procesando {hoja_encontrada}: {e}")

    return aggregated_data

# --- Aggregate ALL data in one go ---
all_aggregated_data = aggregate_data(ruta_excel, meses_a_procesar)

# --- Create a SINGLE DataFrame ---
df_merged = pd.DataFrame.from_dict(all_aggregated_data, orient='index')
df_merged.index.name = 'ATICA'  # Set the index name
df_merged = df_merged.reset_index()  # Reset index to make 'ATICA' a column
df_merged["ATICA"] = df_merged["ATICA"].astype(str)

# --- Load Masterfile ---
masterfile_path = os.path.join(DIR_MASTERFILE, 'Masterfile_CODIGOS.csv')
if not os.path.exists(masterfile_path):
    raise FileNotFoundError(f"El archivo {masterfile_path} no existe.")

df_masterfile = pd.read_csv(masterfile_path)
if 'ATICA' not in df_masterfile.columns or 'TIENDA' not in df_masterfile.columns or 'EST' not in df_masterfile.columns:
    raise ValueError("El archivo Masterfile_CODIGOS.csv debe contener las columnas 'ATICA', 'TIENDA' y 'EST'.")
df_masterfile['EST'] = pd.to_numeric(df_masterfile['EST'], errors='coerce').fillna(0).astype(int)
df_masterfile['ATICA'] = df_masterfile['ATICA'].astype(str) # Ensure ATICA is string for merging

# --- Merge with Masterfile ---
df_merged = pd.merge(df_masterfile[['ATICA', 'TIENDA', 'EST']], df_merged, on='ATICA', how='left')

df_merged['EST'] = pd.to_numeric(df_merged['EST'], errors='coerce').fillna(0).astype(int)
df_merged = df_merged[["ATICA", "EST", "TIENDA", "Margen Gestión", "Ventas", "Compras"]]
df_merged = df_merged.sort_values(by="ATICA")
df_merged["Margen Gestión"] = df_merged["Margen Gestión"].fillna(0).round(2)
df_merged["Ventas"] = df_merged["Ventas"].fillna(0).round(2)
df_merged["Compras"] = df_merged["Compras"].fillna(0).round(2)

# --- Function to update PyG files ---
def update_pyg_files(df_merged, pyg_directory):
    """Updates PyG files with Margen Gestión."""
    try:
        df_merged['EST'] = df_merged['EST'].astype(int)

        for filename in os.listdir(pyg_directory):
            if filename.endswith('.csv'):
                match = re.search(r'_(\d+)_', filename)
                if match:
                    est_code_file = int(match.group(1))

                    row = df_merged[df_merged['EST'] == est_code_file]
                    if not row.empty:
                        row = row.squeeze()
                    else:
                        continue

                    margen_value = float(row['Margen Gestión']) if 'Margen Gestión' in row and pd.notna(row['Margen Gestión']) else 0.0

                    file_path = os.path.join(pyg_directory, filename)
                    try:
                        pyg_df = pd.read_csv(file_path)
                    except pd.errors.EmptyDataError:
                        print(f"Warning: File {filename} is empty. Skipping.")
                        continue
                    except FileNotFoundError:
                        print(f"Warning: File {filename} not found. Skipping.")
                        continue

                    if 'concepto' in pyg_df.columns and 'imeapu' in pyg_df.columns:
                        pyg_df.loc[pyg_df['concepto'] == 'MARGEN CAJA', 'imeapu'] = margen_value
                        pyg_df.to_csv(file_path, index=False)
                        print(f"Updated {filename} with Margen: {margen_value}")
                    else:
                        print(f"Warning: 'concepto' or 'imeapu' column not found in {filename}. Skipping update.")
    except Exception as e:
        print(f"Error updating PyG files: {e}")

# --- Main Execution Block ---
if __name__ == "__main__":
    # Create a combined CSV
    csv_output_path = os.path.join(DIR_MARGEN_CAJA, 'Margenes_Ventas_Compras.csv')
    df_merged.to_csv(csv_output_path, index=False, encoding='utf-8', float_format='%.2f')
    print("\nResultado final guardado en Margenes_Ventas_Compras.csv:")
    print(df_merged)

    # Update PyG files
    update_pyg_files(df_merged, DIR_PYG_MES)
