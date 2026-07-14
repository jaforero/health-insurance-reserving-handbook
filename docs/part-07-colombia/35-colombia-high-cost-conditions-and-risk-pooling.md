---
title: "Colombia High-Cost Conditions and Risk Pooling"
part: "Parte VII · Colombia"
chapter: 35
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

# Colombia High-Cost Conditions and Risk Pooling

Este capítulo desarrolla un marco actuarial para modelar condiciones de alto costo, eventos catastróficos y mecanismos de mutualización de riesgo en el sistema de salud colombiano. El foco está en la relación entre alto costo, Cuenta de Alto Costo, MIPRES, presupuestos máximos, UPC, reservas IBNR y esquemas de compensación ex post.

En salud, una fracción pequeña de afiliados puede explicar una porción material del gasto total. Este fenómeno no es un accidente estadístico: es una característica estructural de portafolios sanitarios con enfermedades crónicas avanzadas, tratamientos biológicos, oncología, enfermedad renal crónica, VIH, enfermedades huérfanas, trasplantes, UCI, terapias génicas, medicamentos innovadores y eventos agudos de severidad extrema.

El problema actuarial no es solo estimar el costo promedio. Es estimar la distribución completa del costo agregado, sus colas, su volatilidad, la concentración por condición y la capa financiera que debe asumir cada actor.

## Objetivos de aprendizaje

Al terminar este capítulo, el lector debería poder:

- Identificar por qué las condiciones de alto costo requieren tratamiento actuarial separado.
- Diferenciar riesgo esperado, riesgo extremo, riesgo crónico persistente y riesgo catastrófico.
- Diseñar capas de financiamiento entre UPC, ajuste por morbilidad, MIPRES, presupuestos máximos, Cuenta de Alto Costo y mecanismos de pooling.
- Formular modelos de riesgo colectivo para eventos de baja frecuencia y alta severidad.
- Conectar alto costo con reservas IBNR, liquidez, suficiencia y solvencia.
- Definir indicadores de monitoreo para cohortes de alto costo.
- Diseñar controles para evitar doble conteo, selección de riesgos e incentivos perversos.

## 1. Qué es alto costo en salud

Alto costo no debe definirse únicamente por monto absoluto. Una condición o evento puede ser de alto costo por varias razones:

- severidad financiera individual;
- persistencia multianual;
- baja frecuencia y alta varianza;
- concentración en pocos pacientes;
- dependencia de tecnologías o medicamentos innovadores;
- requerimiento de atención especializada;
- necesidad de seguimiento clínico continuo;
- exposición a litigios, tutelas, glosas o disputas;
- rezagos largos de autorización, facturación, auditoría o pago.

Una definición operativa útil clasifica el alto costo en cuatro categorías:

| Categoría | Ejemplos | Rasgo actuarial dominante |
|---|---|---|
| Crónico persistente | ERC, VIH, diabetes complicada | Alta recurrencia y predictibilidad parcial |
| Catastrófico agudo | UCI prolongada, trauma severo, trasplante | Severidad extrema y baja frecuencia |
| Innovación tecnológica | Terapias biológicas, oncológicos, terapias génicas | Inflación médica y riesgo de adopción |
| Huérfano o raro | Enfermedades huérfanas, medicamentos ultraespecializados | Muy baja frecuencia, cola severa |

Cada categoría requiere una técnica distinta. Un modelo promedio por afiliado es insuficiente para capturar cola, persistencia y concentración.

## 2. Por qué la UPC no basta para alto costo extremo

La UPC es una herramienta de financiamiento prospectivo. Puede funcionar razonablemente para gasto esperado recurrente si la población es suficientemente grande y el riesgo está bien mutualizado. Sin embargo, las condiciones de alto costo generan problemas cuando:

- la frecuencia es baja y volátil;
- la severidad es extrema;
- la población expuesta por EPS o región es pequeña;
- el evento no está bien capturado por variables demográficas;
- el tratamiento está fuera del paquete ordinario de financiación;
- el costo depende de decisiones clínicas, judiciales o regulatorias;
- el pago ocurre con rezagos relevantes.

En términos de riesgo agregado:

$$
S = \sum_{j=1}^{N} X_j
$$

donde:

- \(N\) es el número aleatorio de eventos de alto costo;
- \(X_j\) es la severidad del evento \(j\);
- \(S\) es la pérdida agregada del periodo.

El valor esperado \(E[S]\) es necesario, pero no suficiente. Para solvencia, liquidez y presupuestos máximos también importan:

- percentiles altos de \(S\);
- varianza;
- TVaR;
- concentración por condición;
- sensibilidad a nuevos tratamientos;
- dependencia entre eventos;
- rezagos de reporte y pago.

Un presupuesto basado solo en media histórica puede subestimar la cola si la distribución cambia o si pocos pacientes concentran costos excepcionales.

## 3. Capas de financiamiento

Un diseño técnico razonable debe separar capas. La separación evita mezclar riesgos de naturaleza distinta y reduce doble conteo.

| Capa | Riesgo cubierto | Instrumento esperado |
|---|---|---|
| Capa 1 | Morbilidad común y gasto ordinario | UPC base + ajuste demográfico |
| Capa 2 | Morbilidad crónica predecible | UPC ajustada por morbilidad |
| Capa 3 | Alto costo recurrente identificado | Cuenta de Alto Costo / compensación clínica |
| Capa 4 | Tecnologías No UPC o MIPRES | Presupuestos máximos / modelo específico |
| Capa 5 | Eventos extremos no diversificables | Pooling, corredor, reaseguro o fondo catastrófico |
| Capa 6 | Choques sistémicos | Reserva macro, ajuste regulatorio o financiación extraordinaria |

La pregunta clave es: ¿qué capa paga qué riesgo?

Si esta definición no es explícita, el sistema puede pagar dos veces el mismo riesgo o, por el contrario, dejar una brecha sin financiación.

## 4. Cuenta de Alto Costo como mecanismo de pooling

La Cuenta de Alto Costo puede entenderse actuarialmente como un mecanismo de seguimiento, gestión y compensación parcial para condiciones de alta carga. Su valor no está solo en transferir recursos, sino en construir información comparable sobre cohortes clínicas.

Desde una perspectiva de reserving, la información de alto costo permite:

- identificar cohortes de gasto persistente;
- estimar severidad esperada por estadio clínico;
- medir incidencia y prevalencia;
- proyectar transiciones de enfermedad;
- monitorear calidad, oportunidad y resultados;
- segmentar reservas por condición;
- anticipar presión sobre liquidez.

El riesgo técnico es tratar la Cuenta de Alto Costo como sustituto de un modelo prospectivo de morbilidad. No lo es. Debe verse como una capa complementaria.

## 5. MIPRES, No UPC y presupuestos máximos

MIPRES y los presupuestos máximos concentran un problema actuarial distinto: tecnologías, servicios o medicamentos que pueden presentar baja frecuencia, alta severidad y rápida inflación médica.

El cálculo retrospectivo simple tipo precio por cantidad puede ser débil cuando:

- hay pocos casos y alta volatilidad;
- entran nuevas tecnologías;
- cambia la indicación clínica;
- se judicializa el acceso;
- cambia el precio unitario;
- existe sustitución terapéutica;
- hay incertidumbre sobre persistencia del tratamiento;
- hay concentración regional o por prestador.

Para estos riesgos, el enfoque debe pasar de promedio histórico a distribución de pérdida agregada.

## 6. Modelo de riesgo colectivo

El modelo de riesgo colectivo separa frecuencia y severidad:

$$
S = X_1 + X_2 + \dots + X_N
$$

con:

$$
N \sim \text{Poisson}(\lambda), \quad X_j \sim F_X
$$

o alternativas:

- \(N \sim\) binomial negativa si hay sobredispersión;
- \(X \sim\) gamma, lognormal, Pareto o mezcla;
- dependencia entre eventos mediante factores de tendencia, región, proveedor o tecnología;
- simulación Monte Carlo cuando no hay solución cerrada.

El output no debe ser solo \(E[S]\). Debe incluir:

| Output | Uso |
|---|---|
| Media | Presupuesto esperado |
| Percentil 75 / 90 / 95 / 99 | Rango de suficiencia |
| TVaR | Capital o colchón de cola |
| Probabilidad de exceso | Diseño de corredor |
| Contribución por condición | Gestión clínica |
| Sensibilidad a precio | Negociación y política farmacéutica |

Esta estructura es especialmente útil para enfermedades huérfanas, oncológicos, terapias de alto costo y eventos con baja credibilidad estadística.

## 7. Frecuencia

La frecuencia puede modelarse por:

- número de pacientes incidentes;
- número de tratamientos iniciados;
- número de ciclos;
- número de autorizaciones;
- número de eventos hospitalarios;
- número de pacientes que cruzan un umbral de costo;
- número de pacientes que progresan a un estado clínico severo.

Ejemplo de frecuencia esperada:

$$
\lambda_{g,t} =
\text{exposición}_{g,t}
\times
\text{incidencia}_{g,t}
\times
\text{factor de detección}_{g,t}
$$

donde \(g\) puede ser EPS, región, condición, régimen o grupo clínico.

La frecuencia debe ajustarse por:

- envejecimiento;
- prevalencia acumulada;
- mejora diagnóstica;
- cambios de cobertura;
- adopción tecnológica;
- transición epidemiológica;
- pandemia u otros choques.

## 8. Severidad

La severidad de alto costo tiende a tener cola derecha. Por eso, usar una media simple puede ser peligroso.

Factores de severidad:

| Factor | Ejemplo |
|---|---|
| Estadio clínico | ERC estadio 5 vs estadio 3 |
| Línea terapéutica | Primera línea vs terapia avanzada |
| Complicaciones | UCI, infecciones, recaídas |
| Prestador | Alta complejidad, centro especializado |
| Tecnología | Biológico, terapia génica, dispositivo implantable |
| Duración | Tratamiento temporal vs crónico |
| Precio | Negociación, regulación, disponibilidad |
| Glosa | Valor facturado vs reconocido |

Una práctica recomendada es modelar severidad por condición y etapa, no solo por agregado No UPC.

## 9. Modelos multiestado para alto costo

Muchas enfermedades de alto costo no son eventos aislados. Tienen trayectoria. Los modelos de Markov o semi-Markov permiten modelar transiciones.

Ejemplo para enfermedad renal crónica:

```text
ERC 3 -> ERC 4 -> ERC 5 sin diálisis -> Diálisis -> Trasplante -> Seguimiento -> Fallecimiento
```

Cada estado tiene:

- costo esperado;
- duración esperada;
- probabilidad de transición;
- mortalidad;
- probabilidad de complicación;
- patrón de utilización.

El valor esperado de costo futuro puede aproximarse como:

$$
E[C_{0:T}] = \sum_{t=0}^{T} \sum_s P(Y_t=s) \times c_s
$$

donde:

- \(Y_t\) es el estado clínico en \(t\);
- \(c_s\) es el costo esperado del estado \(s\);
- \(P(Y_t=s)\) surge de la matriz de transición.

Este enfoque es útil para cohortes CAC y para presupuestar progresión clínica.

## 10. Pooling ex ante y ex post

Hay dos enfoques principales para mutualizar alto costo:

| Enfoque | Descripción | Ventaja | Riesgo |
|---|---|---|---|
| Ex ante | El riesgo se incorpora antes vía score o prima ajustada | Incentiva gestión prospectiva | Puede subcompensar cola rara |
| Ex post | Se compensa después de observar evento o gasto | Protege contra ruina financiera | Puede reducir incentivos de eficiencia |

La solución robusta suele combinar ambos:

- ajuste prospectivo por morbilidad común y crónica;
- compensación ex post para eventos extremos;
- corredores de riesgo para desviaciones agregadas;
- auditoría clínica para validar elegibilidad;
- indicadores de calidad para evitar subprestación.

## 11. Corredores de riesgo

Un corredor de riesgo limita pérdidas o ganancias extremas alrededor de un costo esperado.

Ejemplo:

| Ratio observado / esperado | Tratamiento |
|---|---|
| 0.00–0.85 | La EPS devuelve parte del excedente |
| 0.85–1.15 | Zona de riesgo retenido |
| 1.15–1.30 | Compensación parcial |
| > 1.30 | Compensación alta o pooling |

El corredor reduce volatilidad, pero debe diseñarse con cuidado. Si es demasiado generoso, elimina incentivos de gestión. Si es demasiado estrecho, no protege contra riesgo catastrófico.

## 12. Stop-loss y reaseguro

Un mecanismo stop-loss cubre costos por encima de un umbral.

Para un afiliado o evento:

$$
\text{cobertura} = \max(0, X - d)
$$

donde \(d\) es el deducible o attachment point.

Para portafolio:

$$
\text{cobertura agregada} = \max(0, S - D)
$$

Estos esquemas pueden implementarse como:

- reaseguro privado;
- fondo solidario;
- mecanismo administrado por ADRES;
- compensación sectorial;
- corredor regulatorio;
- reserva catastrófica.

La selección del umbral debe depender de:

- tamaño de población;
- volatilidad histórica;
- capacidad patrimonial;
- concentración de alto costo;
- frecuencia esperada;
- severidad extrema;
- política de incentivos.

## 13. Doble conteo

El doble conteo es uno de los riesgos más importantes.

Puede ocurrir cuando una misma condición se financia simultáneamente por:

- UPC base;
- ajuste de morbilidad;
- Cuenta de Alto Costo;
- presupuesto máximo;
- recobro o mecanismo No UPC;
- reaseguro;
- reserva adicional.

Para evitarlo, cada condición o evento debe mapearse a una capa primaria y, si aplica, a una capa secundaria.

| Riesgo | Capa primaria | Capa secundaria |
|---|---|---|
| Diabetes controlada | UPC ajustada por morbilidad | Gestión clínica |
| ERC avanzada | UPC ajustada + CAC | Pooling si supera umbral |
| Medicamento huérfano No UPC | Presupuesto máximo | Stop-loss / fondo |
| UCI catastrófica | UPC / IBNR | Reaseguro o corredor |
| Oncología avanzada | Morbilidad + alto costo | MIPRES si tecnología No UPC |

La nota técnica debe documentar esta asignación.

## 14. Reservas IBNR para alto costo

El alto costo afecta IBNR de forma distinta al gasto ordinario.

Características:

- mayor rezago de autorización;
- cuentas complejas;
- glosas más frecuentes;
- auditoría médica intensiva;
- facturas grandes con liquidación parcial;
- posibles recobros o mecanismos especiales;
- alta sensibilidad a pocos casos.

Por eso, el reserving debe separar triángulos o modelos por capa de riesgo:

| Segmento | Método recomendado |
|---|---|
| Gasto ordinario masivo | Chain Ladder, GLM, BF |
| Alto costo recurrente | BF con expected loss clínico |
| Eventos catastróficos | Caso a caso + simulación |
| No UPC / MIPRES | Modelo separado por tecnología |
| Glosas de alto valor | Modelo de probabilidad de reconocimiento |

El IBNR total debe reconciliarse contra el costo esperado por cohorte clínica.

## 15. Expected loss ratio ajustado

Para Bornhuetter-Ferguson, el expected loss ratio puede ajustarse por alto costo:

$$
\text{ELR}_{g} =
\text{ELR base}
\times
\text{factor de morbilidad}_{g}
\times
\text{factor alto costo}_{g}
\times
\text{factor tendencia}_{g}
$$

Donde:

- \(g\) puede ser EPS, región, cohorte o contrato;
- el factor de morbilidad viene del capítulo 34;
- el factor alto costo captura concentración en CAC, MIPRES o eventos extremos;
- el factor tendencia captura inflación médica y adopción tecnológica.

Esto permite evitar que el BF use una expectativa plana para poblaciones con perfiles clínicos muy distintos.

## 16. Indicadores de monitoreo

Un tablero de alto costo debe combinar incidencia, severidad, persistencia, cola y liquidez.

| Indicador | Definición | Uso |
|---|---|---|
| Top 1% share | Gasto del 1% más costoso / gasto total | Concentración |
| Top 5% share | Gasto del 5% más costoso / gasto total | Concentración ampliada |
| Casos > umbral | Afiliados que superan valor definido | Stop-loss |
| PMPM alto costo | Gasto alto costo / exposición | Suficiencia |
| Incidencia por condición | Nuevos casos / población | Tendencia epidemiológica |
| Prevalencia persistente | Casos activos recurrentes | Riesgo estructural |
| Costo por estadio | Costo medio por estado clínico | Modelo multiestado |
| O/E alto costo | Observado / esperado | Calibración |
| IBNR alto costo | Reserva por cohorte | Liquidez |
| Glosa alto valor | Glosa / facturado alto costo | Operación |
| Días a pago | Tiempo factura-pago | Flujo de caja |
| Severidad P95/P99 | Percentiles de costo | Cola |

Estos indicadores deben revisarse por EPS, régimen, región, prestador, condición y tecnología.

## 17. Segmentación recomendada

Para modelar alto costo, una segmentación mínima puede incluir:

- oncología;
- enfermedad renal crónica;
- VIH;
- enfermedades huérfanas;
- trasplantes;
- UCI prolongada;
- salud mental severa;
- medicamentos biológicos;
- terapias No UPC;
- neonatos de alta complejidad;
- discapacidad o rehabilitación intensiva;
- multimorbilidad avanzada.

La segmentación no debe ser demasiado fina al inicio. Si cada celda tiene pocos casos, el modelo pierde credibilidad. En esos casos, conviene agrupar por familias clínicas y usar credibilidad o suavizamiento.

## 18. Credibilidad

Las condiciones raras tienen poca experiencia propia. La teoría de credibilidad ayuda a combinar experiencia local y referencia externa.

Forma simple:

$$
\hat{\mu} = Z \mu_{\text{local}} + (1-Z)\mu_{\text{referencia}}
$$

donde:

- \(Z\) es el peso de credibilidad;
- \(\mu_{\text{local}}\) es la experiencia observada;
- \(\mu_{\text{referencia}}\) puede ser nacional, sectorial o histórica;
- \(\hat{\mu}\) es la severidad o frecuencia estimada.

Esto evita reaccionar de forma excesiva a pocos casos extremos, sin ignorar evidencia local.

## 19. Escenarios y estrés

El alto costo requiere escenarios.

Ejemplos:

| Escenario | Supuesto |
|---|---|
| Adopción tecnológica rápida | Aumento de pacientes tratados con nueva terapia |
| Shock de precio | Incremento unitario por medicamento |
| Diagnóstico temprano | Mayor frecuencia, menor severidad futura |
| Rezago de pago | Aumento de IBNR y cuentas pendientes |
| Judicialización | Mayor acceso a tecnologías específicas |
| Concentración geográfica | Brote o cluster regional |
| Choque macro | Devaluación o inflación importada en medicamentos |

Cada escenario debe producir impacto en:

- costo esperado;
- percentiles altos;
- IBNR;
- flujo de caja;
- suficiencia de UPC;
- presupuesto máximo;
- necesidad de pooling.

## 20. Gobierno del mecanismo de pooling

Un esquema de pooling debe tener reglas explícitas.

| Componente | Pregunta |
|---|---|
| Elegibilidad | ¿Qué condiciones o eventos entran? |
| Umbral | ¿Desde qué valor aplica? |
| Base de costo | ¿Facturado, reconocido, pagado o técnico? |
| Auditoría | ¿Quién valida diagnóstico y pertinencia? |
| Periodo | ¿Mensual, trimestral, anual? |
| Retención | ¿Qué parte queda en la EPS? |
| Compensación | ¿Qué parte paga el fondo? |
| Doble conteo | ¿Cómo se coordina con UPC, CAC y MIPRES? |
| Calidad | ¿Se condiciona a resultados clínicos? |
| Información | ¿Qué datos se reportan y con qué estándar? |

Sin estas reglas, el pooling puede convertirse en un mecanismo de traslado de pérdidas sin control.

## 21. Riesgos de comportamiento

El alto costo crea incentivos relevantes:

- clasificar pacientes para obtener compensación;
- desplazar costos hacia capas financiadas externamente;
- retrasar facturación para periodos favorables;
- sobredimensionar severidad;
- fragmentar servicios;
- evitar pacientes no compensados;
- subinvertir en prevención si el alto costo se compensa completamente.

Controles:

- auditoría clínica independiente;
- reglas de persistencia diagnóstica;
- validación con medicamentos y procedimientos;
- revisión de outliers;
- indicadores de calidad;
- retención parcial obligatoria;
- comparación entre pares;
- trazabilidad de autorización, prestación, factura y pago.

## 22. Relación con calidad y gestión clínica

El pooling no debe ser solo financiero. Debe vincularse a gestión clínica.

Para condiciones crónicas, un alto costo observado puede reflejar:

- enfermedad inevitablemente severa;
- diagnóstico tardío;
- baja adherencia;
- fallas de prevención;
- barreras de acceso;
- mala coordinación asistencial;
- precio alto;
- tecnología ineficiente;
- codificación o facturación deficiente.

Por eso, el análisis debe integrar indicadores clínicos:

- control metabólico;
- progresión de estadio;
- hospitalizaciones evitables;
- adherencia;
- seguimiento especializado;
- oportunidad de diagnóstico;
- desenlaces;
- mortalidad;
- reingresos;
- complicaciones.

## 23. Integración con RIPS-FEV

El fortalecimiento de RIPS y facturación electrónica puede mejorar el modelamiento de alto costo si permite:

- trazabilidad evento-factura-pago;
- identificación más oportuna de diagnósticos;
- validación estructurada;
- reducción de subregistro;
- mejor calendario de incurrencia;
- separación entre valor facturado, reconocido y pagado;
- auditoría de glosas y devoluciones;
- linkage longitudinal por afiliado.

La calidad de datos será determinante. Un modelo de alto costo basado en datos incompletos puede subestimar frecuencia, sobreestimar severidad o asignar mal la cola.

## 24. Arquitectura técnica recomendada

Una arquitectura de alto costo debe incluir:

| Módulo | Función |
|---|---|
| Identificación de casos | Detectar afiliados, eventos y condiciones |
| Agrupación clínica | Clasificar por condición, estadio y tecnología |
| Costing técnico | Separar facturado, reconocido, pagado e incurrido |
| Modelo frecuencia-severidad | Estimar distribución agregada |
| Modelo multiestado | Proyectar progresión crónica |
| Reserving | Estimar IBNR y obligaciones pendientes |
| Pooling | Aplicar reglas de compensación |
| Backtesting | Comparar observado vs esperado |
| Gobierno | Versiones, supuestos, controles y auditoría |

Esta arquitectura debe operar a nivel afiliado-evento y agregarse por EPS, región, condición y capa financiera.

## 25. Ejemplo conceptual

Supóngase una cohorte de enfermedad huérfana con:

- 120 pacientes expuestos;
- incidencia esperada de 8 nuevos tratamientos al año;
- severidad media de 450 millones;
- severidad P95 de 1.200 millones;
- alta incertidumbre de precio;
- rezago medio de pago de 180 días.

Un presupuesto por media esperada puede estimar:

$$
E[S] = 8 \times 450 = 3.600 \text{ millones}
$$

Pero si la distribución tiene cola severa, el percentil 95 del agregado puede ser materialmente superior. Para liquidez y pooling, el presupuesto debería considerar:

- media;
- rango de suficiencia;
- probabilidad de exceder umbral;
- costo esperado por encima del umbral;
- IBNR por rezago;
- sensibilidad a precio y número de pacientes.

## 26. Checklist operativo

Antes de implementar un mecanismo de alto costo o pooling, debe verificarse:

- ¿La definición de alto costo está documentada?
- ¿La condición pertenece a UPC, No UPC, CAC, MIPRES o capa mixta?
- ¿Existe umbral de activación?
- ¿El costo base es facturado, reconocido, pagado o técnico?
- ¿Se separa frecuencia de severidad?
- ¿Se estima distribución agregada y no solo promedio?
- ¿Se calcula P95/P99 o TVaR?
- ¿Se identifican rezagos de pago e IBNR?
- ¿Hay validación clínica de casos?
- ¿Se controla doble conteo?
- ¿Se mantiene retención para preservar incentivos?
- ¿Se evalúan escenarios de precio y adopción?
- ¿Se monitorean calidad y resultados clínicos?
- ¿El modelo fue validado contra periodos históricos?
- ¿La nota técnica documenta supuestos, limitaciones y versión?

## 27. Conclusión

Las condiciones de alto costo requieren una arquitectura actuarial propia. No basta con promedios históricos ni con una UPC demográfica. El sistema debe separar capas de riesgo, modelar frecuencia y severidad, estimar colas, reconocer rezagos, coordinar CAC/MIPRES/UPC y definir mecanismos de pooling con reglas claras.

Para Colombia, el avance técnico más importante es pasar de presupuestos deterministas a distribuciones de pérdida agregada. Esto permite evaluar suficiencia, diseñar corredores, estimar IBNR, proteger la liquidez de la red prestadora y reducir incentivos de selección de riesgos.

El alto costo no puede desaparecer por modelación. Pero sí puede hacerse visible, medible, financiable y gobernable.

## Fuentes de trabajo del proyecto

- ASOP No. 56, *Modeling*, como referencia para uso, validación, gobierno y riesgo de modelo.
- ASOP No. 45, *The Use of Health Status Based Risk Adjustment Methodologies*, como referencia para morbilidad y ajuste de riesgo.
- `gemini-deep-research-report.md`, secciones sobre modelos de riesgo colectivo, Monte Carlo, Cuenta de Alto Costo, MIPRES, presupuestos máximos y recomendaciones para Colombia.
- `chatgpt-deep-research-report.md`, secciones sobre alto costo, enfermedades catastróficas, Cuenta de Alto Costo, MIPRES, reservas y ajuste de riesgo.

## Próximo capítulo

➡️ **[Colombia RIPS-FEV Data Quality and Validation](36-colombia-rips-fev-data-quality-and-validation.md)**
