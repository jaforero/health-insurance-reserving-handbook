---
title: "Health Reserving Governance, Controls and Reporting"
part: "Parte VI · Especificidades de salud"
chapter: 28
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

# Health Reserving Governance, Controls and Reporting

Este capítulo cierra el bloque de especificidades de salud con un marco práctico de gobierno, controles y reporting para reservas. En seguros de salud, la reserva no es únicamente un resultado de modelo. Es un proceso mensual o periódico que integra datos clínicos, operación de cuentas, contratos, contabilidad, tesorería, auditoría médica, regulación, juicio actuarial y comunicación ejecutiva.

Un proceso técnicamente sólido puede fallar si no tiene controles de datos, trazabilidad de supuestos, validación independiente, reconciliación financiera y documentación. A la inversa, un proceso bien gobernado puede mejorar progresivamente aunque inicie con métodos simples. El objetivo del gobierno no es burocratizar el reserving, sino hacerlo reproducible, explicable y confiable.

## Objetivos de aprendizaje

Al finalizar este capítulo, el lector debería poder:

- Diseñar un marco de gobierno para reservas de salud.
- Definir roles, responsabilidades y niveles de aprobación.
- Implementar controles de datos, modelos, supuestos y resultados.
- Construir un calendario de cierre actuarial.
- Documentar juicio actuarial, cambios metodológicos y limitaciones.
- Preparar reportes ejecutivos, técnicos y regulatorios.
- Diseñar monitoreo continuo y backtesting.

## 1. Gobierno del reserving

Gobierno del reserving es el conjunto de políticas, procesos, controles y responsabilidades que aseguran que las reservas sean:

- técnicamente razonables;
- consistentes con la información disponible;
- reproducibles;
- reconciliadas con finanzas;
- documentadas;
- revisadas;
- comunicadas con claridad;
- actualizadas ante nueva evidencia.

En salud, el gobierno debe cubrir no solo el modelo actuarial, sino también el flujo de datos y los procesos operativos que determinan el pasivo.

## 2. Principios rectores

Un marco robusto debe seguir principios básicos:

| Principio | Implicación práctica |
|---|---|
| Trazabilidad | Cada resultado debe poder reconstruirse |
| Reproducibilidad | El mismo input debe producir el mismo output |
| Materialidad | El esfuerzo de control se enfoca en riesgos relevantes |
| Independencia | Resultados críticos tienen revisión técnica |
| Consistencia | Definiciones estables entre periodos |
| Transparencia | Supuestos y limitaciones se documentan |
| Proporcionalidad | Complejidad acorde con riesgo y datos |
| Actualización | Cambios de experiencia modifican supuestos cuando corresponde |

Estos principios aplican tanto a métodos clásicos como a GLM, GAM, machine learning o modelos multiestado.

## 3. Roles y responsabilidades

El proceso de reservas de salud requiere coordinación entre múltiples áreas.

| Rol | Responsabilidades |
|---|---|
| Actuarial | Metodología, supuestos, estimación, backtesting |
| Finanzas | Contabilidad, cuentas por pagar, cierre financiero |
| Operaciones | Radicación, auditoría, estados de cuentas |
| Auditoría médica | Glosas, pertinencia, reconocimiento |
| Tecnología/datos | Extracción, transformación, calidad y linaje |
| Jurídica | Controversias, contratos, litigios |
| Tesorería | Pagos, giros, flujo de caja |
| Dirección técnica | Aprobación y uso de resultados |
| Auditoría interna | Revisión de controles |

Un error común es asumir que reserving es responsabilidad exclusiva del área actuarial. En salud, la estimación depende de procesos operativos y financieros que deben gobernarse conjuntamente.

## 4. Matriz RACI

Una matriz RACI ayuda a asignar responsabilidad:

| Actividad | Responsable | Aprueba | Consultado | Informado |
|---|---|---|---|---|
| Extracción de datos | Datos | Actuarial | Operaciones | Finanzas |
| Validación de calidad | Actuarial | Actuarial senior | Datos | Finanzas |
| Reconciliación contable | Finanzas | Finanzas | Actuarial | Dirección |
| Selección de supuestos | Actuarial | Comité técnico | Finanzas/Operación | Dirección |
| Resultado final | Actuarial | Dirección técnica | Finanzas | Auditoría |
| Cambios metodológicos | Actuarial | Comité técnico | Riesgos/Auditoría | Dirección |
| Reporte ejecutivo | Actuarial | Dirección | Finanzas | Junta/Comité |

La matriz debe adaptarse a la estructura de la entidad.

## 5. Calendario de cierre

Un calendario de cierre define fechas, responsables y dependencias.

Ejemplo mensual:

| Día hábil | Actividad |
|---:|---|
| 1 | Cierre de fuentes operativas |
| 2 | Extracción de pagos, radicaciones, glosas y saldos |
| 3 | Validaciones de datos |
| 4 | Reconciliación con contabilidad y tesorería |
| 5 | Ejecución de modelos |
| 6 | Revisión de resultados y variaciones |
| 7 | Ajustes documentados y sensibilidad |
| 8 | Revisión técnica |
| 9 | Aprobación ejecutiva |
| 10 | Emisión de reporte final |

El calendario debe indicar qué ocurre si una fuente llega tarde o falla una reconciliación.

## 6. Inventario de fuentes

El inventario de fuentes documenta qué datos alimentan la reserva.

| Fuente | Contenido | Dueño | Control clave |
|---|---|---|---|
| Pagos | Giros y salidas de caja | Tesorería | Cruce bancario |
| Reclamaciones | Servicios y cuentas | Operaciones | Duplicados y fechas |
| Radicaciones | Cuentas recibidas | Operaciones | Conteo y monto |
| Glosas | Objeciones y estados | Auditoría médica | Aging y saldos |
| Contabilidad | Cuentas por pagar | Finanzas | Reconciliación |
| Contratos | Tarifas y modalidades | Jurídica/Contratación | Vigencia |
| Afiliados | Exposición | Operaciones | Días cubiertos |
| Riesgo clínico | Diagnósticos y morbilidad | Datos/Actuarial | Disponibilidad al corte |

Cada fuente debe tener fecha de corte, versión y responsable.

## 7. Linaje de datos

El linaje describe cómo un dato se transforma desde la fuente hasta el reporte final.

Debe documentar:

- sistema fuente;
- tabla o archivo;
- fecha de extracción;
- filtros aplicados;
- reglas de limpieza;
- reglas de exclusión;
- transformaciones;
- agregaciones;
- controles;
- versión del dataset final.

Sin linaje, no es posible explicar diferencias entre cierres ni reproducir resultados.

## 8. Controles de datos

Controles mínimos:

| Control | Propósito |
|---|---|
| Conteo de registros | Detectar extracciones incompletas |
| Suma de montos | Validar contra fuentes financieras |
| Fechas válidas | Evitar periodos imposibles |
| Duplicados | Prevenir sobreestimación |
| Valores negativos | Clasificar ajustes o recuperaciones |
| Estados válidos | Evitar categorías no mapeadas |
| Reconciliación pagos | Cuadre con tesorería |
| Reconciliación saldos | Cuadre con cuentas por pagar |
| Exposición | Cuadre de afiliados o miembros-mes |
| Cambios vs mes anterior | Detectar anomalías |

Los controles deben tener umbrales de aceptación y reglas de escalamiento.

## 9. Controles de modelo

Los controles de modelo verifican que la metodología se ejecute correctamente.

Incluyen:

- versión de código o plantilla;
- versión de supuestos;
- parámetros usados;
- selección de factores;
- validación de outputs intermedios;
- comparación contra ejecución anterior;
- revisión de sensibilidad;
- pruebas de estrés;
- backtesting;
- revisión independiente.

Un modelo no controlado puede producir resultados aparentemente precisos pero irreproducibles.

## 10. Inventario de modelos

Todo modelo utilizado debe estar en un inventario.

Campos mínimos:

| Campo | Descripción |
|---|---|
| Nombre del modelo | Identificador |
| Objetivo | Qué estima |
| Alcance | Productos o segmentos |
| Responsable | Dueño técnico |
| Método | Chain Ladder, BF, GLM, etc. |
| Inputs | Fuentes principales |
| Outputs | Reservas, intervalos, diagnósticos |
| Frecuencia | Mensual, trimestral, anual |
| Estado | Desarrollo, producción, retiro |
| Última validación | Fecha |
| Limitaciones | Riesgos conocidos |

El inventario evita modelos informales no gobernados.

## 11. Supuestos

Los supuestos son decisiones técnicas que afectan el resultado.

Ejemplos:

- factores de desarrollo;
- tail factors;
- expected loss ratio;
- PMPM esperado;
- tendencia médica;
- estacionalidad;
- factor de completitud;
- probabilidad de reconocimiento de glosas;
- tasa de reapertura;
- selección de segmentos;
- tratamiento de outliers;
- margen o provisión de incertidumbre.

Cada supuesto material debe tener:

- fuente;
- justificación;
- fecha de aprobación;
- sensibilidad;
- responsable;
- criterio de actualización.

## 12. Juicio actuarial

El juicio actuarial es necesario cuando la evidencia no es mecánica. Debe documentarse explícitamente.

Ejemplos:

- excluir una diagonal afectada por pago masivo;
- seleccionar factor distinto al promedio histórico;
- usar Bornhuetter-Ferguson por inmadurez;
- aplicar escenario por shock regulatorio;
- ajustar por cambio contractual;
- incorporar tendencia adicional por inflación médica;
- modificar tasa de reconocimiento de glosas.

El juicio no es una debilidad si está razonado, documentado y revisado.

## 13. Cambios metodológicos

Todo cambio metodológico debe tener control formal.

Clasificación:

| Tipo | Ejemplo | Aprobación |
|---|---|---|
| Menor | Corrección de etiqueta o formato | Actuarial |
| Moderado | Cambio de segmentación | Actuarial senior |
| Mayor | Cambio de método principal | Comité técnico |
| Crítico | Cambio con impacto financiero material | Dirección/Comité |

El documento de cambio debe incluir:

- motivo;
- descripción;
- impacto cuantitativo;
- pruebas realizadas;
- comparación contra método anterior;
- fecha de aplicación;
- aprobación.

## 14. Materialidad

La materialidad define qué diferencias requieren análisis o escalamiento.

Puede expresarse como:

- porcentaje de reservas;
- monto absoluto;
- porcentaje de patrimonio;
- porcentaje de primas o UPC;
- desviación por segmento;
- impacto en resultado financiero;
- impacto regulatorio.

Ejemplo:

| Nivel | Criterio | Acción |
|---|---|---|
| Bajo | Menor a 1% de reserva | Documentar |
| Medio | 1%-3% | Explicar y revisar |
| Alto | 3%-5% | Aprobación técnica |
| Crítico | Mayor a 5% | Escalamiento ejecutivo |

Los umbrales deben definirse internamente.

## 15. Reconciliación financiera

La reserva actuarial debe reconciliarse con:

- pagos;
- cuentas por pagar;
- saldos de prestadores;
- glosas;
- provisiones contables;
- recuperaciones;
- contratos;
- exposición;
- estados financieros.

Una reconciliación típica:

$$
\text{Pasivo estimado} = \text{Cuentas conocidas}
+ \text{IBNR}
+ \text{IBNER}
+ \text{Disputas esperadas}
- \text{Recuperaciones esperadas}
$$

Las diferencias entre el pasivo actuarial y los saldos contables deben explicarse, no ocultarse.

## 16. Roll-forward de reservas

El roll-forward explica cómo cambió la reserva de un cierre a otro.

Componentes:

| Componente | Interpretación |
|---|---|
| Reserva inicial | Saldo anterior |
| Pagos del periodo | Reducción por pagos |
| Nuevas ocurrencias | Costo del nuevo periodo |
| Desarrollo adverso/favorable | Cambio de estimación |
| Cambios de supuestos | Efecto metodológico |
| Cambios de exposición | Crecimiento o reducción |
| Cambios de mix/riesgo | Morbilidad o segmentación |
| Reserva final | Nuevo saldo |

El roll-forward es una herramienta central de comunicación ejecutiva.

## 17. Backtesting

El backtesting compara estimaciones pasadas con resultados emergentes.

Debe responder:

- ¿La reserva fue suficiente?
- ¿Dónde se concentró el error?
- ¿El error fue aleatorio o sistemático?
- ¿El método subestima periodos recientes?
- ¿Los supuestos de tendencia fueron adecuados?
- ¿Las glosas se reconocieron como se esperaba?
- ¿Los pagos siguieron el patrón estimado?
- ¿La exposición cambió frente a lo previsto?

El backtesting debe alimentar cambios de supuestos, no ser un reporte decorativo.

## 18. Indicadores de monitoreo

Indicadores recomendados:

| Indicador | Uso |
|---|---|
| Reserva/PMPM | Normalización por exposición |
| IBNR/costo último | Madurez |
| Pagos vs esperado | Desarrollo emergente |
| Reporte vs esperado | Rezago de cuentas |
| Aging de cuentas | Riesgo operativo |
| Glosas pendientes | Incertidumbre de reconocimiento |
| Tasa de reapertura | Desarrollo tardío |
| Desviación por segmento | Sesgo |
| Error de backtesting | Calibración |
| Ratio observado/esperado | Suficiencia |

Los indicadores deben revisarse por producto, red, contrato, región y tipo de servicio cuando sea material.

## 19. Reporting ejecutivo

El reporte ejecutivo debe ser claro y accionable.

Contenido mínimo:

- reserva total;
- cambio vs cierre anterior;
- principales drivers;
- suficiencia estimada;
- incertidumbre;
- segmentos críticos;
- cambios de supuestos;
- riesgos emergentes;
- decisiones requeridas;
- limitaciones.

Debe evitar exceso de detalle técnico. La audiencia ejecutiva necesita entender qué cambió, por qué cambió y qué implica.

## 20. Reporting técnico

El reporte técnico debe permitir revisión y reproducción.

Contenido:

- descripción de datos;
- controles ejecutados;
- metodología;
- supuestos;
- factores seleccionados;
- resultados por segmento;
- reconciliaciones;
- sensibilidad;
- backtesting;
- cambios metodológicos;
- limitaciones;
- anexos de tablas.

El reporte técnico es la evidencia principal de gobierno actuarial.

## 21. Reporting financiero

Finanzas necesita información para cierre contable.

Contenido:

- reserva final por cuenta contable;
- movimiento vs periodo anterior;
- componente IBNR;
- componente cuentas conocidas;
- glosas y disputas;
- recuperaciones;
- explicación de variaciones;
- conciliación contra saldos;
- soportes de aprobación.

La conciliación debe ser suficientemente granular para evitar ajustes manuales no trazados.

## 22. Reporting regulatorio

Cuando aplica, el reporte regulatorio debe cumplir definiciones, formatos y periodicidad exigidos. Aunque los requerimientos cambian por jurisdicción, un proceso robusto debe mantener:

- definiciones consistentes;
- soporte de datos;
- trazabilidad de cálculos;
- firmas o aprobaciones;
- evidencia de revisión;
- explicación de cambios relevantes;
- archivo histórico.

Si el reporte regulatorio exige una fórmula específica, la entidad puede mantener además una estimación económica interna, reconciliando ambas.

## 23. Comunicación de incertidumbre

Las reservas no son valores exactos. El reporte debe comunicar incertidumbre.

Formas de comunicación:

- rango razonable;
- percentiles;
- escenarios;
- sensibilidad de supuestos;
- semáforo de riesgo;
- drivers cualitativos;
- materialidad.

Ejemplo:

| Escenario | Reserva |
|---|---:|
| Favorable | 95 |
| Central | 100 |
| Adverso | 112 |
| Extremo | 125 |

El objetivo es evitar falsa precisión y permitir decisiones informadas.

## 24. Escenarios y stress testing

Los escenarios ayudan a evaluar vulnerabilidad.

Escenarios típicos:

- inflación médica superior;
- aumento de utilización;
- retraso de pagos;
- conciliación adversa de glosas;
- shock epidemiológico;
- cambio regulatorio;
- pérdida de información;
- salida de prestador clave;
- aumento de alto costo;
- deterioro de morbilidad.

Cada escenario debe tener justificación, magnitud e impacto.

## 25. Validación independiente

Los resultados materiales deben revisarse independientemente.

La revisión puede cubrir:

- datos;
- código o plantilla;
- metodología;
- supuestos;
- selección de factores;
- reconciliación;
- resultados;
- reporte;
- cumplimiento de políticas internas.

La independencia puede ser interna o externa, según materialidad y regulación.

## 26. Evidencia y archivo

El proceso debe conservar evidencia:

- datasets usados;
- versión de código;
- supuestos;
- outputs;
- controles;
- aprobaciones;
- reportes;
- comunicaciones;
- cambios metodológicos;
- reconciliaciones.

El archivo debe permitir responder: qué se sabía al corte, qué se calculó, quién aprobó y por qué.

## 27. Automatización

La automatización reduce errores, pero no elimina responsabilidad.

Automatizar:

- extracción de datos;
- controles repetitivos;
- construcción de triángulos;
- ejecución de modelos;
- generación de reportes;
- comparación contra cierres previos;
- alertas de anomalías.

No automatizar sin revisión:

- selección final de supuestos;
- tratamiento de shocks;
- juicio actuarial;
- explicación ejecutiva;
- aprobación final.

La automatización debe tener logs, versionamiento y controles.

## 28. Herramientas reproducibles

Un proceso reproducible debería usar:

- scripts versionados;
- configuración externa de supuestos;
- carpetas de inputs y outputs;
- nombres de archivos con fecha de corte;
- logs de ejecución;
- validaciones automáticas;
- documentación de ambiente;
- pruebas de consistencia.

La reproducibilidad no exige tecnología compleja. Exige disciplina.

## 29. Aplicación al contexto colombiano

En Colombia, el gobierno del reserving de salud debe considerar:

- diferencias entre prestación, radicación, contabilización y pago;
- glosas, devoluciones y conciliaciones;
- giro directo;
- contratos capitados, paquetes y pagos prospectivos;
- RIPS y factura electrónica;
- tecnologías financiadas por mecanismos especiales;
- cuentas de alto costo;
- saldos EPS-IPS;
- cambios normativos;
- intervención o reorganización de entidades;
- calidad y oportunidad de datos.

La estimación actuarial debe poder reconciliarse con operación y contabilidad. En un entorno con alta sensibilidad financiera y regulatoria, la documentación y trazabilidad son tan importantes como el modelo.

## 30. Ejemplo de paquete de cierre

Un paquete mensual de cierre podría incluir:

| Archivo | Contenido |
|---|---|
| memo ejecutivo | Resultado, drivers, riesgos |
| memo técnico | Metodología y supuestos |
| triángulos | Pagados, incurridos, reportados |
| inventario conocido | Cuentas pendientes y glosas |
| reconciliación | Contabilidad, pagos, saldos |
| backtesting | Comparación contra emergente |
| sensibilidad | Escenarios y materialidad |
| aprobaciones | Evidencia de revisión |

Este paquete reduce dependencia de conocimiento informal.

## 31. Checklist de cierre

Antes de aprobar reservas, confirmar:

- Las fuentes fueron cerradas y fechadas.
- Los controles de datos pasaron o fueron documentados.
- Los pagos reconcilian con tesorería.
- Las cuentas conocidas reconcilian con contabilidad.
- Los contratos materiales están reflejados.
- Las glosas y disputas están tratadas.
- La exposición está validada.
- Los triángulos fueron revisados.
- Los supuestos materiales están documentados.
- El resultado fue comparado contra cierre anterior.
- El backtesting fue revisado.
- Las limitaciones están comunicadas.
- La aprobación quedó registrada.

## 32. Checklist de comité

Para comité técnico o ejecutivo:

- ¿Cuál es la reserva central?
- ¿Cuál es el rango razonable?
- ¿Qué cambió desde el cierre anterior?
- ¿Cuáles son los tres principales drivers?
- ¿Qué segmentos explican la variación?
- ¿Qué supuestos cambiaron?
- ¿Qué riesgos emergentes existen?
- ¿Qué tan confiables son los datos?
- ¿Qué limitaciones deben escalarse?
- ¿Qué decisiones se requieren?

El comité debe enfocarse en decisiones y riesgos, no solo en números.

## 33. Conclusiones

El reserving de salud requiere gobierno explícito. La complejidad de datos, contratos, glosas, morbilidad, tendencia y pagos hace que el resultado dependa tanto del proceso como del método.

Un marco robusto define roles, controla datos, versiona modelos, documenta supuestos, reconcilia finanzas, valida resultados y comunica incertidumbre. Esto permite que la reserva sea defendible ante dirección, auditoría, reguladores y usuarios internos.

Con este capítulo se completa el bloque de especificidades generales de salud. El siguiente bloque profundiza en la aplicación al contexto colombiano.

## Referencias

- ASOP No. 1, Introductory Actuarial Standard of Practice.
- ASOP No. 23, Data Quality.
- ASOP No. 38, Using Models Outside the Actuary's Area of Expertise.
- ASOP No. 43, Property/Casualty Unpaid Claim Estimates.
- ASOP No. 45, The Use of Health Status Based Risk Adjustment Methodologies.
- ASOP No. 56, Modeling.
- Society of Actuaries, materiales técnicos sobre health reserving governance, model risk management, actuarial controls and reporting.

## Próximo capítulo

➡️ **[Colombia Health Reserving Methodologies](../part-07-colombia/29-colombia-health-reserving-methodologies.md)**
