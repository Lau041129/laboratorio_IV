# https://github.com/Lau041129/laboratorio_IV

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

# Guardamos la alerta en el DataFrame para usarla en los gráficos y resúmenes
df['alerta'] = alerta

# 4. Evolución Temporal y Detección de Alertas con Matplotlib
print("\n--- GENERANDO GRÁFICO DE EVOLUCIÓN TEMPORAL ---")
fig, ax1 = plt.subplots(figsize=(12, 6))

color_temp = 'tab:red'
ax1.set_xlabel('Fecha y Hora')
ax1.set_ylabel('Temperatura (°C)', color=color_temp)
line1 = ax1.plot(df.index, df['temperatura_C'], color=color_temp, label='Temperatura (°C)', alpha=0.8)
ax1.tick_params(axis='y', labelcolor=color_temp)

ax2 = ax1.twinx()  
color_volt = 'tab:blue'
ax2.set_ylabel('Voltaje de Batería (V)', color=color_volt)
line2 = ax2.plot(df.index, df['voltaje_bateria_V'], color=color_volt, label='Voltaje Batería (V)', alpha=0.8)
ax2.tick_params(axis='y', labelcolor=color_volt)

df_alertas = df[df['alerta']]
scatter_alertas = ax2.scatter(df_alertas.index, df_alertas['voltaje_bateria_V'], 
                              color='darkred', zorder=5, label='Alerta Detectada', s=25)

plt.title('Evolución Temporal de Temperatura y Batería con Indicación de Alertas')
lines = line1 + line2 + [scatter_alertas]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper right')

ax1.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# 5. Resumen Diario con Pandas
print("\n--- RESUMEN DIARIO DE TELEMETRÍA ---")
resumen_diario = df.groupby(df.index.date).agg(
    temp_promedio=('temperatura_C', 'mean'),
    temp_maxima=('temperatura_C', 'max'),
    temp_minima=('temperatura_C', 'min'),
    voltaje_promedio=('voltaje_bateria_V', 'mean'),
    voltaje_minimo=('voltaje_bateria_V', 'min'),
    cantidad_alertas=('alerta', 'sum')
)

print(resumen_diario.head())