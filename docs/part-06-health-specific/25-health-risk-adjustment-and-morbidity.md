---
title: "Health Risk Adjustment and Morbidity"
part: "Parte VI · Especificidades de salud"
chapter: 25
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

# Health Risk Adjustment and Morbidity

Este capítulo desarrolla el ajuste de riesgo y la morbilidad como componentes centrales del reserving de salud. En una cartera médica, dos poblaciones con la misma exposición pueden tener costos esperados radicalmente distintos si difieren en edad, sexo, diagnóstico, condiciones crónicas, utilización previa, región, red de atención o severidad clínica.

El ajuste de riesgo permite normalizar la experiencia para separar cambios de morbilidad de cambios de tendencia, utilización, severidad o desarrollo. En reserving, su objetivo principal no es calcular una prima comercial, sino mejorar la estimación del costo último, explicar variaciones y reducir sesgos por mezcla poblacional.

## Objetivos de aprendizaje

Al finalizar este capítulo, el lector debería poder:

- Definir morbilidad y ajuste de riesgo en el contexto de reservas de salud.
- Diferenciar ajuste demográfico, clínico, farmacéutico, histórico y socioeconómico.
- Construir exposición ajustada por riesgo y PMPM ajustado.
- Identificar el rol de modelos tipo HCC, ACG, CRG, DxCG y agrupadores clínicos.
- Reconocer riesgos de codificación, selección adversa, sobreajuste y gaming.
- Integrar scores de riesgo en métodos de reserving, backtesting y monitoreo.
- Aplicar criterios de gobierno y calidad de datos para modelos de morbilidad.

## 1. Concepto de morbilidad

Morbilidad es la carga de enfermedad de una población. En seguros de salud, la morbilidad se refleja en:

- prevalencia de condiciones crónicas;
- incidencia de eventos agudos;
- severidad clínica;
- multimorbilidad;
- discapacidad o dependencia funcional;
- consumo de medicamentos;
- frecuencia de hospitalización;
- uso de servicios de alto costo;
- persistencia de diagnósticos en el tiempo.

La morbilidad no es equivalente al costo observado. El costo observado depende también de acceso, red, tarifas, auditoría, glosas, política de pago y beneficios cubiertos.

## 2. Ajuste de riesgo

El ajuste de riesgo es un conjunto de métodos para estimar el costo esperado relativo de una persona o grupo, dadas sus características observables.

Una formulación general es:

$$
E[C_i \mid X_i] = \mu_i
$$

donde:

- \(C_i\) es el costo esperado del individuo \(i\);
- \(X_i\) es el vector de características de riesgo;
- \(\mu_i\) es el costo esperado ajustado.

El resultado puede expresarse como un score relativo:

$$
r_i = \frac{\mu_i}{\bar{\mu}}
$$

Si \(r_i = 1.50\), el individuo tiene costo esperado 50% superior al promedio de referencia.

## 3. Por qué importa en reserving

El reserving tradicional puede asumir implícitamente que el mix de riesgo es estable. En salud, esa hipótesis puede fallar por:

- envejecimiento de afiliados;
- cambio de composición regional;
- concentración de pacientes crónicos;
- entrada o salida de grupos empresariales;
- cambios de red;
- cambios de cobertura;
- selección adversa;
- migración de pacientes de alto costo;
- epidemias o shocks de morbilidad.

Sin ajuste de riesgo, un aumento de PMPM puede interpretarse como tendencia médica cuando en realidad proviene de mayor carga de enfermedad. También puede ocurrir lo contrario: una mejora aparente puede deberse a salida de pacientes complejos.

## 4. Exposición ajustada por riesgo

La exposición ajustada por riesgo combina tiempo cubierto y riesgo relativo:

$$
E^* = \sum_i E_i r_i
$$

donde:

- \(E_i\) es la exposición del individuo;
- \(r_i\) es su score de riesgo relativo;
- \(E^*\) es la exposición equivalente ajustada.

El PMPM ajustado puede calcularse como:

$$
\text{PMPM ajustado} = \frac{C}{E^*}
$$

Esto permite comparar periodos o segmentos con diferente morbilidad.

## 5. Ejemplo simple

Supóngase dos grupos con igual exposición:

| Grupo | Miembros-mes | Score promedio | Exposición ajustada |
|---|---:|---:|---:|
| A | 10,000 | 0.80 | 8,000 |
| B | 10,000 | 1.40 | 14,000 |

Ambos grupos tienen 10,000 miembros-mes, pero el grupo B tiene 75% más exposición ajustada:

$$
\frac{14{,}000}{8{,}000} - 1 = 75\%
$$

Si ambos grupos presentan el mismo costo bruto, el grupo B está relativamente mejor de lo que parece. Si ambos presentan el mismo PMPM bruto, el grupo A podría estar deteriorado frente a su riesgo esperado.

## 6. Fuentes de ajuste

El ajuste de riesgo puede usar distintas fuentes:

| Fuente | Ejemplos | Ventaja | Riesgo |
|---|---|---|---|
| Demográfica | edad, sexo, región | Disponible y estable | Bajo poder predictivo |
| Clínica | diagnósticos, procedimientos | Captura morbilidad | Calidad de codificación |
| Farmacéutica | medicamentos crónicos | Señal temprana | Cobertura incompleta |
| Histórica | costos pasados | Alto poder predictivo | Puede premiar ineficiencia |
| Socioeconómica | ingreso, ruralidad, privación | Captura acceso y necesidad | Disponibilidad y sensibilidad |
| Operativa | red, canal, autorización | Explica utilización | Riesgo de confundir gestión con salud |

La selección de variables debe responder al objetivo. Un modelo para reservas puede aceptar algunas variables históricas; un modelo de compensación regulatoria puede requerir restricciones más estrictas para evitar incentivos perversos.

## 7. Ajuste demográfico

El ajuste demográfico usa variables como:

- edad;
- sexo;
- región;
- zona urbana/rural;
- grupo de afiliación;
- tipo de plan;
- composición familiar.

Es simple, auditable y estable. Sin embargo, suele explicar solo una parte limitada de la variación individual del costo médico. En portafolios con alta carga crónica, el ajuste demográfico puede ser insuficiente para comparar experiencia o proyectar reservas.

## 8. Ajuste clínico basado en diagnósticos

Los modelos clínicos agrupan diagnósticos en categorías de riesgo. Ejemplos internacionales incluyen:

- HCC, Hierarchical Condition Categories;
- ACG, Adjusted Clinical Groups;
- CRG, Clinical Risk Groups;
- DxCG, Diagnostic Cost Groups;
- índices de comorbilidad como Charlson o Elixhauser.

Estos modelos buscan resumir morbilidad en variables predictivas. La idea general es:

$$
\mu_i = f(\text{edad}_i, \text{sexo}_i, \text{diagnósticos}_i, \text{interacciones}_i)
$$

La jerarquía evita contar dos veces condiciones relacionadas. Por ejemplo, una categoría severa puede desplazar una categoría menos severa dentro de la misma familia clínica.

## 9. Multimorbilidad

La multimorbilidad ocurre cuando una persona tiene múltiples condiciones clínicas. Es especialmente relevante porque el costo conjunto puede no ser aditivo.

Ejemplo:

| Condición | Riesgo aislado |
|---|---:|
| Diabetes | 1.30 |
| Enfermedad renal | 2.20 |
| Insuficiencia cardíaca | 1.80 |

El riesgo conjunto puede ser mayor que la suma simple por interacciones clínicas y mayor intensidad de atención.

Los modelos deben considerar:

- número de condiciones;
- severidad;
- interacciones;
- persistencia;
- progresión;
- polifarmacia;
- hospitalizaciones previas.

## 10. Ajuste farmacéutico

El consumo de medicamentos puede ser una señal fuerte de morbilidad crónica. Grupos farmacéuticos pueden identificar condiciones como:

- diabetes;
- hipertensión;
- VIH;
- cáncer;
- enfermedad renal;
- enfermedades autoinmunes;
- salud mental;
- enfermedades huérfanas.

Ventajas:

- puede estar disponible antes que diagnósticos completos;
- refleja tratamiento activo;
- puede mejorar predicción de gasto.

Limitaciones:

- no todos los medicamentos son específicos de una condición;
- puede faltar información de dispensación;
- cambios de cobertura afectan observación;
- adherencia no siempre es conocida;
- medicamentos de alto costo pueden dominar el score.

## 11. Ajuste histórico

El costo histórico es altamente predictivo, pero debe usarse con cuidado. Puede reflejar:

- morbilidad real;
- acceso diferencial;
- ineficiencia;
- fraude o abuso;
- tarifas altas;
- concentración de prestadores;
- eventos no recurrentes.

En reserving, el costo histórico puede ser útil para estimar persistencia de alto costo. En modelos de compensación o incentivos, puede crear problemas si remunera gasto pasado sin distinguir necesidad médica de ineficiencia.

## 12. Modelos prospectivos y concurrentes

Los modelos de ajuste pueden ser prospectivos o concurrentes.

| Tipo | Descripción | Uso |
|---|---|---|
| Prospectivo | Usa información pasada para predecir costo futuro | Capitación, presupuesto, reservas prospectivas |
| Concurrente | Usa información del mismo periodo para explicar costo del periodo | Evaluación, normalización, benchmarking |
| Retrospectivo | Ajusta después de observar experiencia | Compensación ex post, análisis de desviaciones |

Para reserving, la distinción es crítica. Un modelo que usa diagnósticos observados después de la fecha de valoración puede introducir leakage.

## 13. Leakage en modelos de morbilidad

El leakage ocurre cuando el modelo usa información no disponible al momento de la valoración.

Ejemplos:

- diagnóstico registrado después del corte;
- medicamento dispensado después del corte;
- hospitalización futura;
- costo final conocido;
- estado de alto costo identificado retrospectivamente;
- glosa resuelta después de la fecha de valoración.

Regla práctica:

Toda variable de ajuste de riesgo debe tener una fecha de observación y debe verificarse que esté disponible al corte.

## 14. Calibración del score

Un score de riesgo debe calibrarse contra experiencia observada.

Si \(r_i\) es el score relativo y \(\bar{C}\) es el costo promedio, entonces:

$$
\widehat{C}_i = r_i \bar{C}
$$

La calibración evalúa si:

$$
\sum_i \widehat{C}_i \approx \sum_i C_i
$$

y si la aproximación se mantiene por:

- decil de riesgo;
- edad;
- sexo;
- región;
- condición clínica;
- tipo de contrato;
- prestador;
- periodo calendario.

Un modelo puede estar calibrado en agregado y fallar severamente en subgrupos.

## 15. Métricas de desempeño

Métricas útiles:

| Métrica | Uso |
|---|---|
| R² predictivo | Varianza explicada |
| MAE | Error absoluto individual |
| RMSE | Penaliza errores grandes |
| C-statistic | Clasificación de alto costo |
| Lift por decil | Concentración de riesgo |
| Observado/Esperado | Calibración por grupo |
| Error PMPM ajustado | Comparación de segmentos |
| Estabilidad temporal | Robustez del score |

En reserving, la métrica más relevante puede no ser el error individual, sino la capacidad para explicar variaciones agregadas y reducir sesgo por mezcla.

## 16. Uso en Bornhuetter-Ferguson

El ajuste de riesgo puede mejorar el expected loss o expected PMPM en Bornhuetter-Ferguson.

Una formulación posible:

$$
\widehat{U}_t =
E_t^* \times \text{PMPM esperado ajustado}
$$

donde:

- \(E_t^*\) es exposición ajustada por riesgo;
- el PMPM esperado ajustado representa costo esperado por unidad de riesgo.

La reserva BF sería:

$$
R_t =
\widehat{U}_t \times (1 - \% \text{desarrollado})
$$

Esto evita aplicar el mismo costo esperado a periodos con diferente morbilidad.

## 17. Uso en métodos de completitud

En métodos de completitud PMPM, el ajuste de riesgo permite comparar periodos recientes contra una base homogénea:

$$
\text{PMPM observado ajustado}_{t,d}
=
\frac{C_{t,d}}{E_t^*}
$$

Luego:

$$
\widehat{\text{PMPM último ajustado}}_{t}
=
\frac{\text{PMPM observado ajustado}_{t,d}}{q_d}
$$

Finalmente:

$$
\widehat{C}_{t}
=
E_t^* \times \widehat{\text{PMPM último ajustado}}_{t}
$$

Este enfoque es útil cuando cambia la composición clínica de la población.

## 18. Uso en GLM, GAM y ML

El ajuste de riesgo puede incorporarse como:

- variable explicativa;
- offset;
- segmentación;
- peso de exposición;
- normalizador de target;
- score externo;
- conjunto de variables clínicas detalladas.

Ejemplo conceptual:

$$
g(\mu_i) =
\alpha +
\beta_1 \log(E_i) +
\beta_2 r_i +
f(\text{edad}_i) +
X_i \gamma
$$

En modelos machine learning, el score de riesgo puede complementar variables clínicas granulares. Debe evitarse doble conteo si el score ya resume diagnósticos usados por el modelo.

## 19. Alto costo

Los pacientes de alto costo requieren tratamiento especial. Pueden representar una proporción baja de afiliados y una proporción alta del costo.

Opciones actuariales:

- modelar alto costo por separado;
- usar truncamiento y cargo de exceso;
- aplicar pooling;
- usar modelos de severidad extrema;
- construir escenarios;
- separar eventos recurrentes de eventos únicos;
- incorporar persistencia clínica.

El ajuste de riesgo ayuda a identificar alta morbilidad esperada, pero no elimina la volatilidad de eventos extremos.

## 20. Selección adversa y cream-skimming

Cuando la compensación financiera no reconoce morbilidad, aparecen incentivos a seleccionar población de bajo riesgo o evitar población compleja.

El ajuste de riesgo reduce estos incentivos al alinear recursos con necesidad esperada. Sin embargo, también puede introducir nuevos riesgos:

- codificación oportunista;
- intensificación diagnóstica;
- selección de variables manipulables;
- pérdida de incentivos de prevención si todo riesgo se compensa;
- complejidad técnica y opacidad.

Por eso el diseño debe equilibrar precisión, transparencia, estabilidad e incentivos.

## 21. Riesgo de codificación

Los diagnósticos observados no son una medición pura de morbilidad. Dependen de:

- acceso al servicio;
- intensidad de registro;
- calidad del prestador;
- incentivos de facturación;
- auditoría;
- sistemas de información;
- cambios de catálogos;
- reglas de validación.

Un aumento de diagnósticos puede significar mayor enfermedad, mejor captura o codificación más agresiva. Los modelos deben monitorear intensidad de codificación.

## 22. Calidad de datos

Controles mínimos:

| Control | Riesgo mitigado |
|---|---|
| Fechas de diagnóstico | Leakage temporal |
| Diagnósticos válidos | Códigos inexistentes o mal formados |
| Persistencia clínica | Diagnósticos aislados espurios |
| Homologación de catálogos | Rupturas por cambio de versión |
| Duplicados | Sobreconteo de condiciones |
| Medicamentos coherentes | Señales farmacéuticas falsas |
| Costos extremos | Distorsión de calibración |
| Cobertura activa | Diagnósticos fuera de exposición |
| Trazabilidad de prestador | Cambios de codificación por fuente |

Sin controles de datos, el ajuste de riesgo puede amplificar errores.

## 23. Aplicación al contexto colombiano

En Colombia, el ajuste de riesgo es relevante para reserving por varias razones:

- la UPC y otros mecanismos de financiación pueden no capturar toda la heterogeneidad clínica;
- la carga de enfermedad puede variar por región, edad, régimen, red y acceso;
- RIPS, facturación electrónica, MIPRES, cuentas de alto costo y datos de prestación pueden aportar señales clínicas;
- glosas y devoluciones pueden distorsionar costos observados;
- tecnologías de alto costo y enfermedades crónicas pueden concentrar riesgo;
- cambios regulatorios u operativos pueden afectar registro y reconocimiento.

Para una EPS, asegurador o analista actuarial, un score de morbilidad puede usarse para explicar desviaciones de siniestralidad, ajustar PMPM, segmentar reservas y evaluar suficiencia.

La adopción debe ser gradual: primero diagnósticos descriptivos, luego modelos simples y auditables, después modelos predictivos con validación temporal y gobierno robusto.

## 24. Ejemplo conceptual

Supóngase:

| Periodo | Miembros-mes | Score promedio | Costo observado |
|---|---:|---:|---:|
| 2025-Q1 | 100,000 | 1.00 | 50,000,000 |
| 2026-Q1 | 100,000 | 1.20 | 57,000,000 |

PMPM bruto 2025:

$$
\frac{50{,}000{,}000}{100{,}000} = 500
$$

PMPM bruto 2026:

$$
\frac{57{,}000{,}000}{100{,}000} = 570
$$

El aumento bruto es 14%. Pero la exposición ajustada de 2026 es:

$$
100{,}000 \times 1.20 = 120{,}000
$$

PMPM ajustado 2026:

$$
\frac{57{,}000{,}000}{120{,}000} = 475
$$

La lectura cambia: el costo bruto sube, pero ajustado por morbilidad el costo por unidad de riesgo baja. Sin ajuste, se podría concluir erróneamente que hay deterioro.

## 25. Backtesting

El backtesting debe evaluar:

- error agregado con y sin ajuste de riesgo;
- error por decil de score;
- error por condición crónica;
- error por alto costo;
- estabilidad de scores entre periodos;
- cambios de codificación;
- suficiencia de reservas por segmento;
- comparación contra PMPM bruto y PMPM ajustado.

Preguntas clave:

- ¿El ajuste redujo sesgo por mezcla?
- ¿El modelo subestimó pacientes de alto costo?
- ¿El score fue estable?
- ¿Hubo drift de codificación?
- ¿La reserva explicada por morbilidad coincide con la experiencia posterior?

## 26. Gobierno del modelo

La documentación debe incluir:

- objetivo del ajuste;
- población cubierta;
- fuentes de datos;
- fecha de corte;
- variables usadas;
- variables excluidas;
- tratamiento de diagnósticos;
- jerarquías clínicas;
- calibración;
- validación temporal;
- resultados por subgrupo;
- limitaciones;
- riesgos de codificación;
- monitoreo;
- responsables técnicos.

Cuando el ajuste de riesgo afecta reservas oficiales, debe tratarse como componente del modelo actuarial y estar sujeto a revisión independiente.

## 27. Checklist práctico

Antes de usar ajuste de riesgo en reserving, confirmar:

- El objetivo es claro: normalización, proyección, segmentación o explicación.
- Las variables están disponibles al corte.
- La exposición está medida correctamente.
- Los diagnósticos están validados.
- El score está calibrado.
- No hay doble conteo con otras variables.
- El modelo fue validado temporalmente.
- Se monitorea intensidad de codificación.
- Los resultados se revisan por subgrupo.
- El uso en reservas está documentado.

## 28. Conclusiones

El ajuste de riesgo permite que el reserving de salud distinga entre crecimiento de costo y cambio de morbilidad. Esta distinción es crítica para interpretar PMPM, seleccionar supuestos, aplicar Bornhuetter-Ferguson, evaluar suficiencia y explicar variaciones.

Un buen ajuste de riesgo no es necesariamente el modelo más complejo. Es el modelo que mejora la explicación actuarial, reduce sesgo, respeta la información disponible al corte, es validable y puede gobernarse. En salud, especialmente en contextos con alta heterogeneidad clínica, esta disciplina es indispensable para reservas más robustas.

El siguiente capítulo aborda modelos de pago y contratos de prestadores, que modifican la forma en que la morbilidad se transforma en obligación financiera.

## Referencias

- ASOP No. 1, Introductory Actuarial Standard of Practice.
- ASOP No. 23, Data Quality.
- ASOP No. 38, Using Models Outside the Actuary's Area of Expertise.
- ASOP No. 43, Property/Casualty Unpaid Claim Estimates.
- ASOP No. 45, The Use of Health Status Based Risk Adjustment Methodologies.
- ASOP No. 56, Modeling.
- Society of Actuaries, materiales técnicos sobre risk adjustment, morbidity, health reserving y predictive modeling.
- Reportes de investigación del proyecto sobre ajuste de riesgo, morbilidad y contexto colombiano.

## Próximo capítulo

➡️ **[Health Provider Contracts and Payment Models](26-health-provider-contracts-and-payment-models.md)**
