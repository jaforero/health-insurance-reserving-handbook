---
title: "Colombia Solvency, Liquidity and Stress Testing"
part: "Parte VII · Colombia"
chapter: 38
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

# Colombia Solvency, Liquidity and Stress Testing

Este capítulo desarrolla un marco actuarial para analizar solvencia, liquidez y escenarios de estrés en aseguramiento de salud en Colombia. Conecta la suficiencia de UPC, reservas IBNR, alto costo, glosas, cuentas por pagar, flujo de caja, patrimonio, riesgo de modelo y sostenibilidad financiera.

La solvencia responde si los activos y el patrimonio son suficientes frente a las obligaciones esperadas y adversas. La liquidez responde si existe caja suficiente para pagar oportunamente. Ambas dimensiones están relacionadas, pero no son equivalentes. Una entidad puede ser solvente en balance y enfrentar presión de liquidez; también puede pagar temporalmente sus obligaciones mientras acumula un déficit económico estructural.

En salud, esta distinción es crítica porque los pasivos se desarrollan con rezagos, las cuentas médicas pasan por auditoría y glosa, los eventos de alto costo pueden concentrarse en pocos afiliados, y la suficiencia de la UPC puede deteriorarse por morbilidad, inflación médica, tecnología y cambios operativos.

## Objetivos de aprendizaje

Al terminar este capítulo, el lector debería poder:

- Diferenciar solvencia, liquidez, suficiencia técnica y flujo de caja.
- Diseñar un balance económico simplificado para una EPS o asegurador de salud.
- Construir un modelo de flujo de caja prospectivo para pagos médicos.
- Definir escenarios de estrés por morbilidad, alto costo, inflación médica, glosas, rezagos y tecnología.
- Conectar IBNR, cuentas por pagar y liquidez.
- Calcular indicadores de alerta temprana.
- Diseñar reporting técnico y ejecutivo para comités de riesgo, finanzas y dirección.

## 1. Solvencia vs liquidez

Solvencia y liquidez miden riesgos distintos.

| Concepto | Pregunta | Horizonte |
|---|---|---|
| Solvencia | ¿Los activos y el patrimonio cubren obligaciones? | Mediano y largo plazo |
| Liquidez | ¿Hay caja para pagar a tiempo? | Corto plazo |
| Suficiencia UPC | ¿El ingreso prospectivo cubre costo esperado? | Periodo tarifario |
| Reserva técnica | ¿El pasivo registrado refleja obligaciones incurridas? | Fecha de corte |
| Capital económico | ¿Hay capacidad para soportar escenarios adversos? | Horizonte de riesgo |

La solvencia puede deteriorarse por subestimación de reservas, insuficiencia de UPC, crecimiento de alto costo, mala calidad de cartera, deterioro de activos o déficit operativo persistente. La liquidez puede deteriorarse por acumulación de cuentas médicas, pagos tardíos, giros insuficientes, recuperación lenta de glosas, concentración de prestadores o choques de caja.

## 2. Balance económico simplificado

Una visión actuarial de solvencia puede representarse como:

$$
\text{Posición económica} = \text{Activos admisibles}
-
\text{Pasivos técnicos}
-
\text{Otros pasivos}
$$

Donde:

- activos admisibles son activos líquidos o realizables con calidad suficiente;
- pasivos técnicos incluyen obligaciones conocidas, IBNR, IBNER, alto costo y margen de incertidumbre;
- otros pasivos incluyen obligaciones administrativas, financieras, tributarias o contractuales.

Una entidad puede mostrar patrimonio contable positivo y, aun así, tener una posición económica débil si:

- las reservas están subestimadas;
- las cuentas por pagar están envejecidas;
- los activos no son líquidos;
- hay glosas contabilizadas de forma optimista;
- existe déficit estructural entre UPC e incurrido;
- el alto costo no está provisionado adecuadamente.

## 3. Liquidez operativa

La liquidez se mide por capacidad de cubrir pagos esperados.

Modelo básico:

$$
\text{Gap de liquidez}_{t} = \text{Entradas de caja}_{t}
-
\text{Salidas de caja}_{t}
$$

Con acumulado:

$$
\text{Caja acumulada}_{t} = \text{Caja inicial}
+
\sum_{k=1}^{t}
\text{Gap de liquidez}_{k}
$$

Entradas típicas:

- UPC;
- pagos o giros del sistema;
- recuperación de cuentas;
- rendimientos financieros;
- aportes de capital;
- compensaciones;
- otros ingresos operativos.

Salidas típicas:

- pagos a IPS;
- medicamentos;
- alto costo;
- pagos MIPRES o No UPC, según el flujo aplicable;
- costos administrativos;
- conciliaciones;
- intereses o financiación;
- obligaciones laborales y tributarias.

El modelo debe proyectarse por semanas o meses, no solo por año.

## 4. Relación entre IBNR y liquidez

IBNR no es caja inmediata, pero anticipa caja futura. Si el IBNR aumenta por rezagos de radicación, puede haber presión de liquidez diferida. Si los pagos están artificialmente bajos por restricción de caja, el triángulo de pagos puede subestimar la obligación económica.

La relación puede verse así:

| Señal | Interpretación |
|---|---|
| IBNR estable y cuentas por pagar crecientes | Problema de liquidez o pago |
| IBNR creciente y pagos crecientes | Mayor incurrido o rezago |
| IBNR decreciente y pagos bajos | Posible subestimación si hay backlog |
| Reconocido creciente y pagado estable | Acumulación de obligación |
| Glosa creciente | Incertidumbre de reconocimiento futuro |

Por eso, solvencia y liquidez deben analizarse conjuntamente.

## 5. Riesgos principales

Un marco de estrés debe cubrir al menos estos riesgos:

| Riesgo | Driver | Impacto |
|---|---|---|
| Morbilidad | Envejecimiento, cronicidad, multimorbilidad | Mayor costo esperado |
| Alto costo | Cáncer, ERC, VIH, huérfanas, UCI | Cola severa |
| Inflación médica | Precios, salarios, tecnología | Mayor severidad |
| Tecnología | Nuevos medicamentos o procedimientos | Presión No UPC o presupuesto máximo |
| Operación | Rezagos, glosas, backlog | Mayor pasivo pendiente |
| Liquidez | Descalce entradas/salidas | Mora y deterioro de red |
| Regulación | Cambios de cobertura o reglas de pago | Ruptura de experiencia |
| Datos | Incompletitud o cambio de calidad | Riesgo de modelo |
| Prestadores | Concentración o negociación | Severidad y caja |
| Choques sistémicos | Pandemia, clima, macroeconomía | Frecuencia y severidad extremas |

Cada riesgo debe mapearse a una variable de modelo.

## 6. Escenarios de estrés

Un escenario de estrés no es una predicción puntual. Es una prueba de resistencia.

Ejemplos:

| Escenario | Supuesto técnico |
|---|---|
| Morbilidad adversa | Aumento de frecuencia en crónicos y alto costo |
| Inflación médica alta | Incremento de severidad por encima de inflación general |
| Alto costo extremo | Entrada de pocos casos con severidad P99 |
| Rezago de radicación | Desplazamiento de cuentas hacia periodos posteriores |
| Deterioro de glosas | Mayor porcentaje de glosa levantada |
| Liquidez restringida | Menor entrada de caja o pago tardío |
| Tecnología nueva | Mayor adopción de tratamiento de alto costo |
| Choque epidemiológico | Aumento simultáneo de frecuencia y severidad |
| Concentración IPS | Prestador dominante acelera radicación |
| Ruptura de datos | Cambio de FEV/RIPS altera comparabilidad |

Cada escenario debe reportar impacto en:

- resultado técnico;
- IBNR;
- cuentas por pagar;
- caja acumulada;
- patrimonio económico;
- indicadores de solvencia;
- pagos a prestadores;
- necesidad de capital o financiación.

## 7. Escenarios determinísticos y estocásticos

Hay dos enfoques complementarios:

| Enfoque | Uso |
|---|---|
| Determinístico | Comunicación ejecutiva, sensibilidad simple |
| Estocástico | Capital económico, colas, distribución de resultados |

Un escenario determinístico puede decir: “inflación médica +8%, rezago pago +30 días, alto costo +15%”.

Un modelo estocástico puede simular miles de trayectorias de frecuencia, severidad, pagos, glosas y caja para estimar percentiles:

$$
\text{Capital económico}_{99\%} = Q_{99\%}(\text{Pérdida})
-
E[\text{Pérdida}]
$$

También puede usarse TVaR:

$$
\text{TVaR}_{99\%} = E[\text{Pérdida} \mid \text{Pérdida} > Q_{99\%}]
$$

TVaR es útil cuando la cola extrema importa, como en alto costo.

## 8. Riesgo de ruina

La teoría de ruina pregunta por la probabilidad de que los pasivos o pérdidas acumuladas excedan los recursos disponibles.

Forma simplificada:

$$
U_t = U_0 + P_t - S_t - E_t
$$

donde:

- $U_t$ es capital o excedente disponible;
- $U_0$ es excedente inicial;
- $P_t$ son ingresos o primas;
- $S_t$ son siniestros o costos médicos;
- $E_t$ son gastos y otros egresos.

Riesgo de ruina:

$$
P(U_t < 0 \text{ para algún } t \leq T)
$$

En salud, este enfoque debe adaptarse porque los ingresos, pagos y obligaciones tienen reglas institucionales. Aun así, la lógica es útil para evaluar si la entidad puede sostener choques adversos.

## 9. Dependencias

Los riesgos no son independientes. Un choque macroeconómico puede aumentar inflación médica y simultáneamente deteriorar liquidez. Una pandemia puede aumentar frecuencia de servicios, reducir oportunidad de atención, generar backlog y cambiar severidad. Una nueva tecnología puede aumentar costo esperado y presión regulatoria.

Dependencias relevantes:

| Dependencia | Ejemplo |
|---|---|
| Morbilidad + alto costo | Crónicos progresan a eventos severos |
| Inflación + tecnología | Nuevos tratamientos elevan severidad |
| Liquidez + glosas | Restricción de caja aumenta disputas |
| Datos + reservas | Cambio de RIPS altera desarrollo observado |
| Prestador + caja | Concentración acelera presión de pagos |
| Macroeconomía + medicamentos | Importados suben por tasa de cambio |

Los escenarios deben capturar al menos algunas dependencias. De lo contrario, subestiman eventos adversos simultáneos.

## 10. Proyección de flujo de caja médico

Un modelo mínimo de liquidez médica puede proyectar:

$$
\text{Pagos}_{t} = f(
\text{Reconocido pendiente},
\text{IBNR},
\text{patrón de pago},
\text{glosas},
\text{alto costo},
\text{capacidad de caja}
)
$$

Componentes:

| Componente | Descripción |
|---|---|
| Backlog reconocido | Cuentas aceptadas y no pagadas |
| Radicado no reconocido | Cuentas en auditoría |
| IBNR | Servicios no observados |
| IBNER | Desarrollo adicional |
| Glosas | Probabilidad de levantamiento |
| Alto costo | Casos materiales |
| Pagos programados | Calendario contractual |
| Restricción de caja | Límite operativo de pago |

La salida debe ser mensual:

- pagos esperados;
- pagos en estrés;
- caja final;
- déficit acumulado;
- edad de cuentas por pagar.

## 11. Indicadores de alerta temprana

Un tablero de solvencia y liquidez debe incluir:

| Indicador | Interpretación |
|---|---|
| Siniestralidad UPC | Costo médico / ingreso UPC |
| IBNR / costo mensual | Tamaño relativo del pasivo no reportado |
| Cuentas por pagar / costo mensual | Meses de obligación acumulada |
| Días promedio de pago | Presión de liquidez |
| P95 de rezago pago | Cola operativa |
| Glosa / facturado | Incertidumbre de reconocimiento |
| Alto costo / costo total | Concentración |
| Top prestadores / pagos | Riesgo de concentración |
| Caja / pagos próximos 30 días | Cobertura de liquidez |
| O/E morbilidad | Suficiencia ajustada por riesgo |
| Patrimonio económico / pasivo técnico | Solvencia económica |
| Stress loss / patrimonio | Resistencia a escenarios |

Estos indicadores deben monitorearse con tendencia, no solo como foto de corte.

## 12. Matriz de severidad y respuesta

Cada indicador debe tener umbrales.

| Estado | Condición | Acción |
|---|---|---|
| Verde | Dentro de rango esperado | Monitoreo ordinario |
| Amarillo | Desviación moderada | Análisis de driver |
| Naranja | Desviación material | Plan de mitigación |
| Rojo | Riesgo crítico | Comité extraordinario |

La respuesta puede incluir:

- ajuste de provisiones;
- revisión de pagos;
- negociación con prestadores;
- activación de pooling;
- solicitud de capital;
- priorización de caja;
- revisión de glosas;
- actualización de expected loss;
- stress adicional.

## 13. Suficiencia UPC bajo estrés

La suficiencia UPC puede evaluarse como:

$$
\text{Ratio de suficiencia} = \frac{\text{Ingreso UPC esperado}}
{\text{Costo médico esperado} + \text{gasto administrativo técnico}}
$$

Bajo estrés:

$$
\text{Ratio estrés} = \frac{\text{Ingreso UPC estrés}}
{\text{Costo médico estrés} + \text{gasto técnico estrés}}
$$

Si el ratio está persistentemente por debajo de 1, el problema no es solo de liquidez. Es un déficit técnico.

El análisis debe separarse por:

- régimen;
- región;
- grupo etario;
- morbilidad;
- alto costo;
- red;
- contrato;
- periodo.

## 14. Activos y calidad de activos

Solvencia no depende únicamente de pasivos. También depende de la calidad y liquidez de activos.

Preguntas:

- ¿Qué parte de activos es caja?
- ¿Qué parte son cuentas por cobrar?
- ¿Qué antigüedad tienen?
- ¿Qué probabilidad de recaudo tienen?
- ¿Existen restricciones de uso?
- ¿Hay concentración de deudores?
- ¿Los activos pueden realizarse antes de los pagos médicos?
- ¿Hay deterioro contable insuficiente?

Una cuenta por cobrar de baja recuperabilidad no protege liquidez real.

## 15. Stress de activos

Escenarios:

| Escenario | Impacto |
|---|---|
| Recaudo tardío | Deterioro de caja |
| Deterioro de cartera | Reducción de patrimonio económico |
| Menor rendimiento financiero | Menor ingreso |
| Restricción de liquidez | Activos no monetizables |
| Concentración de deudor | Riesgo de incumplimiento |

El análisis conjunto activo-pasivo es necesario porque los choques pueden afectar ambos lados del balance.

## 16. Asset adequacy y salud

ASOP 57 enfatiza que, cuando se emiten opiniones sobre reservas y elementos actuariales, deben considerarse métodos, supuestos, datos, cambios metodológicos, eventos posteriores y documentación. En salud, el principio aplicable es que los activos disponibles deben evaluarse contra pasivos técnicos bajo escenarios razonables y adversos.

Una prueba simplificada de adecuación:

$$
\text{Activos líquidos y realizables}
\geq
\text{Pasivos técnicos esperados}
+
\text{stress de pasivos}
$$

Si no se cumple, se requiere análisis de mitigación:

- capital adicional;
- reestructuración de pagos;
- mejora de recaudo;
- reducción de rezagos;
- mecanismos de pooling;
- ajuste de provisiones;
- cambios de red o contratos;
- gestión clínica de alto costo.

## 17. Eventos posteriores

Los eventos posteriores al corte pueden cambiar la conclusión.

Ejemplos:

- conciliación masiva con IPS;
- entrada de casos catastróficos;
- cambio regulatorio;
- nueva información de glosas;
- pago extraordinario;
- pérdida de liquidez;
- fallo judicial;
- ajuste de UPC;
- información de MIPRES;
- deterioro de cartera.

El reporte debe indicar si se revisaron eventos posteriores relevantes y cómo afectan la estimación.

## 18. Cambios de método y supuestos

Todo cambio material debe cuantificarse cuando sea posible.

Ejemplos:

- pasar de pagos a reconocidos;
- cambiar factores de desarrollo;
- incorporar alto costo separado;
- cambiar expected loss ratio;
- modificar margen;
- cambiar tratamiento de glosas;
- excluir periodos afectados por ruptura;
- incorporar modelo de morbilidad;
- pasar de determinístico a estocástico.

El reporte debe separar variación por experiencia de variación por método.

## 19. Escenario base, adverso y severo

Una estructura práctica:

| Escenario | Uso |
|---|---|
| Base | Plan financiero central |
| Adverso | Gestión de riesgo y contingencia |
| Severo | Solvencia, capital y continuidad |

Ejemplo de supuestos:

| Variable | Base | Adverso | Severo |
|---|---:|---:|---:|
| Inflación médica | Esperada | +5 p.p. | +10 p.p. |
| Alto costo | Esperado | P90 | P99 |
| Rezago pago | Histórico | +30 días | +90 días |
| Glosa levantada | Esperada | +10% | +25% |
| Ingreso UPC | Esperado | -2% | -5% |
| Cartera recuperable | Esperada | -10% | -30% |

Los valores son ilustrativos; deben calibrarse con experiencia propia y juicio técnico.

## 20. Modelo de capital económico

Un modelo de capital económico puede estimar:

$$
\text{Capital requerido} = Q_{\alpha}(\text{Pérdida económica})
-
\text{Pérdida esperada}
$$

La pérdida económica puede incluir:

- desviación de costo médico;
- IBNR adicional;
- alto costo extremo;
- deterioro de glosas;
- deterioro de cartera;
- descalce de liquidez;
- gastos financieros;
- shocks regulatorios o tecnológicos.

El nivel $\alpha$ debe definirse según apetito de riesgo y uso del modelo.

## 21. Prueba de continuidad operativa

La continuidad no depende solo de capital. También depende de capacidad de mantener red y pagos.

Preguntas:

- ¿Cuántos meses de pagos médicos cubre la caja?
- ¿Qué prestadores concentran el riesgo?
- ¿Qué pasa si el principal prestador acelera radicación?
- ¿Qué pasa si se bloquea financiación de corto plazo?
- ¿Qué servicios críticos se afectarían?
- ¿Qué pagos deben priorizarse?
- ¿Qué mecanismos de contingencia existen?

El stress testing debe traducirse en plan operativo.

## 22. Plan de mitigación

Cada escenario crítico debe tener respuesta.

| Riesgo | Mitigación |
|---|---|
| IBNR subestimado | Revisión metodológica y margen |
| Alto costo extremo | Pooling, reaseguro, caso a caso |
| Déficit UPC | Evidencia técnica para ajuste y gestión clínica |
| Glosas deterioradas | Auditoría y conciliación priorizada |
| Liquidez insuficiente | Plan de caja y negociación |
| Datos débiles | Validación y reconciliación |
| Concentración IPS | Diversificación o acuerdo contractual |
| Tecnología nueva | Evaluación de impacto presupuestal |

Sin plan de mitigación, el stress test es solo un ejercicio descriptivo.

## 23. Reporting para comité

Un reporte ejecutivo debe incluir:

- posición de solvencia;
- posición de liquidez;
- cambios contra periodo anterior;
- drivers principales;
- escenarios de estrés;
- brechas de caja;
- suficiencia UPC;
- IBNR y cuentas por pagar;
- alto costo y concentración;
- alertas;
- decisiones requeridas.

Un reporte técnico debe incluir:

- datos;
- metodología;
- supuestos;
- modelos;
- validación;
- sensibilidades;
- limitaciones;
- anexos reproducibles.

## 24. Gobierno del stress testing

El proceso debe definir:

| Elemento | Requisito |
|---|---|
| Periodicidad | Mensual, trimestral o por evento |
| Escenarios | Base, adverso, severo, inverso |
| Responsable | Actuarial, riesgos, finanzas |
| Aprobación | Comité técnico o junta |
| Datos | Fuente y fecha de corte |
| Modelo | Versión y cambios |
| Umbrales | Verde/amarillo/naranja/rojo |
| Acciones | Planes de mitigación |
| Seguimiento | Cierre de acciones |

El gobierno debe evitar que los escenarios se ajusten para producir resultados cómodos.

## 25. Reverse stress testing

El reverse stress testing parte de una falla y pregunta qué condiciones la causarían.

Ejemplos:

- ¿Qué aumento de alto costo agota caja en 90 días?
- ¿Qué reducción de ingresos UPC produce patrimonio económico negativo?
- ¿Qué porcentaje de glosas levantadas rompe solvencia?
- ¿Qué rezago de pago vuelve inmanejable la red?
- ¿Qué severidad P99 requiere capital adicional?

Este enfoque ayuda a identificar vulnerabilidades no obvias.

## 26. Checklist operativo

Antes de cerrar un informe de solvencia y liquidez:

- ¿Las reservas están actualizadas?
- ¿El IBNR fue reconciliado con contabilidad?
- ¿Las cuentas por pagar tienen aging?
- ¿La caja está proyectada semanal o mensualmente?
- ¿Se separa solvencia de liquidez?
- ¿Se evalúa alto costo por cola?
- ¿Se estresa inflación médica?
- ¿Se estresan glosas y reconocimientos?
- ¿Se considera cartera y calidad de activos?
- ¿Se incluyen eventos posteriores?
- ¿Se cuantifican cambios metodológicos?
- ¿Hay escenarios base, adverso y severo?
- ¿Existe plan de mitigación?
- ¿El comité aprobó supuestos?
- ¿El reporte es reproducible?

## 27. Conclusión

La gestión de solvencia y liquidez en salud no puede depender de indicadores contables aislados. Requiere una visión integrada de activos, pasivos, reservas, UPC, alto costo, glosas, pagos, morbilidad, tecnología y escenarios adversos.

Para Colombia, la prioridad técnica es convertir el stress testing en una herramienta recurrente de gobierno. No basta con estimar una reserva central; hay que medir qué pasa si la morbilidad empeora, si la liquidez se restringe, si el alto costo se concentra, si las glosas se levantan o si los activos no se recuperan.

El resultado debe ser accionable: alertas tempranas, planes de mitigación, decisiones de capital, priorización de caja, ajustes metodológicos y evidencia técnica para discusión regulatoria.

## Fuentes de trabajo del proyecto

- ASOP No. 57, *Asset Adequacy Analysis for Life Insurance, Annuity, or Health Insurance Reserves and Other Liabilities*.
- ASOP No. 56, *Modeling*, como referencia para uso previsto, estructura, supuestos, volatilidad, validación y riesgo de modelo.
- ASOP No. 28, *Statements of Actuarial Opinion Regarding Health Insurance Assets and Liabilities*.
- `gemini-deep-research-report.md`, secciones sobre solvencia, liquidez, IBNR, teoría de ruina, TVaR, dependencia de cola, UPC, alto costo y sostenibilidad del SGSSS.
- `chatgpt-deep-research-report.md`, secciones sobre reservas, solvencia, eventos extremos, inflación médica, riesgo catastrófico y modernización actuarial.

## Próximo capítulo

➡️ **39 · Colombia Scenario Planning and Reform Roadmap** *(pendiente de crear)*
