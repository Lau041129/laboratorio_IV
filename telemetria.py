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