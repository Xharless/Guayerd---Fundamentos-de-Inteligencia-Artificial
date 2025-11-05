
# El grafico de los clientes, ver las caracteristicas de los clientes 
# El grafico de los ingresos por categoria, ver por ejemplo si es almacen, cuales son los productos dentro de almacen que mas ingresos generan

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
try:
    df = pd.read_csv('../Clase 7/analisis_ventas_completo.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])
    print("Archivo 'analisis_ventas_completo.csv' cargado y preparado.")
except FileNotFoundError:
    print("Error: No se encontró 'analisis_ventas_completo.csv'.")
    print("Asegúrate de haber ejecutado los scripts de limpieza y unión primero.")
    exit()
print("\n--- Variables clave seleccionadas: 'categoria', 'ingreso_total', 'fecha', 'nombre_cliente' ---")

print("\nGenerando Visualización 1: Ingresos por Categoría...")
ingresos_categoria = df.groupby('categoria')['ingreso_total'].sum().sort_values(ascending=False)

plt.figure(figsize=(12, 7))
sns.barplot(x=ingresos_categoria.values, y=ingresos_categoria.index, palette='viridis_r')
plt.title('Ingresos Totales por Categoría de Producto', fontsize=16)
plt.xlabel('Ingresos Totales ($)', fontsize=12)
plt.ylabel('Categoría', fontsize=12)
plt.tight_layout()
plt.savefig('ingresos_por_categoria.png')
print("Gráfico guardado como 'ingresos_por_categoria.png'")
print("\nGenerando Visualización 2: Evolución de Ingresos Mensuales...")


df['mes'] = df['fecha'].dt.to_period('M')
ingresos_mensuales = df.groupby('mes')['ingreso_total'].sum()


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


print("\nGenerando Visualización 3: Top 10 Clientes...")


top_clientes = df.groupby('nombre_cliente')['ingreso_total'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 8))
sns.barplot(x=top_clientes.values, y=top_clientes.index, palette='plasma')
plt.title('Top 10 Clientes por Gasto Total', fontsize=16)
plt.xlabel('Gasto Total ($)', fontsize=12)
plt.ylabel('Nombre del Cliente', fontsize=12)
plt.tight_layout()
plt.savefig('top_10_clientes.png')
print("Gráfico guardado como 'top_10_clientes.png'")



print("\nAnálisis visual completado. Revisa los 3 gráficos generados en la carpeta.")

