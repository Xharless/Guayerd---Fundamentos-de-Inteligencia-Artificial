# Tema
* Control de stock y ventas

# Problematica 
* No existe un mecanismo facil para poder relacionar las ventas del productos con el stock, lo que pude generar escasez de recursos o exceso de inventario.

# Solución
* Un programa que consulte las ventas de cada producto, detectando cuales son los que tienen menor stock y genere alertas sobre productos bajo de stock o productos en alta rotación que necesiten reposición urgente.

# Diagrama de flujo
![alt text](<Diagrama de flujo.jpg>)

# Dataset de referencia 
 
## **productos.xlsx**
1. **ID_Producto (int):** Columna con los valores unicos de cada producto (PK)
2. **nombre (str):** Columna con los nombres de cada producto
3. **categoria (str):** Columna con la categoria de cada producto
4. **stock_actual (int):** Columna con el stock actual que tiene el producto
5. **stock_minimo (str):** Columna con el nivel mínimo de stock definido por la empresa, si el stock actual es menor a este, lanza una alerta
6. **precio (int):** Columna con el precio de cada producto


## **ventas.xlsx**
1. **ID_venta (int):** Columna con valores que representan a cada venta de un producto (PK)
2. **fecha (int):** Columna con los valores de la fecha de la venta
3. **ID_Producto (int):** Columna con el valor unico del producto (FK)
4. **cantidad (int):** Columna con la cantidad de productos que se están vendiendo
5. **ID_Cliente (int):** Columna con el identificador del cliente que compro los productos (FK)


## **clientes.xlsx**
1. **ID_cliente (int):** Columna con valores unicos para cada cliente (PK)
2. **nombre (str):** Columna con los nombres de cada cliente
3. **email (str):** Columna con los correos electronicos de cada cliente
4. **ciudad (str):** Columna con los nombres de las ciudades de cada cliente

# Fuente y escala de los datasets

- **Fuente:** Los datasets son simulados para fines educativos y fueron generados manualmente para representar un escenario típico de gestión de stock y ventas.
- **Escala:** Cada archivo contiene aproximadamente 20-50 registros, cubriendo un mes de operaciones ficticias.

# Pasos del programa

1. Cargar los datasets de productos, ventas y clientes.
2. Relacionar las ventas con los productos usando el ID_Producto.
3. Calcular el stock restante de cada producto después de las ventas.
4. Comparar el stock actual con el stock mínimo definido.
5. Generar alertas para productos con stock bajo o alta rotación.
6. Mostrar o exportar el reporte de alertas.

# Pseudocódigo

```plaintext
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
```

# Sugerencias y mejoras aplicadas con Copilot

- Se sugirió automatizar la generación de alertas usando comparaciones directas entre el stock actual y el stock mínimo.
- Se recomendó agregar un umbral para identificar productos de alta rotación.
- Copilot propuso estructurar el pseudocódigo para mayor claridad y eficiencia.
- Se mejoró la definición de los datasets, agregando tipos de datos y relaciones entre tablas.

