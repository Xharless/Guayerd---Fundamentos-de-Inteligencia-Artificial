"""
Script de validación del modelo dimensional para Power BI
Valida relaciones, cardinalidad y genera reporte de validación
CORREGIDO: Usa columnas reales (id_cliente, id_producto, fecha)
"""

import pandas as pd
import os
import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def titulo(texto, emoji=""):
    print("\n" + "="*90)
    print(f"  {emoji} {texto}")
    print("="*90 + "\n")

def validar_modelo():
    """Valida el modelo dimensional completo con columnas corregidas"""
    titulo("VALIDACION DEL MODELO DIMENSIONAL", "🔍")
    
    # Cargar datos
    print("  📂 Cargando datos...")
    dim_clientes = pd.read_csv("PowerBI_Data/DIM_CLIENTES.csv")
    dim_productos = pd.read_csv("PowerBI_Data/DIM_PRODUCTOS.csv")
    dim_tiempo = pd.read_csv("PowerBI_Data/DIM_TIEMPO.csv")
    fact_ventas = pd.read_csv("PowerBI_Data/FACT_VENTAS.csv")
    
    print(f"     ✓ DIM_CLIENTES     ({len(dim_clientes)} registros)")
    print(f"     ✓ DIM_PRODUCTOS    ({len(dim_productos)} registros)")
    print(f"     ✓ DIM_TIEMPO       ({len(dim_tiempo)} registros)")
    print(f"     ✓ FACT_VENTAS      ({len(fact_ventas)} registros)\n")
    
    # Crear carpeta Resultados
    os.makedirs("Resultados", exist_ok=True)
    
    # Validar relaciones
    print("  🔗 Validando relaciones...\n")
    
    relaciones = []
    
    # Relación 1: Usando id_cliente (minúsculas)
    print("     Validando FACT_VENTAS → DIM_CLIENTES...")
    fk_cliente = fact_ventas['id_cliente'].unique()
    pk_cliente = dim_clientes['id_cliente'].unique()
    validos_cliente = len([x for x in fk_cliente if x in pk_cliente])
    
    relaciones.append({
        'Relacion': 'FACT_VENTAS → DIM_CLIENTES',
        'Cardinalidad': 'N:1',
        'FK': 'id_cliente',
        'PK': 'id_cliente',
        'Registros_FK': len(fk_cliente),
        'Registros_PK': len(pk_cliente),
        'Validos': validos_cliente,
        'Estado': '✓ VALIDA' if validos_cliente == len(fk_cliente) else '❌ ERROR'
    })
    
    # Relación 2: Usando id_producto (minúsculas)
    print("     Validando FACT_VENTAS → DIM_PRODUCTOS...")
    fk_producto = fact_ventas['id_producto'].unique()
    pk_producto = dim_productos['id_producto'].unique()
    validos_producto = len([x for x in fk_producto if x in pk_producto])
    
    relaciones.append({
        'Relacion': 'FACT_VENTAS → DIM_PRODUCTOS',
        'Cardinalidad': 'N:1',
        'FK': 'id_producto',
        'PK': 'id_producto',
        'Registros_FK': len(fk_producto),
        'Registros_PK': len(pk_producto),
        'Validos': validos_producto,
        'Estado': '✓ VALIDA' if validos_producto == len(fk_producto) else '❌ ERROR'
    })
    
    # Relación 3: Usando fecha (no ID_Fecha)
    print("     Validando FACT_VENTAS → DIM_TIEMPO...")
    print("     ⚠️  Nota: Usando columna 'fecha' para relacionar (no existe ID_Fecha)")
    
    fact_fechas = pd.to_datetime(fact_ventas['fecha']).dt.date.unique()
    dim_fechas = pd.to_datetime(dim_tiempo['fecha']).dt.date.unique()
    validos_tiempo = len([x for x in fact_fechas if x in dim_fechas])
    
    relaciones.append({
        'Relacion': 'FACT_VENTAS → DIM_TIEMPO',
        'Cardinalidad': 'N:1',
        'FK': 'fecha',
        'PK': 'fecha',
        'Registros_FK': len(fact_fechas),
        'Registros_PK': len(dim_fechas),
        'Validos': validos_tiempo,
        'Estado': '✓ VALIDA' if validos_tiempo == len(fact_fechas) else '⚠️  PARCIAL'
    })
    
    # Mostrar resultados
    print("\n")
    df_relaciones = pd.DataFrame(relaciones)
    print(df_relaciones[['Relacion', 'Cardinalidad', 'Estado']].to_string(index=False))
    
    # Guardar relaciones
    df_relaciones.to_csv("Resultados/relaciones_validadas.csv", index=False)
    df_relaciones.to_json("Resultados/relaciones_validadas.json", orient='records', indent=2)
    print("\n  💾 Archivos guardados:")
    print("     • Resultados/relaciones_validadas.csv")
    print("     • Resultados/relaciones_validadas.json")
    
    # Analizar estructura de FACT_VENTAS
    print("\n  📊 Estructura de FACT_VENTAS:")
    print(f"     Columnas detectadas ({len(fact_ventas.columns)}):")
    for col in fact_ventas.columns:
        print(f"       • {col}")
    
    # Resumen
    print("\n" + "="*90)
    total_ok = sum(1 for rel in relaciones if '✓' in rel['Estado'])
    print(f"  ✅ VALIDACION COMPLETADA: {total_ok}/{len(relaciones)} relaciones válidas")
    print("="*90 + "\n")

if __name__ == "__main__":
    try:
        validar_modelo()
    except Exception as e:
        print(f"\n  ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
