# Documentación de archivos de datos

---

## **cliente.xlsx**
1. **id_cliente (int):** Columna con valores unicos para cada cliente (PK)
2. **nombre_cliente (str):** Columna con los nombres de cada cliente
3. **email (str):** Columna con los correos electronicos de cada cliente
4. **ciudad (str):** Columna con los nombres de las ciudades de cada cliente
5. **fecha_alta (str):** Columna con la fecha

---
## **detalle_ventas.xlsx**
1. **id_venta (int):** Columna con valores que representan a cada venta de un producto (FK)
2. **id_producto (int):** Columna con los valores unicos de cada producto (FK)
3. **nombre_producto (str):** Columna con nombres de cada producto
4. **cantidad (int):** Columna con la cantidad de productos 
5. **precio_unitario (str):** Precio unitario del producto
6. **importe(int):** Valor de la multiplicación entre la cantidad por el precio

---
## **ventas.xlsx**
1. **id_venta (int):** Columna con valores que representan a cada venta de un producto (PK)
2. **fecha (int):** Columna con los valores de la fecha de la venta
3. **id_cliente (int):** Columna con el id del cliente que hizo la compra (FK)
4. **email (str):** Columna con los correos electronicos de cada cliente
5. **medio_pago (str):** Tipo de pago que realizo el cliente

---
## **productos.xlsx**
1. **id_producto (int):** Columna con los valores unicos de cada producto (FK)
2. **nombre_producto (str):** Columna con el nombre del producto
3. **categoria (str):** Columna con la categoria de cada producto
4. **precio_unitario (int):** Precio de cada producto

