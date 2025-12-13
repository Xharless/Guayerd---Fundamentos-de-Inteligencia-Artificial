# Módulo 1: ¿Cómo aprenden las máquinas?

## Las máquinas aprenden de tres formas generales
La IA utiliza algoritmos para predecir y clasificar puntos de datos recopilados tanto en BD como de fenómenos naturales. Pero los algoritmos tienen 3 formas generales en las que pueden aprender de estos datos para obtener mejores resultados y proporcionar mejores predicciones: 
* Aprendizaje supervisado
* Aprendizaje no supervisado
* Aprendizaje de refuerzo

## Aprendizaje supervisado
Los humanos dan a un sistema de IA lo que se llaman **datos estructurados**. Se trata de un conjunto de datos y cifras organizados en categorías ordenadas y etiquetadas, de la misma forma en que podría poner información meteorológica en una tabla.

Los datos estructurados también pueden tomar la forma de imágenes. 

## Aprendizaje no supervisado
Este aprendizaje entrena una máquina con datos no etiquetados, como el texto de un libro, esto es más dificil porque el sistema no puede hacer predicciones hasta que haya estructurado los propios datos. Por ejemplo, un sistema puede recibir muchos artículos sobre diferentes tipos de plantas y formar sus propias conclusiones sobre sus atributos. Cuando el sistema ingiere texto nuevo que describe una planta. la identifica y le otorga un valor de confianza

## Aprendizaje de refuerzo
La maquina no recibe información específica que ingerir. Aprende mediante el sistema de ensayo y error. Los algoritmos de la máquina son recompensados cuando realiza una acción correcta y penalizados cuando no es así

## ¿Cómo aprenden las máquinas?
**El aprendizaje automático clásico** y los miembros de un grupo de tecnologías llamado **ecosistema del aprendizaje profundo**. Estudiar estas dos tecnologias de aprendizaje automatico es como mirar bajo el capó de dos autos y ver que tipo de motor tienen. 

# Módulo 2: Aprendizaje automático clásico

## Aprendizaje automático clásico
Los sistemas de IA aprendían ingiriendo datos y mejorando en el reconocimiento de patrones. Los sistemas de IA podían predecir cosas como la distancia entre puntos o la intensidad de los valores. 

El aprendizaje automático clásico utiliza un pequeño número de algoritmos en una disposición relativamente sencilla. A veces, los algoritmos de aprendizaje automático son binarios, lo que significa que solo generan uno de dos valores. Los resultados binarios típicos pueden ser 1 o un 0, un SI o un NO, y un VERDADERO o un FALSO

Otros algoritmos del aprendizaje clásico son más complicados. Por ejemplo, su resultado podría representarse como una posición en un gráfico multidimensional en lugar de “este punto” o “aquel punto”. Estos son tres algoritmos típicos que se utilizan en la informática clásica:

* Árbol de decisión
* Regresión lineal
* Regresión logística

## Árbol de decisión
Es un algoritmo de aprendizaje supervisado. Funciona como un diagrama de flujo. Un diagrama de flujo es como un arbol de decision invertido. 

## Regresión lineal
Es otro tipo de algoritmo. Se refiere a datos que pueden representarse gráficamente com una línea recta.

## Regresión logistica
En algunas situaciones, una relacion no se desarrolla en linea recta. A veces, un sistema utiliza valores que requieren un tipo de resultado especifico y limitado, como algo entre 0 y 1. En esta situación, un grafico puede formar lo que se denomina una función sigmoidea o una curva en forma de S. 

## Comparación entre la regresión lineal y logística

Las regresiones lineal y logística resultan útiles en los siguientes casos:

* Una regresión lineal responde a una pregunta como “Si esto aumenta en X, ¿cuánto aumentará Y?”.
* Una regresión logística responde a una pregunta del tipo “Si esto aumenta en X, ¿el valor de Y se acercará más a 0 o a 1?”.

# Modulo 3: El ecosistema del aprendizaje profundo

## Inspirado en el cerebro humano
Hoy en día, el aprendizaje automático ha evolucionado hasta convertirse en una colección de potentes aplicaciones denominadas ecosistema del aprendizaje profundo. La base de muchas aplicaciones se llama red neuronal. Una red neuronal utiliza circuitos electrónicos inspirados en la forma en que se comunican las neuronas en el cerebro humano.

En una red neuronal, un componente llamado perceptrón actúa como el equivalente de una sola neurona. Un perceptrón tiene una capa de entrada, una o más capas ocultas y una capa de salida. Una señal entra en la capa de entrada y las capas ocultas ejecutan algoritmos sobre la señal. Luego, el resultado se pasa a la capa de salida.

Las capas ocultas de una red neuronal se asemejan, como grupo, al largo cuerpo celular que conecta las dendritas con los axones dentro de una célula del cerebro humano. Esas capas ocultas contienen nodos. Cada nodo ejecuta un algoritmo y bits de código adicional para probar y ajustar su resultado. Cuando el valor alcanza un determinado umbral, el nodo se “activa”.

## Una ruta por una red neuronal 
El funcionamiento de una red neuronal es pura matemática. La red no “piensa”; calcula. Pero utiliza esos cálculos para crear un resultado que los humanos puedan interpretar como una respuesta o una recomendación.

## El aprendizaje automático suele ser ensayo y error 
En las lecciones anteriores de este curso se ha explicado cómo una red neuronal toma decisiones basándose en lo que aprende. Pero puede que aún se pregunte cómo empieza a aprender una red neuronal. La respuesta es: ajustándose continuamente, en un proceso que los humanos denominan ensayo y error.

Una vez que una red neuronal ha ingerido o ya ha aprendido cierta cantidad de datos, los almacena en su “cuerpo de información”, llamado corpus. Para aprender, la red neuronal compara constantemente los nuevos datos o los resultados de sus cálculos con su corpus. Si la red determina que los nuevos datos o resultados no coinciden con los patrones que ya ha establecido, los modiﬁca para conseguir un resultado mejor. 

## El aprendizaje automático hace muchas conjeturas
El aprendizaje automático utiliza su enorme velocidad de cálculo para hacer muchas conjeturas que lo acercan cada vez más a una respuesta. Hace su primera conjetura al azar, establece esa conjetura como variable y luego comprueba la precisión de la conjetura con los datos antiguos y nuevos. Luego realiza un ajuste en la variable y vuelve a intentarlo.

En muchas aplicaciones modernas de la IA, los datos no estructurados implicados son lo suficientemente complejos como para abrumar incluso a un simple perceptrón, como por ejemplo, decidir si pedir pizza en una lección anterior. Así pues, un perceptrón requiere más capacidad mental en forma de aprendizaje profundo. El aprendizaje profundo se basa en múltiples capas de nodos (incluso múltiples grupos de perceptrones con múltiples capas de nodos) para terminar el trabajo en un tiempo razonable.

## De los perceptrones al aprendizaje profundo
En una lección anterior, Marc ha pedido una pizza utilizando un perceptrón en el que una capa oculta de nodos ha hecho la mayor parte del trabajo. Pero los sistemas avanzados de IA utilizan muchas capas ocultas cuyos algoritmos transmiten los resultados de cálculos sofisticados. Esto se llama red neuronal profunda (DNN). Las capas de DNN se pueden organizar en grupos o en bloques elaborados de grupos para obtener mayor potencia. Las DNN pueden incluso duplicarse en equipos competidores que juzgan y aprenden de los errores de los demás, sin intervención humana. Esto crea un potente aprendizaje de refuerzo.

# Módulo 4: IA generativa 

## ¿Qué es la IA generativa?
La IA generativa es un tipo de inteligencia artificial que crea contenido nuevo y original que nunca nadie ha visto anteriormente. Los modelos de IA generativa son un tipo de sistema de IA de aprendizaje profundo que utiliza algoritmos para generar contenido a partir de una solicitud que se ha presentado, de ahí el nombre de IA generativa. 

Entonces, lo que distingue la IA generativa de otros sistemas de IA es su capacidad para generar contenido nuevo y que se considera creativo, como imágenes, vídeos, música, datos sintéticos, ensayos, respuestas a preguntas y más.

## ¿Cómo funciona la IA generativa?
Este es el proceso general de la IA generativa. 
1. Primero, una persona alimenta a la IA con una gran cantidad de datos. Datos que podrían ser cualquier cosa, desde imágenes y sonidos hasta texto y números.

2. A continuación, la IA analiza estos datos, buscando patrones y relaciones entre las diferentes piezas de información. La red neuronal se entrena sobre la base de un conjunto de datos con ejemplos del tipo de resultado que se pretende generar, como imágenes o texto. Durante el proceso entrenamiento, la red neuronal aprende a identificar patrones y relaciones en los datos de entrada y utilizarlos para generar nuevos resultados que sean similares, pero no idénticos, a los ejemplos con los que fue entrenado.

3. Luego, la IA usa lo que ha aprendido para crear algo nuevo. La red neuronal genera nuevos resultados especificando un valor inicial aleatorio. El valor inicial sirve como punto de inicio para el proceso de generación. La red neuronal procesa el valor inicial y genera nuevos resultados que se basan en los patrones y relaciones que ha aprendido durante el entrenamiento. Por ejemplo, si alguien suministró a la IA una serie de imágenes de perros, podría utilizar sus conocimientos de diferentes razas de perros para crear una imagen de un nuevo perro que no existe en la vida real.

## Tipos de modelos de IA generativa
* **Codificador automático variable (VAE)**: Considere los modelos de codificador automático variable (VAE) como un habilidoso artista que puede mirar una pintura, crear rápidamente un boceto de una versión simplificada de la misma y, a continuación, recrear de la nueva pintura usando solo ese boceto simplificado como referencia. El artista captura los elementos esenciales de la pintura y luego los usa para crear una nueva obra de arte.
* **Red generativa antagónica (GAN):** Considere el modelo de red generativa antagónica (GAN) como una competición entre un hábil falsificador (el generador) y un talentoso crítico de arte (el discriminador). El falsificador crea pinturas falsas, mientras que el crítico trata de determinar si cada pintura es genuina o una falsificación. A medida que el falsificador mejora su técnica, el crítico se vuelve más perspicaz y este ciclo continúa hasta que el falsificador puede crear falsificaciones casi perfectas. El generador trata de crear datos que sean lo suficientemente reales para engañar al discriminador
* **Autorregresivo**: Imagine un modelo autorregresivo como un hábil narrador que escucha el comienzo de una historia y luego la continúa prediciendo lo que va a pasar basándose en las palabras y los eventos que han ocurrido hasta el momento. El narrador utiliza su conocimiento del lenguaje, la gramática y las convenciones de narración de historias para crear una continuación coherente y atractiva de la historia. Son particularmente adecuados para generar texto

# Módulo 5: Tendencias futuras de la IA

## ¿Adónde va la IA desde aquí?
Vivimos en el segundo nivel de la IA, llamado IA amplia, en el que los sistemas de aprendizaje automático han empezado a aparecer en nuestra vida cotidiana. Una IA amplia no puede pensar de forma abstracta, elaborar estrategias ni utilizar la experiencia previa para aportar ideas nuevas y creativas. Pero los científicos de datos y los programadores ya están trabajando en el tercer nivel, denominado IA general. El objetivo de la IA general es crear sistemas capaces de realizar cualquier tarea intelectual que pueda realizar un ser humano, y mucho más. Algunos científicos creen que este objetivo podrá alcanzarse en unos veinte años (a principios de la década de 2040).