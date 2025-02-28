#########################################################################
## Captura valores margen caja en secciones                            ##
## Diferencia entre margen Demarca Controlada y                        ##
## Demarca Incontrolada                                                ##
##                                                                     ##
##                                                                     ##
## Guardar Resultado en ficheros establecimientos del PyG_mes          ##
##                                                                     ##
#########################################################################

import os
import pandas as pd
from datetime import datetime
import calendar
import re

# --- Configuration ---
SHEET_NAME_MES = 'Mes'
COLUMNA_MASTERFILE_ATICA = 'ATICA'
COLUMNA_MASTERFILE_TIENDA = 'TIENDA'  # Added TIENDA
COLUMNA_MASTERFILE_EST = 'EST'
COLUMNA_VENTAS_MES_START_INDEX = 6
COLUMNA_COMPRAS_MES_START_INDEX = 10
COLUMNA_PYG_CONCEPTO = 'concepto'
COLUMNA_PYG_IMEAPU = 'imeapu'
COLUMNA_PYG_CODIGO_2 = 'codigo_2'
COLUMNA_MARGEN_CAJA_ATICA_INDEX = 0
COLUMNA_SECCION_INDEX = 10
COLUMNA_MARGEN_CAJA_DEMARCA_COMNTROLADA_INDEX = 32
COLUMNA_MARGEN_CAJA_DEMARCA_INCOMNTROLADA_INDEX = 34

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_BASE = os.path.join(BASE_DIR, 'POC')
DIR_PYG_MES = os.path.join(RUTA_BASE, 'PYG_MES')
DIR_MASTERFILE = os.path.join(RUTA_BASE, 'MASTERFILES')
DIR_MARGEN_CAJA = os.path.join(RUTA_BASE, 'MARGEN_CAJA')

def convert_euro_format(value):
    """Convierte valores en formato europeo a float"""
    try:
        if pd.isna(value) or value == 0:
            return 0.0
        value = str(value).replace('€', '').replace('.', '', str(value).count('.') - 1).replace(',', '.').strip()
        return float(value)
    except ValueError:
        return 0.0

def get_target_month_names(current_month_number):
    """Returns a list of month names (uppercase) from January to the previous month."""
    spanish_months = {
        1: 'ENERO', 2: 'FEBRERO', 3: 'MARZO', 4: 'ABRIL', 5: 'MAYO', 6: 'JUNIO',
        7: 'JULIO', 8: 'AGOSTO', 9: 'SEPTIEMBRE', 10: 'OCTUBRE', 11: 'NOVIEMBRE', 12: 'DICIEMBRE'
    }
    return [spanish_months[m] for m in range(1, current_month_number)]

def process_margen_caja(directory, current_month):
    """Processes multiple MARGEN_CAJA worksheets, accumulating data."""
    try:
        excel_files = [f for f in os.listdir(directory) if f.endswith(('.xlsx', '.xls'))]
        if not excel_files:
            raise FileNotFoundError(f"No Excel files found in {directory}")

        file_path = os.path.join(directory, excel_files[0])
        xl = pd.ExcelFile(file_path)
        target_months = get_target_month_names(current_month)
        print(f"Target month names: {target_months}")

        all_data = []
        for sheet_name in xl.sheet_names:
            if sheet_name.upper() == SHEET_NAME_MES.upper():
                continue

            for target_month in target_months:
                if sheet_name.upper().startswith(target_month + " ") and len(sheet_name) == len(target_month) + 3:
                    try:
                        df = pd.read_excel(xl, sheet_name=sheet_name, header=None)

                        temp_df = pd.DataFrame({
                            'ATICA': df.iloc[:, COLUMNA_MARGEN_CAJA_ATICA_INDEX],
                            'SECCION': df.iloc[:, COLUMNA_SECCION_INDEX],
                            'CAJA_CONTROLADA': df.iloc[:, COLUMNA_MARGEN_CAJA_DEMARCA_COMNTROLADA_INDEX],
                            'CAJA_INCONTROLADA': df.iloc[:, COLUMNA_MARGEN_CAJA_DEMARCA_INCOMNTROLADA_INDEX]
                        })

                        temp_df.dropna(subset=['ATICA'], inplace=True)
                        temp_df = temp_df[temp_df['ATICA'].astype(str).str.strip() != '']
                        temp_df = temp_df[temp_df['ATICA'].astype(str) != '0']
                        temp_df = temp_df[~temp_df['SECCION'].astype(str).str.contains('Total', case=False)]
                        temp_df = temp_df[~temp_df['SECCION'].isna()]
                        temp_df = temp_df[temp_df['SECCION'].astype(str).str.strip() != '']
                        temp_df['ATICA'] = temp_df['ATICA'].astype(str).str.strip()
                        temp_df['SECCION'] = temp_df['SECCION'].astype(str)

                        for col in ['CAJA_CONTROLADA', 'CAJA_INCONTROLADA']:
                            temp_df[col] = temp_df[col].apply(convert_euro_format)

                        all_data.append(temp_df)
                    except Exception as e:
                        print(f"Error reading sheet {sheet_name}: {e}")
                        continue

        if not all_data:
            raise ValueError("No valid data found in any of the worksheets.")

        margen_df = pd.concat(all_data, ignore_index=True)
        margen_df = margen_df.groupby(['ATICA', 'SECCION'])[['CAJA_CONTROLADA', 'CAJA_INCONTROLADA']].sum().reset_index()

        masterfile_path = os.path.join(DIR_MASTERFILE, 'Masterfile_CODIGOS.csv')
        masterfile_df = pd.read_csv(masterfile_path)
        masterfile_df = masterfile_df.rename(columns={
            COLUMNA_MASTERFILE_ATICA: 'ATICA',
            COLUMNA_MASTERFILE_EST: 'EST',
            COLUMNA_MASTERFILE_TIENDA: 'TIENDA'  # Rename TIENDA
        })
        # Include TIENDA in the merge
        masterfile_df = masterfile_df[['ATICA', 'EST', 'TIENDA']]

        margen_df = pd.merge(margen_df, masterfile_df, on='ATICA', how='left')
        margen_df['EST'] = pd.to_numeric(margen_df['EST'].astype(str).str.split('.').str[0], errors='coerce').fillna(0).astype(int)

        for col in ['CAJA_CONTROLADA', 'CAJA_INCONTROLADA']:
            margen_df[col] = pd.to_numeric(margen_df[col], errors='coerce').fillna(0)

        # Include TIENDA in the output columns
        margen_df = margen_df[['ATICA', 'TIENDA', 'EST', 'SECCION', 'CAJA_CONTROLADA', 'CAJA_INCONTROLADA']]
        margen_df.columns = ['Código ATICA', 'Tienda', 'Código EST', 'Sección', 'Demarca Controlada', 'Demarca Incontrolada']

        for col in ['Demarca Controlada', 'Demarca Incontrolada']:
            margen_df[col] = margen_df[col].apply(lambda x: '{:.2f}'.format(x))

        output_file = os.path.join(directory, 'Margenes_Detalle_por_seccion.csv')
        margen_df.to_csv(output_file, index=False, na_rep='')

        return margen_df

    except Exception as e:
        print(f"Error processing margin file: {e}")
        return None

def update_pyg_files(margen_df, pyg_directory):
    """Updates PyG files with aggregated margin data."""
    try:
        for filename in os.listdir(pyg_directory):
            if not filename.endswith('.csv'):
                continue

            match = re.search(r'_(\d{4})_', filename)
            if not match:
                print(f"Skipping file: {filename} (doesn't match expected format)")
                continue

            est_code = int(match.group(1))
            file_path = os.path.join(pyg_directory, filename)
            pyg_df = pd.read_csv(file_path)
            print(f"\n--- Processing PyG file: {filename}, EST Code: {est_code} ---")

            est_rows = margen_df[margen_df['Código EST'] == est_code].copy()

            if est_rows.empty:
                print(f"No matching data found for EST code {est_code}. Skipping.")
                continue

            for _, row in est_rows.iterrows():
                seccion = row['Sección']
                controlada_concepto = f'VARIACION EXISTENCIAS DEMARCA CONTROLADA{seccion}'
                incontrolada_concepto = f'VARIACION EXISTENCIAS DEMARCA INCONTROLADA{seccion}'

                if controlada_concepto in pyg_df[COLUMNA_PYG_CONCEPTO].values:
                    try:
                        row_index = pyg_df[pyg_df[COLUMNA_PYG_CONCEPTO] == controlada_concepto].index
                        if not row_index.empty:
                            print(f"    Updating '{controlada_concepto}' with value: {row['Demarca Controlada']}")
                            pyg_df.loc[row_index[0], COLUMNA_PYG_IMEAPU] = float(row['Demarca Controlada'])
                        else:
                            print(f"    ERROR: Could not find row index for '{controlada_concepto}'")
                    except ValueError as e:
                        print(f"    Error updating '{controlada_concepto}': {e}")
                else:
                    print(f"    Concept '{controlada_concepto}' NOT FOUND in PyG file.")

                if incontrolada_concepto in pyg_df[COLUMNA_PYG_CONCEPTO].values:
                    try:
                        row_index = pyg_df[(pyg_df[COLUMNA_PYG_CONCEPTO] == incontrolada_concepto) &
                                           (~pyg_df[COLUMNA_PYG_CODIGO_2].astype(str).str.startswith('61004'))].index
                        if not row_index.empty:
                            print(f"    Updating '{incontrolada_concepto}' with value: {row['Demarca Incontrolada']}")
                            pyg_df.loc[row_index[0], COLUMNA_PYG_IMEAPU] = float(row['Demarca Incontrolada'])
                        else:
                            print(f"    ERROR: Could not find row index for '{incontrolada_concepto}'")

                    except ValueError as e:
                        print(f"    Error updating '{incontrolada_concepto}': {e}")
                else:
                    print(f"    Concept '{incontrolada_concepto}' NOT FOUND in PyG file.")

            pyg_df.to_csv(file_path, index=False)
            print(f"Updated file: {filename}")

    except Exception as e:
        print(f"Error updating PyG files: {e}")

if __name__ == "__main__":
    current_month = datetime.now().month
    
    ######################################
    # current_month = 10  # For testing
    ######################################
    
    
    try:
        margen_df = process_margen_caja(DIR_MARGEN_CAJA, current_month)
        if margen_df is not None:
            print("\nComplete Margen de Caja DataFrame:")
            print(margen_df)
            print("\nUpdating PyG files...")
            update_pyg_files(margen_df, DIR_PYG_MES)
    except Exception as e:
        print(f"Error in main execution: {e}")