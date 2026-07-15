---
title: "Playbook de implementación y plantillas"
description: "Guía de implementación, controles, entregables y plantillas para operacionalizar un proceso de reservas de salud."
chapter: 40
part: "part-07-colombia"
language: "es"
status: "draft"
version: "0.1.11"
last_updated: "2026-07-14"
jurisdiction: "Colombia"
---

# Playbook de implementación y plantillas

Este capítulo convierte la hoja de ruta técnica de Colombia en un playbook operativo. Su objetivo es entregar plantillas, checklists y estructuras de trabajo que puedan usarse para implementar reserving, IBNR, calidad de datos, ajuste por morbilidad, alto costo, solvencia, liquidez y reporting en una EPS, asegurador, consultor, auditor o equipo regulatorio.

Los capítulos anteriores describen métodos. Este capítulo organiza la ejecución. La diferencia es importante: una metodología técnicamente correcta puede fallar si no tiene responsables, calendario, datos reconciliados, controles, evidencia, aprobación y trazabilidad.

## Objetivos de aprendizaje

Al terminar este capítulo, el lector debería poder:

- Diseñar un plan de implementación de reserving y analítica actuarial en salud.
- Usar plantillas de nota técnica, RACI, matriz de datos, control de supuestos y comité.
- Definir entregables mínimos por frente de trabajo.
- Establecer una cadencia mensual de cierre actuarial.
- Construir paquetes de auditoría y evidencia.
- Preparar una transición ordenada hacia modelos de morbilidad, alto costo y stress testing.

## 1. Estructura del playbook

El playbook se organiza en diez módulos:

| Módulo | Propósito |
|---|---|
| 1. Gobierno | Roles, decisiones, aprobaciones |
| 2. Datos | Inventario, calidad, linaje y reconciliación |
| 3. Reservas | IBNR, IBNER, obligaciones y métodos |
| 4. Glosas | Probabilidad de reconocimiento y desarrollo |
| 5. Alto costo | Segmentación, cola y pooling |
| 6. Morbilidad | Ajuste de riesgo y suficiencia UPC |
| 7. Liquidez | Flujo de caja y cuentas por pagar |
| 8. Solvencia | Balance económico y estrés |
| 9. Reporting | Notas, tableros y comités |
| 10. Auditoría | Evidencia, reproducibilidad y hallazgos |

Cada módulo debe tener un dueño, una frecuencia, una fuente de datos, una salida y un control.

## 2. Plantilla de charter del proyecto

El charter define el alcance y evita ambigüedad.

| Campo | Contenido esperado |
|---|---|
| Nombre del proyecto | Ejemplo: implementación de IBNR y reporting actuarial |
| Patrocinador | Dirección financiera, técnica o riesgos |
| Dueño técnico | Actuarial |
| Objetivo | Qué decisión soporta |
| Alcance | Segmentos, periodos, entidades, productos |
| Fuera de alcance | Temas excluidos explícitamente |
| Fecha de corte inicial | Primer periodo de análisis |
| Fuentes | Sistemas y archivos incluidos |
| Entregables | Nota técnica, modelo, dashboard, reporte |
| Frecuencia | Mensual, trimestral, piloto |
| Criterio de éxito | Métricas verificables |
| Riesgos | Datos, talento, plazos, dependencias |
| Aprobación | Comité o responsable |

Un proyecto sin charter termina discutiendo alcance durante el cierre.

## 3. RACI mínimo

Una matriz RACI debe definir responsabilidad real.

| Actividad | Actuarial | Datos/TI | Finanzas | Operación | Auditoría médica | Riesgos | Dirección |
|---|---|---|---|---|---|---|---|
| Extracción de datos | C | R | C | C | C | I | I |
| Validación de calidad | R | R | C | C | C | C | I |
| Reconciliación contable | C | C | R | C | I | C | I |
| Construcción de triángulos | R | C | C | I | I | C | I |
| Selección metodológica | R | I | C | I | C | C | A |
| Revisión de glosas | C | I | C | C | R | C | I |
| Alto costo caso a caso | C | I | C | C | R | C | A |
| Stress testing | R | C | R | I | C | R | A |
| Nota técnica | R | C | C | C | C | C | A |
| Aprobación final | C | I | C | I | I | C | A |

Leyenda:

- R: responsable de ejecutar.
- A: accountable o aprobador.
- C: consultado.
- I: informado.

## 4. Calendario mensual de cierre actuarial

Un cierre mensual puede estructurarse así:

| Día hábil | Actividad | Responsable |
|---|---|---|
| D+1 | Congelar corte de datos | Datos/TI |
| D+2 | Validar completitud y llaves | Datos + actuarial |
| D+3 | Reconciliar pagos, reconocidos y contabilidad | Finanzas |
| D+4 | Actualizar triángulos | Actuarial |
| D+5 | Actualizar glosas y alto costo | Operación + auditoría médica |
| D+6 | Ejecutar modelos IBNR/IBNER | Actuarial |
| D+7 | Revisar variaciones | Actuarial + finanzas |
| D+8 | Ejecutar sensibilidades y estrés | Actuarial + riesgos |
| D+9 | Preparar nota técnica y reporte ejecutivo | Actuarial |
| D+10 | Comité de aprobación | Dirección |

La cadencia puede ajustarse, pero el orden lógico debe preservarse: datos, reconciliación, modelo, revisión, aprobación.

## 5. Matriz de inventario de datos

Toda implementación debe iniciar con inventario.

| Fuente | Dueño | Periodo disponible | Granularidad | Campos clave | Calidad | Uso |
|---|---|---|---|---|---|---|
| Afiliación |  |  | Afiliado-mes | ID, edad, sexo, régimen |  | Exposición |
| RIPS |  |  | Prestación | Diagnóstico, CUPS, fecha |  | Morbilidad |
| FEV |  |  | Factura | Factura, prestador, valor |  | Facturación |
| Radicación |  |  | Cuenta | Fecha radicación, estado |  | Rezagos |
| Pagos |  |  | Pago | Fecha, valor, factura |  | Triángulos |
| Glosas |  |  | Glosa | Causal, valor, estado |  | IBNER |
| MIPRES |  |  | Prescripción | Tecnología, indicación |  | No UPC |
| CAC |  |  | Cohorte | Condición, estado |  | Alto costo |
| Contabilidad |  |  | Cuenta contable | Pasivo, pago, provisión |  | Reconciliación |
| Contratos |  |  | Prestador | Modalidad, tarifa |  | Precio |

La columna “calidad” debe tener evidencia: no basta con “buena” o “regular”.

## 6. Checklist de calidad de datos

Controles mínimos:

- Campos obligatorios completos.
- Fechas válidas.
- Valores no negativos o explicados.
- Afiliado identificado.
- Servicio dentro de vigencia de afiliación.
- Diagnóstico válido.
- Procedimiento válido.
- Factura única o duplicado explicado.
- Pago vinculado a factura o cuenta.
- Glosa vinculada a cuenta original.
- Notas crédito vinculadas.
- Prestador válido.
- Régimen y municipio consistentes.
- Moneda y unidades homogéneas.
- Corte de datos documentado.

Cada control debe producir:

- número de registros afectados;
- valor financiero afectado;
- materialidad;
- decisión: corregir, excluir, ajustar o documentar.

## 7. Plantilla de reconciliación financiera

La reconciliación debe explicar diferencias entre operación, contabilidad y modelo.

| Concepto | Valor | Fuente | Comentario |
|---|---:|---|---|
| Facturado bruto |  | FEV / cuentas |  |
| Devoluciones |  | Operación |  |
| Facturado neto |  | Cálculo |  |
| Glosado |  | Auditoría |  |
| Reconocido |  | Finanzas / operación |  |
| Pagado |  | Tesorería |  |
| Pendiente reconocido |  | Cálculo |  |
| Radicado no liquidado esperado |  | Modelo |  |
| IBNER |  | Modelo |  |
| IBNR |  | Modelo |  |
| Provisión total técnica |  | Modelo |  |
| Pasivo contable |  | Contabilidad |  |
| Diferencia explicada |  | Análisis |  |
| Diferencia no explicada |  | Análisis |  |

La diferencia no explicada debe estar bajo umbral de materialidad.

## 8. Plantilla de nota técnica de IBNR

Una nota técnica mínima debe contener:

| Sección | Contenido |
|---|---|
| Objetivo | Qué pasivo se estima |
| Alcance | Población, producto, periodo |
| Fecha de corte | Fecha contable y fecha de extracción |
| Definiciones | IBNR, IBNER, obligaciones conocidas |
| Datos | Fuentes, filtros, validaciones |
| Reconciliación | Puente operativo-contable-actuarial |
| Segmentación | Régimen, región, servicio, alto costo |
| Métodos | Chain Ladder, BF, GLM, caso a caso |
| Supuestos | Factores, ELR, glosas, tendencia |
| Selección | Criterio actuarial |
| Resultados | Por segmento y total |
| Variación | Cambio contra cierre anterior |
| Sensibilidades | Supuestos críticos |
| Backtesting | Precisión histórica |
| Limitaciones | Datos, métodos, cambios operativos |
| Gobierno | Revisión y aprobación |
| Anexos | Triángulos, tablas, controles |

La nota técnica debe poder reconstruirse con los archivos de soporte.

## 9. Plantilla de control de supuestos

| Supuesto | Valor | Fuente | Método de selección | Cambio vs anterior | Impacto | Aprobador |
|---|---:|---|---|---:|---:|---|
| Factor desarrollo 0-1 |  | Triángulo | Promedio ponderado |  |  |  |
| Factor cola |  | Juicio / experiencia | Selección actuarial |  |  |  |
| ELR esperado |  | UPC / experiencia | BF |  |  |  |
| Glosa levantada |  | Histórico glosas | Modelo / promedio |  |  |  |
| Alto costo esperado |  | CAC / MIPRES | Riesgo colectivo |  |  |  |
| Inflación médica |  | Tendencia | Escenario |  |  |  |
| Margen técnico |  | Política | Riesgo residual |  |  |  |

Los supuestos no deben cambiar sin explicación.

## 10. Plantilla de análisis de variación

| Driver | Impacto | Evidencia | Comentario |
|---|---:|---|---|
| Exposición |  | Afiliación |  |
| Frecuencia |  | Servicios |  |
| Severidad |  | Costo medio |  |
| Morbilidad |  | Score / condiciones |  |
| Alto costo |  | Casos materiales |  |
| Glosas |  | Auditoría |  |
| Desarrollo |  | Triángulos |  |
| Liquidez |  | Pagos |  |
| Método |  | Nota técnica |  |
| Datos |  | Validaciones |  |
| Total variación |  | Reconciliación |  |

Esta tabla debe explicar el movimiento del pasivo o resultado técnico entre cierres.

## 11. Plantilla de backtesting

| Periodo estimado | Estimación original | Observado actual | Error | Error % | Comentario |
|---|---:|---:|---:|---:|---|
|  |  |  |  |  |  |

Análisis adicional:

- error por segmento;
- error por método;
- error por madurez;
- error por alto costo;
- sesgo sistemático;
- decisión metodológica.

Un backtesting que no modifica decisiones futuras es un control incompleto.

## 12. Plantilla de glosas

| Causal | Valor glosado | % levantado histórico | Valor esperado reconocido | Edad promedio | Acción |
|---|---:|---:|---:|---:|---|
| Pertinencia |  |  |  |  |  |
| Soporte |  |  |  |  |  |
| Tarifa |  |  |  |  |  |
| Duplicidad |  |  |  |  |  |
| Cobertura |  |  |  |  |  |
| Otra |  |  |  |  |  |

Las glosas deben modelarse como probabilidad y severidad de reconocimiento futuro, no como simple exclusión automática.

## 13. Plantilla de alto costo

| Condición / tecnología | Casos | Costo esperado | P95 | IBNR | Mecanismo | Comentario |
|---|---:|---:|---:|---:|---|---|
| Oncología |  |  |  |  | UPC / MIPRES |  |
| ERC |  |  |  |  | CAC / UPC |  |
| VIH |  |  |  |  | CAC / UPC |  |
| Huérfanas |  |  |  |  | MIPRES / pooling |  |
| Trasplantes |  |  |  |  | Alto costo |  |
| UCI prolongada |  |  |  |  | UPC / stop-loss |  |

Cada fila debe indicar si el riesgo está financiado por UPC, CAC, MIPRES, presupuesto máximo, pooling u otro mecanismo.

## 14. Plantilla de modelo de morbilidad

| Elemento | Definición |
|---|---|
| Unidad de análisis | Afiliado-mes o afiliado-año |
| Periodo observación |  |
| Periodo predicción |  |
| Target | Costo UPC, total, alto costo, etc. |
| Variables demográficas | Edad, sexo, región, régimen |
| Variables clínicas | Diagnósticos, agrupadores, crónicos |
| Variables farmacia | Medicamentos, persistencia |
| Variables utilización | Hospitalización, urgencias, UCI |
| Modelo base | Demográfico |
| Modelo clínico | GLM/GAM |
| Challenger | Boosting / ML |
| Métricas | O/E, MAE, deciles, calibración |
| Controles | Upcoding, estabilidad, sesgo |

El modelo debe iniciar en shadow mode antes de afectar transferencias o decisiones financieras.

## 15. Plantilla de stress testing

| Variable | Base | Adverso | Severo | Fuente |
|---|---:|---:|---:|---|
| Inflación médica |  |  |  |  |
| Alto costo |  |  |  |  |
| IBNR |  |  |  |  |
| Glosa levantada |  |  |  |  |
| Rezago pago |  |  |  |  |
| Ingreso UPC |  |  |  |  |
| Cartera recuperable |  |  |  |  |
| Liquidez inicial |  |  |  |  |

Salidas:

| Métrica | Base | Adverso | Severo |
|---|---:|---:|---:|
| Provisión total |  |  |  |
| Déficit de caja |  |  |  |
| Patrimonio económico |  |  |  |
| Cuentas por pagar |  |  |  |
| Días de pago |  |  |  |
| Necesidad de capital |  |  |  |

## 16. Plantilla de comité actuarial

Agenda mínima:

1. Cambios de datos.
2. Reconciliación financiera.
3. Resultado de reservas.
4. Variación contra periodo anterior.
5. Alto costo.
6. Glosas.
7. Liquidez.
8. Solvencia y stress testing.
9. Supuestos modificados.
10. Limitaciones.
11. Decisiones requeridas.
12. Aprobaciones.
13. Acciones y responsables.

Acta mínima:

| Decisión | Responsable | Fecha compromiso | Evidencia requerida | Estado |
|---|---|---|---|---|
|  |  |  |  |  |

Las decisiones deben quedar vinculadas a evidencia.

## 17. Plantilla de dashboard ejecutivo

Indicadores mínimos:

| Indicador | Actual | Anterior | Variación | Estado |
|---|---:|---:|---:|---|
| Siniestralidad UPC |  |  |  |  |
| Provisión total |  |  |  |  |
| IBNR |  |  |  |  |
| Cuentas por pagar |  |  |  |  |
| Días promedio de pago |  |  |  |  |
| Glosa / facturado |  |  |  |  |
| Alto costo / total |  |  |  |  |
| Caja / pagos 30 días |  |  |  |  |
| Stress loss / patrimonio |  |  |  |  |
| Riesgo de datos |  |  |  |  |

Cada indicador debe tener umbral verde, amarillo, naranja o rojo.

## 18. Plantilla de paquete de auditoría

El paquete de auditoría debe incluir:

- nota técnica final;
- base de datos congelada o identificador de extracción;
- diccionario de datos;
- controles de calidad;
- reconciliación contable;
- triángulos;
- supuestos;
- resultados por método;
- selección actuarial;
- sensibilidad;
- backtesting;
- acta de aprobación;
- versión de código o modelo;
- cambios contra periodo anterior;
- limitaciones;
- evidencia de revisión independiente.

La regla práctica: un tercero competente debe poder reconstruir el resultado.

## 19. Plantilla de issue log

| ID | Hallazgo | Materialidad | Responsable | Acción | Fecha | Estado |
|---|---|---|---|---|---|---|
|  |  | Alta / Media / Baja |  |  |  | Abierto / Cerrado |

Tipos de hallazgo:

- datos incompletos;
- duplicados;
- falta de reconciliación;
- cambio operativo;
- método no documentado;
- supuesto sin soporte;
- diferencia contable;
- error de fórmula;
- link roto;
- capítulo fuera del nav;
- falla de build.

## 20. Plantilla de decisión metodológica

| Elemento | Contenido |
|---|---|
| Decisión |  |
| Alternativas evaluadas |  |
| Método seleccionado |  |
| Razón técnica |  |
| Evidencia |  |
| Impacto financiero |  |
| Riesgos |  |
| Limitaciones |  |
| Aprobador |  |
| Fecha |  |

Esto evita que la metodología dependa de memoria institucional.

## 21. Plantilla de control de cambios

| Versión | Fecha | Cambio | Motivo | Impacto | Aprobador |
|---|---|---|---|---:|---|
|  |  |  |  |  |  |

Cambios que deben registrarse:

- nueva fuente;
- cambio de filtro;
- cambio de método;
- cambio de supuesto;
- cambio de segmentación;
- cambio de tratamiento de glosas;
- cambio de calendario;
- cambio de capítulo o nav;
- cambio de plantilla.

## 22. Plantilla de validación MkDocs

Para este repositorio, el cierre editorial debe verificar:

- todos los `.md` están en `mkdocs.yml`;
- `mkdocs.yml` no apunta a archivos faltantes;
- cada capítulo tiene front matter;
- cada capítulo tiene un solo H1;
- no hay code fences desbalanceados;
- no hay links internos rotos;
- los bloques “Próximo capítulo” no apuntan a capítulos inexistentes;
- `python scripts/audit_docs.py` termina sin issues;
- `python -m mkdocs build --strict` termina sin warnings.

Esta validación es parte del control de entrega.

## 23. Plantilla de definición de listo

Un capítulo o entregable está listo cuando:

| Criterio | Estado |
|---|---|
| Archivo guardado en ruta correcta |  |
| Front matter completo |  |
| H1 único |  |
| Incluido en nav |  |
| Próximo capítulo actualizado |  |
| Fuentes internas citadas |  |
| Sin links rotos |  |
| Auditoría estructural limpia |  |
| Build strict exitoso |  |
| Revisión conceptual realizada |  |

No debe subirse a GitHub antes de cumplir estos criterios.

## 24. Playbook de implementación mínima

Orden recomendado:

1. Crear inventario de datos.
2. Ejecutar validaciones básicas.
3. Reconciliar contra contabilidad.
4. Construir triángulos.
5. Estimar IBNR con dos métodos.
6. Seleccionar resultado y documentar juicio.
7. Analizar glosas.
8. Separar alto costo.
9. Construir tablero de liquidez.
10. Ejecutar stress base/adverso/severo.
11. Documentar nota técnica.
12. Presentar a comité.
13. Registrar decisiones.
14. Cerrar hallazgos.
15. Versionar entregables.

## 25. Playbook avanzado

Después de estabilizar lo mínimo:

1. Construir matriz afiliado-mes.
2. Crear agrupadores de morbilidad.
3. Estimar modelo demográfico base.
4. Estimar modelo clínico GLM/GAM.
5. Evaluar challenger ML.
6. Operar shadow model.
7. Modelar alto costo con frecuencia-severidad.
8. Integrar MIPRES, CAC y No UPC.
9. Estimar capital económico.
10. Automatizar reportes.
11. Implementar validación independiente.
12. Recalibrar periódicamente.

## 26. Riesgos de ejecución

| Riesgo | Señal temprana | Mitigación |
|---|---|---|
| Datos no confiables | Reconciliación falla | Fase de calidad antes de modelar |
| Falta de dueño | Acciones sin cierre | RACI y comité |
| Modelo opaco | No se explica resultado | Base GLM/GAM interpretable |
| Doble conteo | UPC, CAC, MIPRES mezclados | Mapa de capas |
| Uso prematuro | Modelo sin backtesting | Shadow mode |
| Cambios no controlados | Resultados no reproducibles | Control de versiones |
| Dependencia manual | Cierre lento | Automatización gradual |
| Falta de auditoría | Supuestos sin soporte | Paquete de evidencia |

## 27. Cierre de Parte VII

La Parte VII traduce el reserving actuarial al contexto colombiano. El recorrido parte de metodologías de reserving en salud, pasa por triángulos, datos, glosas, capitación, ajuste por morbilidad, alto costo, RIPS-FEV, provisiones técnicas, solvencia y escenarios, y termina en este playbook de implementación.

La conclusión práctica es directa: Colombia no necesita solamente mejores modelos. Necesita mejores procesos técnicos. Un modelo aislado no resuelve el problema si los datos no están reconciliados, las reservas no son trazables, las glosas no se modelan, el alto costo no se separa, la liquidez no se proyecta y las decisiones no quedan documentadas.

Este playbook busca que cada capítulo se convierta en acción verificable.

## Fuentes de trabajo del proyecto

- ASOP No. 1, *Introductory Actuarial Standard of Practice*, como referencia general de práctica actuarial.
- ASOP No. 23, *Data Quality*, como referencia conceptual para selección, revisión y comunicación de datos.
- ASOP No. 28, *Statements of Actuarial Opinion Regarding Health Insurance Assets and Liabilities*.
- ASOP No. 45, *The Use of Health Status Based Risk Adjustment Methodologies*.
- ASOP No. 56, *Modeling*.
- ASOP No. 57, *Asset Adequacy Analysis for Life Insurance, Annuity, or Health Insurance Reserves and Other Liabilities*.
- `gemini-deep-research-report.md`, recomendaciones priorizadas y brechas para Colombia.
- `chatgpt-deep-research-report.md`, recomendaciones de implementación, datos, ajuste de riesgo, reservas y modernización actuarial.

## Próximo capítulo

Fin de la Parte VII · Colombia.
