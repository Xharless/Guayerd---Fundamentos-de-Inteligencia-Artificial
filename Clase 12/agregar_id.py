import pandas as pd
import numpy as np
import os

# Encontrar la ruta correcta
ruta_lectura = '../SPRINT-2/Data/ventas_limpio.csv'
ruta_guardado = '../SPRINT-2/Data/ventas_limpio.csv'

# Verificar que existe
if not os.path.exists(ruta_lectura):
    print(f"❌ No se encuentra: {ruta_lectura}")
    print(f"Ruta absoluta: {os.path.abspath(ruta_lectura)}")
    exit(1)

# Cargar el CSV
print("Leyendo archivo...")
df = pd.read_csv(ruta_lectura)
print(f"✓ {len(df)} registros leídos")

# Agregar columna id_producto con números aleatorios entre 1 y 100
print("Agregando columna id_producto...")
df['id_producto'] = np.random.randint(1, 101, size=len(df))

# Guardar
print("Guardando archivo...")
df.to_csv(ruta_guardado, index=False)

print("\n" + "="*60)
print("✓ Columna id_producto agregada")
print(f"✓ {len(df)} registros actualizados")
print("="*60)
print("\nPrimeros 5 registros:")
print(df.head())