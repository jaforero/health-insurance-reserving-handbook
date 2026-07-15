---
title: Comparación entre Mack y Bootstrap
description: Comparación actuarial de los supuestos, resultados, fortalezas y usos de Mack y Bootstrap para cuantificar la incertidumbre de reservas.
status: draft
version: "0.1.7"
chapter: "10"
part: "part-03-stochastic-reserving"
language: "es"
last_updated: "2026-07-14"
---

# Comparación entre Mack y Bootstrap

Mack y Bootstrap parten de Chain Ladder y buscan cuantificar la incertidumbre de la reserva. Mack lo hace mediante fórmulas analíticas basadas en medias y varianzas condicionales. Bootstrap lo hace generando múltiples historias y desarrollos futuros simulados.

No son métodos rivales. En una práctica actuarial sólida funcionan como controles complementarios.

## Objetivos

Al finalizar este capítulo, el lector podrá:

- explicar las diferencias conceptuales entre Mack y Bootstrap;
- comparar sus supuestos y resultados;
- reconocer qué fuentes de incertidumbre representa cada método;
- interpretar diferencias entre errores estándar y percentiles;
- seleccionar un enfoque según el uso del análisis;
- construir una reconciliación defendible para gestión, auditoría y gobierno.

## Punto de partida común

Ambos métodos requieren que Chain Ladder sea una representación razonable del desarrollo esperado.

Comparten, entre otros, estos riesgos:

- factores históricos no representativos;
- efectos de calendario;
- cambios de mezcla o beneficios;
- segmentación insuficiente;
- cola no observada;
- datos incompletos o inconsistentes.

La simulación no corrige una mala especificación. Un Bootstrap con muchas iteraciones puede reproducir con gran precisión la incertidumbre de un modelo equivocado.

## Diferencia conceptual

### Mack

Mack responde:

> ¿Qué error de predicción implican las medias y varianzas condicionales del modelo Chain Ladder?

Su resultado central es el MSEP y su raíz cuadrada, el error estándar.

### Bootstrap

Bootstrap responde:

> ¿Qué resultados produciría el modelo si la experiencia observada y el proceso futuro variaran de acuerdo con el mecanismo de remuestreo y simulación?

Su resultado central es una muestra de la distribución predictiva.

## Comparación resumida

| Característica | Mack | Bootstrap |
| --- | --- | --- |
| Estimación central | Chain Ladder | Cercana a Chain Ladder |
| Cálculo de incertidumbre | Analítico | Simulación |
| Distribución completa | No, requiere aproximación adicional | Sí, bajo el esquema simulado |
| Error estándar | Directo | Empírico |
| Intervalo asimétrico | Requiere supuesto distributivo | Se obtiene de percentiles simulados |
| Riesgo de parámetros | Sí | Sí, mediante remuestreo y reajuste |
| Riesgo de proceso | Sí | Sí, si se simula explícitamente |
| Costo computacional | Bajo | Medio o alto |
| Reproducibilidad | Determinística | Requiere semilla y control Monte Carlo |
| Decisiones de implementación | Relativamente pocas | Varias |
| Riesgo de modelo | No completo | No completo |

## Supuestos estadísticos

### Mack

Requiere:

- media condicional proporcional;
- estructura de varianza definida;
- independencia entre periodos de origen;
- estimación razonable de factores y varianzas.

Se denomina *distribution-free* porque no especifica una distribución completa. Sin embargo, un intervalo normal o lognormal sí añade una hipótesis distributiva.

### Bootstrap

Requiere:

- un modelo base correctamente especificado;
- residuos suficientemente representativos e intercambiables;
- una regla para corregir y remuestrear residuos;
- una distribución para el riesgo de proceso, cuando corresponda;
- decisiones sobre negativos, ceros, cola y dependencia.

El Bootstrap residual suele describirse como semiparamétrico: remuestrea residuos de manera empírica, pero con frecuencia usa una distribución paramétrica para simular el proceso futuro.

## Fuentes de incertidumbre

| Fuente | Mack | Bootstrap |
| --- | --- | --- |
| Proceso | Fórmula analítica | Simulación de celdas futuras |
| Parámetros | Fórmula analítica | Reestimación en pseudo-triángulos |
| Forma asimétrica | No directamente | Sí, dentro del diseño de simulación |
| Dependencia | Limitada por supuestos | Solo si se modela explícitamente |
| Cola | Requiere extensión | Requiere simulación o escenarios |
| Cambio estructural | No | No |
| Error de datos | No | No |

La tabla muestra por qué ambos deben acompañarse de escenarios y juicio actuarial.

## Resultados que deben compararse

Una reconciliación útil incluye:

- ultimate e IBNR esperados;
- error estándar total;
- coeficiente de variación;
- resultados por periodo de origen;
- intervalos comparables;
- P75, P90, P95 y P99;
- contribución de proceso y parámetros;
- sensibilidad a cola;
- reserva registrada y probabilidad de insuficiencia.

No debe compararse un intervalo normal de Mack con percentiles Bootstrap sin explicar que provienen de supuestos distintos.

## Intervalos de predicción

### Aproximación con Mack

Con reserva \(\widehat R\) y error estándar \(SE\):

$$
\widehat R\pm z_{1-\alpha/2}SE
$$

La aproximación normal es simétrica. Una aproximación lognormal evita reservas negativas y produce asimetría, pero cambia la interpretación y requiere calibración.

### Percentiles Bootstrap

Si \(R^{(1)},\ldots,R^{(B)}\) son reservas simuladas:

$$
L=Q_{\alpha/2}(R),
\qquad
U=Q_{1-\alpha/2}(R)
$$

Los límites reflejan la forma empírica generada por el modelo. No necesitan ser simétricos alrededor de la media.

## Ejemplo conceptual

Supóngase una reserva Chain Ladder de 150.

Mack produce:

- error estándar: 18;
- CV: 12 %;
- intervalo normal aproximado del 95 %: 114.7 a 185.3.

Bootstrap produce:

- media: 151;
- mediana: 148;
- desviación estándar: 19;
- P75: 161;
- P95: 190;
- P99: 215.

Las desviaciones estándar son cercanas, pero Bootstrap muestra una cola derecha más larga. La diferencia no implica automáticamente que uno sea correcto y el otro incorrecto; debe investigarse la forma distributiva y el diseño de simulación.

## Reconciliación de diferencias

Cuando los resultados divergen, revisar en este orden:

1. triángulo y fecha de valuación;
2. factores seleccionados;
3. tail factor;
4. definición de reserva total;
5. segmentación;
6. tratamiento de ceros y negativos;
7. corrección y centrado de residuos;
8. parámetro de dispersión;
9. distribución de proceso;
10. número de simulaciones;
11. agregación entre periodos y segmentos;
12. método distributivo usado con Mack.

Una diferencia grande en la estimación media suele ser más preocupante que una diferencia moderada en percentiles.

## Criterios de selección

### Mack es especialmente útil cuando

- se necesita un cálculo rápido y transparente;
- el triángulo es estable;
- el error estándar es el resultado principal;
- se requiere un benchmark reproducible;
- la capacidad computacional es limitada;
- el objetivo es monitoreo periódico.

### Bootstrap es especialmente útil cuando

- se necesitan percentiles o medidas de cola;
- la distribución puede ser asimétrica;
- se evalúa suficiencia de una reserva registrada;
- se requiere una distribución para capital o estrés;
- se desea separar y visualizar fuentes de variación;
- existe capacidad para validar la simulación.

### Usar ambos cuando

- la reserva es material;
- existe revisión independiente;
- los resultados alimentan gobierno o solvencia;
- se necesita distinguir error analítico de forma distributiva;
- se desea una prueba de razonabilidad cruzada.

## Aplicación en seguros de salud

| Situación | Lectura recomendada |
| --- | --- |
| Portafolio grande y estable | Mack como referencia rápida; Bootstrap como contraste |
| Grandes reclamaciones | Bootstrap puede representar mejor asimetría si se segmenta correctamente |
| Cambio de sistema de radicación | Ninguno sin ajuste y escenario estructural |
| Glosas o conciliaciones masivas | Revisar dependencia y efectos calendario antes de aplicar ambos |
| Base incurrida con reservas caso consistentes | Comparar Mack y Bootstrap sobre incurrido |
| Base pagada con rezago operativo | Analizar sensibilidad de edades tempranas y cola |
| Reforma regulatoria o cambio de beneficios | Complementar con métodos a priori y escenarios |

En Colombia deben considerarse cambios en RIPS, facturación electrónica, glosas, acuerdos de pago y modelos de contratación. Si afectan varias filas simultáneamente, la independencia histórica deja de ser razonable.

## Flujo recomendado

```text
Validación y reconciliación de datos
                ↓
Diagnósticos de Chain Ladder
                ↓
Estimación central
                ↓
Mack
                ↓
Bootstrap
                ↓
Reconciliación de diferencias
                ↓
Escenarios estructurales
                ↓
Juicio actuarial y selección final
```

## Comunicación a gestión

Un reporte ejecutivo puede mostrar:

| Métrica | Resultado |
| --- | ---: |
| Estimación central | 150 |
| Error estándar Mack | 18 |
| CV Mack | 12 % |
| Media Bootstrap | 151 |
| P75 Bootstrap | 161 |
| P95 Bootstrap | 190 |
| Reserva registrada | 170 |
| Probabilidad simulada de excedencia | 18 % |

El mensaje debe separar claramente:

- mejor estimación;
- margen o nivel de suficiencia;
- incertidumbre capturada por el modelo;
- riesgos no modelados;
- decisiones de gestión.

## Errores frecuentes

- tratar Mack como una distribución completa;
- omitir el riesgo de proceso en Bootstrap;
- comparar percentiles con definiciones distintas;
- asumir que más simulaciones eliminan sesgo;
- usar residuos no revisados;
- ignorar dependencia entre segmentos;
- sumar percentiles individuales para obtener el total;
- interpretar P95 como peor caso;
- omitir error Monte Carlo;
- reportar precisión estadística sin riesgo estructural.

## Controles de gobierno

La documentación debe identificar:

1. propósito del análisis;
2. triángulos y segmentación;
3. supuestos compartidos;
4. parámetros específicos de Mack;
5. diseño del Bootstrap;
6. cola y dependencia;
7. resultados comparables;
8. reconciliación de diferencias;
9. validación histórica;
10. limitaciones;
11. selección actuarial;
12. revisión independiente.

## Lista de verificación

- [ ] Los modelos usan el mismo triángulo y fecha de corte.
- [ ] Los factores centrales están reconciliados.
- [ ] El tail factor es comparable.
- [ ] Mack incluye proceso y parámetros.
- [ ] Bootstrap incluye simulación de proceso.
- [ ] Los residuos fueron corregidos y revisados.
- [ ] La simulación es estable.
- [ ] Los percentiles se agregaron correctamente.
- [ ] Se revisaron efectos calendario.
- [ ] Se documentó riesgo de modelo.
- [ ] Se explicaron las diferencias materiales.
- [ ] El resultado final incorpora juicio actuarial.

## Conclusión

Mack proporciona una medida analítica, rápida y transparente del error de predicción de Chain Ladder. Bootstrap produce una distribución predictiva flexible que permite analizar asimetría y cola.

Cuando ambos presentan resultados coherentes, aumenta la confianza en la cuantificación de incertidumbre bajo el modelo. Cuando divergen, la diferencia es una señal diagnóstica que debe investigarse, no promediarse automáticamente.

## Capítulos relacionados

Anterior: [Bootstrap Chain Ladder](09-bootstrap-chain-ladder.md).  
Siguiente: [Bornhuetter-Ferguson](../part-02-classical-reserving/11-bornhuetter-ferguson.md).
