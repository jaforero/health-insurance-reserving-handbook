---
title: Comparación de métodos clásicos de reserving
description: Comparación práctica de Chain Ladder, Bornhuetter-Ferguson, Benktander y Cape Cod, con criterios de selección para reservas de salud.
status: draft
version: "0.1.6"
chapter: "14"
part: "part-02-classical-reserving"
language: "es"
last_updated: "2026-07-14"
---

# Comparación de métodos clásicos de reserving

Los métodos clásicos de reserving no compiten solo por precisión matemática. Cada uno responde a una pregunta distinta y asigna diferente peso a la experiencia observada, la expectativa previa, la exposición y el juicio actuarial.

La selección de método debe depender del objetivo, la madurez de los datos, la calidad del triángulo y el contexto operativo. En salud, además, debe considerar rezagos de radicación, auditoría, glosas, pagos parciales, cambios de red y variaciones de morbilidad.

## Métodos cubiertos

Esta parte cubre cuatro enfoques clásicos:

- Chain Ladder;
- Bornhuetter-Ferguson;
- Benktander;
- Cape Cod.

Todos pueden ser útiles. Ninguno debe aplicarse sin diagnóstico.

## Resumen conceptual

| Método | Fuente principal de señal | Mejor uso |
| --- | --- | --- |
| Chain Ladder | Experiencia observada | Años con desarrollo creíble y patrón estable |
| Bornhuetter-Ferguson | Expectativa previa + observado | Años inmaduros con expectativa previa confiable |
| Benktander | Transición entre BF y Chain Ladder | Casos intermedios con experiencia emergente |
| Cape Cod | Exposición + experiencia desarrollada | Calibrar costo esperado desde experiencia propia |

La diferencia central es el peso relativo entre observado y esperado.

## Chain Ladder

Chain Ladder proyecta lo observado usando factores de desarrollo:

$$
Ultimate^{CL} = Observado \times CDF
$$

Fortalezas:

- simple;
- transparente;
- ampliamente usado;
- útil con triángulos maduros y estables;
- fácil de explicar y reproducir.

Debilidades:

- sensible a años recientes inmaduros;
- hereda sesgos de factores históricos;
- no incorpora exposición directamente;
- puede reaccionar demasiado a ruido temprano;
- requiere estabilidad de patrones.

En salud, Chain Ladder debe revisarse frente a cambios de proceso de pago, glosas y radicación.

## Bornhuetter-Ferguson

BF combina observado con expectativa previa:

$$
Ultimate^{BF} =
Observado + Esperado \times (1 - p)
$$

Fortalezas:

- estabiliza años inmaduros;
- incorpora pricing, presupuesto o expectativa técnica;
- reduce sensibilidad a observaciones tempranas;
- útil cuando Chain Ladder es errático.

Debilidades:

- depende de la calidad del esperado;
- puede ocultar señales emergentes;
- requiere justificar ELR o costo esperado;
- puede ser subjetivo si no se documenta.

En salud, BF es útil si existe una expectativa técnica robusta por población, contrato o producto.

## Benktander

Benktander se ubica entre BF y Chain Ladder:

$$
Ultimate^{B} =
Observado + Ultimate^{BF} \times (1 - p)
$$

Fortalezas:

- transición gradual hacia experiencia observada;
- menos rígido que BF;
- menos sensible que Chain Ladder puro;
- útil para comparar escenarios.

Debilidades:

- comparte riesgos de BF y Chain Ladder;
- puede ser más difícil de comunicar;
- requiere expectativa previa y factores razonables;
- no elimina incertidumbre.

Benktander es útil cuando el actuario no quiere depender completamente ni del observado ni del esperado.

## Cape Cod

Cape Cod estima una tasa esperada usando exposición y experiencia desarrollada:

$$
Tasa =
\frac{\sum Observado}
{\sum Exposición \times p}
$$

Luego:

$$
Esperado_i = Exposición_i \times Tasa
$$

Fortalezas:

- incorpora exposición;
- útil para calibrar BF;
- conecta reserving con costo por unidad;
- ayuda a separar volumen y severidad.

Debilidades:

- depende de exposición bien definida;
- requiere ajuste de tendencia y mix;
- puede sesgarse por años atípicos;
- no resuelve problemas de heterogeneidad.

En salud, Cape Cod puede ser muy útil si se trabaja con meses-miembro, pero debe considerar morbilidad y cambios de cobertura.

## Criterios de selección

Una selección razonable considera:

- madurez del año de origen;
- estabilidad de factores;
- credibilidad de la experiencia observada;
- disponibilidad de expectativa previa;
- calidad de exposición;
- cambios operativos;
- materialidad de la reserva;
- objetivo del reporte.

No es obligatorio seleccionar un único método para todos los años. Es común usar Chain Ladder para años maduros y BF o Benktander para años recientes.

## Selección por madurez

Una regla conceptual:

| Madurez | Método preferente |
| --- | --- |
| Alta | Chain Ladder |
| Media | Benktander o combinación |
| Baja | Bornhuetter-Ferguson |
| Baja con buena exposición | Cape Cod + BF |

Esta tabla no reemplaza el juicio. Solo organiza la discusión.

## Comparación pagado vs incurrido

En salud, la selección de método debe considerar la base:

- base pagada: más objetiva, pero más rezagada;
- base incurrida: más temprana, pero depende de reserva caso;
- comparación entre bases: útil para validar suficiencia.

Un método puede ser adecuado en base pagada y no en base incurrida, o viceversa.

## Uso de múltiples métodos

Una práctica robusta es presentar varios métodos:

| Año origen | Chain Ladder | BF | Benktander | Selección |
| --- | ---: | ---: | ---: | ---: |
| 2022 | 100 | 101 | 100 | 100 |
| 2023 | 120 | 118 | 119 | 119 |
| 2024 | 160 | 145 | 152 | 150 |

La selección final debe explicar por qué se eligió un valor o rango.

No se debe promediar métodos automáticamente sin justificación. Un promedio puede ocultar problemas en vez de resolverlos.

## Rango razonable

En muchos casos, el resultado final no debería comunicarse como un punto exacto, sino como una selección dentro de un rango razonable.

El rango puede basarse en:

- métodos alternativos;
- sensibilidad de factores;
- sensibilidad de pérdida esperada;
- escenarios de tendencia;
- exclusión de años atípicos;
- juicio sobre operación.

La estimación puntual puede ser necesaria para contabilidad, pero el análisis técnico debe mostrar incertidumbre.

## Documentación requerida

Una comparación de métodos debe documentar:

- datos usados;
- fecha de valuación;
- definición de origen y desarrollo;
- base pagada o incurrida;
- factores seleccionados;
- exposición y expectativa previa;
- métodos calculados;
- selección final;
- sensibilidad;
- limitaciones.

Esta documentación permite que el resultado sea auditado y defendido.

## Recomendación práctica para salud

Para un portafolio de salud, un flujo práctico es:

1. Construir triángulos pagados e incurridos.
2. Revisar incrementales y acumulados.
3. Calcular Chain Ladder en ambas bases.
4. Estimar exposición y costo esperado.
5. Calcular BF o Cape Cod para años recientes.
6. Comparar resultados por año de origen.
7. Revisar sensibilidad y cambios operativos.
8. Seleccionar reservas con juicio documentado.

Este flujo evita depender de una sola vista del riesgo.

## Cierre de la Parte 2

Los métodos clásicos siguen siendo fundamentales porque son transparentes, auditables y fáciles de comunicar. Su limitación no es la antigüedad, sino el uso mecánico.

Un buen análisis clásico debe responder:

- qué datos se usaron;
- qué método se aplicó;
- qué supuestos se hicieron;
- por qué el resultado es razonable;
- qué incertidumbre queda.

Los capítulos posteriores introducen métodos estocásticos, estadísticos y de machine learning, pero todos se apoyan en esta base.

## Capítulos relacionados

Anterior: [Método Cape Cod](13-cape-cod-method.md).  
Siguiente: [GLM para reserving de pérdidas](../part-04-statistical-models/15-glm-for-loss-reserving.md).

