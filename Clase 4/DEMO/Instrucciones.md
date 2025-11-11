# Instructivo de prompts para Copilot

Este documento contiene plantillas y ejemplos de prompts en español para usar con Copilot (o un asistente similar) cuando trabajes en el proyecto "Control de stock y ventas". Incluye prompts cortos y largos, un pequeño "contrato" que puedes pegar para que Copilot entienda el formato esperado, y ejemplos prácticos aplicados a `programa.py` y a los datasets.

## Reglas rápidas (antes de escribir un prompt)

- Sé claro y específico: indica el archivo a modificar, la función o bloque objetivo y la salida esperada.
- Proporciona contexto corto: copia 3-8 líneas relevantes del archivo si el prompt es sobre código existente.
- Define criterios de aceptación: qué condiciones deben cumplirse (tests, formato, validaciones).
- Indica el estilo: PEP 8, docstrings tipo Google, o comentarios en español.

---

### Mejoras recomendadas (pequeñas pero importantes)

Antes de generar la revisión, asegúrate de aplicar estas tres mejoras al prompt para evitar ambigüedades:

1. Cálculo de la puntuación global (0–100): para cada una de las cuatro categorías calcule una nota de 1 a 5. La puntuación global sobre 100 se obtiene como: (suma_de_las_4_notas / 20) * 100. Incluya el cálculo y muestre la tabla de conversión.

2. Qué hacer si faltan ejemplos de código: si no existen al menos 3 fragmentos de código relevantes, indique explícitamente cuáles archivos faltan o por qué no es posible extraer ejemplos, y proponga 3 ubicaciones concretas (archivo+función/líneas) donde sería útil añadir ejemplos.


# Instructivo de prompts para Copilot

Este documento contiene plantillas y ejemplos de prompts en español para usar con Copilot (o un asistente similar) cuando trabajes en el proyecto "Control de stock y ventas". Incluye prompts cortos y largos, un pequeño "contrato" que puedes pegar para que Copilot entienda el formato esperado, y ejemplos prácticos aplicados a `programa.py` y a los datasets.

## Reglas rápidas (antes de escribir un prompt)

- Sé claro y específico: indica el archivo a modificar, la función o bloque objetivo y la salida esperada.
- Proporciona contexto corto: copia 3-8 líneas relevantes del archivo si el prompt es sobre código existente.
- Define criterios de aceptación: qué condiciones deben cumplirse (tests, formato, validaciones).
- Indica el estilo: PEP 8, docstrings tipo Google, o comentarios en español.

---

## Plantillas de prompts

1) Prompt corto — modificación simple

"En `programa.py`, agrega una función `generar_metadatos(estructura)` que reciba el diccionario de estructura de columnas y muestre una tabla con columnas: 'Columna', 'Tipo', 'Escala'. Usa `tabulate` y añade docstring en español." 

2) Prompt largo — cambio no trivial con validaciones y excepciones

"En `programa.py`:

- Añade las constantes `ESTRUCTURA_PRODUCTOS`, `ESTRUCTURA_CLIENTES`, `ESTRUCTURA_VENTAS` con las definiciones de tipo y escala 
- Implementa una función `validar_dataframe(df, estructura)` que verifique que las columnas requeridas existen y que los tipos básicos coincidan (int, float, str, date). Debe devolver `True` o lanzar `ValueError` con mensaje claro si hay discrepancias.
- Envuelve la carga de archivos en `cargar_datos(path, estructura)` que maneje excepciones y devuelva un `DataFrame` ya tipado (con conversiones seguras). Documenta con docstrings en español.

Requisitos: mantener PEP8, usar `pandas`, `tabulate` opcional. Añade pruebas simples en el docstring con ejemplos de uso." 

3) Prompt para generar tests unitarios

"Crea un archivo `tests/test_validadores.py` con pruebas unitarias para `validar_int`, `validar_email` y `validar_dataframe` (usa pytest)." 

---

## Contrato (corto) para pegar al inicio de un prompt

Usa este bloque al principio de prompts largos para estandarizar la respuesta esperada:

"CONTRATO:
- Entregar solo el código o el parche solicitado (sin explicaciones largas).
- Incluir docstrings en español para funciones nuevas.
- Seguir PEP8 y no introducir dependencias innecesarias.
- Incluir ejemplos de uso o pruebas rápidas en docstrings.
FIN DEL CONTRATO"

---

## Ejemplos aplicados al proyecto (prompts listos para usar)

Ejemplo A — Generar metadatos automáticos:

"CONTRATO: ...FIN DEL CONTRATO\n
En `programa.py`, agrega la constante `ESTRUCTURA_PRODUCTOS` y una función `generar_metadatos(estructura)` que imprima la tabla de metadatos usando `tabulate`. Añade una opción en el menú principal para ver metadatos de `productos`." 

Ejemplo B — Validar y cargar archivos:

"CONTRATO: ...FIN DEL CONTRATO\n
Implementa `cargar_datos(path, estructura)` en `programa.py` que lea un Excel con `pandas.read_excel`, verifique columnas con `validar_dataframe` y convierta tipos básicos. Si falta una columna lanzar `ValueError` con mensaje: 'Falta columna {columna}'." 

Ejemplo C — Mejorar la interacción del menú:

"En `programa.py` refactoriza el menú para separar: 1) Documentación, 2) Datos, 3) Reportes. Cada opción debe ser una función. Mantén compatibilidad con la entrada por número actual." 

---

## Buenas prácticas al usar prompts con Copilot

- Proporciona siempre el archivo y la región de interés si el cambio debe ser localizado.
- Si pides refactorizar, pide además que mantenga la compatibilidad con la API actual (por ejemplo, el menú y la manera de llamar `mostrar_seccion`).
- Pide pruebas unitarias pequeñas junto con los cambios.
- Para cambios grandes, solicita un `diff` o un parche en vez de solo el código final.

---

## Plantillas de prompts de ejemplo 

- Plantilla: "Reescribe la función X en `ruta/archivo.py` para que devuelva Y y maneje errores Z. Incluye docstring y ejemplo de uso." 
- Plantilla: "Agrega validaciones de entrada en `ruta/archivo.py`: controlar tipos y rangos. Si falla, lanzar `ValueError` con mensaje explicativo." 

---

## Cómo iterar con Copilot (workflow recomendado)

1. Escribe un prompt corto para obtener una primera versión.
2. Revisa el código generado localmente (ejecuta pruebas o flake8). 
3. Solicita a Copilot correcciones específicas (p. ej. "Corrige esta función para manejar valores nulos").
4. Repite hasta cumplir criterios de aceptación.

---

## Ejemplo de prompt completo (lista para pegar)

"CONTRATO:\n- Entregar solo el parche solicitado.\n- Incluir docstrings en español.\n- Seguir PEP8.\nFIN DEL CONTRATO\n\nEn `programa.py`: agregar `ESTRUCTURA_PRODUCTOS` y `generar_metadatos(estructura)`. Añadir opción en el menú principal para mostrar metadatos. Usar `tabulate`." 

---

## Siguientes pasos sugeridos

- Quieres que aplique uno de estos prompts ahora en `programa.py` para generar código? Indica cuál (por ejemplo: "Aplicar Ejemplo A").
- ¿Prefieres que primero cree tests básicos para validadores antes de tocar código de producción? 

---

Fin del instructivo.
