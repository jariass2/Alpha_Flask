#########################################################################
## Procesa files en FINAL_RESULT para hacer comprobación de descuadres ##
## Restar Haber - Debe por grupos 6 y 7                                ##
## Restar total grupo 6 - total grupo 7                                ##
##                                                                     ##
#########################################################################

#1. Sumamos todos los registros con CUEAPU comenzando por 7 y valor de D-HAPU igual a H
#2. En los registros con CUEAPU comenzando por 7 y valor de D-HAPU igual a D se les coloca signo negativo a los que sean positivos y se suman.
#3. Sumamos los  resultados de las dos operaciones anteriores para conseguir total grupo 7
#4. Sumamos todos los registros con CUEAPU comenzando por 6 y valor de D-HAPU igual a H
#5. En los registros con CUEAPU comenzando por 6 y valor de D-HAPU igual a D se les coloca signo negativo a los que sean positivos y se suman.
#6. Sumamos los  resultados de las dos operaciones anteriores para conseguir total grupo 6
#7. Sumamos el resultado de procesar los registros 7 con el resultado de los registros 6


import os
import pandas as pd
import locale

# Configuración
RUTA_BASE = 'POC/'
DIR_RESULTADOS_FINALES = os.path.join(RUTA_BASE, 'SUMAS_Y_SALDOS', 'FINAL_RESULT')

# Configura el locale para usar coma como separador decimal y punto para miles
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

def procesar_archivos():
    # Itera sobre los archivos en el directorio de resultados finales
    for filename in os.listdir(DIR_RESULTADOS_FINALES):
        if filename.endswith('.csv'):  # Asume que los archivos son CSV
            file_path = os.path.join(DIR_RESULTADOS_FINALES, filename)
            print(f'Procesando archivo: {filename}')  # Imprime el nombre del archivo actualmente procesado

            # Lee el archivo en un DataFrame de pandas
            df = pd.read_csv(file_path)

            # Inicializa los totales para cada archivo
            total_7_h = 0
            total_7_d = 0
            total_6_h = 0
            total_6_d = 0

            # 1. Sumamos todos los registros con CUEAPU comenzando por 7 y valor de D-HAPU igual a H
            cueapu_7_h = df[(df['CUEAPU'].astype(str).str.startswith('7')) & (df['D-HAPU'] == 'H')]
            total_7_h = cueapu_7_h['total_IMEAPU'].sum()

            # 2. En los registros con CUEAPU comenzando por 7 y valor de D-HAPU igual a D, se les coloca signo negativo a los que sean positivos y se suman
            cueapu_7_d = df[(df['CUEAPU'].astype(str).str.startswith('7')) & (df['D-HAPU'] == 'D')]
            #total_7_d = cueapu_7_d['total_IMEAPU'].apply(lambda x: -x if x > 0 else x).sum()
            total_7_d = -cueapu_7_d['total_IMEAPU'].sum()

            # 3. Sumamos los resultados de las dos operaciones anteriores para conseguir total grupo 7
            total_7 = total_7_h + total_7_d

            # 4. Sumamos todos los registros con CUEAPU comenzando por 6 y valor de D-HAPU igual a H
            cueapu_6_h = df[(df['CUEAPU'].astype(str).str.startswith('6')) & (df['D-HAPU'] == 'H')]
            total_6_h = cueapu_6_h['total_IMEAPU'].sum()

            # 5. En los registros con CUEAPU comenzando por 6 y valor de D-HAPU igual a D, se les coloca signo negativo a los que sean positivos y se suman
            cueapu_6_d = df[(df['CUEAPU'].astype(str).str.startswith('6')) & (df['D-HAPU'] == 'D')]
            #total_6_d = cueapu_6_d['total_IMEAPU'].apply(lambda x: -x if x > 0 else x).sum()
            total_6_d = -cueapu_6_d['total_IMEAPU'].sum()

            # 6. Sumamos los resultados de las dos operaciones anteriores para conseguir total grupo 6
            total_6 = total_6_h + total_6_d

            # 7. Restamos el resultado de procesar los registros 7 con el resultado de los registros 6
            resultado = total_7 + total_6

            # Imprime todos los resultados con formato de dos decimales para cada archivo
            print(f'Archivo: {filename}')
            print(f'Valor total_6_h: {locale.format_string("%.2f", total_6_h, grouping=True)}')
            print(f'Valor total_6_d: {locale.format_string("%.2f", total_6_d, grouping=True)}')
            print(f'Valor total_7_h: {locale.format_string("%.2f", total_7_h, grouping=True)}')
            print(f'Valor total_7_d: {locale.format_string("%.2f", total_7_d, grouping=True)}')
            print(f'Valor total_6: {locale.format_string("%.2f", total_6, grouping=True)}')
            print(f'Valor total_7: {locale.format_string("%.2f", total_7, grouping=True)}')
            print(f'Valor resultado: {locale.format_string("%.2f", resultado, grouping=True)}')
            print('---')

if __name__ == "__main__":
    procesar_archivos()
