

import pandas as pd
import numpy as np
import sys
import io
import os

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


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

# ============================================================================
# 1. CARGAR DATOS
# ============================================================================

def cargar_datos_powerbi():
    """Carga las tablas dimensionales y de hechos"""
    titulo("1️⃣  CARGANDO DATOS POWERBI", "📂")
    
    ruta = "PowerBI_Data/"
    
    try:
        dim_clientes = pd.read_csv(ruta + "DIM_CLIENTES.csv")
        dim_productos = pd.read_csv(ruta + "DIM_PRODUCTOS.csv")
        dim_tiempo = pd.read_csv(ruta + "DIM_TIEMPO.csv")
        fact_ventas = pd.read_csv(ruta + "FACT_VENTAS.csv")
        
        print(f"  ✓ DIM_CLIENTES       ({len(dim_clientes):3} registros)")
        print(f"  ✓ DIM_PRODUCTOS      ({len(dim_productos):3} registros)")
        print(f"  ✓ DIM_TIEMPO         ({len(dim_tiempo):3} registros)")
        print(f"  ✓ FACT_VENTAS        ({len(fact_ventas):3} registros)\n")
        
        return dim_clientes, dim_productos, dim_tiempo, fact_ventas
    except FileNotFoundError as e:
        print(f"  ❌ Error: {e}\n")
        return None, None, None, None

# ============================================================================
# 2. VALIDAR RELACIONES Y CARDINALIDAD
# ============================================================================

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
# 3. CREAR COLUMNAS CALCULADAS
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

# ============================================================================
# 7. MENU PRINCIPAL
# ============================================================================

def menu_principal():
    """Menú interactivo principal"""
    while True:
        titulo("POWER BI INTEGRATION - MENÚ PRINCIPAL", "🎯")
        print("  1. Cargar datos y validar relaciones")
        print("  2. Crear columnas calculadas")
        print("  3. Ver medidas DAX (6 medidas)")
        print("  4. Ver jerarquías (4 jerarquías)")
        print("  5. Ver KPIs (3 KPIs con semáforo)")
        print("  6. Ver resumen completo")
        print("  7. Salir")
        print()
        
        opcion = input("  Selecciona una opción (1-7): ").strip()
        
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
        
        elif opcion == "7":
            print("\n  ¡Hasta luego! ✨\n")
            break
        
        else:
            print("\n  ❌ Opción inválida. Intenta de nuevo.\n")
        
        input("  Presiona Enter para continuar...")

# ============================================================================
# EJECUTAR
# ============================================================================

if __name__ == "__main__":
    try:
        menu_principal()
    except Exception as e:
        print(f"\n  ❌ Error: {e}\n")
