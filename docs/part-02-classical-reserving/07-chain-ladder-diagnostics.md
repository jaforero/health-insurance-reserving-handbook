---
title: "Diagnósticos y backtesting de Chain Ladder"
description: "Marco práctico para evaluar suficiencia, estabilidad, sesgo, efectos calendario y desempeño fuera de muestra de Chain Ladder."
chapter: "07"
part: "02-classical-reserving"
language: "es"
status: "review"
version: "0.6.0"
last_updated: "2026-07-17"
tags:
  - chain-ladder
  - diagnosticos
  - backtesting
  - validacion
  - salud
---

# Diagnósticos y backtesting de Chain Ladder

## 1. Propósito

Chain Ladder convierte un patrón histórico de desarrollo en una proyección. La aritmética puede ser correcta y, aun así, la estimación resultar poco representativa por cambios de operación, mezcla, beneficios, red, precios, glosas, recuperaciones o calendario. Este capítulo organiza la validación en cinco preguntas:

1. ¿Los datos observados son completos, conciliados y comparables?
2. ¿Los factores tienen volumen y estabilidad suficientes?
3. ¿Existen patrones sistemáticos por origen, desarrollo o calendario?
4. ¿La regla seleccionada predice razonablemente datos no usados en el ajuste?
5. ¿Las decisiones, excepciones y limitaciones quedaron documentadas?

Un diagnóstico no valida por sí solo el método. La conclusión surge del conjunto de evidencia y del juicio actuarial proporcional a la materialidad.

## 2. Notación y universo observado

Sea $C_{i,j}$ el valor acumulado del periodo de origen $i$ a la edad de desarrollo $j$. La máscara $M_{i,j}$ distingue celdas observadas de celdas futuras:

$$
M_{i,j} = 1 \text{ si la celda es observada; } 0 \text{ en otro caso}
$$

No debe inferirse que un valor igual a cero es futuro. Un cero observado es información; una celda futura es ausencia estructural de observación. Para cada enlace $j$ a $j+1$, el ratio individual es:

$$
r_{i,j} = \frac{C_{i,j+1}}{C_{i,j}}
$$

El ratio solo es válido cuando ambas celdas son observadas y el denominador satisface la regla de elegibilidad definida. El factor ponderado por volumen es:

$$
f_j = \frac{\sum_i C_{i,j+1}}{\sum_i C_{i,j}}
$$

Las sumas deben usar exactamente el mismo conjunto de pares válidos.

## 3. Puertas de entrada antes de diagnosticar factores

### 3.1 Reconciliación

Como mínimo, debe verificarse:

- total de la base canónica frente al triángulo incremental;
- incremental frente a diferencias del acumulado;
- última diagonal frente al corte de valuación;
- unidades, moneda, signo y alcance;
- ausencia de duplicados no explicados;
- tratamiento explícito de negativos, recuperaciones y reversos.

Si la reconciliación falla, el problema es de datos o definición y no debe tratarse ajustando factores.

### 3.2 Comparabilidad

Documentar si la historia contiene cambios materiales en:

- cobertura, deducibles, copagos o red;
- mezcla de población, producto, región o prestador;
- reglas de autorización, radicación, auditoría o pago;
- tarifas, inflación médica o contratos;
- glosas, conciliaciones, recobros o recuperaciones;
- sistemas, migraciones o calidad de captura.

Cuando un cambio no pueda normalizarse, debe evaluarse segmentación, exclusión justificada o un método alternativo.

## 4. Diagnósticos de factores

### 4.1 Suficiencia por enlace

Para cada edad se reportan:

- número de pares válidos;
- volumen del denominador;
- concentración por origen;
- rango, mediana y cuartiles de ratios;
- cantidad de ratios menores que uno;
- cantidad de pares excluidos y causa.

No existe un número universal de observaciones que garantice credibilidad. En edades tardías suele haber menos pares; la decisión debe considerar materialidad, estabilidad y evidencia de cola.

### 4.2 Estabilidad frente a reglas alternativas

Conviene comparar, al menos:

- ponderado por volumen;
- promedio simple;
- mediana;
- experiencia reciente;
- selección manual documentada.

Para una alternativa $a$, la diferencia relativa puede expresarse como:

$$
d_{j,a} = \frac{f_{j,a} - f_{j,base}}{f_{j,base}}
$$

Una diferencia grande no invalida automáticamente una regla, pero exige explicar por qué la experiencia que recibe más peso es la más representativa.

### 4.3 Influencia y exclusiones

Debe medirse cuánto cambia el factor al retirar un origen a la vez. Si $f_j^{(-i)}$ es el factor sin el origen $i$:

$$
I_{i,j} = \frac{f_j^{(-i)} - f_j}{f_j}
$$

La exclusión de un dato extremo no se justifica solo porque reduce la reserva o estabiliza una gráfica. Debe existir una causa verificable y documentarse el efecto con y sin la exclusión.

### 4.4 Monotonicidad y signos

En pagos acumulados, valores decrecientes pueden reflejar recuperaciones, reversos o correcciones. En incurridos, también pueden reflejar liberación de reserva caso. Estos movimientos no deben corregirse mecánicamente; se debe confirmar su naturaleza, consistencia contable y efecto sobre los ratios.

## 5. Diagnósticos por dimensión

### 5.1 Periodo de origen

Graficar ratios y errores por origen permite identificar cohortes afectadas por epidemias, cambios de beneficio, mezcla, red o calidad de datos.

### 5.2 Edad de desarrollo

La dispersión debe revisarse por enlace. Una edad con pocos pares, bajo volumen o factores alternativos muy diferentes puede dominar el CDF de los orígenes recientes.

### 5.3 Periodo calendario

Cada celda pertenece a una diagonal calendario. Patrones sobre diagonales pueden indicar inflación, cambios operativos, cierres masivos, huelgas, migraciones o choques regulatorios. Chain Ladder supone que el patrón de desarrollo estimado es transportable; un efecto calendario persistente cuestiona esa transportabilidad.

### 5.4 Residuo descriptivo

Para comparar celdas sin presentar el residuo como una medida formal de incertidumbre, puede usarse:

$$
e_{i,j} = \frac{C_{i,j+1} - f_j C_{i,j}}{\sqrt{\max(|C_{i,j}|,\epsilon)}}
$$

donde $\epsilon$ evita dividir por cero. El análisis busca estructura por origen, desarrollo y calendario, no normalidad automática. Para cuantificar error de predicción se requieren métodos como Mack o bootstrap y sus propios supuestos.

## 6. Backtesting fuera de muestra

### 6.1 Corte retrospectivo

Se elige una fecha histórica $t$. Solo se usan celdas disponibles en $t$ para estimar factores. Las observaciones posteriores se reservan para evaluación. Es indispensable volver a estimar los factores en cada corte; usar factores calculados con datos futuros introduce fuga de información.

### 6.2 Predicción de la siguiente diagonal

Para una celda retenida con valor real $A_k$ y esperado $E_k$:

$$
Error_k = A_k - E_k
$$

$$
ErrorRelativo_k = \frac{A_k - E_k}{A_k}
$$

El error relativo solo se calcula cuando $A_k$ no es cero. Para un resumen robusto a escalas distintas:

$$
WAPE = \frac{\sum_k |A_k - E_k|}{\sum_k |A_k|}
$$

También se reportan sesgo agregado, error absoluto, número de celdas y volumen evaluado. WAPE no debe interpretarse cuando el denominador es inmaterial.

### 6.3 Rolling-origin

Repetir el ejercicio en varios cortes crea vintages comparables. Como mínimo, el reporte debe incluir:

| Campo | Contenido |
|---|---|
| corte | fecha de información disponible |
| celda o diagonal | observación retenida |
| real | valor observado posteriormente |
| esperado | proyección obtenida en el corte |
| error | real menos esperado |
| método | regla de selección y cola |
| versión | código, datos y parámetros |

Un único corte puede coincidir favorablemente por azar. La evidencia debe cubrir diferentes edades y condiciones operativas.

### 6.4 Runoff de reservas

Para un portafolio existente al corte anterior, una convención útil es:

$$
Desarrollo_t = R_{t-1} - P_t - R_t
$$

donde $R_{t-1}$ es la reserva inicial para ese portafolio, $P_t$ los pagos del periodo y $R_t$ la reserva remanente bajo alcance comparable. El signo debe definirse en el reporte. El análisis separa cambios por experiencia, supuestos, alcance, moneda y metodología.

## 7. Sensibilidad

La sensibilidad mínima compara:

- reglas de selección;
- inclusión o exclusión de observaciones materiales;
- ventanas históricas;
- factor de cola;
- segmentación;
- triángulos pagados e incurridos, cuando ambos son confiables.

Para un escenario $s$:

$$
Impacto_s = IBNR_s - IBNR_{base}
$$

El rango de escenarios es una medida de sensibilidad, no un intervalo probabilístico.

## 8. Criterios de decisión

Los umbrales deben definirse antes de observar el resultado y calibrarse a materialidad, volatilidad y uso. Son señales de revisión, no reglas universales. Una conclusión debería clasificar cada hallazgo como:

- aceptado sin ajuste;
- aceptado con limitación;
- ajustado con justificación;
- requiere método alternativo;
- bloquea el uso.

## 9. Evidencia mínima

El expediente reproducible debe conservar:

1. corte, alcance, unidades y reconciliaciones;
2. máscara de observación y reglas de elegibilidad;
3. ratios, candidatos y factores seleccionados;
4. exclusiones con causa e impacto;
5. cola y sustento;
6. backtests por corte y métricas;
7. sensibilidades;
8. conclusión, limitaciones y aprobación;
9. versión de datos, código y configuración.

## 10. Relación con Demo 6

Demo 6 ya produce ratios individuales, candidatos, CDF, sensibilidad y alertas determinísticas. El incremento v0.6.0 debe añadir cortes retrospectivos, comparación real frente a esperado y reportes de runoff sin cambiar el resultado base de Chain Ladder.

## 11. Referencias y alcance profesional

- [Método Chain Ladder](06-chain-ladder-method.md)
- [Bornhuetter-Ferguson](11-bornhuetter-ferguson.md)
- [Comparación de métodos clásicos](14-classical-reserving-methods-comparison.md)
- [Demo 6](../examples/06-demo-chain-ladder-datos-propios.md)
- [Bibliografía y evidencia](../bibliography.md)

Este marco aplica los principios de propósito, datos, supuestos, pruebas, validación de resultados, documentación y seguimiento descritos en `ASB-ASOP01-2013`, `ASB-ASOP28-2024`, `ASB-ASOP43-2007` y `ASB-ASOP56-2019`. ASOP 43 se usa como referencia histórica y análoga de estimación de reclamaciones no pagadas; no sustituye normas de salud ni regulación colombiana. La aplicabilidad profesional debe evaluarse para la jurisdicción, entidad y fecha de valuación.
