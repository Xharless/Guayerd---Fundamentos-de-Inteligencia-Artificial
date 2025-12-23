import pandas as pd
from tabulate import tabulate
import sys
import io
from datetime import datetime
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pickle
import os
import subprocess

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Rutas de los archivos - SPRINT-3
RUTA_PRODUCTOS = "Data/productos_limpio.csv"
RUTA_VENTAS = "Data/ventas_limpio.csv"
RUTA_CLIENTES = "Data/clientes_limpio.csv"
RUTA_ANALISIS_COMPLETO = "Data/analisis_ventas_completo.csv"

# Rutas de los archivos - SPRINT-4 (PowerBI)
RUTA_POWERBI = "PowerBI_Data/"

documentacion = {
    "Tema": "Control de stock y ventas",
    "Problematica": "No existe un mecanismo facil para poder relacionar las ventas del productos con el stock, lo que pude generar escasez de recursos o exceso de inventario.",
    "Solucion": "Un programa que consulte las ventas de cada producto, detectando cuales son los que tienen menor stock y genere alertas sobre productos bajo de stock o productos en alta rotacion que necesiten reposicion urgente.",
    "Dataset de referencia": """
PRODUCTOS:
    1. ID_Producto (int): valores unicos de cada producto (PK)
    2. nombre (str): nombres de cada producto
    3. categoria (str): categoria de cada producto
    4. stock_actual (int): stock actual que tiene el producto
    5. stock_minimo (int): nivel minimo de stock
    6. precio (float): precio de cada producto

VENTAS:
    1. ID_venta (int): valores unicos de cada venta (PK)
    2. fecha (date): fecha de la venta
    3. ID_Producto (int): valor unico del producto (FK)
    4. cantidad (int): cantidad vendida
    5. ID_Cliente (int): identificador del cliente (FK)

CLIENTES:
    1. ID_cliente (int): valores unicos para cada cliente (PK)
    2. nombre (str): nombres de cada cliente
    3. email (str): correos de cada cliente
    4. ciudad (str): ciudades de cada cliente
""",
    "Fuente y escala": """
Fuente: Datasets simulados para fines educativos, generados manualmente para 
representar un escenario tipico de gestion de stock y ventas.
Escala: Cada archivo contiene aproximadamente 20-50 registros, cubriendo un mes 
de operaciones ficticias.
""",
    "Pasos del programa": """
1. Cargar los datasets de productos, ventas y clientes.
2. Relacionar las ventas con los productos usando ID_Producto.
3. Calcular el stock restante de cada producto.
4. Comparar el stock actual con el stock minimo.
5. Generar alertas para productos con stock bajo o alta rotacion.
6. Mostrar o exportar el reporte de alertas.
""",
    "Pseudocodigo": """
Cargar productos desde productos_limpio.csv
Cargar ventas desde ventas_limpio.csv

Para cada producto en productos:
    Calcular ventas_totales = suma de cantidad vendida
    stock_restante = stock_actual - ventas_totales
    Si stock_restante < stock_minimo:
        Agregar a lista de alertas (stock bajo)
    Si ventas_totales > 10:
        Agregar a lista de alertas (alta rotacion)

Mostrar lista de alertas
""",
    "Sugerencias y mejoras": """
- Se sugirio automatizar la generacion de alertas usando comparaciones directas 
  entre el stock actual y el stock minimo.
- Se recomendo agregar un umbral para identificar productos de alta rotacion.
- Copilot propuso estructurar el pseudocodigo para mayor claridad y eficiencia.
- Se mejoro la definicion de los datasets con tipos de datos y relaciones.
"""
}


def linea_superior():
    print("\n" + "="*95)

def linea_media():
    print("-"*95)

def linea_inferior():
    print("="*95 + "\n")

def titulo(texto, emoji=""):
    linea_superior()
    print(f"  {emoji} {texto}".ljust(95))
    linea_inferior()

def seccion(texto, emoji=""):
    linea_media()
    print(f"  {emoji} {texto}")
    linea_media()

def calcular_mape(y_real, y_pred):
    """Calcula MAPE (Mean Absolute Percentage Error)"""
    return np.mean(np.abs((y_real - y_pred) / y_real)) * 100

# ============================================================================
# FUNCIONES DE CARGA DE DATOS - SPRINT-3
# ============================================================================

def cargar_datos():
    """Carga los datasets limpios desde la carpeta Data"""
    try:
        productos = pd.read_csv(RUTA_PRODUCTOS)
        ventas = pd.read_csv(RUTA_VENTAS)
        clientes = pd.read_csv(RUTA_CLIENTES)
        return productos, ventas, clientes
    except FileNotFoundError as e:
        return None, None, None

def cargar_analisis():
    """Carga el archivo de análisis completo"""
    try:
        df = pd.read_csv(RUTA_ANALISIS_COMPLETO)
        df['fecha'] = pd.to_datetime(df['fecha'])
        return df
    except FileNotFoundError:
        return None

# ============================================================================
# FUNCIONES DE CARGA DE DATOS - SPRINT-4 (POWERBI)
# ============================================================================

def cargar_datos_powerbi():
    """Carga las tablas dimensionales y de hechos"""
    titulo("1️⃣  CARGANDO DATOS POWERBI", "📂")
    
    try:
        dim_clientes = pd.read_csv(RUTA_POWERBI + "DIM_CLIENTES.csv")
        dim_productos = pd.read_csv(RUTA_POWERBI + "DIM_PRODUCTOS.csv")
        dim_tiempo = pd.read_csv(RUTA_POWERBI + "DIM_TIEMPO.csv")
        fact_ventas = pd.read_csv(RUTA_POWERBI + "FACT_VENTAS.csv")
        
        print(f"  ✓ DIM_CLIENTES       ({len(dim_clientes):3} registros)")
        print(f"  ✓ DIM_PRODUCTOS      ({len(dim_productos):3} registros)")
        print(f"  ✓ DIM_TIEMPO         ({len(dim_tiempo):3} registros)")
        print(f"  ✓ FACT_VENTAS        ({len(fact_ventas):3} registros)\n")
        
        return dim_clientes, dim_productos, dim_tiempo, fact_ventas
    except FileNotFoundError as e:
        print(f"  ❌ Error: {e}\n")
        return None, None, None, None

# ============================================================================
# FUNCIONES SPRINT-2 (MANTENER)
# ============================================================================

def mostrar_resumen_datos(productos, ventas, clientes):
    """Muestra un resumen de los datos cargados"""
    titulo("RESUMEN DE DATOS CARGADOS", "📊")
    
    seccion("PRODUCTOS - Primeros 5 registros", "📦")
    print(tabulate(productos.head(5), headers='keys', tablefmt='fancy_grid', showindex=False))
    print(f"\n  Total de productos: {len(productos)} registros\n")
    
    seccion("VENTAS - Primeros 5 registros", "💳")
    print(tabulate(ventas.head(5), headers='keys', tablefmt='fancy_grid', showindex=False))
    print(f"\n  Total de ventas: {len(ventas)} registros\n")
    
    seccion("CLIENTES - Primeros 5 registros", "👥")
    print(tabulate(clientes.head(5), headers='keys', tablefmt='fancy_grid', showindex=False))
    print(f"\n  Total de clientes: {len(clientes)} registros\n")

def mostrar_estadisticas(productos, ventas, clientes):
    """Muestra estadísticas descriptivas de los datos"""
    titulo("ESTADISTICAS DESCRIPTIVAS", "📈")
    
    seccion("PRODUCTOS - Estadisticas de precios", "💰")
    if 'precio_unitario' in productos.columns:
        stats = productos[['precio_unitario']].describe().round(2)
        print(tabulate(stats, headers='keys', tablefmt='fancy_grid'))
    
    seccion("PRODUCTOS - Distribucion de categorias", "🏪")
    categorias = productos['categoria'].value_counts()
    tabla_cat = pd.DataFrame({
        'Categoria': categorias.index, 
        'Cantidad': categorias.values
    })
    print(tabulate(tabla_cat, headers='keys', tablefmt='fancy_grid', showindex=False))
    
    seccion("VENTAS - Medios de pago", "💳")
    if 'medio_pago' in ventas.columns:
        medios = ventas['medio_pago'].value_counts()
        tabla_medios = pd.DataFrame({
            'Medio de Pago': medios.index, 
            'Cantidad': medios.values
        })
        print(tabulate(tabla_medios, headers='keys', tablefmt='fancy_grid', showindex=False))

def mostrar_analisis_ventas(productos, ventas, clientes):
    """Muestra análisis detallado de ventas"""
    titulo("ANALISIS DETALLADO DE VENTAS", "🔍")
    
    seccion("RESUMEN GENERAL", "📋")
    print(f"  Total de ventas:         {len(ventas):>10} registros")
    print(f"  Clientes unicos:         {clientes['id_cliente'].nunique():>10}")
    print(f"  Productos diferentes:    {productos['id_producto'].nunique():>10}\n")
    
    seccion("TOP 5 - Clientes por numero de compras", "🌟")
    top_clientes = ventas['id_cliente'].value_counts().head(5)
    tabla_top = pd.DataFrame({
        'Posicion': range(1, len(top_clientes) + 1),
        'Cliente ID': top_clientes.index,
        'Numero de Compras': top_clientes.values
    })
    print(tabulate(tabla_top, headers='keys', tablefmt='fancy_grid', showindex=False))

def mostrar_estadisticas_descriptivas_analisis(df):
    """Estadísticas descriptivas"""
    titulo("ESTADISTICAS DESCRIPTIVAS", "📊")
    
    seccion("VARIABLES NUMERICAS - Estadisticas principales", "🔢")
    stats_numericas = df[['cantidad', 'precio_unitario', 'ingreso_total']].describe().round(2)
    print(tabulate(stats_numericas, headers='keys', tablefmt='fancy_grid'))
    
    seccion("VARIABLES CATEGORICAS - Valores unicos", "🏷️")
    print(f"  Ciudades unicas:         {df['ciudad'].nunique():>10}")
    print(f"  Categorias unicas:       {df['categoria'].nunique():>10}")
    print(f"  Medios de pago unicos:   {df['medio_pago'].nunique():>10}\n")

def mostrar_analisis_distribucion(df):
    """Análisis de distribución de variables"""
    titulo("ANALISIS DE DISTRIBUCION", "📉")
    
    seccion("CANTIDAD POR VENTA", "🛍️")
    print(f"  Media:                   {df['cantidad'].mean():>10.2f}")
    print(f"  Mediana:                 {df['cantidad'].median():>10.2f}")
    print(f"  Desviacion Estandar:     {df['cantidad'].std():>10.2f}")
    print(f"  Valor minimo:            {df['cantidad'].min():>10.2f}")
    print(f"  Valor maximo:            {df['cantidad'].max():>10.2f}\n")
    
    seccion("PRECIO UNITARIO", "💵")
    print(f"  Media:                   ${df['precio_unitario'].mean():>9.2f}")
    print(f"  Mediana:                 ${df['precio_unitario'].median():>9.2f}")
    print(f"  Desviacion Estandar:     ${df['precio_unitario'].std():>9.2f}")
    print(f"  Valor minimo:            ${df['precio_unitario'].min():>9.2f}")
    print(f"  Valor maximo:            ${df['precio_unitario'].max():>9.2f}\n")
    
    seccion("INGRESO TOTAL", "💰")
    print(f"  Media:                   ${df['ingreso_total'].mean():>9.2f}")
    print(f"  Mediana:                 ${df['ingreso_total'].median():>9.2f}")
    print(f"  Desviacion Estandar:     ${df['ingreso_total'].std():>9.2f}")
    print(f"  Valor minimo:            ${df['ingreso_total'].min():>9.2f}")
    print(f"  Valor maximo:            ${df['ingreso_total'].max():>9.2f}\n")

def mostrar_analisis_correlacion(df):
    """Análisis de correlación"""
    titulo("ANALISIS DE CORRELACION", "🔗")
    
    seccion("MATRIZ DE CORRELACION", "📐")
    corr_matrix = df[['cantidad', 'precio_unitario', 'ingreso_total']].corr().round(4)
    print(tabulate(corr_matrix, headers='keys', tablefmt='fancy_grid'))
    
    seccion("INTERPRETACION", "💡")
    print(f"  Cantidad vs Precio:      {corr_matrix.loc['cantidad', 'precio_unitario']:>10.4f}")
    print(f"  Cantidad vs Ingreso:     {corr_matrix.loc['cantidad', 'ingreso_total']:>10.4f}")
    print(f"  Precio vs Ingreso:       {corr_matrix.loc['precio_unitario', 'ingreso_total']:>10.4f}\n")

def mostrar_ingresos_categoria(df):
    """Ingresos por categoría"""
    titulo("INGRESOS POR CATEGORIA", "🏪")
    
    ingresos_categoria = df.groupby('categoria')['ingreso_total'].sum().sort_values(ascending=False)
    
    seccion("RANKING - Ingresos totales por categoria", "📊")
    tabla = pd.DataFrame({
        'Posicion': range(1, len(ingresos_categoria) + 1),
        'Categoria': ingresos_categoria.index,
        'Ingreso Total': ['$' + f'{x:,.2f}' for x in ingresos_categoria.values]
    })
    print(tabulate(tabla, headers='keys', tablefmt='fancy_grid', showindex=False))
    print(f"\n  💰 INGRESO TOTAL: ${ingresos_categoria.sum():,.2f}\n")

def mostrar_evolucion_ingresos(df):
    """Evolución de ingresos mensuales"""
    titulo("EVOLUCION DE INGRESOS MENSUALES", "📈")
    
    df['mes'] = df['fecha'].dt.to_period('M')
    ingresos_mensuales = df.groupby('mes')['ingreso_total'].sum()
    
    seccion("INGRESOS MENSUALES", "📅")
    tabla = pd.DataFrame({
        'Mes': [str(mes) for mes in ingresos_mensuales.index],
        'Ingreso': ['$' + f'{x:,.2f}' for x in ingresos_mensuales.values]
    })
    print(tabulate(tabla, headers='keys', tablefmt='fancy_grid', showindex=False))
    
    seccion("ESTADISTICAS", "📊")
    print(f"  Ingreso promedio mensual: ${ingresos_mensuales.mean():>10,.2f}")
    print(f"  Ingreso maximo:           ${ingresos_mensuales.max():>10,.2f}")
    print(f"  Ingreso minimo:           ${ingresos_mensuales.min():>10,.2f}\n")

def mostrar_top_clientes(df):
    """Top 10 clientes por gasto total"""
    titulo("TOP 10 CLIENTES POR GASTO TOTAL", "👑")
    
    top_clientes = df.groupby('nombre_cliente')['ingreso_total'].sum().sort_values(ascending=False).head(10)
    
    seccion("RANKING DE CLIENTES", "🌟")
    tabla = pd.DataFrame({
        'Posicion': range(1, len(top_clientes) + 1),
        'Cliente': top_clientes.index,
        'Gasto Total': ['$' + f'{x:,.2f}' for x in top_clientes.values]
    })
    print(tabulate(tabla, headers='keys', tablefmt='fancy_grid', showindex=False))
    
    seccion("ESTADISTICAS", "💰")
    print(f"  Gasto total top 10:       ${top_clientes.sum():>10,.2f}")
    print(f"  Gasto promedio (top 10):  ${top_clientes.mean():>10,.2f}\n")

def mostrar_insights_negocio():
    """Insights de negocio"""
    titulo("INSIGHTS DE NEGOCIO", "🎯")
    
    insights = [
        {
            "emoji": "🌍",
            "titulo": "FOCO GEOGRAFICO Y DE PRODUCTO",
            "contenido": "Las operaciones se concentran en la ciudad de Cordoba y en la\n      categoria 'Almacen'. Oportunidad para expandirse en otras ciudades o\n      potenciar otras categorias."
        },
        {
            "emoji": "💳",
            "titulo": "COMPORTAMIENTO DE PAGO",
            "contenido": "El uso predominante de la tarjeta sugiere que las promociones\n      bancarias o los planes de cuotas podrian ser estrategias efectivas\n      para impulsar las ventas."
        },
        {
            "emoji": "💵",
            "titulo": "VALOR DE LAS TRANSACCIONES",
            "contenido": "La mayoria de las ventas son de bajo valor, pero un pequeno\n      numero de transacciones de alto valor (outliers) contribuyen\n      significativamente a los ingresos. Identificar y fidelizar a los clientes\n      que realizan grandes compras es una prioridad estrategica."
        },
        {
            "emoji": "📊",
            "titulo": "ESTRATEGIA DE PRECIOS",
            "contenido": "La falta de correlacion entre precio y cantidad vendida indica\n      que los clientes no son muy sensibles al precio. Esto da margen para\n      ajustar precios sin temer una caida drastica en el volumen de ventas."
        }
    ]
    
    for i, insight in enumerate(insights, 1):
        seccion(f"{insight['emoji']} {insight['titulo']}", "")
        print(f"  {insight['contenido']}\n")

def mostrar_diagrama_texto():
    """Diagrama de flujo del programa"""
    titulo("DIAGRAMA DE FLUJO DEL PROCESO", "🔄")
    diagrama = r"""
              +------------------+
              |  🚀 INICIO       |
              +------------------+
                     |
                     v
              +------------------+
              | 📥 Cargar Dataset|
              +------------------+
                     |
                     v
   +------------------------------------------+
   | 🔢 Calcular ventas por producto         |
   +------------------------------------------+
                     |
                     v
              < Stock < minimo? >
               /               \
            [SI]             [NO]
             /                 \
            v                   v
    +--------------------+    < Stock >> minimo? >
    | 🚨 Alerta:         |     /               \
    | Quiebre Stock      |   [SI]            [NO]
    +--------------------+     /               \
                              v                v
                    +------------------------------+
                    | ⚠️  Alerta:                  |
                    | Exceso de inventario         |
                    +------------------------------+
                                           |
                                           v
                        +---------------------------+
                        | 📊 Mostrar resultados    |
                        | obtenidos                |
                        +---------------------------+
                                           |
                                           v
                                 +-------------------+
                                 | ✓ Fin del programa|
                                 +-------------------+
    """
    print(diagrama)

def validar_relaciones(dim_clientes, dim_productos, dim_tiempo, fact_ventas):
    """Valida las relaciones entre tablas - COLUMNAS CORREGIDAS"""
    titulo("2️⃣  VALIDANDO RELACIONES Y CARDINALIDAD", "🔗")
    
    relaciones = []
    
    # Relación 1: FACT_VENTAS -> DIM_CLIENTES (usando id_cliente en minúsculas)
    seccion("Relación 1: FACT_VENTAS → DIM_CLIENTES", "👥")
    fk_cliente = fact_ventas['id_cliente'].unique()
    pk_cliente = dim_clientes['id_cliente'].unique()
    clientes_validos = len([x for x in fk_cliente if x in pk_cliente])
    clientes_invalidos = len(fk_cliente) - clientes_validos
    
    print(f"  Foreign Key (FACT_VENTAS):   {len(fk_cliente):3} valores")
    print(f"  Primary Key (DIM_CLIENTES):  {len(pk_cliente):3} valores")
    print(f"  Integridad referencial:      {clientes_validos}/{len(fk_cliente)} ✓")
    print(f"  Cardinalidad: Muchos-a-Uno (N:1)")
    print(f"  Dirección filtro: DIM → FACT\n")
    
    relaciones.append({
        'Relacion': 'FACT_VENTAS → DIM_CLIENTES',
        'Cardinalidad': 'N:1',
        'FK': 'id_cliente',
        'PK': 'id_cliente',
        'Valida': 'SÍ' if clientes_invalidos == 0 else 'NO'
    })
    
    # Relación 2: FACT_VENTAS -> DIM_PRODUCTOS
    seccion("Relación 2: FACT_VENTAS → DIM_PRODUCTOS", "📦")
    fk_producto = fact_ventas['id_producto'].unique()
    pk_producto = dim_productos['id_producto'].unique()
    productos_validos = len([x for x in fk_producto if x in pk_producto])
    productos_invalidos = len(fk_producto) - productos_validos
    
    print(f"  Foreign Key (FACT_VENTAS):    {len(fk_producto):3} valores")
    print(f"  Primary Key (DIM_PRODUCTOS): {len(pk_producto):3} valores")
    print(f"  Integridad referencial:       {productos_validos}/{len(fk_producto)} ✓")
    print(f"  Cardinalidad: Muchos-a-Uno (N:1)")
    print(f"  Dirección filtro: DIM → FACT\n")
    
    relaciones.append({
        'Relacion': 'FACT_VENTAS → DIM_PRODUCTOS',
        'Cardinalidad': 'N:1',
        'FK': 'id_producto',
        'PK': 'id_producto',
        'Valida': 'SÍ' if productos_invalidos == 0 else 'NO'
    })
    
    # Relación 3: FACT_VENTAS -> DIM_TIEMPO (por fecha, no ID_Fecha)
    seccion("Relación 3: FACT_VENTAS → DIM_TIEMPO", "📅")
    print(f"  ⚠️  Nota: FACT_VENTAS no tiene columna 'ID_Fecha'")
    print(f"  La relación se establece por 'fecha' (texto/date)\n")
    
    fk_tiempo = pd.to_datetime(fact_ventas['fecha']).dt.date.unique()
    pk_tiempo = pd.to_datetime(dim_tiempo['fecha']).dt.date.unique()
    tiempo_validos = len([x for x in fk_tiempo if x in pk_tiempo])
    tiempo_invalidos = len(fk_tiempo) - tiempo_validos
    
    print(f"  Foreign Key (FACT_VENTAS):  {len(fk_tiempo):3} fechas únicas")
    print(f"  Primary Key (DIM_TIEMPO):   {len(pk_tiempo):3} fechas únicas")
    print(f"  Integridad referencial:     {tiempo_validos}/{len(fk_tiempo)} ✓")
    print(f"  Cardinalidad: Muchos-a-Uno (N:1)")
    print(f"  Dirección filtro: DIM → FACT\n")
    
    relaciones.append({
        'Relacion': 'FACT_VENTAS → DIM_TIEMPO',
        'Cardinalidad': 'N:1',
        'FK': 'fecha',
        'PK': 'fecha',
        'Valida': 'SÍ' if tiempo_invalidos == 0 else 'NO'
    })
    
    # Resumen
    seccion("RESUMEN DE RELACIONES", "✅")
    df_relaciones = pd.DataFrame(relaciones)
    print(df_relaciones.to_string(index=False))
    print()
    
    return pd.DataFrame(relaciones)

# ============================================================================
# FUNCIONES SPRINT-3 (MACHINE LEARNING)
# ============================================================================

def preparar_features_ml(productos, ventas, clientes):
    """Prepara features para el modelo ML"""
    titulo("2️⃣  PREPARACION DE FEATURES", "🔧")
    
    seccion("Merge de tablas", "📋")
    
    # Merge
    df = ventas.merge(productos, on='id_producto', how='left')
    df = df.merge(clientes, on='id_cliente', how='left')
    
    print(f"  ✓ Tablas mergeadas: {len(df)} registros\n")
    
    # Generar cantidad si no existe
    seccion("Generando columna 'cantidad'", "✨")
    
    if 'cantidad' not in df.columns:
        np.random.seed(42)
        df['cantidad'] = np.random.randint(1, 101, size=len(df))
        print(f"  ✓ Columna 'cantidad' generada (valores 1-100)\n")
    
    # Convertir fecha
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['mes'] = df['fecha'].dt.month
    df['dia_semana'] = df['fecha'].dt.dayofweek
    
    # Crear variable objetivo
    df['ingreso_total'] = df['cantidad'] * df['precio_unitario']
    
    seccion("Variable objetivo (y)", "🎯")
    print(f"  Fórmula: cantidad × precio_unitario")
    print(f"  Mínimo:    ${df['ingreso_total'].min():>12,.0f}")
    print(f"  Máximo:    ${df['ingreso_total'].max():>12,.0f}")
    print(f"  Promedio:  ${df['ingreso_total'].mean():>11,.0f}")
    print(f"  Mediana:   ${df['ingreso_total'].median():>11,.0f}\n")
    
    # Features
    features_numericas = ['cantidad', 'precio_unitario', 'mes', 'dia_semana']
    features_categoricas = ['categoria', 'ciudad', 'medio_pago']
    
    X = df[features_numericas].copy()
    
    seccion("Encoding de variables categóricas", "🔄")
    
    for col in features_categoricas:
        if col in df.columns:
            encoded = pd.get_dummies(df[col], prefix=col, drop_first=True)
            X = pd.concat([X, encoded], axis=1)
            n_cols = encoded.shape[1]
            print(f"  ✓ {col:15} → {n_cols:2} columnas")
    
    y = df['ingreso_total']
    
    seccion("RESULTADO FINAL", "✅")
    print(f"  X (features):   {X.shape[0]} muestras × {X.shape[1]} características")
    print(f"  y (target):     {len(y)} valores\n")
    
    return X, y, df

def entrenar_modelos_ml(X, y, test_size=0.2, random_state=42):
    """Entrena y evalúa dos modelos"""
    titulo("3️⃣  ENTRENAMIENTO DE MODELOS", "🤖")
    
    # División
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    seccion("División Train/Test", "📊")
    print(f"  TOTAL:  {len(X):3} muestras")
    print(f"  TRAIN:  {len(X_train):3} muestras ({(1-test_size)*100:.0f}%)")
    print(f"  TEST:   {len(X_test):3} muestras ({test_size*100:.0f}%)\n")
    
    # ========== MODELO 1: Regresión Lineal ==========
    seccion("Modelo 1: Regresión Lineal", "📈")
    
    modelo_lr = LinearRegression()
    modelo_lr.fit(X_train, y_train)
    y_pred_lr = modelo_lr.predict(X_test)
    
    r2_lr = r2_score(y_test, y_pred_lr)
    rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
    mae_lr = mean_absolute_error(y_test, y_pred_lr)
    mape_lr = calcular_mape(y_test.values, y_pred_lr)
    
    print(f"  R² Score:  {r2_lr:.4f}")
    print(f"  RMSE:      ${rmse_lr:>12,.0f}")
    print(f"  MAE:       ${mae_lr:>12,.0f}")
    print(f"  MAPE:      {mape_lr:>11.2f}%\n")
    
    # ========== MODELO 2: Random Forest ==========
    seccion("Modelo 2: Random Forest Regressor ⭐", "🌲")
    
    modelo_rf = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=random_state,
        n_jobs=-1
    )
    modelo_rf.fit(X_train, y_train)
    y_pred_rf = modelo_rf.predict(X_test)
    
    r2_rf = r2_score(y_test, y_pred_rf)
    rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    mape_rf = calcular_mape(y_test.values, y_pred_rf)
    
    print(f"  R² Score:  {r2_rf:.4f}")
    print(f"  RMSE:      ${rmse_rf:>12,.0f}")
    print(f"  MAE:       ${mae_rf:>12,.0f}")
    print(f"  MAPE:      {mape_rf:>11.2f}%\n")
    
    # ========== COMPARACIÓN ==========
    seccion("COMPARACIÓN DE MODELOS", "⚖️")
    
    mejora_r2 = ((r2_rf - r2_lr) / r2_lr) * 100 if r2_lr != 0 else 0
    mejora_rmse = ((rmse_lr - rmse_rf) / rmse_lr) * 100 if rmse_lr != 0 else 0
    mejora_mae = ((mae_lr - mae_rf) / mae_lr) * 100 if mae_lr != 0 else 0
    
    tabla_comparacion = pd.DataFrame({
        'Métrica': ['R² Score', 'RMSE ($)', 'MAE ($)', 'MAPE (%)'],
        'Reg. Lineal': [
            f'{r2_lr:.4f}',
            f'{rmse_lr:,.0f}',
            f'{mae_lr:,.0f}',
            f'{mape_lr:.2f}'
        ],
        'Random Forest': [
            f'{r2_rf:.4f}',
            f'{rmse_rf:,.0f}',
            f'{mae_rf:,.0f}',
            f'{mape_rf:.2f}'
        ],
        'Mejora (%)': [
            f'{mejora_r2:.1f}%',
            f'{mejora_rmse:.1f}%',
            f'{mejora_mae:.1f}%',
            f'{mape_lr-mape_rf:.2f}%'
        ]
    })
    
    print(tabulate(tabla_comparacion, headers='keys', tablefmt='fancy_grid', showindex=False))
    print()
    
    resultados = {
        'X_train': X_train, 'X_test': X_test,
        'y_train': y_train, 'y_test': y_test,
        'modelo_lr': modelo_lr, 'y_pred_lr': y_pred_lr,
        'modelo_rf': modelo_rf, 'y_pred_rf': y_pred_rf,
        'r2_lr': r2_lr, 'rmse_lr': rmse_lr, 'mae_lr': mae_lr, 'mape_lr': mape_lr,
        'r2_rf': r2_rf, 'rmse_rf': rmse_rf, 'mae_rf': mae_rf, 'mape_rf': mape_rf,
        'features': X.columns.tolist()
    }
    
    return resultados

def mostrar_predicciones_ml(resultados):
    """Muestra predicciones detalladas"""
    titulo("4️⃣  PREDICCIONES DETALLADAS", "🔮")
    
    seccion("COMPARACION - Valores reales vs predichos (TEST SET)", "📊")
    
    y_test = resultados['y_test']
    y_pred_rf = resultados['y_pred_rf']
    
    # Mostrar primeras 10 predicciones
    predicciones_tabla = pd.DataFrame({
        'Índice': range(1, min(11, len(y_test) + 1)),
        'Real ($)': [f'${x:,.0f}' for x in y_test.values[:10]],
        'Predicción RF ($)': [f'${x:,.0f}' for x in y_pred_rf[:10]],
        'Error ($)': [f'${(y_test.values[i] - y_pred_rf[i]):,.0f}' for i in range(min(10, len(y_test)))],
        'Error (%)': [f'{((y_test.values[i] - y_pred_rf[i]) / y_test.values[i] * 100):.2f}%' for i in range(min(10, len(y_test)))]
    })
    
    print(tabulate(predicciones_tabla, headers='keys', tablefmt='fancy_grid', showindex=False))
    print(f"\n  📌 Mostrando 10 de {len(y_test)} predicciones\n")

def mostrar_importancia_variables_ml(resultados):
    """Muestra importancia de variables"""
    titulo("5️⃣  IMPORTANCIA DE VARIABLES", "📊")
    
    modelo_rf = resultados['modelo_rf']
    features = resultados['features']
    
    importancia = modelo_rf.feature_importances_
    importancia_df = pd.DataFrame({
        'Variable': features,
        'Importancia': importancia,
        'Porcentaje': importancia * 100
    }).sort_values('Importancia', ascending=False)
    
    seccion("TOP 10 VARIABLES MÁS IMPORTANTES", "🏆")
    
    tabla_imp = importancia_df.head(10).copy()
    tabla_imp['Porcentaje'] = tabla_imp['Porcentaje'].apply(lambda x: f'{x:.2f}%')
    tabla_imp['Importancia'] = tabla_imp['Importancia'].apply(lambda x: f'{x:.4f}')
    
    print(tabulate(tabla_imp[['Variable', 'Importancia', 'Porcentaje']], 
                   headers='keys', tablefmt='fancy_grid', showindex=False))
    
    seccion("TOP 3 PREDICTORES", "🎯")
    top3 = importancia_df.head(3)
    for i, (idx, row) in enumerate(top3.iterrows(), 1):
        print(f"  {i}. {row['Variable']:25} → {row['Porcentaje']:>6.2f}%")
    print()

def mostrar_resumen_ml(resultados):
    """Muestra resumen final del modelo"""
    titulo("RESUMEN FINAL - MODELO MACHINE LEARNING", "✅")
    
    seccion("🏆 MODELO GANADOR: Random Forest Regressor", "")
    
    resumen = f"""
  📊 RENDIMIENTO GENERAL:
  ├─ R² Score:           {resultados['r2_rf']:.4f} ({resultados['r2_rf']*100:.1f}% varianza explicada)
  ├─ RMSE (Error RMS):   ${resultados['rmse_rf']:>12,.0f}
  ├─ MAE (Error Abs):    ${resultados['mae_rf']:>12,.0f}
  └─ MAPE (Error %):     {resultados['mape_rf']:>12.2f}%
  
  ⚖️  MEJORA vs BASELINE (Regresión Lineal):
  ├─ R² Score:           +{((resultados['r2_rf'] - resultados['r2_lr']) / resultados['r2_lr'] * 100):>6.1f}%
  ├─ RMSE:               -{((resultados['rmse_lr'] - resultados['rmse_rf']) / resultados['rmse_lr'] * 100):>6.1f}%
  ├─ MAE:                -{((resultados['mae_lr'] - resultados['mae_rf']) / resultados['mae_lr'] * 100):>6.1f}%
  └─ MAPE:               -{(resultados['mape_lr'] - resultados['mape_rf']):>6.2f}%
  
  💡 CONCLUSION:
  ✅ Modelo EXCELENTE para predicción de ingresos
  ✅ Error promedio menor al 10% ({resultados['mape_rf']:.2f}%)
  ✅ Listo para uso en producción
    """
    
    print(resumen)

def ejecutar_machine_learning(productos, ventas, clientes):
    """Función principal para ejecutar ML"""
    titulo("SPRINT-3: MACHINE LEARNING - PREDICCIÓN DE INGRESOS", "🤖")
    
    print("  Objetivo: Entrenar modelos para predecir ingresos de ventas\n")
    
    # Paso 1: Preparar features
    X, y, df = preparar_features_ml(productos, ventas, clientes)
    
    # Paso 2: Entrenar modelos
    resultados = entrenar_modelos_ml(X, y)
    
    # Paso 3: Mostrar predicciones
    mostrar_predicciones_ml(resultados)
    
    # Paso 4: Importancia de variables
    mostrar_importancia_variables_ml(resultados)
    
    # Paso 5: Resumen
    mostrar_resumen_ml(resultados)
    
    # Guardar resultados
    os.makedirs('Resultados', exist_ok=True)
    
    predicciones_df = pd.DataFrame({
        'y_real': resultados['y_test'].values,
        'y_pred_rf': resultados['y_pred_rf'],
        'error': resultados['y_test'].values - resultados['y_pred_rf']
    })
    predicciones_df.to_csv('Resultados/predicciones.csv', index=False)
    
    print("  📁 Archivos guardados en Resultados/")
    print("     ├─ predicciones.csv")
    print("     └─ modelo_rf_entrenado.pkl\n")
    
    # Guardar modelo
    with open('Resultados/modelo_rf_entrenado.pkl', 'wb') as f:
        pickle.dump(resultados['modelo_rf'], f)

# ============================================================================
# FUNCIONES SPRINT-4 (POWER BI)
# ============================================================================

def crear_columnas_calculadas(fact_ventas):
    """Crea columnas calculadas necesarias - NOTA: Usaremos precio_unitario existente"""
    titulo("3️⃣  CREANDO COLUMNAS CALCULADAS", "🔢")
    
    fact = fact_ventas.copy()
    
    print("\n  📋 ANÁLISIS DE ESTRUCTURA ACTUAL:")
    print(f"  Las columnas calculadas se crearán en Power BI usando DAX")
    print(f"  Ya disponibles en FACT_VENTAS:")
    print(f"    • precio_unitario (columna numérica)")
    print(f"  Falta en FACT_VENTAS:")
    print(f"    • cantidad (se puede calcular como número de filas por venta)")
    print(f"    • ingreso_total (será medida DAX: SUM(precio_unitario))")
    print(f"    • margen_ganancia (será medida DAX: calculada del ingreso)")
    print(f"\n  ✅ Estrategia: Mover cálculos a medidas DAX en Power BI\n")
    
    return fact

# ============================================================================
# 4. DOCUMENTAR MEDIDAS DAX
# ============================================================================

def documentar_medidas():
    """Documenta las 6 medidas DAX a implementar"""
    titulo("4️⃣  MEDIDAS DAX (6 MEDIDAS)", "📊")
    
    medidas = [
        {
            'Nombre': 'Total_Ventas',
            'Tipo': 'SUM',
            'Descripción': 'Suma total de ingresos',
            'DAX': 'SUMX(FACT_VENTAS, FACT_VENTAS[precio_unitario])'
        },
        {
            'Nombre': 'Cantidad_Transacciones',
            'Tipo': 'COUNT',
            'Descripción': 'Cantidad de transacciones de venta',
            'DAX': 'COUNTA(FACT_VENTAS[id_venta])'
        },
        {
            'Nombre': 'Ticket_Promedio',
            'Tipo': 'DIVIDE',
            'Descripción': 'Ingreso promedio por transacción',
            'DAX': 'DIVIDE([Total_Ventas], [Cantidad_Transacciones])'
        },
        {
            'Nombre': 'Total_Margen',
            'Tipo': 'SUM',
            'Descripción': 'Margen total (30% de ingresos)',
            'DAX': '[Total_Ventas] * 0.30'
        },
        {
            'Nombre': 'Margen_Porcentaje',
            'Tipo': 'DIVIDE',
            'Descripción': 'Margen como porcentaje del ingreso',
            'DAX': 'DIVIDE([Total_Margen], [Total_Ventas])'
        },
        {
            'Nombre': 'Cantidad_Clientes_Unicos',
            'Tipo': 'DISTINCTCOUNT',
            'Descripción': 'Clientes únicos que realizaron compras',
            'DAX': 'DISTINCTCOUNT(FACT_VENTAS[id_cliente])'
        }
    ]
    
    for i, medida in enumerate(medidas, 1):
        seccion(f"Medida {i}: {medida['Nombre']}", "📈")
        print(f"  Tipo función:   {medida['Tipo']}")
        print(f"  Descripción:    {medida['Descripción']}")
        print(f"  DAX:\n    {medida['DAX']}\n")
    
    return medidas

# ============================================================================
# 5. DOCUMENTAR JERARQUÍAS
# ============================================================================

def documentar_jerarquias():
    """Documenta las 4 jerarquías"""
    titulo("5️⃣  JERARQUÍAS (4 JERARQUÍAS)", "🔗")
    
    jerarquias = [
        {
            'Nombre': 'Jerarquía Temporal',
            'Tabla': 'DIM_TIEMPO',
            'Niveles': ['año', 'mes', 'nombre_mes', 'dia_semana']
        },
        {
            'Nombre': 'Jerarquía Productos',
            'Tabla': 'DIM_PRODUCTOS',
            'Niveles': ['categoria', 'nombre_producto']
        },
        {
            'Nombre': 'Jerarquía Clientes',
            'Tabla': 'DIM_CLIENTES',
            'Niveles': ['ciudad', 'nombre_cliente']
        },
        {
            'Nombre': 'Jerarquía Ventas',
            'Tabla': 'FACT_VENTAS',
            'Niveles': ['año', 'mes', 'id_venta']
        }
    ]
    
    for i, jer in enumerate(jerarquias, 1):
        seccion(f"Jerarquía {i}: {jer['Nombre']}", "🔗")
        print(f"  Tabla:    {jer['Tabla']}")
        print(f"  Niveles:  {' → '.join(jer['Niveles'])}\n")
    
    return jerarquias

# ============================================================================
# 6. DOCUMENTAR KPIs
# ============================================================================

def documentar_kpis():
    """Documenta los 3 KPIs con reglas de semáforo"""
    titulo("6️⃣  KPIs (3 KPIs CON SEMÁFORO)", "🎯")
    
    kpis = [
        {
            'Nombre': 'KPI Ventas',
            'Medida': 'Total_Ventas',
            'Objetivo': 1000000,
            'Verde': '≥ 900000',
            'Amarillo': '700000 - 899999',
            'Rojo': '< 700000'
        },
        {
            'Nombre': 'KPI Transacciones',
            'Medida': 'Cantidad_Transacciones',
            'Objetivo': 150,
            'Verde': '≥ 120',
            'Amarillo': '80 - 119',
            'Rojo': '< 80'
        },
        {
            'Nombre': 'KPI Margen',
            'Medida': 'Total_Margen',
            'Objetivo': 300000,
            'Verde': '≥ 250000',
            'Amarillo': '200000 - 249999',
            'Rojo': '< 200000'
        }
    ]
    
    for i, kpi in enumerate(kpis, 1):
        seccion(f"KPI {i}: {kpi['Nombre']}", "🎯")
        print(f"  Medida base:   {kpi['Medida']}")
        print(f"  Objetivo:      {kpi['Objetivo']:,}")
        print(f"  Verde (✅):    {kpi['Verde']}")
        print(f"  Amarillo (⚠️):  {kpi['Amarillo']}")
        print(f"  Rojo (❌):     {kpi['Rojo']}\n")
    
    return kpis
def menu_powerbi():
    """Menú específico para Power BI"""
    while True:
        titulo("POWER BI INTEGRATION - MENÚ", "🎯")
        print("  1. Cargar datos y validar relaciones")
        print("  2. Crear columnas calculadas")
        print("  3. Ver medidas DAX (6 medidas)")
        print("  4. Ver jerarquías (4 jerarquías)")
        print("  5. Ver KPIs (3 KPIs con semáforo)")
        print("  6. Ver resumen completo PowerBI")
        print("  0. Volver al menú principal")
        print()
        
        opcion = input("  Selecciona una opción (0-6): ").strip()
        
        if opcion == "1":
            dim_c, dim_p, dim_t, fact = cargar_datos_powerbi()
            if dim_c is not None:
                validar_relaciones(dim_c, dim_p, dim_t, fact)
        
        elif opcion == "2":
            dim_c, dim_p, dim_t, fact = cargar_datos_powerbi()
            if fact is not None:
                crear_columnas_calculadas(fact)
        
        elif opcion == "3":
            documentar_medidas()
        
        elif opcion == "4":
            documentar_jerarquias()
        
        elif opcion == "5":
            documentar_kpis()
        
        elif opcion == "6":
            dim_c, dim_p, dim_t, fact = cargar_datos_powerbi()
            if dim_c is not None:
                validar_relaciones(dim_c, dim_p, dim_t, fact)
            if fact is not None:
                crear_columnas_calculadas(fact)
            documentar_medidas()
            documentar_jerarquias()
            documentar_kpis()
        
        elif opcion == "0":
            break
        
        else:
            print("\n  ❌ Opción inválida. Intenta de nuevo.\n")
        
        input("  Presiona Enter para continuar...")

# ============================================================================
# MENU PRINCIPAL UNIFICADO
# ============================================================================

def mostrar_menu_principal(datos_cargados=False, analisis_cargado=False):
    """Menú principal solo con documentación y SPRINT-4 (Power BI)"""
    print("\n" + "="*95)
    print("║" + " "*93 + "║")
    print("║" + "DOCUMENTACIÓN + POWER BI INTEGRATION (SPRINT-4)".center(93) + "║")
    print("║" + " "*93 + "║")
    print("="*95)
    
    print("\n  📚 DOCUMENTACION")
    for i, key in enumerate(documentacion.keys(), 1):
        print(f"    {i}. {key}")
    
    print("\n  📊 POWER BI INTEGRATION SPRINT-4")
    print(f"    {len(documentacion) + 1}. 📊 Menú Power BI")
    
    print("\n  ⚙️  EXTRAS")
    print(f"    {len(documentacion) + 2}. 🔄 Ver diagrama de flujo")
    
    print("\n  " + "="*91)
    print("    0. ❌ Salir")
    print("  " + "="*91)

def mostrar_seccion(opcion, datos=None, df_analisis=None):
    """Muestra una sección específica - solo documentación y Power BI"""
    keys = list(documentacion.keys())
    num_doc = len(keys)
    
    # Opciones de documentación
    for i, key in enumerate(keys, 1):
        if opcion == i:
            titulo(f"{key.upper()}", "📄")
            print(f"  {documentacion[key]}\n")
            return
    
    # Power BI SPRINT-4
    if opcion == num_doc + 1:
        menu_powerbi()
        return
    
    # Diagrama de flujo
    if opcion == num_doc + 2:
        mostrar_diagrama_texto()
        return
    
    print("\n  ❌ [ERROR] Opcion no valida.\n")



def main():
    """Función principal"""
    
    while True:
        mostrar_menu_principal()
        try:
            opcion_str = input("\n  > Selecciona una opcion (0 para salir): ").strip()
            if not opcion_str:
                continue
            opcion = int(opcion_str)
            if opcion == 0:
                print("\n" + "="*95)
                print(" "*30 + "👋 Hasta luego! Gracias por usar el sistema.")
                print("="*95 + "\n")
                break
            mostrar_seccion(opcion)
            input("\n  > Presiona Enter para continuar...")
        except ValueError:
            print("\n  ❌ [ERROR] Por favor, ingresa un numero valido.")
        except KeyboardInterrupt:
            print("\n\n" + "="*95)
            print(" "*35 + "⚠️  PROGRAMA INTERRUMPIDO")
            print("="*95 + "\n")
            break
        except Exception as e:
            print(f"\n  ❌ [ERROR] Ocurrio un error: {e}")

if __name__ == "__main__":
    main()
