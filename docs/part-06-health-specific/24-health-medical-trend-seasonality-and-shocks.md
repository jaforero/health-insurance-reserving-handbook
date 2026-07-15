---
title: "Health Medical Trend, Seasonality and Shocks"
part: "Parte VI · Especificidades de salud"
chapter: 24
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

# Health Medical Trend, Seasonality and Shocks

Este capítulo desarrolla tres fuerzas que afectan directamente las reservas de salud: tendencia médica, estacionalidad y shocks. Aunque los métodos de reserving suelen apoyarse en patrones históricos de desarrollo, la experiencia de salud puede cambiar rápidamente por inflación médica, nuevas tecnologías, cambios de utilización, epidemias, ajustes regulatorios, cambios de red, acumulación de demanda o variaciones operativas.

La estimación actuarial debe distinguir entre desarrollo normal de reclamaciones y cambios reales en el nivel esperado del costo médico. Si esta distinción no se hace, el modelo puede interpretar incorrectamente una tendencia como rezago, una estacionalidad como deterioro o un shock como patrón permanente.

## Objetivos de aprendizaje

Al finalizar este capítulo, el lector debería poder:

- Definir tendencia médica y separar sus componentes principales.
- Distinguir tendencia de utilización, severidad, mix, morbilidad e inflación.
- Identificar patrones estacionales clínicos, administrativos y financieros.
- Reconocer shocks que invalidan o debilitan patrones históricos.
- Incorporar tendencia, estacionalidad y shocks en métodos de reserving.
- Diseñar controles de backtesting y monitoreo para periodos recientes.

## 1. Tendencia médica

La tendencia médica representa el cambio esperado en el costo médico por unidad de exposición a través del tiempo. En forma simplificada:

$$
T = \frac{\text{Costo esperado futuro}}{\text{Costo esperado base}} - 1
$$

En salud, la tendencia no es un solo fenómeno. Puede provenir de:

- mayor utilización;
- mayor severidad;
- inflación de tarifas;
- cambios tecnológicos;
- cambio de mix de servicios;
- mayor morbilidad;
- envejecimiento de la población;
- cambios de acceso;
- cambios regulatorios;
- cambios en cobertura;
- comportamiento de prestadores;
- cambios en auditoría y reconocimiento.

Por tanto, aplicar una tasa única de tendencia sin diagnóstico puede ocultar riesgos importantes.

## 2. Descomposición de la tendencia

Una descomposición práctica separa exposición, utilización, severidad y mix:

$$
1 + T_C =
(1 + T_E)(1 + T_U)(1 + T_S)(1 + T_M) - 1
$$

donde:

- $T_C$ es la tendencia del costo total;
- $T_E$ es el cambio de exposición;
- $T_U$ es la tendencia de utilización;
- $T_S$ es la tendencia de severidad o precio;
- $T_M$ es el efecto de mix, morbilidad o complejidad.

Para reserving, normalmente interesa aislar $T_U$, $T_S$ y $T_M$, porque la exposición se modela explícitamente.

## 3. Tendencia de utilización

La tendencia de utilización mide cambios en la cantidad de servicios por unidad de exposición:

$$
T_U =
\frac{U_t}{U_{t-1}} - 1
$$

Puede aumentar por:

- mayor demanda médica;
- envejecimiento de la población;
- expansión de cobertura;
- menor barrera de acceso;
- más autorizaciones aprobadas;
- cambios de práctica médica;
- acumulación de demanda represada;
- campañas de diagnóstico;
- epidemias o brotes.

También puede disminuir por:

- restricciones de red;
- cambios de copago o autorización;
- sustitución hacia atención ambulatoria;
- prevención efectiva;
- cambios de codificación;
- retrasos de reporte.

El actuario debe validar si el cambio de utilización es clínico, administrativo o de datos.

## 4. Tendencia de severidad

La tendencia de severidad mide cambios en el costo promedio por servicio, evento o reclamación:

$$
T_S =
\frac{S_t}{S_{t-1}} - 1
$$

Puede estar asociada con:

- inflación tarifaria;
- renegociación contractual;
- cambio de prestador;
- mayor complejidad clínica;
- nuevos medicamentos;
- nuevas tecnologías;
- concentración de alto costo;
- menor glosa o mayor reconocimiento;
- cambios en copagos o deducibles;
- pagos extraordinarios.

Una severidad creciente no siempre implica mayor precio. Puede reflejar cambio de mix hacia servicios más complejos.

## 5. Tendencia de mix

El mix describe la composición de servicios, diagnósticos, prestadores o poblaciones. Si cambia el mix, el costo promedio puede cambiar incluso si las tarifas unitarias son estables.

Ejemplo:

| Servicio | Costo unitario | Participación base | Participación actual |
|---|---:|---:|---:|
| Consulta | 100 | 70% | 55% |
| Procedimiento | 500 | 25% | 35% |
| Hospitalización | 2,000 | 5% | 10% |

El costo promedio aumenta aunque cada servicio conserve su precio. En reserving, este efecto puede confundirse con tendencia de severidad si no se estandariza.

## 6. Morbilidad y riesgo poblacional

La tendencia también puede provenir de cambios en la morbilidad de la población cubierta. Dos portafolios con igual exposición pueden tener costos esperados distintos si cambia la composición por edad, diagnóstico, región o riesgo clínico.

Una forma de controlar este efecto es usar exposición ajustada:

$$
E^* = \sum_i E_i r_i
$$

donde $r_i$ es un factor relativo de riesgo.

El PMPM ajustado por riesgo se calcula como:

$$
\text{PMPM ajustado} = \frac{C}{E^*}
$$

Si el PMPM bruto sube pero el PMPM ajustado permanece estable, el cambio puede estar explicado por morbilidad, no por deterioro de eficiencia.

## 7. Tendencia observada vs tendencia esperada

La tendencia observada se calcula con datos históricos. La tendencia esperada incorpora juicio prospectivo.

| Tipo | Base | Uso |
|---|---|---|
| Observada | Experiencia histórica | Diagnóstico y calibración |
| Normalizada | Experiencia ajustada por mix o riesgo | Comparación homogénea |
| Prospectiva | Supuestos futuros | Proyección |
| Implícita | Derivada de tarifas, contratos o presupuestos | Validación |
| Seleccionada | Juicio actuarial documentado | Reserving y pricing |

En reserving, la tendencia seleccionada debe considerar si el periodo de valoración ya contiene parte del cambio esperado.

## 8. Estacionalidad

La estacionalidad es un patrón recurrente dentro del año. En salud puede afectar:

- ocurrencia de servicios;
- reporte;
- facturación;
- auditoría;
- pagos;
- cierres contables.

Una serie mensual puede mostrar variación por razones clínicas y administrativas simultáneamente.

Ejemplos:

| Patrón | Posible causa |
|---|---|
| Aumento respiratorio | Temporadas de infección |
| Caída en vacaciones | Menor demanda o menor radicación |
| Picos de cierre | Procesos contables |
| Pagos concentrados | Ciclos de tesorería |
| Mayor siniestralidad escolar | Calendario académico |
| Campañas preventivas | Programas de detección |

El método debe separar estacionalidad médica de estacionalidad operativa.

## 9. Estacionalidad de ocurrencia

La estacionalidad de ocurrencia se relaciona con la fecha de servicio. Refleja cambios reales en utilización o severidad médica.

Puede analizarse con:

$$
I_m = \frac{\text{PMPM del mes } m}{\text{PMPM promedio anual}}
$$

donde $I_m$ es un índice estacional del mes $m$.

Si enero tiene $I_{ene}=1.10$, el costo esperado de enero es 10% superior al promedio anual, manteniendo constantes otros factores.

## 10. Estacionalidad de reporte

La estacionalidad de reporte se relaciona con la fecha de radicación o recepción de cuentas. Puede reflejar:

- vacaciones administrativas;
- retrasos de prestadores;
- cierres de facturación;
- cambios de sistemas;
- acumulación de cuentas;
- campañas de depuración.

No debe confundirse con mayor ocurrencia médica. Si el reporte cae en diciembre y sube en enero, el costo de servicio puede no haber cambiado.

## 11. Estacionalidad de pago

La estacionalidad de pago se relaciona con tesorería y procesos financieros. Puede depender de:

- calendarios de giro;
- disponibilidad presupuestal;
- acuerdos con prestadores;
- pagos masivos;
- conciliaciones;
- cierres de año;
- restricciones de caja.

Los triángulos pagados son especialmente sensibles a esta estacionalidad. Un cambio en calendario de pagos puede distorsionar factores de desarrollo.

## 12. Efectos calendario

Los efectos calendario atraviesan diagonales del triángulo. Pueden aparecer cuando un evento externo afecta todos los periodos de origen observados en un mismo periodo calendario.

Ejemplos:

- cambio regulatorio;
- inflación médica extraordinaria;
- cambio de sistema de facturación;
- política de pago nueva;
- shock epidemiológico;
- conciliación masiva;
- cambio de red.

En un triángulo, estos efectos pueden verse como diagonales anómalas. Si no se ajustan, contaminan factores de desarrollo.

## 13. Shocks

Un shock es un evento no recurrente o abrupto que altera la experiencia. Puede ser temporal o permanente.

Tipos de shocks:

| Tipo | Ejemplo | Efecto |
|---|---|---|
| Epidemiológico | Brote, pandemia | Utilización y severidad |
| Regulatorio | Cambio de cobertura | Nivel de costo |
| Operativo | Cambio de sistema | Reporte y pago |
| Contractual | Cambio de red o tarifa | Severidad |
| Judicial | Fallos o tutelas | Cobertura y acceso |
| Económico | Inflación o devaluación | Medicamentos e insumos |
| Tecnológico | Nueva terapia | Severidad y mix |

La primera pregunta es si el shock afecta ocurrencia, reporte, reconocimiento o pago.

## 14. Shocks temporales vs permanentes

No todos los shocks deben proyectarse igual.

| Clasificación | Tratamiento |
|---|---|
| Temporal y cerrado | Ajuste puntual o exclusión |
| Temporal con cola | Escenario de runoff |
| Permanente | Cambio de nivel o tendencia |
| Transitorio con rebote | Modelar demanda represada |
| Incierto | Escenarios ponderados |

Un pago masivo atrasado puede ser un shock de caja, no un aumento de costo médico. Una nueva tecnología cubierta puede ser un cambio permanente de severidad.

## 15. Demanda represada

La demanda represada ocurre cuando servicios esperados no se realizan en un periodo y aparecen posteriormente. Puede observarse después de:

- restricciones de movilidad;
- congestión de red;
- cambios de autorización;
- huelgas o cierres;
- pandemias;
- problemas de acceso;
- migraciones de sistema.

En reserving, la demanda represada puede generar una aparente caída seguida de aumento. Proyectar solo con el periodo de caída subestima reservas; proyectar solo con el rebote puede sobreestimarlas.

## 16. Incorporación en métodos clásicos

### Chain Ladder

Chain Ladder supone que los patrones históricos de desarrollo son informativos. Tendencia, estacionalidad o shocks pueden violar este supuesto.

Posibles ajustes:

- excluir diagonales anómalas;
- seleccionar factores manualmente;
- segmentar periodos afectados;
- usar factores ponderados;
- complementar con Bornhuetter-Ferguson;
- usar escenarios.

### Bornhuetter-Ferguson

Bornhuetter-Ferguson permite incorporar una expectativa a priori de pérdida o PMPM. Es útil cuando los datos recientes están inmaduros o afectados por shocks.

La clave es documentar la expectativa:

$$
\widehat{U} = \text{Exposición} \times \text{PMPM esperado}
$$

La tendencia seleccionada afecta directamente ese PMPM esperado.

### Cape Cod

Cape Cod puede estimar una expectativa basada en experiencia ajustada por exposición. Es útil si se normaliza por cambios de mix, tendencia y exposición.

## 17. Incorporación en GLM y GAM

Los modelos estadísticos pueden incorporar covariables:

- periodo calendario;
- mes de servicio;
- mes de reporte;
- tendencia temporal;
- indicadores de shock;
- días hábiles;
- tipo de contrato;
- red de prestador;
- mix de servicios;
- factores de riesgo.

Un GLM puede capturar tendencia lineal o categórica. Un GAM puede capturar relaciones suaves no lineales:

$$
g(\mu) = \alpha + f_1(\text{tiempo}) + f_2(\text{mes}) + X\beta
$$

La inclusión de covariables mejora explicación, pero requiere cuidado para no sobreajustar eventos no recurrentes.

## 18. Incorporación en modelos machine learning

Modelos de árboles, boosting o deep learning pueden capturar interacciones entre tendencia, estacionalidad y segmentación. Sin embargo, también pueden aprender ruido operativo como si fuera señal permanente.

Controles mínimos:

- validación temporal;
- backtesting rolling-origin;
- variables observables al corte;
- análisis de estabilidad;
- importancia de variables;
- comparación contra benchmarks;
- escenarios fuera de muestra.

La capacidad predictiva no sustituye el juicio actuarial sobre permanencia del shock.

## 19. Backtesting de tendencia

El backtesting debe responder:

- ¿La tendencia seleccionada fue suficiente?
- ¿El error provino de utilización, severidad o mix?
- ¿La estacionalidad fue capturada?
- ¿El shock fue temporal o permanente?
- ¿El modelo reaccionó demasiado tarde?
- ¿El modelo sobrerreaccionó a un evento no recurrente?

Una métrica útil es el error de PMPM último:

$$
\text{Error PMPM} =
\frac{\widehat{\text{PMPM último}} - \text{PMPM real}}{\text{PMPM real}}
$$

También debe revisarse el error por segmento, no solo agregado.

## 20. Monitoreo prospectivo

El monitoreo debe incluir señales tempranas:

- variación de PMPM observado;
- frecuencia por mil;
- severidad promedio;
- mix de servicios;
- aging de cuentas;
- velocidad de reporte;
- velocidad de pago;
- proporción de glosas;
- concentración de alto costo;
- indicadores epidemiológicos;
- cambios normativos o contractuales.

Las señales deben clasificarse como clínicas, operativas, financieras o de datos.

## 21. Aplicación al contexto colombiano

En Colombia, tendencia, estacionalidad y shocks pueden estar influenciados por:

- cambios de UPC o mecanismos de financiación;
- modificaciones de cobertura;
- ajustes de presupuestos máximos;
- glosas, devoluciones y conciliaciones;
- cambios en facturación electrónica y RIPS;
- giros directos;
- concentración de alto costo;
- acciones judiciales;
- cambios en red de prestación;
- diferencias regionales de acceso;
- calendarios de cierre y reporte.

El actuario debe evitar interpretar cambios administrativos como cambios médicos sin evidencia. También debe evitar ignorar cambios clínicos reales porque se parecen a rezagos operativos.

## 22. Ejemplo conceptual

Supóngase que el PMPM observado aumenta de 100 a 118. La descomposición muestra:

| Componente | Impacto |
|---|---:|
| Utilización | 6% |
| Severidad | 5% |
| Mix de alto costo | 4% |
| Efecto combinado | 3% |

La tendencia total aproximada es:

$$
(1.06)(1.05)(1.04) - 1 = 15.8\%
$$

El resto hasta 18% podría explicarse por interacción, cambios residuales o ruido. La reserva debe usar esta información para seleccionar supuestos, no simplemente extrapolar 18% como tendencia permanente.

## 23. Checklist práctico

Antes de aplicar tendencia o ajustar por shocks, validar:

- La exposición está medida consistentemente.
- La tendencia se analiza por utilización, severidad y mix.
- La estacionalidad clínica se separa de la administrativa.
- Los pagos masivos se identifican.
- Los cambios regulatorios están documentados.
- Los cambios contractuales están incorporados.
- Los shocks se clasifican como temporales o permanentes.
- El backtesting revisa periodos recientes.
- La metodología documenta el juicio actuarial.
- Los escenarios adversos son explícitos.

## 24. Conclusiones

Tendencia médica, estacionalidad y shocks son esenciales para interpretar reservas de salud. Los patrones históricos de desarrollo son útiles, pero pueden fallar cuando el nivel de costo, el mix, la operación o el entorno cambian.

Una práctica robusta separa tendencia de utilización, severidad, mix y morbilidad; distingue estacionalidad de ocurrencia, reporte y pago; y clasifica shocks según permanencia e impacto. Esta disciplina reduce el riesgo de reservas insuficientes o excesivas y mejora la comunicación con áreas financieras, técnicas y operativas.

El siguiente capítulo profundiza en risk adjustment, morbilidad y segmentación clínica como herramientas para normalizar experiencia y mejorar estimaciones.

## Referencias

- ASOP No. 1, Introductory Actuarial Standard of Practice.
- ASOP No. 23, Data Quality.
- ASOP No. 38, Using Models Outside the Actuary's Area of Expertise.
- ASOP No. 43, Property/Casualty Unpaid Claim Estimates.
- ASOP No. 56, Modeling.
- Society of Actuaries, materiales técnicos sobre medical trend, health reserving y completion factors.

## Próximo capítulo

➡️ **[Health Risk Adjustment and Morbidity](25-health-risk-adjustment-and-morbidity.md)**
