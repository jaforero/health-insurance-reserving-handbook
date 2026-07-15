---
title: Glosario actuarial y de reserving en salud
subtitle: Vocabulario controlado para conceptos, medidas, métodos y operaciones del handbook
author: Health Insurance Reserving Handbook
version: 1.0
chapter: Glossary
part: Repository Governance
status: Draft
last_updated: 2026-07-14
language: es
jurisdiction: General con aplicaciones a Colombia
tags:
  - glossary
  - controlled-vocabulary
  - ibnr
  - reserving
  - health-insurance
  - colombia
prerequisites: []
related_chapters:
  - index.md
  - methodology-selection-guide.md
  - part-01-foundations/01-ibnr-and-reserving.md
  - part-01-foundations/02-triangle-construction.md
  - part-01-foundations/03-development-factors.md
  - part-02-classical-reserving/14-classical-reserving-methods-comparison.md
  - part-07-colombia/29-colombia-health-reserving-methodologies.md
  - roadmap.md
---

# Glosario actuarial y de reserving en salud

> Este glosario es un vocabulario controlado. Su finalidad no es reunir todas las acepciones posibles, sino fijar el significado que debe tener cada término dentro del handbook.

## Advertencia de alcance

Las definiciones son técnicas y educativas. No reemplazan definiciones legales, contractuales, contables o regulatorias. Una misma expresión —por ejemplo, *reserva*, *incurred*, *provisión* o *glosa*— puede tener alcances distintos según la jurisdicción, la entidad, el contrato, el sistema fuente y el propósito de la valoración.

Cuando una definición sea relevante para una decisión real, el autor debe identificar, en este orden:

1. la obligación económica o contractual;
2. la definición normativa o contable aplicable a la fecha de valoración;
3. la definición del sistema fuente y sus reglas operativas;
4. la definición analítica usada por el modelo;
5. las reconciliaciones entre esas cuatro capas.

Las referencias a Actuarial Standards of Practice (ASOP) describen un marco profesional de Estados Unidos. No son automáticamente vinculantes en Colombia ni sustituyen regulación local vigente.

## 1. Cómo usar este glosario

Cada capítulo debe usar el **término preferido**. Un término en inglés puede conservarse en cursiva cuando sea estándar en la literatura o cuando una traducción aumente la ambigüedad. Los alias se admiten para búsquedas y explicaciones, pero no deben alternarse sin declarar equivalencia.

Las etiquetas tienen el siguiente significado:

| Etiqueta | Regla editorial |
|---|---|
| **Preferido** | Forma canónica para títulos, texto, variables y metadatos. |
| **Alias admitido** | Puede aparecer después de definir su equivalencia con el término preferido. |
| **Ambiguo** | Requiere base, fecha, estado o alcance adicional. |
| **Desaconsejado** | Debe reemplazarse porque oculta una distinción material. |
| **Jurisdiccional** | Debe contrastarse con la fuente oficial vigente y el contrato aplicable. |

!!! danger "Regla de interpretación"
    Ninguna etiqueta de una base de datos prueba por sí sola que un importe sea pagado, incurrido, reconocido, adeudado o cubierto. La semántica debe verificarse mediante reglas de negocio, trazabilidad a eventos y reconciliación contable u operativa.

## 2. Convenciones de idioma

| Término preferido | Uso recomendado | Evitar o precisar |
|---|---|---|
| *reserving* | Proceso completo de estimación, validación, selección, gobierno y comunicación de reservas | Traducirlo unas veces como “reservas” y otras como “provisionamiento” sin explicar el cambio |
| *ultimate* | Costo final estimado de una cohorte bajo una medida definida | “Final” si todavía puede haber reaperturas, recuperaciones o desarrollo de cola |
| *development* | Evolución de una medida a través de edades de desarrollo | “Crecimiento” cuando incluye disminuciones, reversos o recuperaciones |
| *runoff* | Desarrollo posterior de una cohorte o cartera cerrada | “Liquidación” si no implica extinción contractual |
| *backtesting* | Validación retrospectiva con cortes históricos reproducibles | Comparación contra información futura incorporada al entrenamiento |
| *paid* | Importe pagado bajo una regla de pago definida | “Cerrado” o “resuelto” como si fueran equivalentes |
| *incurred* | Medida reportada que, si no se precisa otra cosa, es pagado más reserva de caso | “Causado” sin reconciliar la definición contable u operativa |
| *case reserve* | Estimación registrada para reclamos reportados y pendientes | “IBNR” como sinónimo |
| *tail factor* | Factor para desarrollo posterior a la última edad observada | “Ajuste final” sin método ni horizonte |
| *link ratio* | Razón edad-a-edad observada o seleccionada | “CDF”, que es acumulativo hacia *ultimate* |

## 3. Notación canónica

Los subíndices $i$ y $j$ representan, respectivamente, periodo de origen y edad de desarrollo. Si un capítulo utiliza otra granularidad, debe declararla.

| Símbolo | Definición canónica |
|---|---|
| $i$ | Índice del periodo de origen: servicio, ocurrencia, reporte u otra cohorte declarada. |
| $j$ | Índice o edad de desarrollo desde el origen declarado. |
| $X_{i,j}$ | Importe incremental de la celda $(i,j)$. |
| $C_{i,j}$ | Importe acumulado: $C_{i,j}=\sum_{h=0}^{j}X_{i,h}$. La medida —pagado, incurrido, allowed u otra— debe indicarse. |
| $P_{i,j}$ | Pagos acumulados observados para origen $i$ a desarrollo $j$. |
| $O_{i,j}$ | Reserva de caso pendiente registrada para reclamos reportados. |
| $I_{i,j}$ | Incurrido reportado acumulado: $I_{i,j}=P_{i,j}+O_{i,j}$, salvo definición explícita distinta. |
| $U_i$ | Costo *ultimate* de la cohorte $i$ bajo una base, cobertura y horizonte definidos. |
| $R_i(C)$ | Reserva o desarrollo pendiente respecto de la medida observada $C$: $R_i(C)=U_i-C_{i,k_i}$. |
| $R_i^{(P)}$ | Pasivo de claims no pagados antes de otros ajustes: $R_i^{(P)}=U_i-P_{i,k_i}$. |
| $R_i^{(I)}$ | Desarrollo pendiente sobre incurrido reportado: $R_i^{(I)}=U_i-I_{i,k_i}$. |
| $f_j$ | Factor edad-a-edad desde $j$ hasta $j+1$. |
| $F_j$ | Factor acumulado desde $j$ hasta *ultimate*; también denominado CDF. |
| $p_{i,j}$ | Proporción estimada reportada, pagada o completada a $j$, según se declare. |
| $q_{i,j}$ | Proporción pendiente: $q_{i,j}=1-p_{i,j}$. |
| $E_i$ | Exposición correspondiente a la cohorte $i$. |
| $MM_i$ | Meses-miembro de la cohorte $i$. |
| $N_i$ | Conteo de reclamos, personas o eventos; el objeto contado debe declararse. |
| $S_i$ | Severidad media: costo dividido por el conteo coherente con ese costo. |
| $D_t$ | Información que estaba disponible en la fecha de valoración $t$. |
| $\widehat{\theta}$ | Estimación puntual de un parámetro o cantidad $\theta$. |

!!! note "La reserva depende de la base"
    Si $C=P$, $U-C$ representa claims no pagados. Si $C=I=P+O$, $U-C$ representa desarrollo adicional sobre lo ya reportado y reservado. Es incorrecto presentar ambos resultados como “IBNR” sin indicar la convención.

## 4. Distinciones que no deben colapsarse

### 4.1 Fechas y periodos

| Concepto | Evento que ordena el dato | Riesgo de confusión |
|---|---|---|
| Fecha de servicio | Prestación clínica o consumo cubierto | Puede diferir de ocurrencia, factura y reporte |
| Fecha de ocurrencia | Evento asegurado que origina la obligación | En salud puede ser episodio, servicio, diagnóstico o incapacidad, según cobertura |
| Fecha de reporte o radicación | Recepción formal de información o cuenta | No implica aceptación, adjudicación ni pago |
| Fecha de adjudicación | Decisión operativa sobre elegibilidad, cobertura e importe | Puede haber readjudicaciones y reversos |
| Fecha de pago | Movimiento de efectivo o compensación reconocida como pago | Puede diferir de la fecha contable |
| Fecha contable | Reconocimiento en un periodo financiero | Depende de políticas de cierre y contabilización |
| Fecha de valoración | Corte de información usado para estimar | Determina qué información pertenece a $D_t$ |
| Periodo de origen | Cohorte agrupada por servicio, ocurrencia, reporte u otra fecha | Debe nombrarse; “mes del claim” es insuficiente |
| Periodo calendario | Intersección entre origen y desarrollo | Mezcla efectos de múltiples cohortes y puede revelar shocks operativos |

### 4.2 Medidas monetarias

| Medida | Qué representa | No equivale necesariamente a |
|---|---|---|
| *Billed* / facturado | Valor presentado por proveedor o reclamante | Costo cubierto, allowed, incurrido o pagado |
| *Allowed* / reconocido | Importe elegible después de reglas contractuales, de red o de cobertura | Obligación final si faltan auditoría, coordinación o recuperaciones |
| Pagado | Efectivo o equivalente desembolsado según una regla definida | Claim cerrado, costo final o ausencia de obligación pendiente |
| Reserva de caso | Estimación registrada para reclamos reportados pendientes | Pago futuro exacto, IBNR puro o margen prudencial |
| Incurrido reportado | Normalmente, pagado más reserva de caso | Devengo contable, facturado o *ultimate* |
| *Ultimate* | Costo final estimado bajo base y horizonte definidos | Valor observado ni certeza contractual |
| Pasivo de claims no pagados | Parte del *ultimate* aún no pagada, con los componentes exigidos por la base aplicable | Desarrollo sobre incurrido reportado |
| Provisión contable | Importe reconocido bajo una norma contable | Mejor estimación actuarial o mínimo regulatorio |
| Mínimo regulatorio | Piso o metodología exigida por una autoridad | Mejor estimación, valor contable o obligación contractual completa |
| Margen | Ajuste explícito sobre una estimación central por un propósito definido | Incertidumbre predictiva ni error estándar |

### 4.3 Componentes de claims no pagados

Bajo la convención canónica $I=P+O$:

\[
R_i^{(P)}=U_i-P_i=O_i+\left(U_i-I_i\right).
\]

La expresión $U_i-I_i$ puede combinar reclamos verdaderamente no reportados e insuficiencia o exceso de reservas de caso. Por eso, el handbook aplica la siguiente política:

| Término | Definición preferida | Nota de uso |
|---|---|---|
| IBNR puro | Obligación por eventos incurridos que aún no han sido reportados a la entidad | No incluye reserva de caso |
| RBNS | Reserva para reclamos reportados pero no liquidados | Suele aproximarse con $O_i$, sujeto a la definición del sistema |
| IBNER | Desarrollo esperado por insuficiencia o exceso de la estimación registrada para reclamos reportados | Puede ser negativo; no es un margen |
| IBNR amplio | $U_i-I_i$, cuando la práctica local agrupa IBNR puro e IBNER | Debe rotularse “IBNR incluido IBNER” |
| Claims no pagados | $U_i-P_i$, antes o después de gastos, recuperables y descuento según se declare | Incluye reserva de caso y desarrollo pendiente |

### 4.4 Riesgo e incertidumbre

| Fuente | Definición | Ejemplo |
|---|---|---|
| Riesgo de proceso | Variación aleatoria de resultados aun con parámetros y modelo correctos | Conteos y severidades futuros |
| Riesgo de parámetro | Incertidumbre por estimar parámetros con una muestra finita | Factores de desarrollo inestables |
| Riesgo de modelo | Error por estructura, implementación o uso inadecuado del modelo | Cola mal especificada o dependencia ignorada |
| Riesgo de datos | Error, sesgo, ausencia o semántica incorrecta de los datos | Duplicados, truncamiento o cambios de códigos |
| Riesgo operativo | Falla de procesos que altera datos o resultados | Backlog, migración de plataforma o pagos represados |
| Riesgo contractual | Incertidumbre sobre derechos y obligaciones del contrato | Liquidaciones de PGP o recuperables discutidos |
| Riesgo regulatorio | Cambio o interpretación de requisitos aplicables | Nuevo piso, cobertura o regla de reconocimiento |
| Margen o ajuste prudencial | Decisión de añadir una cantidad por un objetivo de suficiencia | Percentil, costo de capital o PAD definido |

## 5. Glosario alfabético

### A

**Adjudicación (*adjudication*) — Preferido.** Proceso que determina elegibilidad, cobertura, reglas contractuales e importe reconocido de un reclamo. No equivale a pago; puede incluir negación, ajuste, reverso y readjudicación.

**ALAE (*allocated loss adjustment expense*).** Gasto de gestión asignable a un claim específico. Debe separarse del costo del beneficio cuando su inclusión cambie el alcance del *ultimate*. Véase también ULAE.

**Ajuste de nivel (*on-level adjustment*).** Transformación de experiencia histórica a una base comparable de tarifas, beneficios, precios, contratos o exposición. No debe confundirse con tendencia futura.

**Año de origen.** Periodo anual que agrupa eventos por una fecha definida. Use “año de servicio”, “año de ocurrencia” o “año de reporte” en lugar de “año del claim”.

**Apertura o reapertura.** Cambio de estado que vuelve a activar un claim cerrado o incrementa su obligación. Debe preservarse como evento, no sobrescribirse, si afecta el desarrollo histórico.

**ASOP (*Actuarial Standard of Practice*).** Estándar profesional emitido por el Actuarial Standards Board de Estados Unidos. En este handbook es fuente de buenas prácticas cuando resulte pertinente, no una norma colombiana.

**Auditoría de trazabilidad (*audit trail*).** Evidencia reproducible de fuentes, transformaciones, parámetros, ejecuciones, revisiones y aprobaciones que permite reconstruir un resultado.

### B

**Backlog.** Inventario de reclamos, facturas o transacciones pendientes de procesamiento. Puede distorsionar la diagonal reciente y crear patrones calendario que un método de desarrollo no corrige por sí solo.

**Backtesting — Preferido.** Evaluación de un método desde cortes históricos *as-of*, usando solamente información que habría estado disponible en cada fecha. Un backtest con datos futuros filtrados no es evidencia fuera de muestra.

**Benchmark.** Método simple, estable y reproducible contra el cual se compara un candidato. No tiene que ser el método final; debe ser suficientemente defendible para revelar si la complejidad añade valor.

**Benktander.** Método de credibilidad que actualiza iterativamente una expectativa previa con experiencia emergente. Suele ubicarse entre Bornhuetter-Ferguson y Chain Ladder en sensibilidad a los datos observados.

**Billed — Preferido en inglés cuando exista ambigüedad.** Importe facturado o cobrado antes de aplicar reglas de reconocimiento, cobertura, contrato o auditoría.

**Bornhuetter-Ferguson (BF).** Método que combina un *ultimate* esperado independiente con la proporción no desarrollada. La experiencia observada no redefine mecánicamente el *ultimate* completo de periodos inmaduros.

**Bootstrap Chain Ladder.** Procedimiento de remuestreo, normalmente basado en residuos de un modelo compatible con Chain Ladder, para aproximar una distribución predictiva. Su validez depende del esquema de residuos, la estructura media-varianza y el tratamiento de la cola.

### C

**Calendario (*calendar period*).** Periodo determinado conjuntamente por origen y desarrollo. Es útil para identificar inflación, cambios de sistema, backlog o políticas que afectan varias cohortes en el mismo momento.

**Cape Cod.** Método que estima una relación de costo esperado respecto de exposición usando experiencia agregada y desarrollo. Requiere exposición comparable y homogeneidad suficiente después de ajustes.

**Capitación — Jurisdiccional/contractual.** Pago prospectivo por persona y periodo para un conjunto definido de servicios y responsabilidades. No debe modelarse como fee-for-service sin reconciliar liquidaciones, exclusiones y riesgo transferido.

**Case reserve.** Véase **reserva de caso**.

**CDF (*cumulative development factor*).** Factor acumulado desde una edad de desarrollo hasta *ultimate*: $F_j=\prod_{h=j}^{J-1} f_h$, incluyendo cola cuando corresponda. No es un *link ratio* individual.

**Cierre de claim.** Estado operativo que indica que no se espera actividad adicional bajo una regla del sistema. No prueba que el costo sea *ultimate* ni impide reaperturas.

**Claim — Ambiguo.** Unidad de reclamación. Puede significar persona, episodio, factura, cuenta, autorización, servicio o línea. Todo dataset debe declarar su unidad y una llave estable.

**Claim de alto costo.** Claim, episodio o persona cuyo costo excede un umbral definido. El umbral, la base —bruta o neta—, el periodo y el tratamiento del exceso deben documentarse.

**Claims no pagados (*unpaid claims*).** Obligación estimada atribuible a claims y gastos incluidos que todavía no se ha pagado a la fecha de valoración. Véase $R^{(P)}$.

**Cohorte.** Conjunto de observaciones que comparten un origen o característica definida. Una cohorte no es necesariamente un periodo de calendario.

**Completitud.** Proporción de una cantidad *ultimate* que se estima observada a una edad determinada. Debe indicar si se refiere a reporte, adjudicación, reconocimiento o pago.

**Completion factor.** Véase **factor de completitud**.

**Condiciones cambiantes (*changing conditions*).** Cambios conocidos o razonablemente esperados que reducen la comparabilidad histórica: beneficios, red, precios, mix, regulación, sistemas, prácticas de reserva o adjudicación.

**Coordinación de beneficios (COB).** Reglas para distribuir responsabilidad cuando varias coberturas podrían pagar el mismo servicio. Puede generar recuperaciones o ajustes tardíos.

**Credibilidad.** Grado de peso asignado a experiencia observada respecto de una expectativa externa. Debe depender de volumen, estabilidad, madurez y calidad, no solo de edad de desarrollo.

**Curva de runout.** Perfil temporal de reporte, adjudicación o pago posterior al periodo de servicio. Puede expresarse mediante proporciones acumuladas o distribuciones de rezago.

### D

**Data leakage.** Véase **filtración de información**.

**Denegación (*denial*).** Decisión de no reconocer total o parcialmente un reclamo bajo una regla de cobertura o procesamiento. Debe distinguirse de devolución, glosa y error técnico.

**Descuento.** Conversión de flujos futuros a valor presente con una curva y convención definidas. No debe aplicarse si la base de medición exige valores nominales.

**Desviance.** Medida de discrepancia entre observaciones y un modelo de familia exponencial, comparada con un modelo saturado. Su escala y distribución dependen de la familia.

**Diagonal.** Conjunto de celdas observadas en el mismo corte de calendario dentro de un triángulo. La última diagonal contiene la información más reciente y suele ser la más expuesta a cambios operativos.

**Distribución predictiva.** Distribución de resultados futuros o cantidades no observadas que integra las fuentes de incertidumbre incluidas en el modelo. No es equivalente a la distribución de un parámetro.

**Drift.** Cambio persistente en la distribución de datos, relaciones predictivas o desempeño. Puede ser poblacional, clínico, contractual, operativo o de concepto.

### E

**Edad de desarrollo.** Tiempo transcurrido desde el origen hasta la observación. Debe indicar unidad, convención de extremos y si corresponde a meses completos, cortes contables o periodos discretos.

**ELR (*expected loss ratio*).** Razón esperada de costo *ultimate* a prima o ingreso expuesto definido. En salud puede ser inadecuada si la prima no es comparable o si la obligación se gestiona mejor por exposición poblacional.

**Error estándar.** Desviación estándar estimada de un estimador bajo un modelo. No representa automáticamente la distribución total de la obligación ni un margen prudencial.

**Escenario.** Conjunto coherente de supuestos sobre condiciones futuras. No debe asignársele probabilidad implícita sin una base explícita.

**Estacionalidad.** Patrón recurrente asociado con el calendario, como días hábiles, vacaciones, epidemias estacionales o ciclos de beneficios. No equivale a tendencia.

**Estimación central.** Media, mediana u otra medida seleccionada como punto de referencia. Debe declarar cuál funcional de la distribución representa.

**Exposición.** Medida del volumen de riesgo al que corresponde el costo: meses-miembro, pólizas, vidas, nómina, estancias u otra unidad. Debe ser coherente con cobertura, elegibilidad y periodo.

### F

**Factor de completitud.** Proporción acumulada estimada observada a una edad: $p_j$. Si se deriva de un CDF sin ajustes, $p_j=1/F_j$. Debe nombrarse “de reporte”, “de reconocimiento” o “de pago”.

**Factor de cola (*tail factor*).** Factor que representa desarrollo más allá de la última edad observada. Su selección debe incluir horizonte, extrapolación, sensibilidad y riesgo de reaperturas o recuperaciones.

**Factor de desarrollo edad-a-edad.** Multiplicador $f_j$ que relaciona acumulados de edades consecutivas. Un promedio histórico es un estimador, no una propiedad fija del portafolio.

**Fee-for-service (FFS).** Modalidad en la que el pago se asocia con servicios individuales. La existencia de tarifas por servicio no elimina auditoría, paquetes, topes ni recuperaciones.

**Filtración de información (*data leakage*).** Uso directo o indirecto de información no disponible en la fecha que el modelo pretende simular. Incluye variables futuras, cohortes reetiquetadas y transformaciones calculadas con toda la muestra.

**Frecuencia.** Número de eventos por unidad de exposición. El evento contado debe ser estable y compatible con la severidad.

**Frecuencia-severidad.** Descomposición del costo en conteo y costo medio. Resulta útil cuando sus mecanismos y variables explicativas difieren.

### G

**GAM (*generalized additive model*).** Extensión de un GLM que representa efectos mediante funciones suaves. La flexibilidad debe controlarse mediante penalización, grados de libertad y validación temporal.

**Gate eliminatorio.** Criterio mínimo que un método o dataset debe superar antes de ser puntuado. Un gate fallido no se compensa promediando scores.

**Giro directo — Jurisdiccional.** Mecanismo mediante el cual un pagador designado transfiere recursos directamente a un prestador u otro receptor. Debe determinarse si extingue, reduce o solo cambia el canal de una obligación para la entidad analizada.

**GLM (*generalized linear model*).** Modelo con distribución de familia exponencial, predictor lineal y función de enlace. Deben declararse familia, enlace, offset, estructura de varianza y unidad de observación.

**Glosa — Jurisdiccional.** Objeción total o parcial a una cuenta o concepto facturado dentro de un proceso definido. No equivale automáticamente a ahorro, denegación definitiva, reverso contable ni ausencia de obligación.

**Gobierno de modelos.** Políticas, roles y controles para inventario, cambios, acceso, validación, aprobación, ejecución, monitoreo, documentación y retiro de modelos.

### H

**Holdout.** Muestra separada que no participa en ajuste ni selección de hiperparámetros y se reserva para evaluación final. En reserving debe respetar el orden temporal y el corte *as-of*.

**Hiperparámetro.** Configuración del proceso de estimación que no se ajusta como un parámetro ordinario, por ejemplo profundidad, penalización o número de árboles. Su selección pertenece al proceso de entrenamiento y no al holdout final.

### I

**IBNER (*incurred but not enough reported*).** Diferencia esperada entre el costo final de claims ya reportados y su estimación registrada. Puede reflejar insuficiencia o redundancia de reservas de caso.

**IBNR (*incurred but not reported*) — Ambiguo por práctica.** En sentido estricto, costo de eventos incurridos aún no reportados. En usos amplios puede incluir IBNER. El handbook exige indicar “IBNR puro” o “IBNR incluido IBNER”.

**Incurrido reportado (*reported incurred*).** Bajo la convención del handbook, pagado más reserva de caso. Si un sistema incluye otros devengos, autorizaciones o provisiones, debe usarse otro nombre o declararse la composición.

**Incremental.** Importe reconocido durante una celda de desarrollo, no acumulado desde el origen. Puede ser negativo por reversos, recuperaciones o cambios de estimación.

**Intended purpose.** Objetivo específico para el que se diseña y usa un modelo, incluidos decisión, alcance, medida y horizonte. La validez es relativa a este propósito.

**Intended user.** Persona o grupo cuya toma de decisiones se pretende apoyar. No incluye automáticamente a cualquier tercero que reciba el resultado.

**Intervalo de confianza.** Procedimiento frecuentista que, bajo repeticiones y supuestos del modelo, cubre el parámetro objetivo con una frecuencia nominal. No asigna probabilidad posterior al parámetro observado.

**Intervalo creíble.** Región de una distribución posterior que contiene una probabilidad especificada del parámetro o cantidad. Depende del prior, la verosimilitud y la estructura del modelo.

**Intervalo predictivo.** Intervalo para una observación o resultado futuro. Debe incluir la variación de proceso y, cuando corresponda, incertidumbre de parámetros y modelo.

### J

**Juicio actuarial.** Evaluación profesional explícita que integra datos, teoría, operación, contratos, regulación y materialidad. No es una justificación suficiente si no se documentan evidencia, alternativas y sensibilidad.

### L

**Large claim.** Véase **claim de alto costo**.

**Liability / pasivo.** Obligación reconocida o medida bajo un marco definido. No debe usarse como sinónimo automático de estimación actuarial, reserva de caso o provisión regulatoria.

**Link ratio.** Véase **factor de desarrollo edad-a-edad**.

**Loss ratio.** Razón entre costo y prima o ingreso definido. Debe indicarse si el numerador es pagado, incurrido o *ultimate* y si el denominador es emitido, devengado o expuesto.

### M

**Machine learning.** Familia amplia de métodos orientados a aprender patrones predictivos. No implica por sí sola mayor precisión, causalidad, adecuada incertidumbre ni aptitud regulatoria.

**Mack Chain Ladder.** Marco estocástico de distribución libre que estima error estándar de Chain Ladder bajo supuestos condicionales de media, varianza e independencia entre periodos de origen. No modela automáticamente riesgo de cola o estructura futura.

**Margen.** Cantidad añadida o sustraída de una estimación central por un objetivo de prudencia, suficiencia o compensación de riesgo. Debe separarse de la media y documentar base, diversificación y horizonte.

**Materialidad.** Umbral cualitativo y cuantitativo a partir del cual una omisión, error o cambio podría influir en decisiones de usuarios previstos. No es una propiedad universal de una cifra.

**Mes-miembro (*member month*).** Una persona elegible durante un mes según una convención definida. Las fracciones, retroactividad, duplicados y múltiples productos requieren reglas explícitas.

**Método prescrito.** Método exigido por ley, regulación, contrato u otra autoridad identificada. Debe diferenciarse de un método seleccionado por juicio profesional.

**Métrica de evaluación.** Función usada para comparar predicciones y resultados. Debe alinearse con la decisión y no concentrarse únicamente en promedios si importan colas o sesgos por segmento.

**Modelo.** Representación simplificada de relaciones entre entradas, supuestos y resultados, implementada mediante reglas, fórmulas, estadística o algoritmos. Una hoja de cálculo puede ser un modelo.

**Model risk.** Véase **riesgo de modelo**.

**Munich Chain Ladder.** Método que utiliza conjuntamente información pagada e incurrida para ajustar desarrollo cuando sus desviaciones contienen información complementaria. Requiere bases reconciliadas y prácticas de reserva de caso suficientemente interpretables.

**Modelo multiestado.** Modelo de transiciones entre estados como no reportado, reportado, objetado, conciliado, pagado, cerrado o reabierto. Los estados deben ser mutuamente interpretables aunque no necesariamente absorbentes.

### O

**Offset.** Componente conocido del predictor lineal, frecuentemente $\log(E_i)$, cuyo coeficiente se fija en uno. No es una covariable libre.

**Origen.** Dimensión que agrupa la experiencia por la fecha que inicia el desarrollo. Debe declararse el evento y la granularidad.

**Overdispersion / sobredispersión.** Variabilidad superior a la impuesta por una distribución de referencia, por ejemplo Poisson. Puede indicar heterogeneidad, dependencia o especificación incompleta.

### P

**Pagado (*paid*).** Importe desembolsado o compensado hasta una fecha, neto o bruto según se indique. Las reglas para cheques anulados, anticipos, pagos directos y recuperaciones deben documentarse.

**Parámetro.** Cantidad fija pero desconocida dentro de un modelo. Debe distinguirse de una observación futura y de un hiperparámetro.

**Percentil.** Valor $q_\alpha$ tal que una proporción $\alpha$ de la distribución queda en o por debajo, según convención. Su interpretación depende de la distribución modelada.

**Periodo de desarrollo.** Intervalo discreto usado para medir maduración. No siempre coincide con un mes calendario exacto.

**PGP (pago global prospectivo) — Jurisdiccional/contractual.** Acuerdo prospectivo por un conjunto de servicios, población, periodo y reglas de liquidación. El acrónimo no determina por sí solo qué riesgo fue transferido.

**PMPM (*per member per month*).** Costo o ingreso por mes-miembro: $\mathrm{PMPM}=\text{importe}/MM$. El numerador y la elegibilidad del denominador deben compartir cobertura y periodo.

**Población expuesta.** Conjunto de personas o unidades que cumplen las reglas de elegibilidad para una cobertura y periodo. No equivale necesariamente a afiliados registrados al cierre.

**Posterior.** Distribución bayesiana de parámetros o cantidades después de combinar prior y verosimilitud.

**Posterior predictiva.** Distribución de datos o resultados futuros que integra la posterior de parámetros y la variación condicional del proceso.

**Prior.** Distribución o expectativa anterior a la evidencia modelada. Puede basarse en experiencia externa, presupuesto, tarifas o juicio; su fuente y sensibilidad deben declararse.

**Proporción no reportada.** $q_j=1-p_j$, donde $p_j$ es una proporción de reporte definida. No es idéntica a la proporción no pagada.

**Provisión.** Importe reconocido bajo un marco contable, regulatorio o de gestión específico. Debe nombrarse el marco; no usar como equivalente universal de reserva.

### R

**Radicación — Jurisdiccional/operativa.** Recepción formal de una factura, cuenta o reclamación bajo requisitos definidos. Puede no coincidir con el primer conocimiento del evento ni con su aceptación.

**RBNS (*reported but not settled*).** Componente para reclamos reportados y no liquidados. Puede aproximarse mediante reservas de caso, pero la equivalencia depende de estados y reglas del sistema.

**Reaseguro.** Transferencia contractual de riesgo a un reasegurador. Las reservas deben identificar base bruta, recuperables, riesgo de crédito, límites, reinstalaciones y disputas.

**Reconciliación.** Demostración cuantitativa de cómo una medida se transforma o enlaza con otra, explicando diferencias por alcance, fecha, estado y fuente.

**Recuperable.** Importe que se espera cobrar a un tercero, como reasegurador, otro pagador o proveedor. No debe netearse sin declarar contraparte, cobrabilidad y base de presentación.

**Reembolso.** Pago posterior por un costo elegible asumido inicialmente por otra parte. No es sinónimo de recuperable hasta que se define el derecho y su estado.

**Reporte (*reporting*).** Evento mediante el cual la entidad conoce formalmente un claim bajo una regla definida. Difiere de servicio, autorización, radicación y adjudicación.

**Reserva — Ambiguo.** Estimación o importe apartado para obligaciones futuras. El texto debe precisar si es reserva de caso, IBNR, claims no pagados, gasto, margen, provisión contable o mínimo regulatorio.

**Reserva de caso (*case reserve*).** Estimación registrada para la parte pendiente de reclamos ya reportados. Puede ser positiva, cero o, en algunos sistemas, neta de ajustes; su práctica puede cambiar con el tiempo.

**Residual.** Diferencia o transformación de la diferencia entre observado y ajustado. Pearson, deviance y residuos escalados no son intercambiables.

**Retroactividad.** Registro posterior con efecto sobre elegibilidad, cobertura, precio o estado de un periodo anterior. Debe conservarse tanto la fecha efectiva como la fecha de conocimiento.

**Reverso.** Transacción que anula total o parcialmente un registro anterior. No debe eliminarse como “dato negativo” sin investigar el mecanismo.

**Riesgo de datos.** Posibilidad de una decisión incorrecta por datos inadecuados, incompletos, sesgados, desactualizados o mal interpretados.

**Riesgo de modelo.** Posibilidad de efectos adversos por error conceptual, supuestos, datos, implementación, uso, interpretación o cambio fuera del dominio validado.

**Runoff.** Desarrollo observado después de una fecha de valoración o durante la extinción de una cartera. Los estudios de runoff comparan estimaciones anteriores con experiencia emergente.

### S

**Segmentación.** División de experiencia en grupos con mecanismos suficientemente homogéneos. Aumenta interpretabilidad, pero demasiada granularidad reduce credibilidad y estabilidad.

**Severidad.** Costo medio por evento, persona o claim definido. Debe usar el mismo universo y base monetaria que la frecuencia relacionada.

**Shock.** Cambio abrupto que no se explica adecuadamente mediante tendencia gradual. Puede requerir escenario o variable estructural, no extrapolación histórica.

**Spline.** Función por tramos unida bajo restricciones de continuidad, usada en GAM y curvas de desarrollo. Su complejidad se controla con base y penalización.

**Stop-loss.** Cobertura o acuerdo que limita pérdidas por encima de un umbral individual o agregado. Deben modelarse prioridad, límite, periodo, acumulación y cobrabilidad.

**Subrogación.** Derecho de recuperar de un tercero importes pagados bajo circunstancias definidas. El reconocimiento depende de probabilidad, medición y base aplicable.

**Supervisión humana.** Revisión y capacidad efectiva de cuestionar entradas, supuestos, cambios y resultados. No se satisface con una aprobación formal sin evidencia.

**Survival analysis / análisis de supervivencia.** Métodos para tiempo hasta evento con censura y, en ocasiones, riesgos competidores. En reserving puede modelar reporte, pago, cierre o transición.

### T

**Tabular method.** Método que aplica tasas, costos o factores a categorías de exposición o claims. Su simplicidad no elimina necesidad de validar categorías y supuestos.

**Tail factor.** Véase **factor de cola**.

**Tendencia médica (*medical trend*).** Cambio temporal del costo médico por precios, utilización, intensidad, mix, beneficios y otros factores. No equivale a inflación general ni a crecimiento observado sin ajuste de exposición.

**Triángulo de desarrollo.** Matriz por origen y desarrollo cuya zona observada tiene forma triangular en un corte. La agregación supone comparabilidad suficiente dentro de filas, columnas y diagonales.

**TVaR (*tail value at risk*).** Promedio de pérdidas en la cola más allá de un percentil, bajo una convención definida. Requiere una distribución predictiva suficientemente confiable en extremos.

**Tweedie.** Familia de distribuciones de dispersión exponencial que, para ciertos parámetros de potencia, admite masa en cero y valores positivos continuos. Es útil para costo agregado, pero exige validar enlace, potencia y dispersión.

### U

**ULAE (*unallocated loss adjustment expense*).** Gasto de administración de claims que no se asigna a un claim individual. Su provisión requiere un método y una base separados si es material.

**Ultimate — Preferido.** Costo final estimado para una cohorte, después del desarrollo incluido en la definición. Debe especificar bruto/neto, beneficios/gastos, descuento, recuperables y horizonte.

**Utilización.** Frecuencia o intensidad de uso de servicios por unidad de exposición. No debe inferirse únicamente de pagos si hay cambios de precio o procesamiento.

### V

**Validación.** Evaluación de adecuación conceptual, datos, implementación, desempeño, estabilidad, limitaciones y uso para el propósito previsto. No es sinónimo de obtener un buen ajuste dentro de muestra.

**Valoración *as-of*.** Estimación reconstruida con información disponible hasta un corte histórico. Requiere versiones temporales de datos y transformaciones.

**VaR (*value at risk*).** Percentil de una distribución de pérdida para un nivel y horizonte. No describe la magnitud media más allá del percentil.

**Verosimilitud.** Función de los parámetros inducida por un modelo probabilístico para los datos observados. No es la probabilidad de que el modelo sea verdadero.

## 6. Términos institucionales y operativos de Colombia

Esta sección ofrece orientación semántica mínima. Todas las definiciones deben verificarse contra regulación oficial, contratos y manuales operativos vigentes en la fecha analizada.

| Término | Uso controlado en el handbook | Precaución |
|---|---|---|
| ADRES | Entidad administradora de recursos del sistema de salud colombiano | Verificar funciones, mecanismos y denominaciones vigentes; no asumir que todo flujo administrado es ingreso o recuperable de una EPS |
| ARL | Entidad asociada con cobertura de riesgos laborales bajo el marco aplicable | No equiparar su exposición, beneficios ni rezagos con salud general |
| EPS | Entidad responsable de funciones de aseguramiento o gestión del riesgo en salud bajo el régimen aplicable | La obligación depende de cobertura, contratos, mecanismos de financiación y regulación vigente |
| IPS | Prestador de servicios de salud | Sus cuentas por cobrar, ingresos, glosas y deterioro no son automáticamente el IBNR de un asegurador |
| MIPRES | Sistema o mecanismo de prescripción y reporte de tecnologías o servicios según el marco colombiano aplicable | Un registro no prueba por sí solo prestación, cobertura, reconocimiento o pago |
| PBS | Conjunto o plan de beneficios definido por la regulación aplicable | Alcance y terminología pueden cambiar; verificar fecha de vigencia |
| RIPS | Registros individuales de prestación de servicios de salud | La existencia de un registro no garantiza completitud financiera ni elegibilidad |
| FEV-RIPS | Articulación de factura electrónica y soportes de información de servicios, según especificaciones vigentes | Distinguir validación técnica, radicación, reconocimiento y pago |
| UPC | Unidad o pago por capitación definido dentro de la financiación del sistema | No es sinónimo de prima comercial, ingreso disponible ni costo esperado |
| Glosa | Objeción dentro del proceso de revisión de cuentas | Distinguir glosa inicial, respuesta, levantamiento, ratificación, conciliación y resultado financiero |
| Devolución | Retorno de una cuenta o factura por causal definida | Puede ocurrir antes de una evaluación de fondo; no tratar siempre como glosa |
| Conciliación | Proceso para resolver diferencias entre partes | Debe modelarse el momento, probabilidad e importe del resultado, no solo el estado nominal |

!!! warning "No equivalencia entre actores"
    EPS, IPS, medicina prepagada, ARL, aseguradoras y reaseguradores no deben compartir un modelo solo porque usan vocabulario parecido. Cambian la obligación, la exposición, la unidad de cuenta, los contratos y la base regulatoria.

## 7. Términos que requieren calificador obligatorio

| Término incompleto | Calificadores mínimos |
|---|---|
| Reserva | Componente, base, bruto/neto, gastos incluidos y fecha |
| IBNR | Puro o incluido IBNER; sobre paid o incurred; beneficios/gastos |
| Incurrido | Composición exacta y sistema fuente |
| Costo | Billed, allowed, pagado, incurrido o *ultimate*; bruto/neto |
| Claim | Unidad: persona, episodio, cuenta, factura, autorización, servicio o línea |
| Fecha del claim | Servicio, ocurrencia, reporte, radicación, adjudicación o pago |
| Exposición | Unidad, elegibilidad, cobertura, producto y periodo |
| Factor | Edad-a-edad, CDF, completitud, cola, tendencia u otro |
| Precisión | Métrica, horizonte, muestra y benchmark |
| Intervalo | Confianza, creíble o predictivo; nivel y fuentes de incertidumbre |
| Resultado neto | Recuperables, reaseguro, glosas, copagos, descuento e impuestos incluidos |
| Regla regulatoria | Autoridad, norma, versión, vigencia y entidad a la que aplica |

## 8. Abreviaturas

| Abreviatura | Expansión |
|---|---|
| ALAE | *Allocated loss adjustment expense* |
| BF | Bornhuetter-Ferguson |
| CDF | *Cumulative development factor* |
| COB | *Coordination of benefits* |
| ELR | *Expected loss ratio* |
| FFS | *Fee-for-service* |
| GAM | *Generalized additive model* |
| GLM | *Generalized linear model* |
| IBNER | *Incurred but not enough reported* |
| IBNR | *Incurred but not reported* |
| MM | Meses-miembro |
| PGP | Pago global prospectivo |
| PMPM | *Per member per month* |
| RBNS | *Reported but not settled* |
| TVaR | *Tail value at risk* |
| ULAE | *Unallocated loss adjustment expense* |
| VaR | *Value at risk* |

## 9. Política para incorporar o modificar términos

Una propuesta de cambio debe incluir:

1. término preferido y categoría;
2. definición operacional y, si aplica, fórmula;
3. alias, traducciones y términos que no son equivalentes;
4. capítulos, variables y tablas afectados;
5. evidencia técnica, contractual o regulatoria;
6. impacto retrospectivo en resultados y reproducibilidad;
7. revisor responsable y fecha de vigencia.

Los términos eliminados no deben desaparecer silenciosamente. Se mantienen como alias desaconsejados con referencia al término canónico hasta completar la migración de contenido y código.

## 10. Checklist editorial

Antes de aprobar un capítulo o modelo:

- [ ] El evento de origen y la edad de desarrollo están definidos.
- [ ] La unidad de claim y sus llaves están documentadas.
- [ ] *Paid*, *incurred*, *allowed* y *billed* no se mezclan.
- [ ] IBNR puro, IBNER, RBNS y claims no pagados se distinguen.
- [ ] El *ultimate* declara alcance, base, horizonte y tratamiento de gastos.
- [ ] La reserva indica si se calcula contra pagado o incurrido reportado.
- [ ] Exposición y meses-miembro usan reglas de elegibilidad reproducibles.
- [ ] Factores de desarrollo, completitud y cola no se intercambian.
- [ ] Estimación central, incertidumbre predictiva y margen se presentan por separado.
- [ ] Intervalos de confianza, creíbles y predictivos se nombran correctamente.
- [ ] Los términos colombianos tienen fuente, vigencia y entidad aplicable.
- [ ] Los alias de código y de bases de datos se mapean al término canónico.
- [ ] Toda excepción queda registrada con justificación y revisor.

## 11. Fuentes y criterio de evidencia

Este vocabulario sintetiza convenciones actuariales, estadísticas y operativas usadas a lo largo del handbook. Entre sus fuentes conceptuales se encuentran ASOP 5 para claims de salud, ASOP 23 para calidad de datos, ASOP 28 para opiniones sobre activos y pasivos de salud, ASOP 41 para comunicaciones actuariales, ASOP 43 como referencia comparativa de estimaciones de claims no pagados y ASOP 56 para modelación y riesgo de modelo.

Los estándares profesionales establecen expectativas de proceso y comunicación; no convierten una definición en norma local ni demuestran que un método sea predictivamente superior. Para aplicaciones colombianas, las fuentes primarias vigentes y los contratos prevalecen sobre este glosario.

## 12. Próximo archivo

La siguiente pieza de infraestructura editorial es:

```text
docs/bibliography.md
```

La bibliografía debe registrar fuente primaria, versión, alcance, capítulos que la utilizan y cualquier limitación jurisdiccional o de vigencia.
