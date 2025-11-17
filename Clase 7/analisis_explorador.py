
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    df = pd.read_csv('analisis_ventas_completo.csv')
    print("Archivo 'analisis_ventas_completo.csv' cargado con éxito.")
except FileNotFoundError:
    print("Error: No se encontró el archivo 'analisis_ventas_completo.csv'.")
    print("Asegúrate de haber ejecutado primero el script de unión de datos.")
    exit()


df['fecha'] = pd.to_datetime(df['fecha'])



print("\n--- 1. Estadísticas Descriptivas (Variables Numéricas) ---")

stats_numericas = df[['cantidad', 'precio_unitario', 'ingreso_total']].describe()
print(stats_numericas)


print("\n--- Estadísticas Descriptivas (Variables Categóricas) ---")
stats_categoricas = df[['ciudad', 'categoria', 'medio_pago']].describe()
print(stats_categoricas)


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


print("\n--- 3. Análisis de Correlación ---")
corr_matrix = df[['cantidad', 'precio_unitario', 'ingreso_total']].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Matriz de Correlación')
plt.savefig('matriz_correlacion.png')
print("Mapa de calor de correlación guardado como 'matriz_correlacion.png'")
print(corr_matrix)


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


print("\n--- 5. Resumen de Insights de Negocio ---")
print("""
1.  **Foco Geográfico y de Producto**: Las operaciones se concentran en la ciudad de Córdoba y en la categoría 'Almacén'. Esto podría ser una oportunidad para expandirse en otras ciudades o potenciar otras categorías.

2.  **Comportamiento de Pago**: El uso predominante de la tarjeta sugiere que las promociones bancarias o los planes de cuotas podrían ser estrategias efectivas para impulsar las ventas.

3.  **Valor de las Transacciones**: La mayoría de las ventas son de bajo valor, pero un pequeño número de transacciones de alto valor (outliers) contribuyen significativamente a los ingresos. Identificar y fidelizar a los clientes que realizan estas compras grandes es una prioridad estratégica.

4.  **Estrategia de Precios**: La falta de correlación entre precio y cantidad vendida es un hallazgo clave. Indica que los clientes no son muy sensibles al precio. Esto podría dar a la empresa un margen para ajustar precios sin temer una caída drástica en el volumen de ventas.
""")

print("\nAnálisis exploratorio completado. Revisa los gráficos generados en la carpeta.")

