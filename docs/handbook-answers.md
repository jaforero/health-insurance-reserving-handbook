---
title: Respuestas fundamentales del Handbook
description: Respuestas editoriales breves, criterios de uso y fuentes para preguntas fundamentales de reserving.
chapter: handbook-answers
part: repository
language: es
status: review
version: "0.1.0"
last_updated: "2026-11-10"
tags: [q-and-a, reserving, foundations]
---

# Respuestas fundamentales del Handbook

Estas respuestas son síntesis editoriales basadas en los capítulos enlazados. Se publican como contenido del manual y se recuperan literalmente; no se generan durante la consulta. Los criterios orientan la lectura y no sustituyen una estimación con datos ni el juicio actuarial. Revisión técnica inicial: comprobación contra las fuentes del repositorio; revisión actuarial independiente pendiente.

## ¿Cómo funcionan los triángulos de reservas?

<!-- answer:triangles -->

### Preguntas equivalentes

- Como funcionan los triangulos de reservas?
- ¿Qué es un triángulo de desarrollo?
- ¿Cómo se lee un triángulo actuarial?

### Respuesta directa

Un triángulo de desarrollo organiza la experiencia histórica por periodo de origen y edad de desarrollo. Las filas representan periodos de origen; las columnas, edades de desarrollo; y cada celda contiene el valor observado para esa combinación. La zona futura del triángulo corresponde a desarrollo todavía no observado; los vacíos dentro de la zona histórica requieren revisar la calidad de los datos. El triángulo permite estudiar cómo madura cada cohorte; por sí solo no es un método de estimación de reservas.

### Criterios para actuar

- Define primero qué significa origen: servicio, reporte u otra fecha coherente con el objetivo.
- Identifica si las celdas contienen pagos, incurridos, conteos u otra medida; no son intercambiables.
- Distingue valores incrementales y acumulados antes de calcular factores.
- Usa la fecha de valuación para identificar la diagonal disponible; no interpretes el futuro no observado como cero.

### Fuentes verificables

- [02-triangle-construction](part-01-foundations/02-triangle-construction.md)
- [04-incremental-vs-cumulative-triangles](part-01-foundations/04-incremental-vs-cumulative-triangles.md)

## ¿Cómo construyo un triángulo de desarrollo?

<!-- answer:build-triangle -->

### Preguntas equivalentes

- ¿Cómo armar un triángulo de reservas?
- Pasos para construir triangulos actuariales

### Respuesta directa

Para construir un triángulo, define el periodo de origen, la edad de desarrollo, la fecha de valuación y la medida. Organiza los datos en formato largo, agrega la medida para cada combinación de origen y desarrollo y transforma esa tabla en una matriz. Las combinaciones futuras no observadas deben permanecer identificadas como tales.

### Criterios para actuar

- Mantén una definición de origen consistente para todos los registros.
- Revisa duplicados, reversos, monedas, segmentación y conciliación con el corte.
- Separa segmentos con patrones materialmente diferentes cuando exista volumen suficiente.
- Concilia la diagonal y documenta las transformaciones antes de aplicar un método.

### Fuentes verificables

- [02-triangle-construction](part-01-foundations/02-triangle-construction.md)

## ¿Qué diferencia hay entre IBNR e IBNER?

<!-- answer:ibnr-ibner -->

### Preguntas equivalentes

- Diferencia IBNR IBNER
- ¿IBNR y IBNER son lo mismo?

### Respuesta directa

IBNR, en sentido estricto, corresponde a reclamaciones ocurridas que todavía no han sido reportadas o registradas. IBNER corresponde al desarrollo de reclamaciones ya reportadas cuyo monto no está suficientemente estimado. No todo lo pendiente de pago es IBNR: parte puede estar reconocida como reserva caso.

### Criterios para actuar

- Aclara si tu organización utiliza IBNR en sentido estricto o como etiqueta amplia que incluye IBNER.
- Distingue reserva caso, IBNR e IBNER para evitar duplicar componentes del pasivo.
- Documenta la base pagada o incurrida y el perímetro de la estimación.

### Fuentes verificables

- [01-ibnr-and-reserving](part-01-foundations/01-ibnr-and-reserving.md)

## ¿Qué es IBNR?

<!-- answer:ibnr -->

### Preguntas equivalentes

- ¿Qué significa IBNR?
- Explica el IBNR

### Respuesta directa

IBNR significa incurred but not reported: reclamaciones ocurridas que todavía no se han reportado o registrado. En salud, los retrasos entre servicio, facturación, radicación, auditoría y registro explican por qué las obligaciones pueden existir antes de observarse completamente. Su estimación requiere definir la fecha de corte y el alcance del pasivo.

### Criterios para actuar

- Distingue ocurrencia, reporte y pago; una reclamación no pagada puede estar ya reportada.
- Aclara si la definición operativa de IBNR incluye desarrollo de reclamaciones conocidas.
- No confundas una definición general con el cálculo de la reserva de una entidad: ese cálculo requiere datos.

### Fuentes verificables

- [01-ibnr-and-reserving](part-01-foundations/01-ibnr-and-reserving.md)
- [22-health-claim-lifecycle-and-operational-lags](part-06-health-specific/22-health-claim-lifecycle-and-operational-lags.md)

## ¿Qué diferencia hay entre pagado e incurrido?

<!-- answer:paid-incurred -->

### Preguntas equivalentes

- ¿Cuál es la diferencia entre triángulos pagados e incurridos?
- Pagado vs incurrido

### Respuesta directa

El pagado refleja desembolsos ejecutados. El incurrido observado combina pagos y reserva caso bajo la definición contable utilizada; no equivale automáticamente al costo último. Por eso los triángulos pagados e incurridos describen procesos distintos y pueden producir estimaciones diferentes. La base debe documentarse antes de interpretar una reserva.

### Criterios para actuar

- Concilia qué componentes incluye el incurrido observado.
- En pagos, evalúa cambios de velocidad de liquidación; en incurridos, revisa también cambios en reconocimiento y reserva caso.
- Compara estimaciones sobre el mismo perímetro y evita sumar resultados que representen el mismo pasivo.

### Fuentes verificables

- [01-ibnr-and-reserving](part-01-foundations/01-ibnr-and-reserving.md)
- [30-colombia-paid-vs-incurred-triangles](part-07-colombia/30-colombia-paid-vs-incurred-triangles.md)

## ¿Qué diferencia hay entre un triángulo incremental y uno acumulado?

<!-- answer:incremental-cumulative -->

### Preguntas equivalentes

- Incremental vs acumulado
- ¿Son iguales los triángulos incrementales y acumulados?

### Respuesta directa

Un triángulo incremental registra la cantidad correspondiente a cada intervalo de desarrollo. Un triángulo acumulado registra la suma desde el inicio del origen hasta cada edad de desarrollo. Para pasar de incremental a acumulado se suma a lo largo de cada fila; para volver a incremental se toman diferencias entre acumulados consecutivos.

### Criterios para actuar

- Confirma la unidad y frecuencia de desarrollo antes de transformar los datos.
- No acumules una tabla que ya está acumulada.
- Conserva la máscara de observación: una celda futura no es un cero observado.
- Revisa reversos y ajustes; no supongas que todas las series monetarias son necesariamente crecientes.

### Fuentes verificables

- [04-incremental-vs-cumulative-triangles](part-01-foundations/04-incremental-vs-cumulative-triangles.md)

## ¿Qué significa ultimate?

<!-- answer:ultimate -->

### Preguntas equivalentes

- ¿Qué es el costo último?
- Explica ultimate en reservas

### Respuesta directa

El ultimate o costo último es el costo final esperado de las reclamaciones de un periodo de origen. En una base pagada coherente, el monto pendiente se obtiene restando los pagos observados al ultimate estimado. En una base incurrida, debe distinguirse el incurrido observado del desarrollo futuro pendiente.

### Criterios para actuar

- Compara cantidades del mismo origen, corte, moneda y perímetro.
- Distingue costo último de monto pendiente de pago.
- Documenta si el resultado incluye IBNR, IBNER y reserva caso, según la base elegida.

### Fuentes verificables

- [01-ibnr-and-reserving](part-01-foundations/01-ibnr-and-reserving.md)

## ¿Cuáles son los supuestos de Chain Ladder?

<!-- answer:chain-ladder -->

### Preguntas equivalentes

- ¿Cuándo es apropiado usar Chain Ladder?
- Supuestos necesarios para utilizar Chain Ladder

### Respuesta directa

Chain Ladder proyecta desarrollo futuro a partir de patrones observados. Su uso requiere que esos patrones sean suficientemente representativos del futuro: mezcla de riesgo comparable, operación de reporte y pago razonablemente estable, datos coherentes y ausencia de efectos de calendario dominantes sin ajustar. No basta con disponer de un triángulo.

### Criterios para actuar

- Revisa estabilidad de factores, cambios de mezcla y efectos de calendario.
- Investiga cambios en reporte, auditoría y pago antes de extrapolar.
- Contrasta el resultado con diagnósticos y métodos alternativos, especialmente para periodos inmaduros.

### Fuentes verificables

- [06-chain-ladder-method](part-02-classical-reserving/06-chain-ladder-method.md)
- [07-chain-ladder-diagnostics](part-02-classical-reserving/07-chain-ladder-diagnostics.md)

## ¿Cuál es el mejor método para reservas de salud?

<!-- answer:health-method -->

### Preguntas equivalentes

- Para reservas en salud cuál de los métodos es más recomendado?
- ¿Cuál es el método más recomendado para reservas en salud?
- ¿Qué método debería usar para estimar reservas en salud?
- ¿Cuál es el mejor método de reserving en salud?
- ¿Chain Ladder o Bornhuetter-Ferguson para reservas en salud?
- ¿Cómo selecciono el método de reservas en salud?
- ¿Qué método conviene para salud?

### Respuesta directa

No existe un método universalmente superior para reservas de salud. La selección depende del pasivo, la madurez, la estabilidad del desarrollo, la exposición disponible, la calidad de los datos y la existencia de un prior defendible. Chain Ladder puede servir como referencia cuando el desarrollo es estable; para periodos inmaduros, métodos con una expectativa previa justificable pueden aportar mayor estabilidad.

### Criterios para actuar

- Define primero la obligación que necesitas estimar y verifica que los datos la representan.
- Considera Bornhuetter-Ferguson, Cape Cod u otros enfoques con exposición o prior cuando esos insumos sean defendibles.
- Evalúa incertidumbre, sensibilidad y desempeño retrospectivo; seleccionar por buen ajuste histórico no basta.
- Mantén un método central y alternativas de contraste; si el triángulo no representa el proceso, considera otros modelos.

### Fuentes verificables

- [21-health-insurance-reserving-specificities](part-06-health-specific/21-health-insurance-reserving-specificities.md)
- [methodology-selection-guide](methodology-selection-guide.md)


## ¿Por qué es necesario deduplicar los movimientos?

<!-- answer:data-deduplication-why -->

### Preguntas equivalentes

- ¿Por qué debo eliminar duplicados?
- ¿Qué pasa si tengo registros repetidos?
- ¿Cómo afectan los duplicados al IBNR?
- ¿Por qué debo deduplicar registros?

### Respuesta directa

La deduplicación evita que un mismo movimiento económico sea contabilizado más de una vez en pagos, frecuencias y triángulos. Un duplicado técnico puede inflar el acumulado observado, alterar factores de desarrollo y sesgar el costo proyectado o el pasivo no pagado.

### Criterios para actuar

- Define la llave del movimiento económico antes de deduplicar.
- Clasifica pagos parciales, reversos, glosas y ajustes antes de eliminar filas.
- Concilia pagos, frecuencias y triángulos después de aplicar la regla.

### Fuentes verificables

- [04-demo-preparacion-datos](examples/04-demo-preparacion-datos.md)

## ¿Cómo sé si dos filas repetidas son realmente duplicados?

<!-- answer:data-duplicate-identification -->

### Preguntas equivalentes

- ¿Cómo identifico un duplicado técnico?
- ¿Dos filas iguales siempre se eliminan?
- ¿Qué campos definen un movimiento único?

### Respuesta directa

Dos filas son duplicados solo cuando representan el mismo evento económico bajo una llave de negocio y no movimientos distintos del ciclo de la reclamación. La comparación debe preservar la semántica del evento: factura, folio, fechas, importe y tipo de movimiento pueden ser relevantes, pero la llave depende del proceso real.

### Criterios para actuar

- Valida qué evento representa cada fila con el proceso real.
- Evalúa factura, folio, fechas, importe y tipo de movimiento al definir la llave.
- Comprueba que la regla conserva movimientos legítimos y detecta copias entre archivos.

### Fuentes verificables

- [04-demo-preparacion-datos](examples/04-demo-preparacion-datos.md)

## ¿Por qué archivo_fuente no debe formar parte de la llave económica?

<!-- answer:data-source-key -->

### Preguntas equivalentes

- ¿Por qué no uso el nombre del archivo para deduplicar?
- ¿El archivo de origen identifica el movimiento?
- ¿Qué problema genera incluir archivo_fuente en la clave?

### Respuesta directa

El archivo fuente identifica el contenedor técnico, no necesariamente el evento económico. Dos archivos distintos pueden contener la misma transacción. Si el nombre del archivo entra en la llave, una copia del mismo movimiento en dos extractos se considera falsamente como dos eventos diferentes.

### Criterios para actuar

- Construye la llave sobre el evento económico.
- Conserva archivo_fuente como dato de procedencia.
- Documenta reglas de prioridad cuando varios extractos contengan el mismo evento.

### Fuentes verificables

- [04-demo-preparacion-datos](examples/04-demo-preparacion-datos.md)

## ¿Qué ocurre si la fecha de pago es anterior a la fecha de servicio?

<!-- answer:data-negative-lag -->

### Preguntas equivalentes

- ¿Puede existir un rezago negativo?
- ¿Qué significa pago antes del servicio?
- ¿Debo excluir fechas invertidas?

### Respuesta directa

Un pago anterior al servicio produce una edad de desarrollo negativa y normalmente indica un problema de semántica, mapeo, formato o calidad de datos. Las edades negativas rompen la interpretación origen–desarrollo y pueden ubicar importes en celdas imposibles del triángulo.

### Criterios para actuar

- Comprueba la semántica, el formato y el mapeo de las fechas.
- Investiga excepciones operativas antes de clasificar el registro como error.
- No desplaces fechas automáticamente para forzar una edad positiva.

### Fuentes verificables

- [04-demo-preparacion-datos](examples/04-demo-preparacion-datos.md)

## ¿Por qué un importe negativo no debe eliminarse automáticamente?

<!-- answer:data-negative-amount -->

### Preguntas equivalentes

- ¿Los pagos negativos son errores?
- ¿Qué hago con reversos y recuperaciones?
- ¿Por qué conservar glosas negativas?

### Respuesta directa

Un importe negativo puede representar un reverso, recuperación, glosa aceptada, anulación o reclasificación legítima. Eliminarlo sin clasificación sobrestima pagos netos y puede ocultar cambios operativos importantes.

### Criterios para actuar

- Clasifica reversos, recuperaciones, glosas y errores de signo.
- Concilia importes sobre una base bruta o neta consistente.
- No elimines ni aceptes automáticamente un importe por su signo.

### Fuentes verificables

- [04-incremental-vs-cumulative-triangles](part-01-foundations/04-incremental-vs-cumulative-triangles.md)
- [04-demo-preparacion-datos](examples/04-demo-preparacion-datos.md)

## ¿Por qué se construyen triángulos acumulados además de incrementales?

<!-- answer:triangle-incremental-cumulative -->

### Preguntas equivalentes

- ¿Para qué sirven los acumulados?
- ¿Por qué mantener ambas vistas?
- ¿Incremental o acumulado para Chain Ladder?

### Respuesta directa

Los incrementales muestran lo ocurrido en cada edad; los acumulados muestran lo observado hasta esa edad. Ambos describen la misma experiencia, pero responden preguntas distintas. Los acumulados suelen ser la base de Chain Ladder y de factores edad-a-edad; los incrementales permiten detectar estacionalidad, efectos calendario, reversos y celdas atípicas.

### Criterios para actuar

- Usa acumulados para analizar factores edad-a-edad cuando el método lo requiera.
- Examina incrementales para detectar reversos, celdas atípicas y efectos calendario.
- Reconcilia ambas vistas antes de proyectar.

### Fuentes verificables

- [04-incremental-vs-cumulative-triangles](part-01-foundations/04-incremental-vs-cumulative-triangles.md)

## ¿Qué significa que un periodo de origen esté inmaduro?

<!-- answer:triangle-origin-immaturity -->

### Preguntas equivalentes

- ¿Qué es un origen reciente?
- ¿Cómo se interpreta la madurez?
- ¿Por qué falta desarrollo en los últimos periodos?

### Respuesta directa

Un periodo de origen está inmaduro cuando, a la fecha de valoración, solo se ha observado una parte de su desarrollo esperado. La mayor proporción pendiente incrementa la dependencia de factores, cola y supuestos externos; por eso los orígenes recientes suelen concentrar más incertidumbre.

### Criterios para actuar

- Estima la proporción observada con un patrón defendible al corte.
- Evalúa sensibilidad a factores, cola y supuestos externos.
- No confundas mayor madurez con calidad garantizada de los datos.

### Fuentes verificables

- [11-bornhuetter-ferguson](part-02-classical-reserving/11-bornhuetter-ferguson.md)
- [05-age-to-age-development-factors](part-01-foundations/05-age-to-age-development-factors.md)

## ¿Por qué un triángulo descriptivo no implica que Chain Ladder sea elegible?

<!-- answer:triangle-descriptive-not-eligible -->

### Preguntas equivalentes

- ¿Construir un triángulo basta para usar Chain Ladder?
- ¿Por qué el demo puede formar el triángulo pero bloquear el método?
- ¿Ejecutable significa elegible?

### Respuesta directa

Construir una tabla origen–desarrollo demuestra que los datos pueden agregarse, no que el patrón histórico sea estable, representativo o suficiente para proyectar. Chain Ladder requiere historia, comparabilidad, definición consistente, revisión de cambios operativos y factores defendibles.

### Criterios para actuar

- Confirma que el triángulo representa la obligación a estimar.
- Revisa comparabilidad, historia disponible y cambios operativos.
- Valida la estabilidad del patrón antes de aceptar una proyección.

### Fuentes verificables

- [04-demo-preparacion-datos](examples/04-demo-preparacion-datos.md)
- [06-chain-ladder-method](part-02-classical-reserving/06-chain-ladder-method.md)

## ¿Qué efecto tienen los duplicados sobre los factores edad-a-edad?

<!-- answer:triangle-duplicates-factors -->

### Preguntas equivalentes

- ¿Cómo sesga un duplicado los factores de desarrollo?
- ¿Los duplicados pueden cambiar el CDF?
- ¿Qué pasa si duplico una celda del triángulo?

### Respuesta directa

Los duplicados cambian los acumulados usados en numeradores y denominadores y pueden alterar los factores edad-a-edad y el CDF. El sesgo no siempre es proporcional: depende de la edad, el periodo de origen y de si la duplicación afecta una o varias celdas.

### Criterios para actuar

- Resuelve duplicados en el detalle antes de agregar.
- Recalcula acumulados, factores edad-a-edad y CDF.
- Examina el impacto por origen y edad; no presupongas un sesgo proporcional.

### Fuentes verificables

- [05-age-to-age-development-factors](part-01-foundations/05-age-to-age-development-factors.md)
- [04-demo-preparacion-datos](examples/04-demo-preparacion-datos.md)

## ¿Por qué las matrices mensuales suelen requerir una historia suficientemente larga?

<!-- answer:triangle-monthly-history -->

### Preguntas equivalentes

- ¿Por qué 36x36 puede ser insuficiente?
- ¿Cuántos meses necesito para factores mensuales?
- ¿Por qué usar más orígenes que edades?

### Respuesta directa

Una vista mensual puede tener muchas celdas, pero los enlaces tardíos reciben observaciones de pocos periodos de origen. La historia adicional aumenta la evidencia disponible para estimar y diagnosticar factores. En una matriz 36×36 al corte, el enlace 34→35 puede depender de una sola fila; esto no demuestra estabilidad.

### Criterios para actuar

- Cuenta observaciones por enlace de desarrollo, especialmente en edades tardías.
- Revisa volumen, homogeneidad y cambios operativos.
- No uses un número mínimo de meses como garantía universal de suficiencia.

### Fuentes verificables

- [03-demo-triangulos-mensuales-salud](examples/03-demo-triangulos-mensuales-salud.md)

## ¿Cuándo Chain Ladder puede ser poco confiable?

<!-- answer:method-chain-ladder-unreliable -->

### Preguntas equivalentes

- ¿Cuándo no debo usar Chain Ladder?
- ¿Qué rompe el patrón histórico?
- ¿Cuáles son los principales riesgos de CL?

### Respuesta directa

Chain Ladder puede ser poco confiable cuando el patrón histórico no representa los orígenes inmaduros. Los cambios de mezcla, beneficios, red, auditoría, pago, segmentación, inflación o eventos calendario pueden contaminar factores y proyecciones.

### Criterios para actuar

- Investiga cambios de mezcla, beneficios, red, auditoría y pago.
- Evalúa inflación y efectos calendario antes de extrapolar factores.
- Contrasta sensibilidad, segmentación y métodos alternativos según el diagnóstico.

### Fuentes verificables

- [06-chain-ladder-method](part-02-classical-reserving/06-chain-ladder-method.md)

## ¿Por qué Bornhuetter-Ferguson necesita un prior independiente?

<!-- answer:method-bf-prior-independence -->

### Preguntas equivalentes

- ¿Por qué el prior BF no debe salir del mismo triángulo?
- ¿Qué significa independencia del prior?
- ¿Puedo calibrar BF con el observado?

### Respuesta directa

BF usa una expectativa previa para la porción todavía no desarrollada. Esa expectativa debe aportar información distinta de la experiencia que se está evaluando. Si el prior se deriva retrospectivamente del mismo observado, la comparación puede volverse circular y aparentar más evidencia de la que existe.

### Criterios para actuar

- Documenta procedencia, fecha y justificación del prior.
- Alinea población, cobertura y unidad con el observado.
- Evita una construcción retrospectiva circular y prueba sensibilidad al prior.

### Fuentes verificables

- [11-bornhuetter-ferguson](part-02-classical-reserving/11-bornhuetter-ferguson.md)

## ¿Qué diferencia conceptual existe entre Chain Ladder y Bornhuetter-Ferguson?

<!-- answer:method-cl-vs-bf -->

### Preguntas equivalentes

- ¿Cómo se diferencian CL y BF?
- ¿Qué usa la experiencia y qué usa el prior?
- ¿Por qué BF es más estable en periodos recientes?

### Respuesta directa

Chain Ladder proyecta el observado usando el patrón completo; BF conserva el observado y aplica el prior únicamente a la proporción pendiente. En orígenes inmaduros, Chain Ladder puede reaccionar fuertemente a un acumulado pequeño, mientras BF limita esa reacción mediante una expectativa externa.

### Criterios para actuar

- Compara ambos métodos con la misma base y fecha de valoración.
- Revisa madurez y sensibilidad del resultado al acumulado observado.
- Evalúa la calidad del prior y del patrón antes de preferir BF.

### Fuentes verificables

- [11-bornhuetter-ferguson](part-02-classical-reserving/11-bornhuetter-ferguson.md)
- [06-chain-ladder-method](part-02-classical-reserving/06-chain-ladder-method.md)

## ¿Qué aporta Benktander frente a Bornhuetter-Ferguson?

<!-- answer:method-benktander-value -->

### Preguntas equivalentes

- ¿Para qué sirve Benktander?
- ¿Cómo actualiza Benktander el prior?
- ¿Por qué Benktander converge a Chain Ladder?

### Respuesta directa

Benktander actualiza iterativamente el prior de BF con el resultado de la iteración anterior y desplaza gradualmente el peso hacia Chain Ladder. Permite estudiar de forma explícita cuánto depende la estimación del prior y cuánto de la experiencia emergente.

### Criterios para actuar

- Documenta el prior, el patrón y la regla de iteración.
- Define las iteraciones antes de observar la cifra que deseas obtener.
- Evalúa sensibilidad: la iteración no crea evidencia adicional.

### Fuentes verificables

- [12-benktander-method](part-02-classical-reserving/12-benktander-method.md)

## ¿Por qué el demo no debe interpretarse como una reserva regulatoria definitiva?

<!-- answer:governance-demo-not-regulatory -->

### Preguntas equivalentes

- ¿El resultado del demo sirve para reportar una reserva?
- ¿Es una opinión actuarial?
- ¿Puedo usar el cálculo directamente en estados financieros?

### Respuesta directa

El demo ilustra mecánica, datos y controles, pero no incorpora por sí solo todas las obligaciones, bases, contratos, regulación, cola, incertidumbre y validaciones de una estimación profesional. Presentarlo como cifra definitiva puede crear una falsa precisión y omitir componentes que los datos agregados no identifican.

### Criterios para actuar

- Reconcilia datos, perímetro y contratos para una aplicación real.
- Documenta supuestos, regulación aplicable, cola e incertidumbre.
- Somete la estimación a revisión independiente y gobierno del modelo.

### Fuentes verificables

- [03-demo-triangulos-mensuales-salud](examples/03-demo-triangulos-mensuales-salud.md)
- [index](index.md)
