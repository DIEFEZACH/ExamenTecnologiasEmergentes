import pandas as pd
import requests
import hashlib
import time
import sqlite3
import json
from concurrent.futures import ThreadPoolExecutor

# Obtener datos de la API
response = requests.get("https://restcountries.com/v3.1/all")
countries = response.json()

# Función para encriptar con SHA1
def sha1_encrypt(text):
    return hashlib.sha1(text.encode('utf-8')).hexdigest()

# Función para procesar cada país
def process_country(country):
    data = []
    region = country.get('region', '')
    city_name = country.get('name', {}).get('common', '')
    languages = country.get('languages', {}).values()
    
    for language in languages:
        start_time = time.time()
        encrypted_language = sha1_encrypt(language)
        end_time = time.time()
        processing_time = end_time - start_time
        
        data.append({
            "Region": region,
            "City Name": city_name,
            "Language": encrypted_language,
            "Time": processing_time
        })
    return data

# Usar ThreadPoolExecutor para paralelizar
with ThreadPoolExecutor() as executor:
    results = list(executor.map(process_country, countries))

# Aplanar la lista de resultados
data = [item for sublist in results for item in sublist]

# Crear el DataFrame
df = pd.DataFrame(data)

# Calcular métricas de tiempo
total_time = df['Time'].sum()
average_time = df['Time'].mean()
min_time = df['Time'].min()
max_time = df['Time'].max()

print(f"Total Time: {total_time:.2f} ms")
print(f"Average Time: {average_time:.2f} ms")
print(f"Min Time: {min_time:.2f} ms")
print(f"Max Time: {max_time:.2f} ms")

# Guardar en SQLite
conn = sqlite3.connect('data.db')
df.to_sql('countries', conn, if_exists='replace', index=False)
conn.close()

# Guardar en JSON
df.to_json('data.json', orient='records', lines=True)
