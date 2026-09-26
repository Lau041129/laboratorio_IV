import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Cargar el archivo CSV interpretando timestamp como fecha y usándolo como índice
df = pd.read_csv('telemetria_nodo_iot.csv', parse_dates=['timestamp'], index_col='timestamp')

# Verificar la carga correcta
print("--- PRIMERAS FILAS DEL DATAFRAME ---")
print(df.head())
print("\n--- INFORMACIÓN GENERAL ---")
print(df.info()) 

# 2. Estadísticas descriptivas de cada variable numérica
print("\n--- ESTADÍSTICAS DESCRIPTIVAS ---")
estadisticas = df.describe().loc[['mean', 'min', 'max', 'std']]
print(estadisticas)

# 3. Análisis de Alertas
print("\n--- ANÁLISIS DE ALERTAS ---")

# Voltaje
voltaje = df['voltaje_bateria_V'].to_numpy()
alerta_voltaje_bajo = voltaje < 3.5
cant_alerta_voltaje_bajo = np.sum(alerta_voltaje_bajo)
print(f"Alertas de batería baja: {cant_alerta_voltaje_bajo}")

# Temperatura
temperatura = df['temperatura_C'].to_numpy()
alerta_temperatura_alta = temperatura > 23
cant_alerta_temperatura_alta = np.sum(alerta_temperatura_alta)
print(f"Alertas de temperatura alta: {cant_alerta_temperatura_alta}")

# Señal
rssi = df['rssi_dbm'].to_numpy()
alerta_senal_baja = rssi < -85
cant_alerta_senal = np.sum(alerta_senal_baja)
print(f"Alertas de señal débil: {cant_alerta_senal}")

# Humedad
humedad = df['humedad_pct'].to_numpy()
alerta_humedad_alta = humedad > 80
cant_alerta_humedad = np.sum(alerta_humedad_alta)
print(f"Alertas de humedad alta: {cant_alerta_humedad}")

# Al menos una alerta
alerta = alerta_voltaje_bajo | alerta_senal_baja | alerta_temperatura_alta | alerta_humedad_alta
cant_alerta_cualquiera = np.sum(alerta)
print(f"Registros con al menos una alerta: {cant_alerta_cualquiera}")

# (Importante: guardamos la alerta en el DataFrame para usarla en los gráficos y resúmenes)
df['alerta'] = alerta

# print("\n")
# print(df.describe())