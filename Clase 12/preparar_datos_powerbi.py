import pandas as pd
import os
from datetime import datetime
import sys

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def encontrar_carpeta_datos():
    """Encuentra la carpeta Data en diferentes ubicaciones"""
    posibles_rutas = [
        "Data/",
        "../Data/",
        "../../Data/",
        "../SPRINT-2/Data/",
        "SPRINT-2/Data/",
    ]
    
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            print(f"✓ Carpeta encontrada en: {os.path.abspath(ruta)}")
            return ruta
    
    print("❌ No se encontró la carpeta Data/")
    return None

RUTA_DATOS = encontrar_carpeta_datos()
RUTA_SALIDA = "PowerBI_Data/"

if RUTA_DATOS is None:
    print("\n⚠️  Por favor, asegúrate que exista la carpeta 'Data/' con los archivos CSV")
    sys.exit(1)

if not os.path.exists(RUTA_SALIDA):
    os.makedirs(RUTA_SALIDA)
    print(f"✓ Carpeta de salida creada: {RUTA_SALIDA}\n")

def inspeccionar_columnas(df, nombre):
    """Inspecciona y muestra las columnas de un DataFrame"""
    print(f"\n  Columnas de {nombre}:")
    for col in df.columns:
        print(f"    - {col} ({df[col].dtype})")
    return df.columns.tolist()

def limpiar_y_preparar_datos():
    """Prepara los datos para Power BI"""
    
    print("\n" + "="*80)
    print("PREPARACION DE DATOS PARA POWER BI")
    print("="*80)
    
    # Cargar datos
    print("\n[1/5] Cargando archivos CSV...")
    try:
        productos = pd.read_csv(RUTA_DATOS + "productos_limpio.csv")
        print(f"      ✓ productos_limpio.csv ({len(productos)} registros)")
    except FileNotFoundError:
        print(f"      ❌ No se encontró productos_limpio.csv")
        return
    
    try:
        ventas = pd.read_csv(RUTA_DATOS + "ventas_limpio.csv")
        print(f"      ✓ ventas_limpio.csv ({len(ventas)} registros)")
    except FileNotFoundError:
        print(f"      ❌ No se encontró ventas_limpio.csv")
        return
    
    try:
        clientes = pd.read_csv(RUTA_DATOS + "clientes_limpio.csv")
        print(f"      ✓ clientes_limpio.csv ({len(clientes)} registros)")
    except FileNotFoundError:
        print(f"      ❌ No se encontró clientes_limpio.csv")
        return
    
    # Inspeccionar columnas
    print("\n[INSPECCION] Columnas de archivos originales:")
    cols_productos = inspeccionar_columnas(productos, "PRODUCTOS")
    cols_ventas = inspeccionar_columnas(ventas, "VENTAS")
    cols_clientes = inspeccionar_columnas(clientes, "CLIENTES")
    
    # Limpiar nombres de columnas
    productos.columns = [col.lower().strip() for col in productos.columns]
    ventas.columns = [col.lower().strip() for col in ventas.columns]
    clientes.columns = [col.lower().strip() for col in clientes.columns]
    
    # Crear tabla de hechos
    print("\n[2/5] Creando tabla de hechos (FACT_VENTAS)...")
    fact_ventas = ventas.copy()
    
    # Buscar la columna de ID de producto (puede variar el nombre)
    id_prod_col = None
    for col in productos.columns:
        if 'producto' in col.lower() and 'id' in col.lower():
            id_prod_col = col
            break
    if not id_prod_col:
        id_prod_col = productos.columns[0]
    
    # Buscar la columna de nombre de producto
    nombre_prod_col = None
    for col in productos.columns:
        if 'nombre' in col.lower():
            nombre_prod_col = col
            break
    
    # Buscar columnas necesarias en productos
    categoria_col = 'categoria' if 'categoria' in productos.columns else None
    precio_col = 'precio_unitario' if 'precio_unitario' in productos.columns else None
    
    # Preparar tabla de productos para merge
    if id_prod_col in fact_ventas.columns:
        cols_merge_prod = [id_prod_col]
        if nombre_prod_col:
            cols_merge_prod.append(nombre_prod_col)
        if categoria_col:
            cols_merge_prod.append(categoria_col)
        if precio_col:
            cols_merge_prod.append(precio_col)
        
        productos_merge = productos[[c for c in cols_merge_prod if c in productos.columns]].copy()
        
        print(f"      Merging productos usando columna: {id_prod_col}")
        fact_ventas = fact_ventas.merge(
            productos_merge,
            on=id_prod_col,
            how='left'
        )
    
    # Buscar la columna de ID de cliente
    id_cli_col = None
    for col in clientes.columns:
        if 'cliente' in col.lower() and 'id' in col.lower():
            id_cli_col = col
            break
    if not id_cli_col:
        id_cli_col = clientes.columns[0]
    
    # Buscar la columna de nombre de cliente
    nombre_cli_col = None
    for col in clientes.columns:
        if 'nombre' in col.lower():
            nombre_cli_col = col
            break
    
    # Preparar tabla de clientes para merge
    if id_cli_col in fact_ventas.columns:
        cols_merge_cli = [id_cli_col]
        if nombre_cli_col:
            cols_merge_cli.append(nombre_cli_col)
        if 'ciudad' in clientes.columns:
            cols_merge_cli.append('ciudad')
        if 'email' in clientes.columns:
            cols_merge_cli.append('email')
        
        clientes_merge = clientes[[c for c in cols_merge_cli if c in clientes.columns]].copy()
        
        print(f"      Merging clientes usando columna: {id_cli_col}")
        fact_ventas = fact_ventas.merge(
            clientes_merge,
            on=id_cli_col,
            how='left'
        )
    
    # Agregar columnas de fecha
    fecha_col = None
    for col in fact_ventas.columns:
        if 'fecha' in col.lower():
            fecha_col = col
            break
    
    if fecha_col:
        fact_ventas[fecha_col] = pd.to_datetime(fact_ventas[fecha_col])
        fact_ventas['año'] = fact_ventas[fecha_col].dt.year
        fact_ventas['mes'] = fact_ventas[fecha_col].dt.month
        fact_ventas['nombre_mes'] = fact_ventas[fecha_col].dt.strftime('%B')
        fact_ventas['dia_semana'] = fact_ventas[fecha_col].dt.day_name()
        fact_ventas['semana'] = fact_ventas[fecha_col].dt.isocalendar().week
    
    # Calcular ingreso si no existe
    if 'ingreso_total' not in fact_ventas.columns:
        cantidad_col = 'cantidad' if 'cantidad' in fact_ventas.columns else None
        precio_col_fact = precio_col if precio_col in fact_ventas.columns else None
        if cantidad_col and precio_col_fact:
            fact_ventas['ingreso_total'] = fact_ventas[cantidad_col] * fact_ventas[precio_col_fact]
    
    print(f"      ✓ Tabla de hechos creada ({len(fact_ventas)} registros)")
    
    # Crear tabla de dimensión: Productos
    print("\n[3/5] Creando tabla de dimensión (DIM_PRODUCTOS)...")
    dim_productos = productos.copy()
    
    # Seleccionar columnas disponibles
    columnas_prod = [id_prod_col]
    if nombre_prod_col:
        columnas_prod.append(nombre_prod_col)
    if categoria_col:
        columnas_prod.append(categoria_col)
    if precio_col:
        columnas_prod.append(precio_col)
    if 'stock_actual' in dim_productos.columns:
        columnas_prod.append('stock_actual')
    if 'stock_minimo' in dim_productos.columns:
        columnas_prod.append('stock_minimo')
    
    dim_productos = dim_productos[[c for c in columnas_prod if c in dim_productos.columns]]
    
    # Renombrar para consistencia
    dim_productos = dim_productos.rename(columns={
        id_prod_col: 'id_producto',
        nombre_prod_col: 'nombre_producto' if nombre_prod_col else None,
        categoria_col: 'categoria' if categoria_col else None,
        precio_col: 'precio_unitario' if precio_col else None
    })
    dim_productos = dim_productos.dropna(axis=1, how='all')
    
    print(f"      ✓ Dimensión Productos creada ({len(dim_productos)} registros)")
    
    # Crear tabla de dimensión: Clientes
    print("\n[4/5] Creando tabla de dimensión (DIM_CLIENTES)...")
    dim_clientes = clientes.copy()
    
    # Seleccionar columnas disponibles
    columnas_cli = [id_cli_col]
    if nombre_cli_col:
        columnas_cli.append(nombre_cli_col)
    if 'ciudad' in dim_clientes.columns:
        columnas_cli.append('ciudad')
    if 'email' in dim_clientes.columns:
        columnas_cli.append('email')
    
    dim_clientes = dim_clientes[[c for c in columnas_cli if c in dim_clientes.columns]]
    
    # Renombrar para consistencia
    dim_clientes = dim_clientes.rename(columns={
        id_cli_col: 'id_cliente',
        nombre_cli_col: 'nombre_cliente' if nombre_cli_col else None
    })
    dim_clientes = dim_clientes.dropna(axis=1, how='all')
    
    print(f"      ✓ Dimensión Clientes creada ({len(dim_clientes)} registros)")
    
    # Crear tabla de dimensión: Tiempo
    print("\n[5/5] Creando tabla de dimensión (DIM_TIEMPO)...")
    if fecha_col:
        fechas_unicas = fact_ventas[[fecha_col, 'año', 'mes', 'nombre_mes', 'dia_semana', 'semana']].drop_duplicates()
        dim_tiempo = fechas_unicas.sort_values(fecha_col).reset_index(drop=True)
        dim_tiempo = dim_tiempo.rename(columns={fecha_col: 'fecha'})
    else:
        dim_tiempo = pd.DataFrame()
    
    print(f"      ✓ Dimensión Tiempo creada ({len(dim_tiempo)} registros)")
    
    # Guardar archivos
    print("\n[GUARDANDO ARCHIVOS]")
    try:
        fact_ventas.to_csv(RUTA_SALIDA + "FACT_VENTAS.csv", index=False, encoding='utf-8')
        print(f"  ✓ FACT_VENTAS.csv")
        
        dim_productos.to_csv(RUTA_SALIDA + "DIM_PRODUCTOS.csv", index=False, encoding='utf-8')
        print(f"  ✓ DIM_PRODUCTOS.csv")
        
        dim_clientes.to_csv(RUTA_SALIDA + "DIM_CLIENTES.csv", index=False, encoding='utf-8')
        print(f"  ✓ DIM_CLIENTES.csv")
        
        dim_tiempo.to_csv(RUTA_SALIDA + "DIM_TIEMPO.csv", index=False, encoding='utf-8')
        print(f"  ✓ DIM_TIEMPO.csv")
    except Exception as e:
        print(f"  ❌ Error al guardar archivos: {e}")
        return
    
    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DEL MODELO PARA POWER BI")
    print("="*80)
    print(f"\n📊 TABLA DE HECHOS:")
    print(f"  ├─ Registros: {len(fact_ventas):,}")
    print(f"  ├─ Columnas: {len(fact_ventas.columns)}")
    if 'ingreso_total' in fact_ventas.columns:
        print(f"  ├─ Ingresos totales: ${fact_ventas['ingreso_total'].sum():,.2f}")
    if fecha_col:
        print(f"  └─ Rango de fechas: {fact_ventas[fecha_col].min()} a {fact_ventas[fecha_col].max()}")
    
    print(f"\n📦 DIMENSION PRODUCTOS:")
    print(f"  ├─ Registros: {len(dim_productos):,}")
    if 'categoria' in dim_productos.columns:
        print(f"  ├─ Categorías: {dim_productos['categoria'].nunique()}")
    if 'stock_actual' in dim_productos.columns:
        print(f"  └─ Stock total: {dim_productos['stock_actual'].sum():,} unidades")
    
    print(f"\n👥 DIMENSION CLIENTES:")
    print(f"  ├─ Registros: {len(dim_clientes):,}")
    if 'ciudad' in dim_clientes.columns:
        print(f"  └─ Ciudades: {dim_clientes['ciudad'].nunique()}")
    
    print(f"\n📅 DIMENSION TIEMPO:")
    print(f"  └─ Fechas: {len(dim_tiempo):,}")
    
    print("\n" + "="*80)
    print("✅ DATOS LISTOS PARA POWER BI")
    print(f"📁 Archivos guardados en: {os.path.abspath(RUTA_SALIDA)}")
    print("="*80 + "\n")
    
    return fact_ventas, dim_productos, dim_clientes, dim_tiempo

if __name__ == "__main__":
    limpiar_y_preparar_datos()