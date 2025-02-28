#########################################################################
## CALCULAR ENTAS BRUTAS en PyG_mes                                    ##
## Identificar Mes y Año                                               ##
## Extraer Ventas Brutas Fichero Carrefour y crear df                  ##
## Calcular mes_anterior                                               ##
## Sumar valores desde enero hasta mes_anterior                        ##
## Guardar Resultado en PyG_mes                                        ##
## CALCULAR COMPRAS MERCADERIAS                                        ##
## Idem                                                                ##
## Cambia el ceco code de los datos de VENTAS por el codigo ATICA      ##
##                                                                     ##
##                                                                     ##
#########################################################################

import pandas as pd
import os
from datetime import datetime
import re

# --- Configuration ---
# Nombres de las hojas en los archivos Excel
SHEET_NAME_VENTAS = 'VTATOTAL'
SHEET_NAME_COMPRAS = 'COMPRAS'

# Columnas para el proceso de ventas.  Now using index-based names.
COLUMNA_VENTAS_CECO = 3 # Index of CECO column
COLUMNA_VENTAS_BRUTAS = 'ventas_brutas'

# Columnas para el proceso de compras. Now using index-based names.
COLUMNA_COMPRAS_CECO = 9 # Index of CECO column
COLUMNA_COMPRAS = 'compras'

# Columnas en el Masterfile
COLUMNA_MASTERFILE_ATICA = 'ATICA'
COLUMNA_MASTERFILE_TIENDA = 'TIENDA'
COLUMNA_MASTERFILE_EST = 'EST'

# Índices de inicio para las columnas de mes en los archivos Excel
COLUMNA_VENTAS_MES_START_INDEX = 5
COLUMNA_COMPRAS_MES_START_INDEX = 10

# Columnas en los PyG
COLUMNA_PYG_CONCEPTO = 'concepto'
COLUMNA_PYG_IMEAPU = 'imeapu'

# --- Fin de la configuración de variables ---

# Configurar Pandas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Define base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_BASE = os.path.join(BASE_DIR, 'POC')
DIR_VENTAS_BRUTAS = os.path.join(RUTA_BASE, 'VENTAS_BRUTAS')
DIR_COMPRAS_MERCANCIAS = os.path.join(RUTA_BASE, 'COMPRAS_MERCANCIAS')
DIR_PYG_MES = os.path.join(RUTA_BASE, 'PYG_MES')
DIR_MASTERFILE = os.path.join(RUTA_BASE, 'MASTERFILES')

# Obtener mes y año anterior
current_date = datetime.now()
current_month = current_date.month
current_year = current_date.year
if current_month == 1:
    previous_month = 12
    previous_year = current_year - 1
else:
    previous_month = current_month - 1
    previous_year = current_year

########## Debugging #####################################
# previous_month = 1
# previous_year = 2024
##########################################################

def convert_euro_format(value):
    """Convierte valores en formato europeo to float"""
    try:
        if pd.isna(value) or value == 0:
            return pd.NA
        value = str(value).replace('€', '').replace('.', '', str(value).count('.')-1).replace(',', '.').strip()
        result = float(value)
        return result if result != 0 else pd.NA
    except ValueError:
        return pd.NA

def process_ventas_brutas(directory, sheet_name, previous_month, month_col_start_index=COLUMNA_VENTAS_MES_START_INDEX):
    excel_files = [f for f in os.listdir(directory) if f.endswith(('.xlsx', '.xls'))]
    if not excel_files:
        raise FileNotFoundError(f"No Excel files found in {directory}")
    file_path = os.path.join(directory, excel_files[0])
    try:
        if file_path.lower().endswith(".xlsx"):
            df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
        elif file_path.lower().endswith(".xls"):
            df = pd.read_excel(file_path, sheet_name=sheet_name, engine='xlrd')
        else:
            raise ValueError("Unsupported file type. Use .xlsx or .xls")
    except Exception as e:
        raise Exception(f"Error reading Excel file '{file_path}': {e}") from None
    df = df.dropna(how='all')
    # Ensure that columns are strings
    df.columns = [str(col) for col in df.iloc[0]]
    df = df[1:]

    ceco_sums = {}
    for index, row in df.iterrows():
        try:
            ceco = str(row.iloc[COLUMNA_VENTAS_CECO]).strip()
        except IndexError:
            continue
        if pd.isna(ceco) or len(ceco) != 4:
            continue
        total_ventas = 0
        for col_index in range(month_col_start_index, month_col_start_index + previous_month):
            try:
                value = row.iloc[col_index]
                if pd.isna(value):
                    continue
                total_ventas += float(value)
            except (IndexError, ValueError, TypeError) as e:
                print(f"Error processing cell at index {col_index} for CECO '{ceco}': {e}")
                pass
        # Only add to ceco_sums if total_ventas is not 0
        if total_ventas != 0:
            ceco_sums[ceco] = total_ventas
        else:
            ceco_sums[ceco] = pd.NA

    result_df = pd.DataFrame(list(ceco_sums.items()), columns=[COLUMNA_VENTAS_CECO, COLUMNA_VENTAS_BRUTAS])
    # Ensure zero values are converted to NA
    result_df[COLUMNA_VENTAS_BRUTAS] = result_df[COLUMNA_VENTAS_BRUTAS].replace(0, pd.NA)
    return result_df

def process_compras(directory, sheet_name, previous_month, month_col_start_index=COLUMNA_COMPRAS_MES_START_INDEX):
    """Processes compras data, ensuring correct column summation."""
    try:
        excel_files = [f for f in os.listdir(directory) if f.endswith(('.xlsx', '.xls'))]
        if not excel_files:
            raise FileNotFoundError(f"No Excel files found in {directory}")
        file_path = os.path.join(directory, excel_files[0])

        engine = 'openpyxl' if file_path.lower().endswith('.xlsx') else 'xlrd'
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine=engine)

        df = df.dropna(how='all')
        if not all(isinstance(col, str) for col in df.columns):
            raise ValueError("Column headers must be strings.")
        df.columns = df.columns.astype(str)
        df = df[1:]

        ceco_column_index = COLUMNA_COMPRAS_CECO  # Index of the CECO column
        ceco_column_name = df.columns[ceco_column_index] # Name of CECO
        
        month_col_start_index = COLUMNA_COMPRAS_MES_START_INDEX
        
        last_month_index = month_col_start_index + previous_month
        month_columns = df.columns[month_col_start_index:last_month_index]

        if not all(col in df.columns for col in [ceco_column_name] + list(month_columns)):
            raise ValueError(f"Missing required columns in '{file_path}'.")
        #Extract the column
        compras_df = df[[ceco_column_name] + list(month_columns)].copy()
        compras_df = compras_df.rename(columns={ceco_column_name: COLUMNA_COMPRAS_CECO})
        compras_df[COLUMNA_COMPRAS] = compras_df[month_columns].apply(
            lambda row: sum(convert_euro_format(x) for x in row if pd.notna(x)), axis=1
        )
        compras_df = compras_df[[COLUMNA_COMPRAS_CECO, COLUMNA_COMPRAS]].copy()
        compras_df[COLUMNA_COMPRAS] = compras_df[COLUMNA_COMPRAS].replace(0, pd.NA)
        compras_df[COLUMNA_COMPRAS] = compras_df[COLUMNA_COMPRAS].apply(
            lambda x: round(x, 2) if pd.notna(x) else pd.NA
        )

        return compras_df

    except Exception as e:
        print(f"Error in process_compras: {e}")
        return None

def process_masterfile(directory):
    """Loads Masterfile_CODIGOS.csv and extracts ATICA, TIENDA, and EST columns."""
    file_path = os.path.join(directory, 'Masterfile_CODIGOS.csv')
    try:
        df = pd.read_csv(file_path)
        masterfile_df = df[[COLUMNA_MASTERFILE_ATICA, COLUMNA_MASTERFILE_TIENDA, COLUMNA_MASTERFILE_EST]]
        return masterfile_df
    except FileNotFoundError:
        print(f"Error: Masterfile_CODIGOS.csv not found in {directory}")
        return None

def save_merged_dataframe_to_csv(df, directory, previous_month, previous_year):
    """Save the merged DataFrame to a CSV file with the specified naming convention."""
    filename = f"Ventas_y_Compras_{previous_month}_{previous_year}.csv"
    file_path = os.path.join(directory, filename)

    # Round only non-NA values
    df[COLUMNA_VENTAS_BRUTAS] = df[COLUMNA_VENTAS_BRUTAS].apply(lambda x: round(x, 2) if pd.notna(x) else x)
    df[COLUMNA_COMPRAS] = df[COLUMNA_COMPRAS].apply(lambda x: round(x, 2) if pd.notna(x) else x)

    df.to_csv(file_path, index=False, na_rep='')
    print(f"DataFrame saved to {file_path}")

def process_pyg_files(df, directory, previous_month, previous_year):
    """
    Searches for the corresponding PyG file in the directory based on EST code, previous month, and year and updates the "imeapu" column.
    """
    for index, row in df.iterrows():
        est_code = str(row[COLUMNA_MASTERFILE_EST])
        ventas_brutas = row[COLUMNA_VENTAS_BRUTAS]
        compras = row[COLUMNA_COMPRAS]

        # Construct a regex pattern to match the file name
        #file_pattern = re.compile(r"^[^\d]*?(\d+)_(\d{4})_(\d{1,2})_PyG\.csv$")
        file_pattern = re.compile(r".*?(\d+)_?(\d{4})_?(\d{1,2})_PyG\.csv$", re.IGNORECASE)

        found_file = None
        for filename in os.listdir(directory):
            match = file_pattern.match(filename)
            if match:
                matched_est = match.group(1)
                matched_year = int(match.group(2))
                matched_month = int(match.group(3))

                if matched_est == est_code and matched_year == previous_year and matched_month == previous_month:
                    found_file = filename
                    break

        if found_file:
            file_path = os.path.join(directory, found_file)
            try:
                pyg_df = pd.read_csv(file_path)

                if pyg_df.empty:
                    print(f"Skipping empty file: {found_file}")
                    continue

                pyg_df[COLUMNA_PYG_CONCEPTO] = pyg_df[COLUMNA_PYG_CONCEPTO].astype(str)

                # Update ventas_brutas
                ventas_row_index = pyg_df[pyg_df[COLUMNA_PYG_CONCEPTO] == 'VENTA BRUTA (SIN CONCESIONES)'].index
                if not ventas_row_index.empty:
                    pyg_df.loc[ventas_row_index, COLUMNA_PYG_IMEAPU] = ventas_brutas
                else:
                    print(f"Concepto 'VENTA BRUTA (SIN CONCESIONES)' not found in: {found_file}")

                # Update compras
                compras_row_index = pyg_df[pyg_df[COLUMNA_PYG_CONCEPTO] == 'COMPRAS'].index
                if not compras_row_index.empty:
                    pyg_df.loc[compras_row_index, COLUMNA_PYG_IMEAPU] = compras
                else:
                    print(f"Concepto 'COMPRAS' not found in: {found_file}")

                # Save the updated DataFrame back to the original file
                pyg_df.to_csv(file_path, index=False)
                print(f"Updated {found_file}")

            except Exception as e:
                print(f"Error processing {found_file}: {e}")
        else:
            print(f"File not found for EST: {est_code}, Previous Month: {previous_month}, Previous Year: {previous_year}")

try:
    # Procesar ventas y compras
    DIR_COMPRAS_MERCANCIAS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'POC', 'COMPRAS_MERCANCIAS')

    ventas_df = process_ventas_brutas(DIR_VENTAS_BRUTAS, SHEET_NAME_VENTAS, previous_month)
    compras_df = process_compras(DIR_COMPRAS_MERCANCIAS, SHEET_NAME_COMPRAS, previous_month)
    masterfile_df = process_masterfile(DIR_MASTERFILE)

    # Convertir las columnas relevantes a string para asegurar la fusión
    if masterfile_df is not None:
        masterfile_df[COLUMNA_MASTERFILE_ATICA] = masterfile_df[COLUMNA_MASTERFILE_ATICA].astype(str)
        masterfile_df[COLUMNA_MASTERFILE_EST] = masterfile_df[COLUMNA_MASTERFILE_EST].astype(str)
    if ventas_df is not None:
        ventas_df[COLUMNA_VENTAS_CECO] = ventas_df[COLUMNA_VENTAS_CECO].astype(str)
    if compras_df is not None:
        compras_df[COLUMNA_COMPRAS_CECO] = compras_df[COLUMNA_COMPRAS_CECO].astype(str)

    # Fusionar ventas_df con masterfile_df para obtener 'EST'
    if ventas_df is not None and masterfile_df is not None:
        ventas_df = pd.merge(ventas_df, masterfile_df[[COLUMNA_MASTERFILE_ATICA, COLUMNA_MASTERFILE_EST]],
                             left_on=COLUMNA_VENTAS_CECO, right_on=COLUMNA_MASTERFILE_ATICA, how='left')
        ventas_df.dropna(subset=[COLUMNA_MASTERFILE_EST], inplace=True)
        ventas_df.drop(columns=[COLUMNA_MASTERFILE_ATICA], inplace=True)

    # Fusionar compras_df con masterfile_df para obtener 'EST'
    if compras_df is not None and masterfile_df is not None:
        compras_df = pd.merge(compras_df, masterfile_df[[COLUMNA_MASTERFILE_EST]],
                             left_on=COLUMNA_COMPRAS_CECO, right_on=COLUMNA_MASTERFILE_EST, how='left')
        compras_df.dropna(subset=[COLUMNA_MASTERFILE_EST], inplace=True)
        compras_df.drop(columns=[COLUMNA_COMPRAS_CECO], inplace=True)

    # Fusionar los DataFrames de ventas y compras en 'EST'
    if ventas_df is not None and compras_df is not None:
        merged_df = pd.merge(ventas_df, compras_df, on=COLUMNA_MASTERFILE_EST, how='outer')

        # Fusionar con masterfile_df para obtener 'TIENDA'
        if masterfile_df is not None:
            merged_df = pd.merge(merged_df, masterfile_df[[COLUMNA_MASTERFILE_EST, COLUMNA_MASTERFILE_TIENDA]],
                                 on=COLUMNA_MASTERFILE_EST, how='left')

        # Eliminar columnas no necesarias y asegurar el orden correcto
        merged_df = merged_df[[COLUMNA_MASTERFILE_EST, COLUMNA_VENTAS_BRUTAS, COLUMNA_COMPRAS, COLUMNA_MASTERFILE_TIENDA]]

        print("\nDataFrame Consolidado (Ventas, Compras, EST y Tienda):")
        print(merged_df)

        # Guardar el DataFrame final
        save_merged_dataframe_to_csv(merged_df, DIR_PYG_MES, previous_month, previous_year)

        #Process PyG files and updates
        process_pyg_files(merged_df, DIR_PYG_MES, previous_month, previous_year)
    else:
        print("No se pudo generar el DataFrame consolidado porque ventas_df o compras_df es None.")
except Exception as e:
    print(f"Error: {e}")