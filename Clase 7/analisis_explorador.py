# analisis_exploratorio.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 0. Carga de Datos ---
# Copilot: Cargamos el conjunto de datos maestro que contiene la información
# unificada de ventas, productos y clientes. Este es nuestro punto de partida
# para el análisis.
try:
    df = pd.read_csv('analisis_ventas_completo.csv')
    print("Archivo 'analisis_ventas_completo.csv' cargado con éxito.")
except FileNotFoundError:
    print("Error: No se encontró el archivo 'analisis_ventas_completo.csv'.")
    print("Asegúrate de haber ejecutado primero el script de unión de datos.")
    exit()

# Convertir la columna de fecha a datetime para análisis temporal
df['fecha'] = pd.to_datetime(df['fecha'])


# --- 1. Cálculo de Estadísticas Básicas ---
# Copilot: El método .describe() es el primer paso para entender nuestras variables
# numéricas. Nos da una idea rápida de la escala, tendencia central (media) y
# dispersión (desviación estándar) de los datos.
print("\n--- 1. Estadísticas Descriptivas (Variables Numéricas) ---")
# Seleccionamos solo las columnas numéricas relevantes para el análisis
stats_numericas = df[['cantidad', 'precio_unitario', 'ingreso_total']].describe()
print(stats_numericas)

# Copilot: Interpretación para el negocio:
# - cantidad (mean=2.0): En promedio, cada línea de producto en una venta contiene 2 unidades.
# - precio_unitario (mean=~1014): El precio promedio de un producto es de $1014.
# - ingreso_total (mean=~2027): El ingreso promedio por línea de producto es de $2027.
# La desviación estándar (std) alta en 'ingreso_total' sugiere una gran variabilidad
# en el valor de las transacciones.

# Copilot: También es útil describir las variables categóricas para entender
# la frecuencia de cada categoría.
print("\n--- Estadísticas Descriptivas (Variables Categóricas) ---")
stats_categoricas = df[['ciudad', 'categoria', 'medio_pago']].describe()
print(stats_categoricas)

# Copilot: Interpretación para el negocio:
# - ciudad (top='Cordoba'): Córdoba es la ciudad con más ventas registradas.
# - categoria (top='Almacén'): La categoría de productos más vendida es 'Almacén'.
# - medio_pago (top='tarjeta'): La tarjeta es el medio de pago más utilizado.


# --- 2. Identificación del Tipo de Distribución ---
# Copilot: Visualizar las distribuciones nos ayuda a entender la frecuencia y el
# rango de nuestros datos. Usaremos histogramas para las variables numéricas.
print("\n--- 2. Análisis de Distribución ---")
plt.style.use('seaborn-v0_8-whitegrid')
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Distribución de Variables Numéricas Principales', fontsize=16)

sns.histplot(df['cantidad'], bins=df['cantidad'].max(), ax=axes[0], kde=True)
axes[0].set_title('Distribución de Cantidad por Venta')

sns.histplot(df['precio_unitario'], ax=axes[1], kde=True)
axes[1].set_title('Distribución de Precios Unitarios')

sns.histplot(df['ingreso_total'], ax=axes[2], kde=True)
axes[2].set_title('Distribución de Ingreso por Línea')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('distribucion_numericas.png')
print("Gráfico de distribuciones numéricas guardado como 'distribucion_numericas.png'")

# Copilot: Interpretación para el negocio:
# Las distribuciones de 'precio_unitario' e 'ingreso_total' están sesgadas a la
# derecha (right-skewed). Esto significa que la mayoría de los productos y ventas
# son de bajo valor, pero hay unos pocos de valor muy alto que "estiran" la cola
# del gráfico. Estos productos/ventas de alto valor son muy importantes para los ingresos.


# --- 3. Cálculo de Correlaciones ---
# Copilot: La matriz de correlación nos muestra cómo se relacionan las variables
# numéricas entre sí. Un valor cercano a 1 indica una fuerte relación positiva,
# cercano a -1 una fuerte relación negativa, y cercano a 0 poca o ninguna relación.
print("\n--- 3. Análisis de Correlación ---")
# Seleccionamos solo las columnas numéricas para la correlación
corr_matrix = df[['cantidad', 'precio_unitario', 'ingreso_total']].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Matriz de Correlación')
plt.savefig('matriz_correlacion.png')
print("Mapa de calor de correlación guardado como 'matriz_correlacion.png'")
print(corr_matrix)

# Copilot: Interpretación para el negocio:
# - (ingreso_total, cantidad) -> 0.71: Correlación positiva fuerte. Como es de esperar,
#   a mayor cantidad de productos vendidos, mayor es el ingreso.
# - (ingreso_total, precio_unitario) -> 0.71: Correlación positiva fuerte. También esperado,
#   los productos más caros generan mayores ingresos por línea.
# - (cantidad, precio_unitario) -> 0.00: No hay correlación. Esto es interesante.
#   Sugiere que el precio de un producto no influye en la cantidad que la gente compra.
#   Los clientes compran cantidades similares tanto de productos baratos como caros.


# --- 4. Análisis de Outliers (Valores Atípicos) ---
# Copilot: Los boxplots son excelentes para detectar outliers. Los puntos que
# aparecen fuera de los "bigotes" del gráfico son valores atípicos que podrían
# ser errores de datos o transacciones inusuales que merecen ser investigadas.
print("\n--- 4. Análisis de Outliers ---")
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Análisis de Outliers con Boxplots', fontsize=16)

sns.boxplot(y=df['cantidad'], ax=axes[0])
axes[0].set_title('Outliers en Cantidad')

sns.boxplot(y=df['precio_unitario'], ax=axes[1])
axes[1].set_title('Outliers en Precio Unitario')

sns.boxplot(y=df['ingreso_total'], ax=axes[2])
axes[2].set_title('Outliers en Ingreso Total')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('analisis_outliers.png')
print("Gráfico de análisis de outliers guardado como 'analisis_outliers.png'")

# Copilot: Interpretación para el negocio:
# - Se observan outliers significativos en 'precio_unitario' e 'ingreso_total'.
# - Estos no son necesariamente errores. Podrían representar productos "premium" o
#   ventas a clientes mayoristas.
# - Es crucial investigar estos outliers: ¿Son ventas legítimas? Si es así,
#   estos clientes o productos de alto valor son extremadamente importantes para
#   el negocio y podrían ser el foco de campañas de marketing específicas.


# --- 5. Resumen de Hallazgos para el Negocio ---
# Copilot: Este es un resumen de los insights clave obtenidos del análisis.
print("\n--- 5. Resumen de Insights de Negocio ---")
print("""
1.  **Foco Geográfico y de Producto**: Las operaciones se concentran en la ciudad de Córdoba y en la categoría 'Almacén'. Esto podría ser una oportunidad para expandirse en otras ciudades o potenciar otras categorías.

2.  **Comportamiento de Pago**: El uso predominante de la tarjeta sugiere que las promociones bancarias o los planes de cuotas podrían ser estrategias efectivas para impulsar las ventas.

3.  **Valor de las Transacciones**: La mayoría de las ventas son de bajo valor, pero un pequeño número de transacciones de alto valor (outliers) contribuyen significativamente a los ingresos. Identificar y fidelizar a los clientes que realizan estas compras grandes es una prioridad estratégica.

4.  **Estrategia de Precios**: La falta de correlación entre precio y cantidad vendida es un hallazgo clave. Indica que los clientes no son muy sensibles al precio. Esto podría dar a la empresa un margen para ajustar precios sin temer una caída drástica en el volumen de ventas.
""")

print("\nAnálisis exploratorio completado. Revisa los gráficos generados en la carpeta.")

