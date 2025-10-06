

documentacion = {
    "Tema": "Control de stock y ventas",
    "Problematica": "No existe un mecanismo facil para poder relacionar las ventas del productos con el stock, lo que pude generar escasez de recursos o exceso de inventario.",
    "Solución": "Un programa que consulte las ventas de cada producto, detectando cuales son los que tienen menor stock y genere alertas sobre productos bajo de stock o productos en alta rotación que necesiten reposición urgente.",
    "Dataset de referencia": """
productos.xlsx:
    1. ID_Producto (int): valores unicos de cada producto (PK)
    2. nombre (str): nombres de cada producto
    3. categoria (str): categoria de cada producto
    4. stock_actual (int): stock actual que tiene el producto
    5. stock_minimo (str): nivel mínimo de stock definido por la empresa
    6. precio (int): precio de cada producto

ventas.xlsx:
    1. ID_venta (int): valores que representan a cada venta de un producto (PK)
    2. fecha (int): fecha de la venta
    3. ID_Producto (int): valor unico del producto (FK)
    4. cantidad (int): cantidad de productos vendidos
    5. ID_Cliente (int): identificador del cliente (FK)

clientes.xlsx:
    1. ID_cliente (int): valores unicos para cada cliente (PK)
    2. nombre (str): nombres de cada cliente
    3. email (str): correos electronicos de cada cliente
    4. ciudad (str): nombres de las ciudades de cada cliente
""",
    "Fuente y escala de los datasets": """
Fuente: Los datasets son simulados para fines educativos y fueron generados manualmente para representar un escenario típico de gestión de stock y ventas.
Escala: Cada archivo contiene aproximadamente 20-50 registros, cubriendo un mes de operaciones ficticias.
""",
    "Pasos del programa": """
1. Cargar los datasets de productos, ventas y clientes.
2. Relacionar las ventas con los productos usando el ID_Producto.
3. Calcular el stock restante de cada producto después de las ventas.
4. Comparar el stock actual con el stock mínimo definido.
5. Generar alertas para productos con stock bajo o alta rotación.
6. Mostrar o exportar el reporte de alertas.
""",
    "Pseudocódigo": """
Cargar productos desde productos.xlsx
Cargar ventas desde ventas.xlsx

Para cada producto en productos:
    Calcular ventas_totales = suma de cantidad vendida en ventas para ese producto
    stock_restante = stock_actual - ventas_totales
    Si stock_restante < stock_minimo:
        Agregar a lista de alertas (stock bajo)
    Si ventas_totales > umbral_alta_rotacion:
        Agregar a lista de alertas (alta rotación)

Mostrar lista de alertas
""",
    "Sugerencias y mejoras aplicadas con Copilot": """
- Se sugirió automatizar la generación de alertas usando comparaciones directas entre el stock actual y el stock mínimo.
- Se recomendó agregar un umbral para identificar productos de alta rotación.
- Copilot propuso estructurar el pseudocódigo para mayor claridad y eficiencia.
- Se mejoró la definición de los datasets, agregando tipos de datos y relaciones entre tablas.
"""
}

def mostrar_menu():
    print("\n--- Menú de Documentación ---")
    for i, key in enumerate(documentacion.keys(), 1):
        print(f"{i}. {key}")
    print("0. Salir")

def mostrar_seccion(opcion):
    keys = list(documentacion.keys())
    if 1 <= opcion <= len(keys):
        print(f"\n--- {keys[opcion-1]} ---")
        print(documentacion[keys[opcion-1]])
    else:
        print("Opción no válida.")

def main():
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Seleccione una sección para ver (0 para salir): "))
            if opcion == 0:
                print("¡Hasta luego!")
                break
            mostrar_seccion(opcion)
        except ValueError:
            print("Por favor, ingrese un número válido.")

if __name__ == "__main__":
    main()