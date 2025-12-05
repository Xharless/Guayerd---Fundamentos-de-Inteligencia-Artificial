import pandas as pd
import os
import sys

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RUTA_POWERBI = "PowerBI_Data/"

def validar_modelo():
    """Valida que el modelo esté listo para Power BI"""
    
    print("\n" + "="*80)
    print("VALIDACION DE MODELO PARA POWER BI")
    print("="*80)
    
    if not os.path.exists(RUTA_POWERBI):
        print("\n❌ Error: Carpeta PowerBI_Data/ no encontrada")
        print("   Ejecuta primero: python preparar_datos_powerbi.py")
        return False
    
    # Cargar datos
    print("\n[1/6] Validando existencia de archivos...")
    archivos = {
        'FACT_VENTAS.csv': 'Tabla de hechos',
        'DIM_PRODUCTOS.csv': 'Dimensión Productos',
        'DIM_CLIENTES.csv': 'Dimensión Clientes',
        'DIM_TIEMPO.csv': 'Dimensión Tiempo'
    }
    
    dataframes = {}
    for archivo, descripcion in archivos.items():
        ruta_archivo = RUTA_POWERBI + archivo
        if os.path.exists(ruta_archivo):
            df = pd.read_csv(ruta_archivo)
            dataframes[archivo] = df
            print(f"  ✓ {descripcion:30} ({len(df):4} registros)")
        else:
            print(f"  ❌ {descripcion:30} NO ENCONTRADO")
            return False
    
    fact = dataframes['FACT_VENTAS.csv']
    dim_prod = dataframes['DIM_PRODUCTOS.csv']
    dim_cli = dataframes['DIM_CLIENTES.csv']
    dim_time = dataframes['DIM_TIEMPO.csv']
    
    # Validar claves primarias
    print("\n[2/6] Validando claves primarias...")
    
    if 'id_venta' in fact.columns:
        pk_ventas = fact['id_venta'].nunique()
        total_ventas = len(fact)
        estado_pk_ventas = "✓" if pk_ventas == total_ventas else "❌"
        print(f"  {estado_pk_ventas} FACT_VENTAS.id_venta:    {pk_ventas:3} únicos de {total_ventas:3} (PK válida)")
    
    if 'id_producto' in dim_prod.columns:
        pk_prod = dim_prod['id_producto'].nunique()
        total_prod = len(dim_prod)
        estado_pk_prod = "✓" if pk_prod == total_prod else "❌"
        print(f"  {estado_pk_prod} DIM_PRODUCTOS.id_producto: {pk_prod:3} únicos de {total_prod:3} (PK válida)")
    
    if 'id_cliente' in dim_cli.columns:
        pk_cli = dim_cli['id_cliente'].nunique()
        total_cli = len(dim_cli)
        estado_pk_cli = "✓" if pk_cli == total_cli else "❌"
        print(f"  {estado_pk_cli} DIM_CLIENTES.id_cliente:   {pk_cli:3} únicos de {total_cli:3} (PK válida)")
    
    if 'fecha' in dim_time.columns:
        pk_time = dim_time['fecha'].nunique()
        total_time = len(dim_time)
        estado_pk_time = "✓" if pk_time == total_time else "❌"
        print(f"  {estado_pk_time} DIM_TIEMPO.fecha:          {pk_time:3} únicos de {total_time:3} (PK válida)")
    
    # Validar cardinalidad (n:1)
    print("\n[3/6] Validando cardinalidad de relaciones (n:1)...")
    
    # Relación FACT -> DIM_PRODUCTOS
    if 'id_producto' in fact.columns and 'id_producto' in dim_prod.columns:
        fact_prod_ids = fact['id_producto'].nunique()
        dim_prod_ids = dim_prod['id_producto'].nunique()
        cardinalidad_prod = "✓ CORRECTA" if fact_prod_ids <= dim_prod_ids else "❌ INCORRECTA"
        print(f"  {cardinalidad_prod}")
        print(f"    └─ FACT_VENTAS.id_producto:    {fact_prod_ids} únicos")
        print(f"    └─ DIM_PRODUCTOS.id_producto:  {dim_prod_ids} únicos (1)")
    
    # Relación FACT -> DIM_CLIENTES
    if 'id_cliente' in fact.columns and 'id_cliente' in dim_cli.columns:
        fact_cli_ids = fact['id_cliente'].nunique()
        dim_cli_ids = dim_cli['id_cliente'].nunique()
        cardinalidad_cli = "✓ CORRECTA" if fact_cli_ids <= dim_cli_ids else "❌ INCORRECTA"
        print(f"  {cardinalidad_cli}")
        print(f"    └─ FACT_VENTAS.id_cliente:     {fact_cli_ids} únicos")
        print(f"    └─ DIM_CLIENTES.id_cliente:    {dim_cli_ids} únicos (1)")
    
    # Relación FACT -> DIM_TIEMPO
    if 'fecha' in fact.columns and 'fecha' in dim_time.columns:
        fact_time_ids = fact['fecha'].nunique()
        dim_time_ids = dim_time['fecha'].nunique()
        cardinalidad_time = "✓ CORRECTA" if fact_time_ids <= dim_time_ids else "❌ INCORRECTA"
        print(f"  {cardinalidad_time}")
        print(f"    └─ FACT_VENTAS.fecha:          {fact_time_ids} únicos")
        print(f"    └─ DIM_TIEMPO.fecha:           {dim_time_ids} únicos (1)")
    
    # Validar relaciones (sin huérfanos)
    print("\n[4/6] Validando integridad referencial...")
    
    huerfanos = 0
    
    # Validar productos
    if 'id_producto' in fact.columns and 'id_producto' in dim_prod.columns:
        prod_huerfanos = fact[~fact['id_producto'].isin(dim_prod['id_producto'])].shape[0]
        huerfanos += prod_huerfanos
        estado = "✓" if prod_huerfanos == 0 else "⚠️"
        print(f"  {estado} Huérfanos en producto:  {prod_huerfanos}")
    
    # Validar clientes
    if 'id_cliente' in fact.columns and 'id_cliente' in dim_cli.columns:
        cli_huerfanos = fact[~fact['id_cliente'].isin(dim_cli['id_cliente'])].shape[0]
        huerfanos += cli_huerfanos
        estado = "✓" if cli_huerfanos == 0 else "⚠️"
        print(f"  {estado} Huérfanos en cliente:   {cli_huerfanos}")
    
    # Validar fechas
    if 'fecha' in fact.columns and 'fecha' in dim_time.columns:
        time_huerfanos = fact[~fact['fecha'].isin(dim_time['fecha'])].shape[0]
        huerfanos += time_huerfanos
        estado = "✓" if time_huerfanos == 0 else "⚠️"
        print(f"  {estado} Huérfanos en tiempo:   {time_huerfanos}")
    
    if huerfanos == 0:
        print(f"\n  ✓ TODAS LAS RELACIONES SON VÁLIDAS")
    else:
        print(f"\n  ⚠️  ADVERTENCIA: Hay {huerfanos} registros huérfanos")
    
    # Estadísticas del modelo
    print("\n[5/6] Estadísticas del modelo de datos...")
    
    print(f"\n  📊 FACT_VENTAS:")
    print(f"     ├─ Registros:           {len(fact):,}")
    print(f"     ├─ Columnas:            {len(fact.columns)}")
    if 'fecha' in fact.columns:
        print(f"     ├─ Rango de fechas:     {fact['fecha'].min()} a {fact['fecha'].max()}")
    print(f"     └─ Tamaño aproximado:   {fact.memory_usage().sum() / 1024:.2f} KB")
    
    print(f"\n  📦 DIM_PRODUCTOS:")
    print(f"     ├─ Registros:           {len(dim_prod):,}")
    print(f"     ├─ Columnas:            {len(dim_prod.columns)}")
    if 'categoria' in dim_prod.columns:
        print(f"     ├─ Categorías únicas:   {dim_prod['categoria'].nunique()}")
    print(f"     └─ Tamaño aproximado:   {dim_prod.memory_usage().sum() / 1024:.2f} KB")
    
    print(f"\n  👥 DIM_CLIENTES:")
    print(f"     ├─ Registros:           {len(dim_cli):,}")
    print(f"     ├─ Columnas:            {len(dim_cli.columns)}")
    if 'ciudad' in dim_cli.columns:
        print(f"     ├─ Ciudades únicas:     {dim_cli['ciudad'].nunique()}")
    print(f"     └─ Tamaño aproximado:   {dim_cli.memory_usage().sum() / 1024:.2f} KB")
    
    print(f"\n  📅 DIM_TIEMPO:")
    print(f"     ├─ Registros:           {len(dim_time):,}")
    print(f"     ├─ Columnas:            {len(dim_time.columns)}")
    if 'año' in dim_time.columns:
        print(f"     ├─ Años únicos:         {dim_time['año'].nunique()}")
    print(f"     └─ Tamaño aproximado:   {dim_time.memory_usage().sum() / 1024:.2f} KB")
    
    # Resumen de columnas
    print("\n[6/6] Resumen de columnas en cada tabla...")
    
    print(f"\n  FACT_VENTAS:")
    for i, col in enumerate(fact.columns, 1):
        print(f"     {i:2}. {col:25} ({fact[col].dtype})")
    
    print(f"\n  DIM_PRODUCTOS:")
    for i, col in enumerate(dim_prod.columns, 1):
        print(f"     {i:2}. {col:25} ({dim_prod[col].dtype})")
    
    print(f"\n  DIM_CLIENTES:")
    for i, col in enumerate(dim_cli.columns, 1):
        print(f"     {i:2}. {col:25} ({dim_cli[col].dtype})")
    
    print(f"\n  DIM_TIEMPO:")
    for i, col in enumerate(dim_time.columns, 1):
        print(f"     {i:2}. {col:25} ({dim_time[col].dtype})")
    
    # Conclusión
    print("\n" + "="*80)
    print("✅ VALIDACION COMPLETADA")
    print("="*80)
    print("""
PRÓXIMOS PASOS EN POWER BI:

1. Abre Power BI Desktop
2. Click en "Obtener datos" → "Carpeta"
3. Selecciona la carpeta: PowerBI_Data/
4. Carga todos los archivos

5. Crea las relaciones:
   ├─ FACT_VENTAS.id_producto → DIM_PRODUCTOS.id_producto (1:*)
   ├─ FACT_VENTAS.id_cliente → DIM_CLIENTES.id_cliente (1:*)
   └─ FACT_VENTAS.fecha → DIM_TIEMPO.fecha (1:*)

6. Ajusta dirección de filtros:
   └─ De dimensiones hacia hechos (una sola dirección)

7. Crea visualizaciones
8. Publica en Power BI Service
""")
    print("="*80 + "\n")
    
    return True

if __name__ == "__main__":
    validar_modelo()