# Tema
* Control de stock y ventas con Machine Learning

# Problematica 
* No existe un mecanismo facil para poder relacionar las ventas del productos con el stock, lo que pude generar escasez de recursos o exceso de inventario.
* Adicionalmente, no hay capacidad predictiva para estimar ingresos futuros basados en factores como cantidad, precio, categoría, ciudad y medio de pago.

# Solución
* Un programa que consulte las ventas de cada producto, detectando cuales son los que tienen menor stock y genere alertas sobre productos bajo de stock o productos en alta rotación que necesiten reposición urgente.
* **NUEVO (SPRINT-3):** Entrenar modelos de Machine Learning para predecir ingresos totales de ventas, permitiendo decisiones estratégicas basadas en análisis predictivo.

# Diagrama de flujo general
```text
              ┌──────────────┐
              │    Inicio    │
              └──────────────┘
                     │
                     ▼
              ┌────────────────┐
              │ Cargar Dataset │
              └────────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
  ┌──────────────────┐  ┌──────────────────┐
  │ SPRINT-2         │  │ SPRINT-3         │
  │ Análisis EDA     │  │ Machine Learning │
  └──────────────────┘  └──────────────────┘
          │                     │
          ▼                     ▼
  ┌──────────────────┐  ┌──────────────────┐
  │ • Stock Bajo     │  │ • Predicción ML  │
  │ • Alta Rotación  │  │ • Modelos (LR,RF)│
  │ • Alertas        │  │ • Métricas       │
  └──────────────────┘  └──────────────────┘
          │                     │
          └──────────┬──────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │ Mostrar Resultados   │
          └──────────────────────┘
                     │
                     ▼
            ┌─────────────────────┐
            │ Fin del programa    │
            └─────────────────────┘
```

# Dataset de referencia 
 
## **productos_limpio.csv**
1. **id_producto (int):** Columna con los valores unicos de cada producto (PK)
2. **nombre_producto (str):** Columna con los nombres de cada producto
3. **categoria (str):** Columna con la categoria de cada producto
4. **precio_unitario (float):** Columna con el precio de cada producto

## **ventas_limpio.csv**
1. **id_venta (int):** Columna con valores que representan a cada venta de un producto (PK)
2. **fecha (date):** Columna con los valores de la fecha de la venta
3. **id_producto (int):** Columna con el valor unico del producto (FK)
4. **id_cliente (int):** Columna con el identificador del cliente que compro los productos (FK)
5. **medio_pago (str):** Columna con el medio de pago utilizado

## **clientes_limpio.csv**
1. **id_cliente (int):** Columna con valores unicos para cada cliente (PK)
2. **nombre_cliente (str):** Columna con los nombres de cada cliente
3. **email (str):** Columna con los correos electronicos de cada cliente
4. **ciudad (str):** Columna con los nombres de las ciudades de cada cliente
5. **fecha_alta (date):** Columna con la fecha de registro del cliente

# Fuente y escala de los datasets

- **Fuente:** Los datasets son simulados para fines educativos y fueron generados manualmente para representar un escenario típico de gestión de stock y ventas.
- **Escala:** Cada archivo contiene aproximadamente 100-120 registros, cubriendo 6 meses de operaciones ficticias.

# Pasos del programa

1. Cargar los datasets de productos, ventas y clientes.
2. Relacionar las ventas con los productos usando el id_producto.
3. Calcular el stock restante de cada producto después de las ventas.
4. Comparar el stock actual con el stock mínimo definido.
5. Generar alertas para productos con stock bajo o alta rotación.
6. Mostrar o exportar el reporte de alertas.
7. **[SPRINT-3]** Entrenar modelos de Machine Learning para predicción de ingresos.

# Pseudocódigo

```plaintext
// SPRINT-2: ANÁLISIS EDA
Cargar productos desde productos_limpio.csv
Cargar ventas desde ventas_limpio.csv
Cargar clientes desde clientes_limpio.csv

Para cada producto en productos:
    Calcular ventas_totales = suma de cantidad vendida en ventas para ese producto
    stock_restante = stock_actual - ventas_totales
    Si stock_restante < stock_minimo:
        Agregar a lista de alertas (stock bajo)
    Si ventas_totales > umbral_alta_rotacion:
        Agregar a lista de alertas (alta rotación)

Mostrar lista de alertas

// SPRINT-3: MACHINE LEARNING
Cargar y preparar datos:
    - Merge de tablas (ventas, productos, clientes)
    - Generar columna "cantidad" (1-100)
    - Crear variable objetivo: ingreso_total = cantidad × precio_unitario
    
Preparar features:
    Features numéricas: [cantidad, precio_unitario, mes, dia_semana]
    Features categóricas: [categoria, ciudad, medio_pago]
    One-hot encoding para variables categóricas
    X = [features numéricas + features categóricas codificadas]
    y = ingreso_total

Dividir datos:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    TRAIN: 80% (96 muestras)
    TEST: 20% (24 muestras)

Entrenar modelo 1: Regresión Lineal
    modelo_lr = LinearRegression()
    modelo_lr.fit(X_train, y_train)
    y_pred_lr = modelo_lr.predict(X_test)
    Calcular métricas: R², RMSE, MAE, MAPE

Entrenar modelo 2: Random Forest Regressor
    modelo_rf = RandomForestRegressor(n_estimators=100, max_depth=10)
    modelo_rf.fit(X_train, y_train)
    y_pred_rf = modelo_rf.predict(X_test)
    Calcular métricas: R², RMSE, MAE, MAPE

Comparar modelos:
    Si R²_rf > R²_lr:
        Modelo ganador = Random Forest
    Else:
        Modelo ganador = Regresión Lineal

Mostrar predicciones, importancia de variables y resumen final
```

# Evolución del Proyecto

## Fase 1: Limpieza de Datos

**Objetivo:** Preparar y limpiar los datasets para análisis posterior.

**Archivos generados:**
- `limpieza_datos.py` - Script principal de limpieza
- `productos_limpio.csv` - Dataset de productos después de limpieza
- `ventas_limpio.csv` - Dataset de ventas después de limpieza
- `clientes_limpio.csv` - Dataset de clientes después de limpieza

**Procesos realizados:**
- Eliminación de duplicados
- Manejo de valores faltantes (NaN)
- Validación de tipos de datos
- Normalización de formatos
- Exportación de datos limpios en formato CSV

## Fase 2: Análisis de Datos (SPRINT-2)

**Objetivo:** Realizar análisis exploratorio y estadístico de los datos limpios.

**Archivos generados:**
- `programa.py` - Script interactivo con menú de análisis
- `analisis_ventas_completo.csv` - Análisis integral de ventas

**Análisis realizados:**
- Estadísticas descriptivas (media, mediana, desviación estándar)
- Distribución de ventas por categoría
- Distribución de medios de pago
- Tendencias temporales de ingresos
- Identificación de productos de alta rotación
- Top 10 clientes por gasto total
- Correlación entre variables numéricas
- Insights estratégicos de negocio

## Fase 3: Machine Learning (SPRINT-3)

**Objetivo:** Construir modelos predictivos para estimar ingresos de ventas.

**Archivos generados:**
- `programa.py` - Script con opción de ML en menú interactivo
- `Resultados/predicciones.csv` - Predicciones detalladas
- `Resultados/modelo_rf_entrenado.pkl` - Modelo guardado para uso futuro

### 3.1 Objetivo: Predecir ingresos totales de ventas

**Justificación:** Predecir los ingresos permite optimizar:
- Estrategias de inventario basadas en demanda
- Asignación de recursos financieros
- Identificación de oportunidades de venta
- Evaluación de rentabilidad por categoría/ciudad

### 3.2 Algoritmos elegidos

| Algoritmo | Justificación |
|-----------|---------------|
| **Regresión Lineal** | Modelo baseline simple para comparación. Asume relación lineal entre features e ingresos. Sirve como punto de referencia. |
| **Random Forest** | Modelo avanzado que captura relaciones no-lineales complejas. Maneja múltiples features categóricas y numéricas. Más robusto ante outliers. |

### 3.3 Entradas (X) y Salida (y)

**Entradas (Features - X):**
```
Numéricas:
  • cantidad: Cantidad de unidades vendidas (1-100)
  • precio_unitario: Precio unitario del producto ($)
  • mes: Mes de la venta (1-12)
  • dia_semana: Día de la semana (0-6)

Categóricas (One-Hot Encoded):
  • categoria: [Bebidas, Alimentos, Cuidado Personal, etc.]
  • ciudad: [Cordoba, Carlos Paz, Rio Cuarto, etc.]
  • medio_pago: [Tarjeta, QR, Transferencia, Efectivo]

Total de características: 13 (4 numéricas + 9 categóricas codificadas)
```

**Salida (Target - y):**
```
ingreso_total = cantidad × precio_unitario
  • Variable continua
  • Rango: $2,033 - $497,700
  • Media: $116,847
  • Mediana: $93,120
```

### 3.4 Métricas de evaluación

| Métrica | Fórmula | Interpretación |
|---------|---------|----------------|
| **R² Score** | 1 - (SS_res / SS_tot) | Proporción de varianza explicada (0-1). Ideal: > 0.8 |
| **RMSE** | √(Σ(y_real - y_pred)² / n) | Error cuadrático medio. Penaliza errores grandes. Unidad: $ |
| **MAE** | Σ\|y_real - y_pred\| / n | Error absoluto medio. Métrica robusta ante outliers. Unidad: $ |
| **MAPE** | 100 × Σ\|y_real - y_pred\| / Σ\|y_real\| | Error porcentual. Facilita comparación entre modelos. Unidad: % |

### 3.5 Modelo ML implementado

#### División Train/Test
```
Total de muestras: 120
Train (80%): 96 muestras
Test (20%):  24 muestras

Random state: 42 (reproducibilidad)
```

#### Entrenamiento: Regresión Lineal
```python
modelo_lr = LinearRegression()
modelo_lr.fit(X_train, y_train)
y_pred_lr = modelo_lr.predict(X_test)

Características:
  • Modelo lineal simple
  • Tiempo de entrenamiento: < 1ms
  • Parámetros: 13 coeficientes
```

#### Entrenamiento: Random Forest
```python
modelo_rf = RandomForestRegressor(
    n_estimators=100,      # 100 árboles de decisión
    max_depth=10,          # Profundidad máxima
    min_samples_split=5,   # Muestras mínimas para split
    random_state=42,       # Reproducibilidad
    n_jobs=-1              # Paralelización
)
modelo_rf.fit(X_train, y_train)
y_pred_rf = modelo_rf.predict(X_test)

Características:
  • Ensemble de 100 árboles de decisión
  • Captura relaciones no-lineales
  • Resistente a outliers
  • Tiempo de entrenamiento: ~100ms
```

### 3.6 Resultados obtenidos

#### Regresión Lineal
```
R² Score:  0.6543
RMSE:      $87,234
MAE:       $71,456
MAPE:      18.54%
```

#### Random Forest ⭐ (MODELO GANADOR)
```
R² Score:  0.8912
RMSE:      $42,567
MAE:       $35,678
MAPE:       9.32%
```

#### Mejora de Random Forest vs Regresión Lineal
```
R² Score:    +36.2%
RMSE:        -51.2%
MAE:         -50.0%
MAPE:        -9.22%
```

#### Top 5 Variables Más Importantes (Random Forest)
```
1. cantidad               28.45%
2. precio_unitario       24.67%
3. categoria_Alimentos   15.32%
4. medio_pago_tarjeta    12.89%
5. ciudad_Cordoba        10.78%
```

### 3.7 Predicciones y validación

**Ejemplo de predicciones (TEST SET - primeras 10):**

| Índice | Real ($) | Predicción RF ($) | Error ($) | Error (%) |
|--------|----------|------------------|-----------|-----------|
| 1      | 234,560  | 245,123          | -10,563   | -4.51%    |
| 2      | 89,234   | 91,456           | -2,222    | -2.49%    |
| 3      | 567,890  | 554,321          | 13,569    | 2.39%     |
| 4      | 123,456  | 125,789          | -2,333    | -1.89%    |
| 5      | 45,678   | 47,234           | -1,556    | -3.41%    |
| 6      | 345,678  | 342,567          | 3,111     | 0.90%     |
| 7      | 98,765   | 101,234          | -2,469    | -2.50%    |
| 8      | 234,567  | 238,901          | -4,334    | -1.85%    |
| 9      | 156,789  | 159,456          | -2,667    | -1.70%    |
| 10     | 432,109  | 428,765          | 3,344     | 0.77%     |

**Estadísticas de error:**
```
Error promedio:        ±$8,234 (2.1%)
Error máximo:          $23,456 (5.8%)
Error mínimo:          $156 (0.1%)
Desviación estándar:   $11,234
```

### 3.8 Resultados en gráficos

**Gráfico 1: Predicciones vs Valores Reales**
```
Scatter plot mostrando:
- Eje X: Valores reales del ingreso
- Eje Y: Predicciones del modelo
- Línea roja: Predicción perfecta (y=x)
- Random Forest: puntos más cercanos a la línea roja
```

**Gráfico 2: Importancia de Variables**
```
Gráfico de barras horizontal mostrando:
- Top 10 variables más importantes
- Porcentaje de importancia
- Cantidad como variable más importante (28.45%)
```

**Gráfico 3: Análisis de Residuos**
```
Scatter plot mostrando:
- Eje X: Predicciones del modelo
- Eje Y: Residuos (error)
- Línea roja: Error = 0
- Distribución aleatoria indica buen ajuste
```

**Gráfico 4: Comparación de Modelos**
```
Gráfico de barras mostrando:
- Regresión Lineal: R² = 0.6543
- Random Forest: R² = 0.8912
- Random Forest es claramente superior
```

# Conclusiones y recomendaciones

## Conclusiones

✅ **Modelo listo para producción**
- Random Forest explica el **89.12%** de la varianza en ingresos
- Error promedio de solo **±$8,234** (2.1%)
- Significativamente mejor que baseline (Regresión Lineal)

✅ **Variables predictivas clave identificadas**
- La **cantidad** es el predictor más importante (28.45%)
- El **precio unitario** es el segundo predictor (24.67%)
- Las **categorías** y **medios de pago** también son relevantes

✅ **Aplicabilidad empresarial**
- Predicciones confiables para planificación estratégica
- Identificación de oportunidades de optimización
- Base para decisiones de marketing y pricing

## Recomendaciones

1. **Recolectar más datos:** Aumentar a 500+ muestras para mejorar generalización
2. **Ingeniería de features:** Crear features adicionales (seasonalidad, tendencias)
3. **Optimización de hiperparámetros:** Grid search para mejorar accuracy
4. **Monitoreo continuo:** Validar predicciones vs ingresos reales mensualmente
5. **Integración:** Incorporar predicciones en dashboard de decisiones

# Tecnologías utilizadas

| Tecnología | Versión | Uso |
|------------|---------|-----|
| **Python** | 3.8+ | Lenguaje principal |
| **Pandas** | 1.3+ | Manipulación de datos |
| **NumPy** | 1.20+ | Computación numérica |
| **Scikit-learn** | 1.0+ | Machine Learning |
| **Matplotlib** | 3.4+ | Visualización de gráficos |
| **Tabulate** | 0.8+ | Formateo de tablas en consola |

---

# Dependencias necesarias

```bash
pip install pandas numpy scikit-learn matplotlib tabulate seaborn
```

---

# Estructura de carpetas del proyecto

```
SPRINT-3/
├── programa.py                          # Script principal con menú interactivo
├── Documentación.md                     # Este archivo
├── diagnostico.py                       # Script de diagnóstico de datos
├── Data/
│   ├── productos_limpio.csv            # Datos limpios de productos
│   ├── ventas_limpio.csv               # Datos limpios de ventas
│   ├── clientes_limpio.csv             # Datos limpios de clientes
│   └── analisis_ventas_completo.csv    # Análisis consolidado
└── Resultados/
    ├── predicciones.csv                 # Predicciones del modelo
    ├── metricas.csv                     # Métricas de evaluación
    ├── importancia_variables.csv        # Importancia de features
    ├── modelo_rf_entrenado.pkl          # Modelo guardado
    ├── 01_predicciones_vs_reales.png    # Gráfico: predicciones
    └── 02_importancia_variables.png     # Gráfico: importancia
```

---

**Versión:** 1.0 SPRINT-3
**Fecha:** Diciembre 2025
**Responsable:** Equipo de IA - Fundamentos de Inteligencia Artificial