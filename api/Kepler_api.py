import os
import requests
import io
import pandas as pd
import re


def get_csv_files(url_list):

    if not os.path.exists("excel"):
        os.makedirs("excel")

    if not os.path.exists("models"):
        os.makedirs("models")


    for url_query in url_list: # Itera en todas las paginas de la lista ingresada

        pattern = r"table=(.*)&"
        search_obj = re.compile(pattern) 
        search_result = search_obj.search(url_query) 

        #nombrar tabla
        if search_result is not None:
            table_name  = search_result.group(1) + '.csv' # Asigna un nombre al archivo desde un patron de string si es que se encuentra uno
            print(f'Tabla : {table_name}')
        else: # si no se encuentra ningun patron de string se le asigna un nombre unico a la tabla se le asignara un numero de acuerdo al index de la lista
            index = url_list.index(url_query) # Entrega la ubicacion del url en la lista entregada
            table_name = 'tabla_' + str(index) + '.csv'
            print(f"No se ha encontrado {pattern[:-6]} en {url_query}. Por lo que la tabla se llamara: {table_name}")

        #convertir tabla proveniente de la api a .csv
        try:
            print('Solicitando e importando datos a DataFrame .......')
            url = requests.get(url_query, stream=True).content ## la libreria requests permite obtener la tabla desde la api, el parametro stream permite que la conexion permanezca por mas tiempo
            df_scraping=pd.read_csv(io.StringIO(url.decode('utf-8')), low_memory=False) # Decofidifica el .csv en formato UTF-8 y la asigna a una variable como un dataframe de pandas
            print(f'Guardando el archivo {table_name}')
            df_scraping.to_csv(f"excel/{table_name}", index=False) # Escribiendo el dataframe a un archivo .csv
            print(f"Se ha guardado el archivo {table_name}")
        except Exception as e:
            print(f"Ha ocurrido un error {e} intentardo guardar el archivo {table_name} tratando de obtener datos desde : {url_query}")