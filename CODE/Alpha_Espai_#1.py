#########################################################################
## Generamos los datos derivados de la contabilidad equivalente a la   ##
## hoja de calculo DRXXACXXXX.                                         ##
## Coloca los csv en driectorio FINAL_RESULT                           ##
#########################################################################

import pandas as pd
import datetime
import os
import re
import subprocess
import duckdb
import time

########################################################################################
# Configuration
BASE_PATH = 'POC/SUMAS_Y_SALDOS/'
MASTERFILE_PATH = 'POC/MASTERFILES/'
DB_PATH_INTERMEDIATE = BASE_PATH + 'INTERMEDIATE/'
DB_PATH_OUTPUT = BASE_PATH + 'FINAL_RESULT/'

########################################################################################
def clean_tienda_value(tienda_value):
    """
    Clean the TIENDA value by removing any trailing numbers and commas.
    Este paso es necesario para construir el nombre de los ficheros finales por TIENDA
     
    Args:
        tienda_value (str): The original TIENDA value.
    
    Returns:
        str: The cleaned TIENDA value.
    """
    
    # Asegurarse de que el valor sea una cadena
    if not isinstance(tienda_value, str):
        tienda_value = str(tienda_value)
    
    # Eliminar caracteres inválidos para nombres de archivo
    # Los caracteres inválidos incluyen: \ / : * ? " < > |
    tienda_value = re.sub(r'[\\/:*?"<>|]', '', tienda_value)
    
    # Opcional: Reemplazar espacios por guiones bajos o guiones
    tienda_value = re.sub(r'\s+', '_', tienda_value)
    
    # Eliminar números, comas y espacios al final de la cadena (si es necesario)
    tienda_value = re.sub(r',?\s*\d+(,\s*)?$', '', tienda_value)
    
    return tienda_value

########################################################################################
def extract_franquiciado_and_year(file_path):
    """
    Extract the Franquiciado code and year from the file path.
    
    Args:
        file_path (str): The path to the .accdb file.
    
    Returns:
        tuple: A tuple containing the Franquiciado code and year.
    """
    last_dot_index = file_path.rfind('.')
    if last_dot_index != -1:
        codigo_Franquiciado = file_path[last_dot_index - 7:last_dot_index - 4]
        year = file_path[last_dot_index - 4:last_dot_index]
        return codigo_Franquiciado, year
    else:
        raise ValueError("No se encontró un punto en el nombre del archivo.")

########################################################################################
def export_table_to_df(access_file_path, table_name):
    """
    Export a table from an Access database to a DataFrame.
    
    Args:
        access_file_path (str): The path to the .accdb file.
        table_name (str): The name of the table to export.
    
    Returns:
        pd.DataFrame: The exported table as a DataFrame.
    """
    list_tables_cmd = f'mdb-tables -1 {access_file_path}'
    tables = subprocess.check_output(list_tables_cmd, shell=True).decode().split()
    
    if table_name in tables:
        export_cmd = f'mdb-export {access_file_path} {table_name}'
        df = pd.read_csv(subprocess.Popen(export_cmd, shell=True, stdout=subprocess.PIPE).stdout)
        print("Exported DataFrame Columns:", df.columns)  # Debugging: Print column names
        return df
    else:
        raise ValueError(f"La tabla '{table_name}' no existe en la base de datos.")

########################################################################################
def check_and_modify_depapu(df):
    """
    Check if there is only one unique value in DEPAPU apart from 0.
    If so, replace 0 values with that unique value.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the DEPAPU column.
    
    Returns:
        pd.DataFrame: The modified DataFrame.
    """
    if 'DEPAPU' not in df.columns:
        print("Warning: 'DEPAPU' column not found in DataFrame.")
        return df  # Return the original DataFrame if the column is missing

    unique_values = df['DEPAPU'].unique()
    unique_values = [value for value in unique_values if value != 0]
    
    if len(unique_values) == 1:
        df.loc[df['DEPAPU'] == 0, 'DEPAPU'] = unique_values[0]
    
    return df

########################################################################################
def process_accdb_file(file, base_path, db_path_intermediate, db_path_output, masterfile_path):
    """
    Process a single .accdb file.
    
    Args:
        file (str): The name of the .accdb file.
        base_path (str): The base path to the directory containing the .accdb files.
        db_path_intermediate (str): The path to the intermediate output directory.
        db_path_output (str): The path to the final output directory.
    """
    access_file_path = os.path.join(base_path, file)
    file_path = os.path.join(db_path_intermediate, file)
    file_without_extension = os.path.splitext(file_path)[0]
    table_name = 'F_APU'

    try:
        codigo_Franquiciado, year = extract_franquiciado_and_year(file_path)
        print(f"Código de Franquiciado: {codigo_Franquiciado}")
        print(f"Año: {year}")
    except ValueError as e:
        print(e)
        return

    try:
        df = export_table_to_df(access_file_path, table_name)
    except ValueError as e:
        print(e)
        return

    # Debugging: Print the first few rows of the DataFrame
    print("Exported DataFrame:")
    print(df.head())

    # Check and modify DEPAPU values
    df = check_and_modify_depapu(df)

    # Convert FECAPU to datetime and filter by DEPAPU != 0
    df['FECAPU'] = pd.to_datetime(df['FECAPU'])
    filtered_df = df[df['DEPAPU'] != 0]
    
    # Filter by CUEAPU == 4770000 to calculate current_month 
    filtered_df = filtered_df[filtered_df['CUEAPU'] == 4770000]
    
    # Get the most recent year
    most_recent_year = filtered_df['FECAPU'].dt.year.max()
    
    # Filter by the most recent year
    filtered_df = filtered_df[filtered_df['FECAPU'].dt.year == most_recent_year]
    
    # Get the highest month value for the most recent year
    current_month = filtered_df['FECAPU'].dt.month.max()

    output_path = f'{file_without_extension}_{current_month}.csv'
    print(f"Ruta de salida: {output_path}")

    file_name_without_extension = os.path.splitext(file)[0]
    raw_file = f'{db_path_intermediate}raw_{file_name_without_extension}_{current_month}.csv'

    # SQL Query to select relevant columns from the DataFrame
    query = 'SELECT FECAPU, CUEAPU, CONAPU, IMPAPU, IMEAPU, "D-HAPU", DEPAPU FROM df'
    result = duckdb.sql(query)
    result_df = result.fetchdf()

    result_df['Mes'] = current_month
    result_df['Año'] = year
    result_df['Franquiciado'] = codigo_Franquiciado

    # SQL Query to filter out rows where DEPAPU is 0 and order by CUEAPU
    query = """
    SELECT *
    FROM result_df
    WHERE DEPAPU != 0
    ORDER BY CUEAPU;
    """
    filtered_sorted_df = duckdb.sql(query).df()
    filtered_sorted_df.to_csv(raw_file, index=False)

    # SQL Query to group by CUEAPU, D-HAPU, DEPAPU, Año, Mes, and Franquiciado, and sum IMEAPU
    query = """
    SELECT
        CUEAPU,
        "D-HAPU",
        DEPAPU,
        Año,
        Mes,
        Franquiciado,
        SUM(IMEAPU) as total_IMEAPU,
        COUNT(*) as cantidad_registros
    FROM filtered_sorted_df
    GROUP BY CUEAPU, "D-HAPU", DEPAPU, Año, Mes, Franquiciado;
    """
    final_df = duckdb.sql(query).df()

    # Apply the sign change condition
    # En todos los asientos con CUEAPU comenzando por 7 se ha de cambiar el signo de IMEAPU si D-HAPU es D.
    final_df['total_IMEAPU'] = final_df.apply(lambda row: -row['total_IMEAPU'] if str(row['CUEAPU']).startswith('7') and row['D-HAPU'] == 'D' else row['total_IMEAPU'], axis=1)

    ############
    # En todos los asientos con CUEAPU comenzando por 609 se ha de cambiar el signo de IMEAPU si D-HAPU es D.
    final_df['total_IMEAPU'] = final_df.apply(lambda row: -row['total_IMEAPU'] if str(row['CUEAPU']).startswith('609') and row['D-HAPU'] == 'D' else row['total_IMEAPU'], axis=1)
    ##########

    # SQL Query to import the Masterfile_CODIGOS.csv into a DuckDB table
    query_import = f"""
    CREATE OR REPLACE TABLE codigos AS
    SELECT * FROM read_csv_auto('{masterfile_path}/Masterfile_CODIGOS.csv');
    """
    duckdb.sql(query_import)

    # SQL Query to join the final_df with the codigos table on DEPAPU = EST
    query_join = """
    CREATE OR REPLACE TABLE final_table AS
    SELECT
        f.*,  -- all fields from final_df
        c.SOCIEDAD,
        c.CIF,
        c.ATICA,
        c.Provincia,
        c.TIENDA,
        c."Nº Tiendas",
        c.sociedad_2
    FROM final_df f
    LEFT JOIN codigos c ON f.DEPAPU = c.EST;  -- changed DEPAPU to EST
    """
    duckdb.sql(query_join)

    final_df = duckdb.sql("SELECT * FROM final_table").df()
    final_df.to_csv(output_path, index=False)

    for depapu_value in final_df['DEPAPU'].unique():
        df_filtered = final_df[final_df['DEPAPU'] == depapu_value]

        for tienda_value in df_filtered['TIENDA'].unique():
            cleaned_tienda_value = clean_tienda_value(tienda_value)
            df_tienda = df_filtered[df_filtered['TIENDA'] == tienda_value]

            if not df_tienda.empty:
                year = df_tienda['Año'].iloc[0]
                mes = df_tienda['Mes'].iloc[0]
                filename = f"{db_path_output}{cleaned_tienda_value}_{depapu_value}_{year}_{mes}.csv"
                df_tienda.to_csv(filename, index=False)

    print("Datos separados en archivos CSV.")

########################################################################################
# Main function to process all .accdb files in the directory
def main():
    start_time = time.time()

    for file in os.listdir(BASE_PATH):
        if file.endswith('.accdb'):
            process_accdb_file(file, BASE_PATH, DB_PATH_INTERMEDIATE, DB_PATH_OUTPUT, MASTERFILE_PATH)

    end_time = time.time()
    print(f"Tiempo total de ejecución: {end_time - start_time:.2f} segundos")

if __name__ == "__main__":
    main()