import pandas as pd
import numpy as np

# --- 1. Carga de los Archivos Limpios ---
print("Cargando los archivos limpios...")
try:
    clientes_df = pd.read_csv('../Clase 6/clientes_limpio.csv')
    productos_df = pd.read_csv('../Clase 6/productos_limpio.csv')
    ventas_df = pd.read_csv('../Clase 6/ventas_limpio.csv')
    print("Archivos cargados correctamente.")
except FileNotFoundError as e:
    print(f"Error: No se encontró el archivo {e.filename}. Asegúrate de ejecutar primero el script de limpieza.")
    exit()

# --- 2. Generación de Datos de Detalle de Venta (ventas_detalle.csv) ---
print("\n--- Generando archivo 'ventas_detalle.csv' ---")

# Obtener listas de IDs válidos
lista_id_venta = ventas_df['id_venta'].unique()
lista_id_producto = productos_df['id_producto'].unique()

detalles_venta = []
# Para cada venta, asignamos de 1 a 5 productos aleatorios
for id_v in lista_id_venta:
    num_productos = np.random.randint(1, 6)  # Cada venta tendrá entre 1 y 5 items
    productos_vendidos = np.random.choice(lista_id_producto, num_productos, replace=False)
    
    for id_p in productos_vendidos:
        cantidad = np.random.randint(1, 4)  # Cantidad entre 1 y 3
        detalles_venta.append({
            'id_venta': id_v,
            'id_producto': id_p,
            'cantidad': cantidad
        })

ventas_detalle_df = pd.DataFrame(detalles_venta)
ventas_detalle_df.to_csv('ventas_detalle.csv', index=False)
print("Archivo 'ventas_detalle.csv' creado con éxito.")
print(ventas_detalle_df.head())


# --- 3. Creación del DataFrame Maestro para Análisis ---
print("\n--- Uniendo todos los datos en un DataFrame maestro ---")

# Paso 1: Unir ventas con los detalles de venta
df_maestro = pd.merge(ventas_df, ventas_detalle_df, on='id_venta')

# Paso 2: Añadir la información de los productos
df_maestro = pd.merge(df_maestro, productos_df, on='id_producto')

# Paso 3: Añadir la información de los clientes
df_maestro = pd.merge(df_maestro, clientes_df, on='id_cliente')

# --- 4. Enriquecimiento del DataFrame Maestro ---
print("Enriqueciendo el DataFrame con cálculos...")

# Calcular el ingreso total por línea de producto
df_maestro['ingreso_total'] = df_maestro['cantidad'] * df_maestro['precio_unitario']

# Reordenar columnas para mayor claridad
columnas_ordenadas = [
    'id_venta', 'fecha', 'id_cliente', 'nombre_cliente', 'ciudad',
    'id_producto', 'nombre_producto', 'categoria', 'cantidad',
    'precio_unitario', 'ingreso_total', 'medio_pago'
]
df_maestro = df_maestro[columnas_ordenadas]

# Guardar el DataFrame maestro
df_maestro.to_csv('analisis_ventas_completo.csv', index=False)

print("\n¡Proceso completado!")
print("Se ha creado el archivo 'analisis_ventas_completo.csv' con todos los datos unidos.")
print("\nVista previa del DataFrame maestro:")
print(df_maestro.head())

# --- Ejemplo de Análisis Rápido ---
print("\n--- Ejemplo de Análisis: Ingresos totales por Categoría ---")
ingresos_por_categoria = df_maestro.groupby('categoria')['ingreso_total'].sum().sort_values(ascending=False)
print(ingresos_por_categoria)
