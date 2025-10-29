import pandas as pd
import numpy as np


print("Cargando archivos CSV...")
try:
    clientes_df = pd.read_csv('clientes.csv')
    productos_df = pd.read_csv('productos.csv')
    ventas_df = pd.read_csv('ventas.csv') 
    print("Archivos cargados correctamente.")
except FileNotFoundError as e:
    print(f"Error: No se encontró el archivo {e.filename}. Asegúrate de que los archivos CSV estén en la misma carpeta que este script.")
    exit()

print("\n--- Limpiando archivo de clientes ---")

# Estandarizar la columna 'ciudad' a formato Título (ej. "Cordoba")
clientes_df['ciudad'] = clientes_df['ciudad'].str.title()
print("Columna 'ciudad' estandarizada.")

# Convertir 'fecha_alta' a formato de fecha
clientes_df['fecha_alta'] = pd.to_datetime(clientes_df['fecha_alta'], errors='coerce')
print("Columna 'fecha_alta' convertida a formato de fecha.")

# Identificar duplicados sutiles por nombre para revisión manual
duplicados_sutiles = clientes_df[clientes_df.duplicated(subset=['nombre_cliente'], keep=False)]
if not duplicados_sutiles.empty:
    print("\n¡Atención! Se encontraron posibles clientes duplicados para revisar:")
    print(duplicados_sutiles.sort_values('nombre_cliente'))
else:
    print("No se encontraron duplicados por nombre de cliente.")

# Verificar unicidad de 'id_cliente'
if clientes_df['id_cliente'].duplicated().any():
    print(f"¡Error! Hay {clientes_df['id_cliente'].duplicated().sum()} IDs de cliente duplicados.")
else:
    print("La columna 'id_cliente' tiene valores únicos.")


# --- 3. Limpieza del DataFrame de Productos ---
print("\n--- Limpiando archivo de productos ---")


def corregir_categoria(nombre_producto):
    nombre = nombre_producto.lower()

    # Diccionario de categorías y palabras clave asociadas
    mapa_categorias = {
        'Bebidas': ['pepsi', 'coca', 'sprite', 'fanta', 'jugo', 'agua', 'gaseosa', 'energética'],
        'Bebidas Alcohólicas': ['cerveza', 'vino', 'sidra', 'fernet', 'vodka', 'ron', 'gin', 'whisky', 'licor'],
        'Lácteos y Quesos': ['leche', 'yogur', 'queso', 'manteca', 'crema'],
        'Panadería y Repostería': ['pan', 'medialunas', 'bizcochos', 'galletitas', 'alfajor', 'torta'],
        'Almacén': [
            'yerba', 'café', 'té', 'azúcar', 'sal', 'aceite', 'vinagre', 'salsa', 'arroz', 'fideos',
            'lentejas', 'garbanzos', 'porotos', 'harina', 'miel', 'stevia', 'granola', 'avena',
            'sopa', 'caldo', 'aceitunas'
        ],
        'Snacks y Golosinas': ['papas fritas', 'maní', 'frutos secos', 'chocolate', 'turrón', 'barrita', 'caramelos', 'chicle', 'chupetín'],
        'Congelados': ['helado', 'pizza', 'empanadas', 'verduras congeladas', 'hamburguesas'],
        'Limpieza': [
            'detergente', 'lavandina', 'jabón', 'limpiador', 'suavizante', 'limpiavidrios',
            'desengrasante', 'esponjas', 'trapo'
        ],
        'Higiene Personal': [
            'shampoo', 'papel higiénico', 'servilletas', 'toallas húmedas', 'desodorante',
            'crema dental', 'cepillo de dientes', 'hilo dental', 'mascarilla capilar'
        ]
    }

    for categoria, keywords in mapa_categorias.items():
        if any(keyword in nombre for keyword in keywords):
            return categoria

    # Casos especiales que no encajan fácilmente
    if 'dulce de leche' in nombre or 'mermelada' in nombre:
        return 'Bebidas'
    return 'Otros'  # Categoría por defecto si no coincide ninguna


productos_df['categoria_corregida'] = productos_df['nombre_producto'].apply(corregir_categoria)

print("Se ha corregido la columna 'categoria'. Comparando antes y después:")
print(productos_df[['nombre_producto', 'categoria', 'categoria_corregida']].head())


productos_df['categoria'] = productos_df['categoria_corregida']
productos_df = productos_df.drop(columns=['categoria_corregida'])
print("Columna 'categoria' actualizada.")


productos_df['precio_unitario'] = pd.to_numeric(productos_df['precio_unitario'], errors='coerce')
if productos_df['precio_unitario'].isnull().any():
    print("¡Atención! Se encontraron valores no numéricos en 'precio_unitario' y se convirtieron a Nulos (NaN).")


# --- 4. Limpieza del DataFrame de Ventas ---
print("\n--- Limpiando archivo de ventas ---")

# Eliminar columnas redundantes
if 'nombre_cliente' in ventas_df.columns and 'email' in ventas_df.columns:
    ventas_df = ventas_df.drop(columns=['nombre_cliente', 'email'])
    print("Columnas redundantes 'nombre_cliente' y 'email' eliminadas.")

# Estandarizar 'medio_pago' a minúsculas
ventas_df['medio_pago'] = ventas_df['medio_pago'].str.lower()
print("Columna 'medio_pago' estandarizada a minúsculas.")
print("Valores únicos en 'medio_pago':", ventas_df['medio_pago'].unique().tolist())

# --- PASO DE DEPURACIÓN: Imprimir columnas para encontrar el nombre correcto ---
print("\nColumnas encontradas en el archivo de ventas:", ventas_df.columns.tolist())
print("Por favor, revisa la lista de arriba y asegúrate de que el nombre de la columna de fecha sea correcto en la línea de abajo.")

# Convertir 'fecha_venta' a formato de fecha
# Reemplaza 'fecha_venta' si el nombre en tu archivo es diferente.
nombre_columna_fecha = 'fecha' # <-- ¡CAMBIA ESTO SI ES NECESARIO!
ventas_df[nombre_columna_fecha] = pd.to_datetime(ventas_df[nombre_columna_fecha], errors='coerce')
print(f"Columna '{nombre_columna_fecha}' convertida a formato de fecha.")


# --- 5. Guardado de Archivos Limpios ---
print("\n--- Guardando archivos limpios ---")

clientes_df.to_csv('clientes_limpio.csv', index=False)
productos_df.to_csv('productos_limpio.csv', index=False)
ventas_df.to_csv('ventas_limpio.csv', index=False)

print("Proceso de limpieza completado. Se han guardado los siguientes archivos:")
print("- clientes_limpio.csv")
print("- productos_limpio.csv")
print("- ventas_limpio.csv")
