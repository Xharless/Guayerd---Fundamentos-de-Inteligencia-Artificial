# Módulo 1: El proyecto debater

## Project Debater
¿Puede una IA ganar un debate con un experto humano sobre un tema complicado?

IBM Project Devater tendría que se capaz de hacer algo más que responder a preguntas en un lenguaje humano, tendría que tener la capacidad de escuchar una serie de argumentos cimpetitivos planteados por humanos y repsonder a ellos de forma inteligente.

## Pasos de un debate
* **Paso 1: Aprender y comprender el tema**
* **Paso 2: Crear una posición:** Desarrollar un discurso de apertura compuesto por breces fragmentos de texto pegados a partir del corpus, debe detallar su posicion sobre el tema del debate
* **Paso 3: Organizar sus pruebas** 
* **Paso 4: Responder a su oponente**

## Pasos del procesamiento de lenguaje natural
Comprender el lenguaje humano es complicado, incluso para personas que han crecido con él. Para entender el lenguaje hummano, las maquinas necesitan sistemas que los investigadores denominan **procesamiento del lenguaje natural (NLP)**

# Módulo 2: La IA procesa el lenguaje natural
## Segmentación de oraciones y señales en NLP
Los ordenadores funcionan mejor con datos estructurados, en los que todo esta perfectamente agrupado y etiquetado, pero en el lenguaje humano es cualquier cosa menos estructurado. Es muy dificil crear máquinas que puedan trabajar con el lenguaje humano.

## En NLP, las máquinas segmentan las oracioens y extraen significado de "señales" del lenguaje humano.
El lenguaje humano no está estructurado. Aunque se rige por reglas gramaticales, nuestra lengua expresa la información de muchas formas confusas, la información no estructurada es desordenada y dificil de entender. 

Para abordar el "desorden" de la información no estructurada, los ordenadores comienzan con una oración cada vez. Esto se denomina **segmentación de oraciones**, los ordenadores dividen la información en pequeños fragmentos de información, denominados **señales**(tokens), que se pueden clasificar individualmente. Una vez que las señales del texto se han clasificado en una estructura según su significado, NLP puede trabajar con ellos.

Una **Entidad** es un sustantivo que representa una persona, un lugar o una cosa. No es un adjetivo, un verbo ni otro artículo del discurso
* Yo, elefante, y pijama son entidades porque son sustantivos.
* Disparé, un, en y mi no son entidades porque no son sustantivos.

Una **relacion** es un grupo de dos o más entidades que tienen una fuerte conexión entre sí. Una vez que la IA ha clasificado las entidades y relaciones en el texto o en el habla, puede empezar a estructurar la informacion como paso previo para comprenderla.

Un **concepto** es algo implícito en una oración pero que no se dice realmente. Esto es más complicado porque implica emparejar ideas en lugar de las palabras específicas que aparecen en la frase

## Detección de emociones y análisis de opinión
La detección de emociones y el análisis de opinión no es lo mismo, aunque las emociones y las opiniones se refieren a sentimientos más que a hechos o acciones, distinguirlas puede ayudar a un sistema de IA a entender mejor una oración

La **detección de emociones** identifica distintos tipos de emociones humanas. Podemos entrenar la IA para clasificar las emociones. Identificar la señal emocional adecuada puede marcar una gran diferencia cuando un sistema de IA lee un mensaje en las redes sociales o en un chat de atención del cliente, donde las distintas emociones cambian considerablemente el sistema de una frase.

El **análisis de opinion** no es una emocion específica, al menos no como los expertos informaticos utilizan el termino. Es una medida de la intensidad de una emocion

## El problema de la clasificacion
El lenguaje humano está lleno de terminos ambiguos o con doble sentido. Esto se denomina un **problema de clasificacion**. La clasificación puede ser más dificil para un sistema de IA que identificar señales, ya que gran parte de la clasificacion depende del contexto en el que se encuentra la frase


# Módulo 3: NLP convierte señales en significado
## Estructura de un chatbot
* Cuando se hace una pregunta clara relacionada con el propósito del sitio web, como preguntar a un chatbot de compras “¿Cómo puedo obtener un reembolso?”, por lo general le da una respuesta relacionado con su pregunta.

* Cuando se hace una pregunta que no está clara o no está relacionada con el propósito del sitio web, como preguntarle al chatbot de compras “¿Tiene entradas para mi hermana?”, la respuesta será más bien del tipo “Lo siento, no he entendido su pregunta”.

Esto es porque el chatbot está programado para responder solo a determinadas preguntas sobre un tema concreto

## Un chatbot tiene un "frontend" y un "backend"
El frontend de un chatbot es el canal de mensajería. El frontend interactpua con la persona que hace preguntas, tanto escuchando como hablando. El backend de un chatbot es odnde tiene lugar el trabajo duro, desarrolla la lógica de la aplicacion y tiene memoria suficiente para recordar partes anteriores de una conversacion a medida que se desarrolla el dialogo

## El backend del chatbot
Los algoritmos de **clasificadores** pueden correlacioanr muchas formas distintas de formular una pregunta con un conjunto muy reducido de respuestas. Algunos chatbot de comercios minoristas responden a cientos de preguntas diferentes como solo 5 o 6 respuestas posibles. Las preguntas de los chatbots no pueden responder se envian a representantes humanos de antecion al cliente.

## Intenciones, entidades y diálogo
El objetivo del chatbot es identificar lo que se denomina entidades e intenciones, luego utilizar lo que ha encontrado para activar un dialogo
* **Intención:** Es un propósito: la razon por la cual un usuario contacta con le chatbot
* **Entodad:** Es un sustantivo: una persona, un lugar o un objeto. 
* **Dialogo:** Es un diagrama de flujo, una estructura de arbol IF/THEN que ilustra como respondra una maquina a las intenciones del usuario. Un dialogo es lo que responde la maquina despues de que un humano haga una pregunta. El dialogo representa cada una de las posibles palabras o frases que pyede introducir un usuario, la respuesta adecuada para el chatbot y las muchas posibles respuestas posteriores que puede dar el usuario y el software de chatbot condensa cada momento de la conversacion en un **nodo**. Un nodo contiene una declaracion del chatbot y una larga lista ampliable de posibles respuesta