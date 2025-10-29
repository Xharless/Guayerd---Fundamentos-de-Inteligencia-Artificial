# visualizacion_negocio.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 0. Carga y Preparación de Datos ---
# Copilot: Cargamos el dataset maestro, que es el resultado de la limpieza y
# unión de todos nuestros datos. Este archivo es la fuente única de verdad
# para nuestro análisis.
try:
    df = pd.read_csv('../Clase 7/analisis_ventas_completo.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])
    print("Archivo 'analisis_ventas_completo.csv' cargado y preparado.")
except FileNotFoundError:
    print("Error: No se encontró 'analisis_ventas_completo.csv'.")
    print("Asegúrate de haber ejecutado los scripts de limpieza y unión primero.")
    exit()

# --- 1. Selección de Variables Clave ---
# Copilot: Para nuestras visualizaciones, seleccionamos las variables que
# responden directamente a preguntas de negocio.
# - 'categoria' y 'ingreso_total': Para entender la rentabilidad por producto.
# - 'fecha' y 'ingreso_total': Para analizar tendencias y estacionalidad.
# - 'nombre_cliente' y 'ingreso_total': Para identificar clientes de alto valor.
print("\n--- Variables clave seleccionadas: 'categoria', 'ingreso_total', 'fecha', 'nombre_cliente' ---")


# --- 2. Creación de Visualizaciones ---

# --- Visualización 1: Ingresos por Categoría de Producto ---
# Copilot: Esta visualización nos permite identificar qué categorías son las más
# importantes para el negocio en términos de ingresos. Usamos un gráfico de barras
# porque es ideal para comparar valores entre diferentes categorías.

print("\nGenerando Visualización 1: Ingresos por Categoría...")

# Agrupamos los datos por categoría y sumamos los ingresos
ingresos_categoria = df.groupby('categoria')['ingreso_total'].sum().sort_values(ascending=False)

plt.figure(figsize=(12, 7))
sns.barplot(x=ingresos_categoria.values, y=ingresos_categoria.index, palette='viridis')
plt.title('Ingresos Totales por Categoría de Producto', fontsize=16)
plt.xlabel('Ingresos Totales ($)', fontsize=12)
plt.ylabel('Categoría', fontsize=12)
plt.tight_layout()
plt.savefig('ingresos_por_categoria.png')
print("Gráfico guardado como 'ingresos_por_categoria.png'")

# Copilot: Interpretación de Hallazgos (Visualización 1)
# - Patrón Identificado: Existe una clara dominancia de ciertas categorías.
#   'Almacén', 'Bebidas' y 'Lácteos' probablemente lideran los ingresos.
# - Decisión de Negocio: Debemos asegurar el stock de las categorías top.
#   Para las categorías de bajos ingresos, se podría evaluar si requieren más
#   marketing o si son productos de nicho que no necesitan gran inversión.


# --- Visualización 2: Evolución de Ventas en el Tiempo ---
# Copilot: Un gráfico de líneas es perfecto para mostrar cómo una variable
# cambia a lo largo del tiempo. Aquí analizaremos la tendencia de los ingresos
# mensuales para detectar patrones de crecimiento o estacionalidad.

print("\nGenerando Visualización 2: Evolución de Ingresos Mensuales...")

# Agrupamos los ingresos por mes
df['mes'] = df['fecha'].dt.to_period('M')
ingresos_mensuales = df.groupby('mes')['ingreso_total'].sum()

# Convertimos el índice a timestamp para graficarlo correctamente
ingresos_mensuales.index = ingresos_mensuales.index.to_timestamp()

plt.figure(figsize=(12, 6))
sns.lineplot(x=ingresos_mensuales.index, y=ingresos_mensuales.values, marker='o', color='royalblue')
plt.title('Evolución de Ingresos Totales Mensuales', fontsize=16)
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Ingresos Totales ($)', fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.savefig('evolucion_ingresos_mensuales.png')
print("Gráfico guardado como 'evolucion_ingresos_mensuales.png'")

# Copilot: Interpretación de Hallazgos (Visualización 2)
# - Tendencia Identificada: Podemos observar si las ventas tienen una tendencia
#   ascendente (negocio en crecimiento), descendente (problema a investigar) o
#   si hay picos en ciertos meses (estacionalidad).
# - Decisión de Negocio: Si hay una tendencia positiva, podemos proyectar el
#   crecimiento. Si hay estacionalidad, podemos planificar campañas de marketing
#   y gestión de inventario para los meses de alta y baja demanda.


# --- Visualización 3: Top 10 Clientes por Gasto Total ---
# Copilot: Identificar a nuestros clientes más valiosos es crucial. Un gráfico
# de barras horizontales es efectivo para mostrar un ranking de los "Top N" clientes.

print("\nGenerando Visualización 3: Top 10 Clientes...")

# Agrupamos por cliente y sumamos sus gastos
top_clientes = df.groupby('nombre_cliente')['ingreso_total'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 8))
sns.barplot(x=top_clientes.values, y=top_clientes.index, palette='plasma')
plt.title('Top 10 Clientes por Gasto Total', fontsize=16)
plt.xlabel('Gasto Total ($)', fontsize=12)
plt.ylabel('Nombre del Cliente', fontsize=12)
plt.tight_layout()
plt.savefig('top_10_clientes.png')
print("Gráfico guardado como 'top_10_clientes.png'")

# Copilot: Interpretación de Hallazgos (Visualización 3)
# - Patrón Identificado: Es común que un pequeño grupo de clientes genere una
#   parte desproporcionada de los ingresos (Principio de Pareto).
# - Decisión de Negocio: Estos 10 clientes son vitales. Se deben implementar
#   estrategias de fidelización para ellos: programas de lealtad, descuentos
#   exclusivos o comunicación personalizada para asegurar su retención.

print("\nAnálisis visual completado. Revisa los 3 gráficos generados en la carpeta.")

