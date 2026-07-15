---
title: "Auditoría de reclamaciones, denegaciones y controversias"
description: "Modelación del efecto de auditorías, denegaciones, glosas y controversias sobre el monto y el tiempo de las reservas de salud."
chapter: 27
part: "part-06-health-specific"
language: "es"
status: "draft"
version: "0.1.12"
last_updated: "2026-07-14"
---

# Auditoría de reclamaciones, denegaciones y controversias

Este capítulo desarrolla el efecto de la auditoría de cuentas médicas, las denegaciones, glosas, devoluciones y controversias sobre las reservas de salud. En muchos portafolios, una parte material del pasivo no corresponde a reclamaciones no reportadas, sino a reclamaciones conocidas cuyo monto final depende de auditoría médica, revisión contractual, documentación, conciliación y resolución de disputas.

El reserving de salud debe reconocer que una cuenta radicada no es necesariamente una obligación definitiva, una glosa no es necesariamente una recuperación segura y un pago parcial no implica cierre económico. El actuario debe modelar estados, probabilidades de reconocimiento, tiempos de resolución y montos finales esperados.

## Objetivos de aprendizaje

Al finalizar este capítulo, el lector debería poder:

- Distinguir auditoría, devolución, denegación, glosa, ajuste y disputa.
- Separar incertidumbre de monto, incertidumbre de estado e incertidumbre de tiempo.
- Estimar reservas para cuentas conocidas, cuentas objetadas y controversias.
- Reconocer cómo auditoría y glosas afectan triángulos pagados e incurridos.
- Diseñar modelos de probabilidad de reconocimiento y tiempo de resolución.
- Construir controles de reconciliación entre operación, contabilidad y reserving.

## 1. Auditoría de cuentas médicas

La auditoría de cuentas médicas es el proceso mediante el cual el pagador revisa una reclamación para validar cobertura, pertinencia, tarifa, soporte, duplicidad, codificación y cumplimiento contractual.

Puede incluir:

- auditoría administrativa;
- auditoría médica;
- auditoría tarifaria;
- auditoría contractual;
- auditoría de pertinencia;
- auditoría de duplicados;
- auditoría de soportes;
- auditoría de autorizaciones;
- auditoría de calidad de datos.

Desde reserving, la auditoría introduce incertidumbre porque el monto radicado puede diferir del monto finalmente reconocido y pagado.

## 2. Conceptos básicos

Los términos varían por país y operación, pero conviene separar:

| Concepto | Descripción | Efecto actuarial |
|---|---|---|
| Devolución | Cuenta rechazada por forma, soporte o canal | Puede ser reradicada |
| Denegación | Rechazo de cobertura o responsabilidad | Puede generar apelación |
| Glosa | Objeción parcial o total del monto | Incertidumbre de reconocimiento |
| Ajuste | Corrección de valor, tarifa o codificación | Cambia monto reconocido |
| Disputa | Controversia entre partes | Incertidumbre de monto y tiempo |
| Conciliación | Acuerdo posterior | Reduce incertidumbre |
| Reapertura | Movimiento después de cierre | Desarrollo tardío |

Una taxonomía clara evita doble conteo y mejora la medición del pasivo.

## 3. Estados financieros y operativos

Una cuenta médica puede estar en distintos estados:

| Estado | Interpretación | Reserva posible |
|---|---|---|
| Radicada sin auditar | Cuenta conocida, monto no validado | Reserva por valor esperado |
| Auditada sin objeción | Monto reconocido pendiente de pago | Cuenta por pagar |
| Glosada parcial | Monto parcialmente objetado | Reserva por probabilidad de reconocimiento |
| Glosada total | Monto totalmente objetado | Reserva si hay probabilidad de reversión |
| Devuelta | No aceptada formalmente | Reserva si se espera reradicación válida |
| En apelación | Prestador o afiliado controvierte decisión | Reserva por resolución esperada |
| En conciliación | Negociación activa | Reserva por acuerdo esperado |
| Pagada parcial | Saldo pendiente o disputado | Reserva por remanente |
| Cerrada | Sin movimientos esperados | Sin reserva salvo reapertura |
| Reabierta | Cuenta previamente cerrada con nuevo movimiento | Reserva por ajuste esperado |

El estado operativo debe estar fechado. Sin fecha, no puede construirse un historial de desarrollo confiable.

## 4. Incertidumbre de monto

La incertidumbre de monto aparece cuando el valor final reconocido no se conoce.

Ejemplo:

| Concepto | Valor |
|---|---:|
| Monto facturado | 1,000 |
| Monto glosado | 300 |
| Monto reconocido inicial | 700 |
| Monto probable de reversión | 120 |
| Monto final esperado | 820 |

El valor esperado puede expresarse como:

$$
E[M] = M_{\text{reconocido}} + p_{\text{reversión}} \times M_{\text{glosado}}
$$

Si $p_{\text{reversión}} = 40\%$, entonces:

$$
E[M] = 700 + 0.40 \times 300 = 820
$$

La reserva debe reflejar el monto esperado, no necesariamente el valor facturado ni el valor inicialmente reconocido.

## 5. Incertidumbre de estado

La incertidumbre de estado ocurre cuando no se conoce cuál será la trayectoria final de la cuenta.

Una cuenta glosada puede:

- mantenerse glosada;
- aceptarse parcialmente;
- aceptarse totalmente;
- devolverse;
- conciliarse;
- judicializarse;
- pagarse;
- cerrarse sin pago.

Cada ruta tiene probabilidad, monto y tiempo esperados. La reserva debe ponderar estos escenarios.

## 6. Incertidumbre de tiempo

El tiempo de resolución afecta:

- flujo de caja;
- aging de cuentas;
- selección de factores de desarrollo;
- reconocimiento contable;
- cierre financiero;
- estimación de IBNER;
- comunicación de suficiencia.

Una glosa de alta probabilidad de reversión pero resolución lenta puede generar una reserva material durante varios periodos. Un pago rápido puede aparecer como desarrollo acelerado aunque el costo médico no haya cambiado.

## 7. Devoluciones

Una devolución suele indicar que la cuenta no fue aceptada por problemas de forma o soporte. No siempre elimina el pasivo económico.

Preguntas actuariales:

- ¿La prestación ocurrió?
- ¿El servicio estaba cubierto?
- ¿El prestador puede corregir y reradicar?
- ¿La devolución es definitiva o subsanable?
- ¿Cuál es la tasa histórica de reradicación?
- ¿Cuál es el monto reconocido después de reradicación?

Si una devolución tiene alta probabilidad de corrección, excluirla completamente puede subestimar reservas.

## 8. Denegaciones

Una denegación puede estar relacionada con:

- no cobertura;
- falta de autorización;
- servicio excluido;
- duplicidad;
- afiliado no elegible;
- periodo no cubierto;
- incumplimiento contractual;
- falta de pertinencia médica.

La denegación puede ser definitiva o apelable. El modelo debe distinguir:

- denegaciones administrativas;
- denegaciones clínicas;
- denegaciones contractuales;
- denegaciones por elegibilidad;
- denegaciones por documentación.

Cada grupo puede tener tasa de reversión distinta.

## 9. Glosas u objeciones

Las glosas u objeciones pueden ser parciales o totales. Pueden referirse a monto, tarifa, pertinencia, soporte, duplicidad, codificación o contrato.

Variables relevantes:

- tipo de glosa;
- monto glosado;
- porcentaje glosado;
- prestador;
- servicio;
- diagnóstico;
- modalidad contractual;
- edad de la glosa;
- respuesta del prestador;
- historial de conciliación;
- pagos parciales;
- instancia de disputa.

La reserva por glosas puede modelarse como:

$$
R_{\text{glosa}} = \sum_i p_i \times M_i
$$

donde $p_i$ es la probabilidad de reconocimiento y $M_i$ es el monto objetado.

## 10. Ajustes y recobros

Los ajustes pueden aumentar o disminuir la obligación. Pueden aparecer por:

- corrección tarifaria;
- nota crédito;
- nota débito;
- devolución posterior;
- recuperación;
- pago duplicado;
- conciliación;
- auditoría retrospectiva;
- cambio de codificación.

El actuario debe separar ajustes normales de desarrollo tardío. Si los ajustes son recurrentes y materiales, deben incorporarse en la reserva.

## 11. Reaperturas

Una cuenta cerrada puede reabrirse por:

- error administrativo;
- apelación tardía;
- fallo judicial;
- conciliación posterior;
- auditoría retrospectiva;
- soporte adicional;
- ajuste contractual;
- pago duplicado detectado.

La tasa de reapertura es una métrica crítica:

$$
\text{Tasa de reapertura} = \frac{\text{cuentas reabiertas}}{\text{cuentas cerradas}}
$$

Aunque la tasa sea baja, la severidad puede ser alta.

## 12. Inventario de cuentas conocidas

El inventario de cuentas conocidas es una fuente clave para reservas.

Debe contener:

| Campo | Uso |
|---|---|
| ID cuenta | Trazabilidad |
| Prestador | Segmentación |
| Afiliado o episodio | Agrupación |
| Fecha de servicio | Periodo económico |
| Fecha de radicación | Reporte |
| Fecha de auditoría | Proceso |
| Estado actual | Clasificación |
| Monto facturado | Base inicial |
| Monto reconocido | Pasivo aceptado |
| Monto glosado | Controversia |
| Monto pagado | Reducción de pasivo |
| Saldo | Reserva potencial |
| Tipo de glosa | Modelo de probabilidad |
| Fecha de última gestión | Aging |

Sin inventario confiable, las reservas por cuentas conocidas pueden depender demasiado de factores agregados.

## 13. Aging

El aging mide antigüedad de cuentas o controversias.

Ejemplo:

| Rango de antigüedad | Monto pendiente | Probabilidad de pago |
|---|---:|---:|
| 0-30 días | 1,000 | 95% |
| 31-60 días | 800 | 85% |
| 61-90 días | 500 | 70% |
| 91-180 días | 300 | 50% |
| >180 días | 200 | 25% |

La probabilidad de reconocimiento puede disminuir o aumentar con el tiempo, dependiendo del proceso. Por ejemplo, cuentas en conciliación avanzada pueden tener mayor probabilidad de pago que cuentas sin gestión.

## 14. Probabilidad de reconocimiento

La probabilidad de reconocimiento puede estimarse por:

- histórico de glosas resueltas;
- tipo de objeción;
- prestador;
- servicio;
- monto;
- edad de la cuenta;
- respuesta del prestador;
- instancia de disputa;
- modalidad contractual;
- experiencia de conciliación.

Modelo conceptual:

$$
p_i = \Pr(\text{monto reconocido} > 0 \mid X_i)
$$

También puede modelarse la proporción reconocida:

$$
q_i = E\left[\frac{\text{monto reconocido}}{\text{monto glosado}} \mid X_i\right]
$$

La reserva esperada sería:

$$
R_i = M_i \times p_i \times q_i
$$

## 15. Tiempo de resolución

El tiempo hasta resolución puede modelarse con curvas de supervivencia o modelos multiestado.

Definición:

$$
T_i = \text{fecha de resolución}_i - \text{fecha de glosa}_i
$$

Métricas útiles:

- mediana de resolución;
- percentil 75 y 90;
- proporción resuelta a 30, 60, 90 y 180 días;
- aging pendiente;
- velocidad por prestador;
- velocidad por tipo de glosa.

El tiempo afecta flujo de caja y persistencia del pasivo.

## 16. Modelos multiestado

Las controversias pueden representarse como proceso multiestado:

$$
\text{Radicada} \rightarrow \text{Auditada} \rightarrow \text{Glosada} \rightarrow \text{Respondida} \rightarrow \text{Conciliada} \rightarrow \text{Pagada}
$$

También puede existir transición a cierre sin pago:

$$
\text{Glosada} \rightarrow \text{Cerrada sin reconocimiento}
$$

El modelo estima:

- probabilidades de transición;
- tiempos de permanencia;
- monto esperado por transición;
- probabilidad de reapertura.

Este enfoque es más informativo que tratar todas las glosas como un porcentaje fijo.

## 17. Efecto sobre triángulos pagados

Las glosas y denegaciones afectan triángulos pagados porque retrasan pagos o reducen montos.

Efectos posibles:

- desarrollo más lento;
- pagos concentrados por conciliación;
- factores altos en edades tardías;
- diagonales anómalas por depuración;
- cambios por política de auditoría;
- reducción artificial de pagos recientes.

Si una política de auditoría se vuelve más estricta, los pagos pueden caer temporalmente aunque la obligación económica no desaparezca.

## 18. Efecto sobre triángulos incurridos

El incurrido puede definirse de distintas formas:

- facturado;
- permitido;
- reconocido;
- pagado más saldo;
- contable;
- estimado final.

La definición determina cómo entran glosas y disputas. Si el incurrido usa monto facturado, puede sobrestimar obligación. Si usa monto reconocido inicial, puede subestimar reversión de glosas.

La definición debe documentarse y mantenerse consistente.

## 19. Efecto sobre IBNR e IBNER

Las cuentas objetadas suelen pertenecer más a IBNER o a cuentas conocidas pendientes que a IBNR puro.

Separación práctica:

| Componente | Ejemplo |
|---|---|
| IBNR puro | Servicios ocurridos no radicados |
| Cuenta conocida | Radicada pendiente de auditoría |
| IBNER | Desarrollo adicional sobre cuenta conocida |
| Disputa | Monto objetado con probabilidad de reconocimiento |
| Reapertura | Movimiento posterior al cierre |

Mezclar estos componentes puede dificultar explicación y backtesting.

## 20. Métodos de estimación

Opciones:

| Método | Uso |
|---|---|
| Porcentaje histórico de reversión | Portafolios simples |
| Aging por estado | Inventario robusto |
| Probabilidad por tipo de glosa | Segmentación operativa |
| Frecuencia-severidad | Monto esperado por controversia |
| Supervivencia | Tiempo de resolución |
| Multiestado | Trayectorias de disputa |
| GLM/GAM | Probabilidad o proporción reconocida |
| Machine learning | Alta dimensionalidad |
| Escenarios | Cambios operativos o legales |

El método debe ser proporcional a materialidad, datos disponibles y capacidad de gobierno.

## 21. Segmentación

Segmentos útiles:

- prestador;
- red;
- tipo de servicio;
- contrato;
- tipo de glosa;
- estado operativo;
- edad de cuenta;
- monto;
- región;
- línea de negocio;
- alto costo vs corriente;
- pago por evento vs capitación;
- cuentas judicializadas o no judicializadas.

La segmentación debe evitar tanto mezcla excesiva como fragmentación sin credibilidad.

## 22. Cambios operativos

La historia puede volverse no comparable por:

- nueva política de auditoría;
- cambio de proveedor de auditoría;
- cambio de sistema;
- automatización;
- depuración masiva;
- conciliación extraordinaria;
- cambio de contrato;
- cambio regulatorio;
- nuevos requisitos documentales.

Estos cambios deben registrarse como eventos calendario. En triángulos pueden aparecer como diagonales o cohortes anómalas.

## 23. Controles de datos

Controles mínimos:

| Control | Riesgo mitigado |
|---|---|
| Estado único vigente | Doble clasificación |
| Historial de estados | Pérdida de trazabilidad |
| Montos coherentes | Saldos negativos o imposibles |
| Fechas ordenadas | Errores de ciclo |
| IDs únicos | Duplicados |
| Conciliación de pagos | Diferencias con tesorería |
| Conciliación contable | Diferencias con cuentas por pagar |
| Catálogo de glosas | Clasificación inconsistente |
| Aging actualizado | Sobre/subestimación |

La calidad de datos es especialmente importante porque las cuentas disputadas suelen tener movimientos manuales.

## 24. Aplicación al contexto colombiano

En Colombia, las glosas, devoluciones y controversias son componentes centrales del ciclo de cuentas médicas. Pueden involucrar:

- facturación electrónica;
- RIPS;
- soportes clínicos;
- auditoría médica;
- reglas contractuales;
- giro directo;
- conciliaciones EPS-IPS;
- cuentas de alto costo;
- tecnologías con financiación especial;
- procesos judiciales o administrativos.

Para reserving, conviene separar:

- cuentas radicadas sin auditar;
- glosas administrativas;
- glosas médicas;
- devoluciones subsanables;
- controversias en conciliación;
- saldos reconocidos pendientes de pago;
- pagos parciales;
- recuperaciones o notas crédito.

La aplicación específica colombiana puede requerir capítulos propios por su complejidad normativa y operativa.

## 25. Ejemplo conceptual

Supóngase un inventario:

| Estado | Monto | Factor esperado |
|---|---:|---:|
| Reconocido pendiente | 1,000 | 100% |
| Glosa médica | 500 | 45% |
| Glosa administrativa | 300 | 70% |
| Devolución subsanable | 200 | 60% |
| Disputa antigua | 150 | 30% |

Reserva:

$$
R = 1{,}000 + 500(0.45) + 300(0.70) + 200(0.60) + 150(0.30)
$$

$$
R = 1{,}600
$$

El monto facturado total es 2,150, pero el valor esperado reservado es 1,600. La diferencia debe documentarse como probabilidad de no reconocimiento, no como simple descuento arbitrario.

## 26. Backtesting

El backtesting debe comparar:

- monto reservado vs monto finalmente pagado;
- probabilidad estimada vs tasa real de reconocimiento;
- tiempo estimado vs tiempo real de resolución;
- resultados por tipo de glosa;
- resultados por prestador;
- resultados por edad de cuenta;
- recuperaciones esperadas vs reales;
- reaperturas esperadas vs reales.

Métricas:

| Métrica | Uso |
|---|---|
| Observado/Esperado | Calibración |
| Error absoluto | Magnitud de desviación |
| Bias por segmento | Sesgo sistemático |
| Curva de resolución | Tiempo |
| Tasa de reapertura | Desarrollo tardío |
| Tasa de reversión | Reconocimiento de glosas |

El backtesting debe usarse para recalibrar factores y no solo para reportar error.

## 27. Gobierno

La nota técnica debe documentar:

- definiciones de estados;
- catálogo de glosas o denegaciones;
- fuentes de datos;
- reglas de corte;
- criterios de inclusión;
- tratamiento de pagos parciales;
- tratamiento de devoluciones;
- modelo de probabilidad;
- modelo de tiempo;
- factores seleccionados;
- supuestos de conciliación;
- cambios operativos;
- reconciliación contable;
- limitaciones.

El proceso debe involucrar áreas actuarial, financiera, auditoría médica, operaciones y jurídica cuando aplique.

## 28. Checklist práctico

Antes de cerrar reservas por auditoría y disputas, confirmar:

- Las cuentas conocidas están identificadas.
- Los estados operativos son consistentes.
- Los montos facturado, reconocido, glosado, pagado y saldo cuadran.
- Las glosas se clasifican por tipo.
- Las devoluciones subsanables se tratan separadamente.
- Los pagos parciales no se consideran cierre definitivo sin regla explícita.
- Las probabilidades de reconocimiento están calibradas.
- El aging se usa en la estimación.
- Las reaperturas se monitorean.
- Las conciliaciones extraordinarias se documentan.
- La reserva se reconcilia con contabilidad.

## 29. Conclusiones

La auditoría de cuentas médicas, las denegaciones, glosas y controversias son una fuente material de incertidumbre en reserving de salud. No son simples reducciones del monto facturado ni simples retrasos de pago. Son procesos con estados, probabilidades, tiempos y montos esperados.

Una práctica robusta separa cuentas conocidas, IBNR puro, IBNER, disputas y reaperturas. Además, modela la probabilidad de reconocimiento, el tiempo de resolución y el efecto de cambios operativos. Esta disciplina mejora la precisión de reservas, la reconciliación contable y la comunicación con auditoría, finanzas y operaciones.

El siguiente capítulo cierra el bloque de especificidades de salud con gobierno, controles y reporting de reservas.

## Referencias

- ASOP No. 1, Introductory Actuarial Standard of Practice.
- ASOP No. 23, Data Quality.
- ASOP No. 38, Using Models Outside the Actuary's Area of Expertise.
- ASOP No. 43, Property/Casualty Unpaid Claim Estimates.
- ASOP No. 45, The Use of Health Status Based Risk Adjustment Methodologies.
- ASOP No. 56, Modeling.
- Society of Actuaries, materiales técnicos sobre health claims, denials management, completion factors and health reserving.

## Próximo capítulo

➡️ **[Health Reserving Governance, Controls and Reporting](28-health-reserving-governance-controls-and-reporting.md)**
