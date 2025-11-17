import pandas as pd
from tabulate import tabulate
import sys
import io
from datetime import datetime

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Rutas de los archivos
RUTA_PRODUCTOS = "Data/productos_limpio.csv"
RUTA_VENTAS = "Data/ventas_limpio.csv"
RUTA_CLIENTES = "Data/clientes_limpio.csv"
RUTA_ANALISIS_COMPLETO = "Data/analisis_ventas_completo.csv"

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

# Funciones de decoracion
def linea_superior():
    print("\n" + "="*90)

def linea_media():
    print("-"*90)

def linea_inferior():
    print("="*90 + "\n")

def titulo(texto, emoji=""):
    linea_superior()
    print(f"  {emoji} {texto}".ljust(90))
    linea_inferior()

def seccion(texto, emoji=""):
    linea_media()
    print(f"  {emoji} {texto}")
    linea_media()

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

def mostrar_menu(datos_cargados=False, analisis_cargado=False):
    """Menú principal mejorado"""
    print("\n" + "="*90)
    print("║" + " "*88 + "║")
    print("║" + "SISTEMA DE CONTROL DE STOCK Y VENTAS".center(88) + "║")
    print("║" + " "*88 + "║")
    print("="*90)
    
    print("\n  📚 DOCUMENTACION")
    for i, key in enumerate(documentacion.keys(), 1):
        print(f"    {i}. {key}")
    
    print("\n  📊 ANALISIS DE DATOS")
    if datos_cargados:
        print(f"    {len(documentacion) + 1}. 📦 Ver resumen de datos")
        print(f"    {len(documentacion) + 2}. 📈 Ver estadisticas descriptivas")
        print(f"    {len(documentacion) + 3}. 🔍 Ver analisis de ventas")
    else:
        print(f"    {len(documentacion) + 1}. 📦 Ver resumen de datos [No disponible]")
        print(f"    {len(documentacion) + 2}. 📈 Ver estadisticas descriptivas [No disponible]")
        print(f"    {len(documentacion) + 3}. 🔍 Ver analisis de ventas [No disponible]")
    
    if analisis_cargado:
        print("\n  🔬 ANALISIS AVANZADO")
        print(f"    {len(documentacion) + 4}. 📊 Estadisticas descriptivas")
        print(f"    {len(documentacion) + 5}. 📉 Analisis de distribucion")
        print(f"    {len(documentacion) + 6}. 🔗 Analisis de correlacion")
        print(f"    {len(documentacion) + 7}. 💡 Insights de negocio")
        print(f"    {len(documentacion) + 8}. 🏪 Ingresos por categoria")
        print(f"    {len(documentacion) + 9}. 📈 Evolucion de ingresos")
        print(f"    {len(documentacion) + 10}. 👑 Top 10 clientes")
    else:
        print("\n  🔬 ANALISIS AVANZADO")
        print(f"    {len(documentacion) + 4}. 📊 Estadisticas descriptivas [No disponible]")
        print(f"    {len(documentacion) + 5}. 📉 Analisis de distribucion [No disponible]")
        print(f"    {len(documentacion) + 6}. 🔗 Analisis de correlacion [No disponible]")
        print(f"    {len(documentacion) + 7}. 💡 Insights de negocio [No disponible]")
        print(f"    {len(documentacion) + 8}. 🏪 Ingresos por categoria [No disponible]")
        print(f"    {len(documentacion) + 9}. 📈 Evolucion de ingresos [No disponible]")
        print(f"    {len(documentacion) + 10}. 👑 Top 10 clientes [No disponible]")
    
    print("\n  ⚙️  EXTRAS")
    print(f"    {len(documentacion) + 11}. 🔄 Ver diagrama de flujo")
    
    print("\n  " + "="*86)
    print("    0. ❌ Salir")
    print("  " + "="*86)

def mostrar_seccion(opcion, datos=None, df_analisis=None):
    """Muestra una sección específica"""
    keys = list(documentacion.keys())
    num_doc = len(keys)
    
    # Opciones de documentación
    for i, key in enumerate(keys, 1):
        if opcion == i:
            titulo(f"{key.upper()}", "📄")
            print(f"  {documentacion[key]}\n")
            return
    
    # Opciones de análisis Clase 6
    if datos:
        if opcion == num_doc + 1:
            mostrar_resumen_datos(datos[0], datos[1], datos[2])
            return
        elif opcion == num_doc + 2:
            mostrar_estadisticas(datos[0], datos[1], datos[2])
            return
        elif opcion == num_doc + 3:
            mostrar_analisis_ventas(datos[0], datos[1], datos[2])
            return
    
    # Opciones de análisis avanzado
    if df_analisis is not None:
        if opcion == num_doc + 4:
            mostrar_estadisticas_descriptivas_analisis(df_analisis)
            return
        elif opcion == num_doc + 5:
            mostrar_analisis_distribucion(df_analisis)
            return
        elif opcion == num_doc + 6:
            mostrar_analisis_correlacion(df_analisis)
            return
        elif opcion == num_doc + 7:
            mostrar_insights_negocio()
            return
        elif opcion == num_doc + 8:
            mostrar_ingresos_categoria(df_analisis)
            return
        elif opcion == num_doc + 9:
            mostrar_evolucion_ingresos(df_analisis)
            return
        elif opcion == num_doc + 10:
            mostrar_top_clientes(df_analisis)
            return
    
    # Diagrama de flujo
    if opcion == len(documentacion) + 11:
        mostrar_diagrama_texto()
        return
    
    print("\n  ❌ [ERROR] Opcion no valida o datos no disponibles.\n")

def mostrar_pantalla_carga():
    """Pantalla de carga inicial"""
    print("\n" + "="*90)
    print(" "*30 + "⏳ CARGANDO SISTEMA DE CONTROL ⏳")
    print("="*90)

def main():
    """Función principal"""
    mostrar_pantalla_carga()
    productos, ventas, clientes = cargar_datos()
    datos_disponibles = productos is not None
    
    
    datos = (productos, ventas, clientes) if datos_disponibles else None
    df_analisis = cargar_analisis()
    analisis_disponible = df_analisis is not None
    
    while True:
        mostrar_menu(datos_disponibles, analisis_disponible)
        try:
            opcion_str = input("\n  > Selecciona una opcion (0 para salir): ").strip()
            if not opcion_str:
                continue
            opcion = int(opcion_str)
            if opcion == 0:
                print("\n" + "="*90)
                print(" "*25 + "👋 Hasta luego! Gracias por usar el sistema.")
                print("="*90 + "\n")
                break
            mostrar_seccion(opcion, datos, df_analisis)
            input("\n  > Presiona Enter para continuar...")
        except ValueError:
            print("\n  ❌ [ERROR] Por favor, ingresa un numero valido.")
        except KeyboardInterrupt:
            print("\n\n" + "="*90)
            print(" "*30 + "⚠️  PROGRAMA INTERRUMPIDO")
            print("="*90 + "\n")
            break
        except Exception as e:
            print(f"\n  ❌ [ERROR] Ocurrio un error: {e}")

if __name__ == "__main__":
    main()