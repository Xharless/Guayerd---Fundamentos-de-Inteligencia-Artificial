# 📊 SPRINT-4: INTEGRACION POWERBI

## 🎯 Objetivo General
Validar el modelo dimensional, crear columnas calculadas, definir medidas DAX, estructurar jerarquías y diseñar KPIs para visualización en Power BI.

---

## 1️⃣ VALIDACION DE RELACIONES Y CARDINALIDAD

### Relación 1: FACT_VENTAS → DIM_CLIENTES
- **Tipo:** Muchos-a-Uno (N:1)
- **Foreign Key:** FACT_VENTAS.ID_Cliente
- **Primary Key:** DIM_CLIENTES.ID_Cliente
- **Dirección de filtro:** DIM_CLIENTES → FACT_VENTAS
- **Validación:** ✓ Integridad referencial correcta

### Relación 2: FACT_VENTAS → DIM_PRODUCTOS
- **Tipo:** Muchos-a-Uno (N:1)
- **Foreign Key:** FACT_VENTAS.ID_Producto
- **Primary Key:** DIM_PRODUCTOS.ID_Producto
- **Dirección de filtro:** DIM_PRODUCTOS → FACT_VENTAS
- **Validación:** ✓ Integridad referencial correcta

### Relación 3: FACT_VENTAS → DIM_TIEMPO
- **Tipo:** Muchos-a-Uno (N:1)
- **Foreign Key:** FACT_VENTAS.ID_Fecha
- **Primary Key:** DIM_TIEMPO.ID_Fecha
- **Dirección de filtro:** DIM_TIEMPO → FACT_VENTAS
- **Validación:** ✓ Integridad referencial correcta

---

## 2️⃣ COLUMNAS CALCULADAS

### Columna 1: Ingreso_Total
```
Fórmula: = Cantidad × Precio_Unitario
Tipo de dato: Moneda
Ubicación: FACT_VENTAS
Propósito: Cálculo de ingresos por venta
```

### Columna 2: Margen_Ganancia
```
Fórmula: = Ingreso_Total × 30%
Tipo de dato: Moneda
Ubicación: FACT_VENTAS
Propósito: Cálculo de ganancia bruta
Nota: Margen fijo del 30%
```

### Columna 3: Costo_Total
```
Fórmula: = Ingreso_Total - Margen_Ganancia
Tipo de dato: Moneda
Ubicación: FACT_VENTAS
Propósito: Cálculo del costo de venta
```

### Columna 4: Tipo_Venta
```
Fórmula: = 
  IF Ingreso_Total < $50,000 THEN "Pequeña"
  ELSE IF Ingreso_Total < $150,000 THEN "Mediana"
  ELSE IF Ingreso_Total < $300,000 THEN "Grande"
  ELSE "Premium"
  
Tipo de dato: Texto
Ubicación: FACT_VENTAS
Propósito: Categorización de ventas por monto
```

---

## 3️⃣ MEDIDAS DAX (6 MÉTRICAS)

### Medida 1: Total_Ventas
```dax
Total_Ventas = SUM(FACT_VENTAS[Ingreso_Total])
```
- **Tipo:** SUM
- **Descripción:** Suma total de ingresos
- **Formato:** Moneda ($)
- **Uso:** KPI principal, cards, gráficos de tendencias

### Medida 2: Cantidad_Transacciones
```dax
Cantidad_Transacciones = COUNTA(FACT_VENTAS[ID_Venta])
```
- **Tipo:** COUNT
- **Descripción:** Número total de ventas realizadas
- **Formato:** Número entero
- **Uso:** Análisis de volumen, cards

### Medida 3: Ticket_Promedio
```dax
Ticket_Promedio = [Total_Ventas] / [Cantidad_Transacciones]
```
- **Tipo:** DIVIDE
- **Descripción:** Valor promedio de cada transacción
- **Formato:** Moneda ($)
- **Uso:** KPI, análisis de comportamiento de compra

### Medida 4: Total_Margen
```dax
Total_Margen = SUM(FACT_VENTAS[Margen_Ganancia])
```
- **Tipo:** SUM
- **Descripción:** Ganancia total acumulada
- **Formato:** Moneda ($)
- **Uso:** KPI de rentabilidad, análisis financiero

### Medida 5: Margen_Porcentaje
```dax
Margen_Porcentaje = [Total_Margen] / [Total_Ventas]
```
- **Tipo:** DIVIDE
- **Descripción:** Margen como porcentaje de ventas
- **Formato:** Porcentaje
- **Uso:** KPI, análisis de rentabilidad relativa

### Medida 6: Cantidad_Clientes_Unicos
```dax
Cantidad_Clientes_Unicos = DISTINCTCOUNT(FACT_VENTAS[ID_Cliente])
```
- **Tipo:** DISTINCTCOUNT
- **Descripción:** Número de clientes distintos que compraron
- **Formato:** Número entero
- **Uso:** Análisis de base de clientes, cards

---

## 4️⃣ JERARQUIAS

### Jerarquía 1: Temporal (DIM_TIEMPO)
```
Nivel 1: Año
  └─ Nivel 2: Trimestre
      └─ Nivel 3: Mes
          └─ Nivel 4: Semana
              └─ Nivel 5: Día
```
**Uso:** Análisis de tendencias temporales, drill-down mensual

### Jerarquía 2: Productos (DIM_PRODUCTOS)
```
Nivel 1: Categoría
  └─ Nivel 2: Subcategoría
      └─ Nivel 3: Nombre_Producto
```
**Uso:** Análisis por línea de productos, comparativas de categorías

### Jerarquía 3: Clientes (DIM_CLIENTES)
```
Nivel 1: País
  └─ Nivel 2: Ciudad
      └─ Nivel 3: Nombre_Cliente
```
**Uso:** Análisis geográfico, segmentación por región

### Jerarquía 4: Ventas (FACT_VENTAS)
```
Nivel 1: Tipo_Venta
  └─ Nivel 2: Medio_Pago
```
**Uso:** Segmentación de ventas, análisis de canales de pago

---

## 5️⃣ KPIS (3 INDICADORES CLAVE)

### KPI 1: Crecimiento de Ventas Mensual
```
Nombre:      Crecimiento de Ventas
Métrica:     Total_Ventas
Objetivo:    $500,000 mensuales
Meta:        +15% mes a mes
Fórmula:     [Total_Ventas] vs [Total_Ventas_Mes_Anterior]

Semáforo:
  • Verde:    Total_Ventas > $500,000
  • Amarillo: Total_Ventas entre $400,000 - $500,000
  • Rojo:     Total_Ventas < $400,000

Visualización: Gauge + Card + Trend Line
Frecuencia:    Mensual
```

### KPI 2: Margen de Ganancia
```
Nombre:      Margen de Ganancia
Métrica:     Margen_Porcentaje
Objetivo:    30% de margen
Meta:        Mantener > 28%
Fórmula:     [Margen_Porcentaje] = [Total_Margen] / [Total_Ventas]

Semáforo:
  • Verde:    Margen_Porcentaje > 30%
  • Amarillo: Margen_Porcentaje entre 28% - 30%
  • Rojo:     Margen_Porcentaje < 28%

Visualización: Gauge + Card + Area Chart
Frecuencia:    Mensual
```

### KPI 3: Ticket Promedio
```
Nombre:      Ticket Promedio
Métrica:     Ticket_Promedio
Objetivo:    $120,000 por transacción
Meta:        Aumentar valor promedio
Fórmula:     [Ticket_Promedio] = [Total_Ventas] / [Cantidad_Transacciones]

Semáforo:
  • Verde:    Ticket_Promedio > $120,000
  • Amarillo: Ticket_Promedio entre $100,000 - $120,000
  • Rojo:     Ticket_Promedio < $100,000

Visualización: Gauge + Card + Column Chart
Frecuencia:    Mensual
```

---

## 6️⃣ DIRECCION DE FILTROS (CROSS-FILTER)

| Relación | Dirección | Justificación |
|----------|-----------|---------------|
| DIM_TIEMPO → FACT_VENTAS | Una dirección | El tiempo filtra ventas (análisis temporal) |
| DIM_PRODUCTOS → FACT_VENTAS | Una dirección | Los productos filtran ventas (análisis por categoría) |
| DIM_CLIENTES → FACT_VENTAS | Una dirección | Los clientes filtran sus ventas |
| FACT_VENTAS → Dimensiones | Bidireccional (opcional) | Para análisis de clientes sin ventas |

---

## 7️⃣ COLUMNAS INNECESARIAS IDENTIFICADAS

**Análisis realizado:**
- ✓ Todas las columnas en DIM_CLIENTES son necesarias (ID, nombre, email, ciudad, fecha_alta)
- ✓ Todas las columnas en DIM_PRODUCTOS son necesarias (ID, nombre, categoría, precio)
- ✓ Todas las columnas en DIM_TIEMPO son necesarias (ID, fecha, año, trimestre, mes, semana, día)
- ✓ Todas las columnas en FACT_VENTAS son necesarias (IDs foráneos, cantidad, precio, medio_pago)

**Conclusión:** No hay columnas redundantes que eliminar.

---

## 8️⃣ PASOS PARA IMPLEMENTAR EN POWER BI DESKTOP

### Paso 1: Importar datos
1. Power BI Desktop → Get Data → CSV
2. Seleccionar archivos CSV de PowerBI_Data/
3. Cargar DIM_CLIENTES, DIM_PRODUCTOS, DIM_TIEMPO, FACT_VENTAS

### Paso 2: Crear relaciones
1. Ir a Model view
2. Crear relación: FACT_VENTAS.ID_Cliente → DIM_CLIENTES.ID_Cliente
3. Crear relación: FACT_VENTAS.ID_Producto → DIM_PRODUCTOS.ID_Producto
4. Crear relación: FACT_VENTAS.ID_Fecha → DIM_TIEMPO.ID_Fecha
5. Verificar cardinalidad (N:1) y dirección de filtros

### Paso 3: Agregar columnas calculadas
1. New Column en FACT_VENTAS
2. Copiar fórmulas de columnas calculadas (ver sección 2)

### Paso 4: Crear tabla de medidas
1. New Table (vacía)
2. Nombre: "Medidas"
3. Agregar todas las medidas DAX (ver sección 3)

### Paso 5: Crear jerarquías
1. Right-click en columna → New Hierarchy
2. Crear 4 jerarquías (ver sección 4)

### Paso 6: Diseñar dashboard
1. Report view
2. Agregar Cards para Total_Ventas, Ticket_Promedio
3. Agregar Gauges para KPIs
4. Agregar Clustered Column Chart para tendencias
5. Agregar Slicers para filtros

---

## ✅ CHECKLIST FINAL

- [x] Relaciones validadas y cardinalidad correcta
- [x] Integridad referencial verificada
- [x] Dirección de filtros configurada
- [x] 4 columnas calculadas creadas
- [x] 6 medidas DAX documentadas
- [x] 4 jerarquías estructuradas
- [x] 3 KPIs diseñados con semáforo
- [x] Columnas innecesarias identificadas (ninguna)
- [x] Modelo listo para Power BI

---

**Versión:** 1.0 SPRINT-4
**Fecha:** Diciembre 2025
**Estado:** Listo para Power BI Desktop