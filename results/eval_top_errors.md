# Errores Prioritarios — Evaluación de Recuperación

- Total preguntas: 40
- Fallos (P@1=0): 38 (95.0%)

## Categorías más problemáticas
- Ordenadas por mayor tasa de fallo (luego por número de preguntas)

### agentes
- n=4 | fallos=4 (100.0%) | P@1=0.000 | MRR=0.125
- Ejemplos (hasta 5):
  - q_0001 — lbl=covered | top1: pág 81 score=0.6197
    · esperadas: [23, 25]
    · keywords: agente, racional, percepción, acción
    · snippet: decisiones más efectivas. Este aprendizaje puede ser individual o colectivo, donde los agentes comparten conocimientos. Estas arquitecturas son adecuadas para modelar entornos dinámicos donde las situaciones cambian con…
  - q_0002 — lbl=covered | top1: pág 53 score=0.6910
    · esperadas: [31, 32]
    · keywords: observable, estocástico, determinista, episódico, dinámico
    · snippet: satisfaga un conjunto de restricciones definidas. Después de las suficientes experiencias interaccionando con el entorno, el comportamiento del agente racional será independiente del conocimiento que poseía inicialmente…
  - q_0003 — lbl=covered | top1: pág 100 score=0.5770
    · esperadas: [42, 52]
    · keywords: reactivo, basado, meta, planificador, aprendizaje
    · snippet: el diseñador del agente puede introducir sentencias una a una, permitiendo al agente adquirir gradualmente la capacidad de operar en su entorno. Este enfoque se conoce como el método declarativo para construir el sistem…
  - q_0030 — lbl=covered | top1: pág 58 score=0.6765
    · esperadas: [76, 79]
    · keywords: KB, inferencia, reglas
    · snippet: planificación a largo plazo hacen que estos entornos de trabajo sean más desafiantes y requieran algoritmos y enfoques especializados para la toma de decisiones y el control inteligente del agente, que maximice los resu…

### busqueda_no_informada
- n=4 | fallos=4 (100.0%) | P@1=0.000 | MRR=0.000
- Ejemplos (hasta 5):
  - q_0014 — lbl=covered | top1: pág 138 score=0.5666
    · esperadas: [116, 120]
    · keywords: sin heurística, amplitud, profundidad
    · snippet: intermedios, considerando la medida de rendimiento del agente, que guiará la transición desde el estado inicial hasta el estado objetivo. ✓ Ejecución de la búsqueda: Una vez determinada la ruta óptima, se llevan a cabo …
  - q_0015 — lbl=covered | top1: pág 138 score=0.6742
    · esperadas: [117, 118]
    · keywords: cola, nivel, completa
    · snippet: intermedios, considerando la medida de rendimiento del agente, que guiará la transición desde el estado inicial hasta el estado objetivo. ✓ Ejecución de la búsqueda: Una vez determinada la ruta óptima, se llevan a cabo …
  - q_0016 — lbl=covered | top1: pág 138 score=0.7654
    · esperadas: [120, 123]
    · keywords: pila, límite, ciclos
    · snippet: de los nodos del árbol y sus respectivas conexiones. Las búsquedas no informadas hacer a ser tratadas se indica a continuación: Búsqueda Preferentemente por Amplitud: Esta técnica explora todos los nodos de un nivel ant…
  - q_0017 — lbl=covered | top1: pág 154 score=0.7036
    · esperadas: [128, 129]
    · keywords: cola de prioridad, coste, óptima
    · snippet: podría desviar la búsqueda, aumentando el tiempo y los recursos necesarios para encontrar la solución. Se va a utilizar para ejemplificar esta búsqueda el grafo de búsqueda de costo uniforme, con la métrica de que la di…

### busqueda_informada
- n=4 | fallos=4 (100.0%) | P@1=0.000 | MRR=0.000
- Ejemplos (hasta 5):
  - q_0018 — lbl=covered | top1: pág 138 score=0.5753
    · esperadas: [131, 132]
    · keywords: heurística, guía, estimación
    · snippet: intermedios, considerando la medida de rendimiento del agente, que guiará la transición desde el estado inicial hasta el estado objetivo. ✓ Ejecución de la búsqueda: Una vez determinada la ruta óptima, se llevan a cabo …
  - q_0019 — lbl=covered | top1: pág 138 score=0.6651
    · esperadas: [132, 134]
    · keywords: greedy, A*, h(n), g(n)
    · snippet: de los nodos del árbol y sus respectivas conexiones. Las búsquedas no informadas hacer a ser tratadas se indica a continuación: Búsqueda Preferentemente por Amplitud: Esta técnica explora todos los nodos de un nivel ant…
  - q_0020 — lbl=covered | top1: pág 92 score=0.5508
    · esperadas: [134, 137]
    · keywords: admisible, consistente, óptimo
    · snippet: afirmativa, podrías optar por no jugar al fútbol, pero si es negativa, avanzarías al siguiente nodo: "¿Hay viento?". En caso de que la respuesta sea afirmativa, podrías decidir no jugar debido a que el viento podría inf…
  - q_0039 — lbl=covered | top1: pág 86 score=0.5880
    · esperadas: [134, 135]
    · keywords: no sobreestima, costo real, óptimo
    · snippet: En el contexto de la Inteligencia Artificial, las heurísticas son igualmente significativas. Los sistemas de IA pueden incorporar técnicas heurísticas para optimizar la búsqueda de soluciones en escenarios complejos, co…

### optimizacion
- n=3 | fallos=3 (100.0%) | P@1=0.000 | MRR=0.167
- Ejemplos (hasta 5):
  - q_0021 — lbl=covered | top1: pág 170 score=0.5848
    · esperadas: [138, 143]
    · keywords: estado, vecinos, óptimo local
    · snippet: instante. De ser el caso de que sea superior, actualiza la mejor solución. Además, en cada iteración, hay una probabilidad (tasaReinicio) de realizar un reinicio aleatorio, esto implica que la búsqueda se reinicia desde…
  - q_0022 — lbl=covered | top1: pág 165 score=0.6385
    · esperadas: [140, 143]
    · keywords: gradiente, reinicios, temple
    · snippet: de rutas y la asignación de tareas (Haykin, 2009). 3.3.3 Variantes de escalada de colinas Debido a las limitaciones de la búsqueda de escalada de colinas, se han pensado múltiples variantes para superar el problema de q…
  - q_0023 — lbl=covered | top1: pág 163 score=0.6163
    · esperadas: [153, 157]
    · keywords: temperatura, probabilidad, exploración
    · snippet: cuál es el estado actual, mientras que en otros se tiene que comenzar seleccionando uno aleatoriamente. Luego, se repite las siguientes acciones: se evalúa a los vecinos, seleccionando el de mejor valor. Luego, se compa…

### csp
- n=3 | fallos=3 (100.0%) | P@1=0.000 | MRR=0.111
- Ejemplos (hasta 5):
  - q_0025 — lbl=covered | top1: pág 185 score=0.5631
    · esperadas: [158, 166]
    · keywords: variables, dominios, restricciones
    · snippet: • Prueba de objetivo: comprobar si a todas las variables se les asigna un valor y se cumplen todas las restricciones. • Función de coste del trayecto: todos los trayectos tienen el mismo coste. Como se mencionó anterior…
  - q_0026 — lbl=covered | top1: pág 85 score=0.5760
    · esperadas: [164, 166]
    · keywords: MRV, grado, consistencia
    · snippet: empíricas utilizadas por los seres humanos para solucionar problemas complejos y tomar decisiones de manera ágil y efectiva. Las heurísticas, consideradas atajos mentales, se fundamentan en la experiencia y el juicio pr…
  - q_0040 — lbl=covered | top1: pág 195 score=0.5711
    · esperadas: [158, 164]
    · keywords: curso, día, asignación
    · snippet: y entender el conjunto de datos. Un equilibrio adecuado en el número y la distribución de estos nodos es importante para evitar problemas como el sobreajuste o el subajuste, asegurando así que el modelo sea generalizabl…

### turing
- n=2 | fallos=2 (100.0%) | P@1=0.000 | MRR=0.167
- Ejemplos (hasta 5):
  - q_0005 — lbl=covered | top1: pág 23 score=0.5972
    · esperadas: [21, 22]
    · keywords: Turing, prueba, imitación, máquinas
    · snippet: entonces cuando se buscó dotar a las máquinas de recursos para resolver problemas de manera autónoma, sin depender del apoyo humano. Si bien la noción de máquina ha estado presente durante muchos años, fue Alan Turing q…
  - q_0006 — lbl=covered | top1: pág 44 score=0.6218
    · esperadas: [21, 22]
    · keywords: prueba, imitación, interrogador, indistinguible
    · snippet: Turing (1912-1954) propuso la Máquina Niño, en la que se crearía un agente inteligente básico y se sometería a un curso de educación para proporcionarle conocimiento. En su artículo de 1950, "Computing machinery and int…

### reglas_produccion
- n=2 | fallos=2 (100.0%) | P@1=0.000 | MRR=0.250
- Ejemplos (hasta 5):
  - q_0012 — lbl=covered | top1: pág 189 score=0.5216
    · esperadas: [104, 111]
    · keywords: si-entonces, encadenamiento, hechos
    · snippet: productos en el mercado, consecución de objetivos de producción, reducción de la deserción escolar, evaluación de riesgos en proyectos, toma de decisiones legales, planificación de inversiones, previsiones climáticas, p…
  - q_0013 — lbl=covered | top1: pág 126 score=0.6090
    · esperadas: [106, 110]
    · keywords: hacia adelante, hacia atrás, objetivo, datos
    · snippet: se articulan |a través de una estructura de implicación, en la cual la premisa se compone de una conjunción de literales positivos (que pueden ser hechos o condiciones), y la conclusión es un solo literal positivo. Para…

### arboles_decision
- n=2 | fallos=2 (100.0%) | P@1=0.000 | MRR=0.000
- Ejemplos (hasta 5):
  - q_0027 — lbl=covered | top1: pág 191 score=0.6275
    · esperadas: [167, 176]
    · keywords: clasificación, atributo, entropía
    · snippet: específica del árbol, donde se realiza otra pregunta o se toma una decisión final. Este proceso se repite hasta llegar a una "hoja" del árbol, que es donde se toma la decisión final respecto a la clasificación o valor d…
  - q_0028 — lbl=covered | top1: pág 190 score=0.6592
    · esperadas: [176, 182]
    · keywords: precisión, validación, conjunto
    · snippet: negocio). Para cada una de estas etapas se utiliza software o herramientas especializadas que son altamente beneficiosas, debido a que optimizan el proceso, evita errores y ahorran tiempo. Los árboles de decisión se div…

### aprendizaje
- n=2 | fallos=2 (100.0%) | P@1=0.000 | MRR=0.000
- Ejemplos (hasta 5):
  - q_0031 — lbl=uncovered | top1: pág 38 score=0.6043
    · keywords: redes, Q-learning, política
    · snippet: c) Aprendizaje por Refuerzo: Son modelos (agentes) que aprenden a tomar decisiones mediante experimentación e interacción con el medio ambiente, reciben recompensas o penalizaciones en función de las acciones que realiz…
  - q_0032 — lbl=uncovered | top1: pág 46 score=0.3953
    · keywords: transformer, atención, autoregresiva
    · snippet: como agente, es una entidad autónoma que existe en un entorno y se guía por la información que recibe a través de sensores. Actúa de manera racional utilizando actuadores para llevar a cabo acciones. En un instante dado…

### historia
- n=1 | fallos=1 (100.0%) | P@1=0.000 | MRR=0.000
- Ejemplos (hasta 5):
  - q_0007 — lbl=covered | top1: pág 96 score=0.4817
    · esperadas: [3, 5]
    · keywords: Dartmouth, McCarthy, Minsky, expertos
    · snippet: seguimiento y análisis de variables ambientales, permitiendo una mejor respuesta frente a fenómenos como el cambio climático. Los marcos temporales facilitan la estructuración y secuencia de eventos en narrativas, ya se…

### logica_proposicional
- n=1 | fallos=1 (100.0%) | P@1=0.000 | MRR=0.000
- Ejemplos (hasta 5):
  - q_0008 — lbl=covered | top1: pág 68 score=0.7190
    · esperadas: [82, 88]
    · keywords: proposición, conectivos, verdad
    · snippet: Emplean técnicas sofisticadas como la lógica proposicional, la lógica de predicados o sistemas avanzados basados en reglas para procesar y razonar sobre el conocimiento acumulado, conduciéndoles a conclusiones lógicas y…

### logica
- n=1 | fallos=1 (100.0%) | P@1=0.000 | MRR=0.500
- Ejemplos (hasta 5):
  - q_0011 — lbl=covered | top1: pág 89 score=0.6812
    · esperadas: [93, 104]
    · keywords: inferencia, deducción, prueba
    · snippet: aplica a la interpretación semántica de las oraciones. Un claro ejemplo es la oración "María quiere a Patricio" que puede representarse como Quiere(María, Patricio). Las consultas en bases de datos, especialmente con le…

### programacion_lineal
- n=1 | fallos=1 (100.0%) | P@1=0.000 | MRR=0.000
- Ejemplos (hasta 5):
  - q_0024 — lbl=covered | top1: pág 209 score=0.4911
    · esperadas: [157, 158]
    · keywords: función objetivo, restricciones, simplex
    · snippet: • Desarrolladora de Software – Prácticas pre-profesionales en Escuela Superior Politécnica de Chimborazo desde febrero-2013 hasta julio-2013. • Soporte Técnico en Scytel - CNE desde enero-2013 hasta febrero-2013.

### representacion_conocimiento
- n=1 | fallos=1 (100.0%) | P@1=0.000 | MRR=0.000
- Ejemplos (hasta 5):
  - q_0029 — lbl=covered | top1: pág 87 score=0.6000
    · esperadas: [64, 71]
    · keywords: nodos, aristas, conceptos
    · snippet: estructurada (Markman, 2013). Este enfoque guarda semejanza con una característica fundamental de la memoria humana, en la que se tejen numerosas relaciones, de modo que pensar en un concepto puede evocar una multitud d…

### vectores
- n=1 | fallos=1 (100.0%) | P@1=0.000 | MRR=0.000
- Ejemplos (hasta 5):
  - q_0033 — lbl=uncovered | top1: pág 48 score=0.4809
    · keywords: Chroma, vector, embeddings
    · snippet: de situaciones, contribuyendo así al avance y aplicación de esta disciplina. Figura 1.5 Rompecabezas Fuente: Wikipedia Un estado se refiere a una configuración específica en la que se encuentra un agente dentro de su en…

### rag
- n=1 | fallos=1 (100.0%) | P@1=0.000 | MRR=0.000
- Ejemplos (hasta 5):
  - q_0034 — lbl=uncovered | top1: pág 43 score=0.2877
    · keywords: retrieval, generación, contexto
    · snippet: gran escala. Un aspecto importante de cualquier sistema de IA que interactúa con la gente es que debe razonar sobre lo que las personas piensan en lugar de llevar a cabo los comandos de manera literal, para juzgar si lo…

### evaluacion
- n=1 | fallos=1 (100.0%) | P@1=0.000 | MRR=0.000
- Ejemplos (hasta 5):
  - q_0035 — lbl=uncovered | top1: pág 202 score=0.7204
    · keywords: precisión, exhaustividad
    · snippet: Continuando en elejemplo médico, esta métrica es importante en la determinación de la probabilidad de que una persona no tenga una enfermedad cuando la prueba indica un resultado negativo. Puntuación F1: Esta es una mét…

### aplicaciones
- n=1 | fallos=1 (100.0%) | P@1=0.000 | MRR=0.000
- Ejemplos (hasta 5):
  - q_0036 — lbl=uncovered | top1: pág 43 score=0.6880
    · keywords: robot, percepción, planificación
    · snippet: experimentados y las máquinas. La presencia de los métodos de Inteligencia artificial ha puesto a los seres humanos a pensar en los riesgos potenciales de sus avances, piensan algunas personas que los sistemas de IA se …

### agentes_arquitecturas
- n=3 | fallos=2 (66.7%) | P@1=0.333 | MRR=0.333
- Ejemplos (hasta 5):
  - q_0037 — lbl=covered | top1: pág 58 score=0.6073
    · esperadas: [52, 54]
    · keywords: planificación, modelo, objetivos
    · snippet: planificación a largo plazo hacen que estos entornos de trabajo sean más desafiantes y requieran algoritmos y enfoques especializados para la toma de decisiones y el control inteligente del agente, que maximice los resu…
  - q_0038 — lbl=covered | top1: pág 100 score=0.5705
    · esperadas: [51, 52]
    · keywords: condición-acción, estado, percepción
    · snippet: el diseñador del agente puede introducir sentencias una a una, permitiendo al agente adquirir gradualmente la capacidad de operar en su entorno. Este enfoque se conoce como el método declarativo para construir el sistem…

### logica_primer_orden
- n=2 | fallos=1 (50.0%) | P@1=0.500 | MRR=0.500
- Ejemplos (hasta 5):
  - q_0009 — lbl=covered | top1: pág 114 score=0.6600
    · esperadas: [88, 93]
    · keywords: predicados, cuantificadores, dominio
    · snippet: lógica de primer orden incluyen el modus ponens, modus tollens, la introducción de cuantificadores y otras. 2.1.3 Cuantificadores Los cuantificadores son herramientas esenciales en la lógica de primer orden para expresa…
