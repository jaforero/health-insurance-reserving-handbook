---
title: "Deep Learning para reservas actuariales"
description: "Marco de aplicación, validación y gobierno de redes neuronales para reservas de seguros de salud y datos longitudinales de reclamaciones."
status: "draft"
version: "0.1.10"
chapter: "20"
part: "part-05-machine-learning"
language: "es"
last_updated: "2026-07-14"
---

# Deep Learning para reservas actuariales

El aprendizaje profundo, o *deep learning*, utiliza redes neuronales de múltiples capas para representar relaciones complejas. En reserving puede ser útil con datos granulares, alta dimensionalidad e historias longitudinales, pero también aumenta el riesgo de sobreajuste, opacidad y dependencia tecnológica.

El objetivo no es reemplazar automáticamente los métodos clásicos. Una red neuronal debe demostrar valor incremental frente a Chain Ladder, GLM, GAM y árboles, respetando la fecha de corte y los controles actuariales.

## Objetivos de aprendizaje

Al finalizar este capítulo, el lector podrá:

- identificar problemas de reserving apropiados para deep learning;
- distinguir redes densas, embeddings, modelos secuenciales y transformers;
- seleccionar objetivos y funciones de pérdida coherentes;
- diseñar validación temporal sin fuga de información;
- evaluar calibración, incertidumbre y estabilidad;
- establecer benchmarks, explicabilidad y gobierno de producción.

## 1. Cuándo considerar deep learning

Puede ser razonable cuando:

- existen cientos de miles o millones de observaciones;
- hay variables categóricas de alta cardinalidad;
- la secuencia de eventos contiene información;
- existen interacciones difíciles de especificar;
- el modelo se reestima y monitorea con infraestructura adecuada;
- la mejora frente a modelos simples es material y persistente.

Puede ser inadecuado cuando:

- el portafolio es pequeño;
- la historia es corta o cambió estructuralmente;
- la trazabilidad de datos es débil;
- el objetivo está mal definido;
- la explicación regulatoria es prioritaria;
- no existe capacidad de validación y monitoreo.

## 2. Formulaciones del problema

### Predicción a nivel de reclamación

Cada observación representa una reclamación o factura. El objetivo puede ser:

- monto futuro pagado;
- monto final reconocido;
- probabilidad de glosa;
- tiempo hasta cierre;
- probabilidad de reapertura;
- distribución de severidad pendiente.

### Predicción por celda

Cada observación es una celda origen-desarrollo-calendario. La red estima pagos incrementales, conteos o parámetros de una distribución. Esto facilita reconciliación con el triángulo.

### Predicción secuencial

Una reclamación o cohorte tiene una historia ordenada:

$$
x_{i,1},x_{i,2},\ldots,x_{i,t}
$$

El modelo utiliza pagos, estados y eventos anteriores para predecir el siguiente periodo o el resultado final.

### Modelos multiestado

Pueden estimarse probabilidades de transición:

$$
\Pr(S_{t+1}=j\mid S_t=i,X_t)
$$

Esta formulación es relevante para radicación, auditoría, glosa, respuesta, pago, cierre y reapertura.

## 3. Variables admisibles

Todas las variables deben existir al corte.

| Dimensión | Ejemplos |
|---|---|
| Afiliado | edad, región, grupo de riesgo |
| Prestación | servicio, código, complejidad, ámbito |
| Prestador | tipo, red, historial anterior al corte |
| Contrato | modalidad, tarifa, paquete, capitación |
| Tiempo | ocurrencia, reporte, desarrollo, calendario |
| Operación | auditoría, canal, días desde radicación |
| Historia | pagos y ajustes observados, estado vigente |

No son admisibles el monto final, pagos futuros, estado final de cierre ni glosas resueltas después de la valoración.

## 4. Redes densas

Una red densa transforma un vector de variables mediante capas sucesivas:

$$
h^{(\ell)}=\sigma\left(W^{(\ell)}h^{(\ell-1)}+b^{(\ell)}\right)
$$

La salida puede estimar un monto, probabilidad, cuantil o parámetro de distribución.

Ventajas:

- modela relaciones no lineales;
- admite muchas variables;
- combina datos numéricos y categóricos codificados.

Limitaciones:

- puede sobreajustar;
- exige escalamiento y regularización;
- suele ser menos interpretable que GLM, GAM o árboles.

## 5. Embeddings categóricos

Un embedding representa una categoría mediante un vector aprendido:

$$
e_c\in\mathbb{R}^k
$$

Puede utilizarse para prestador, diagnóstico, municipio, servicio o producto. Deben controlarse:

- categorías raras;
- categorías nuevas;
- cambios de codificación;
- dimensionalidad excesiva;
- riesgo de que el embedding memorice el target.

## 6. Modelos secuenciales

### LSTM y GRU

Procesan eventos en orden y conservan un estado interno. Pueden modelar pagos mensuales, cambios de estado y tiempos entre movimientos.

### Convoluciones temporales

Capturan patrones locales en una ventana:

$$
(P_{t-3},P_{t-2},P_{t-1},P_t)\longrightarrow P_{t+1}
$$

Pueden entrenarse en paralelo y resultar más estables que redes recurrentes en algunos problemas.

### Transformers

La atención permite relacionar eventos distantes. Su uso requiere volumen suficiente, control de máscaras temporales y comparación rigurosa con alternativas más simples.

## 7. Funciones de pérdida

| Objetivo | Pérdida o distribución |
|---|---|
| Monto esperado | MAE, MSE, Huber |
| Conteo | Poisson o binomial negativa |
| Severidad positiva | Gamma o lognormal |
| Frecuencia-severidad | Tweedie |
| Cuantil | Pinball loss |
| Estado | Cross-entropy |
| Tiempo hasta evento | Pérdida de supervivencia |
| Distribución | Log-verosimilitud negativa |

La función debe evaluarse junto con sesgo agregado y suficiencia por cohorte. Una mejora en pérdida individual puede coexistir con una reserva total sesgada.

## 8. Restricciones y regularización

Controles habituales:

- penalización L1 o L2;
- dropout;
- parada temprana;
- normalización;
- reducción de capacidad;
- límites en embeddings;
- aumento de datos cuando sea defendible;
- calibración posterior.

Para evitar predicciones negativas puede utilizarse una distribución positiva, una transformación o una activación como `softplus`. Cualquier ajuste posterior debe documentarse.

## 9. Incertidumbre predictiva

Una red estándar produce una estimación puntual. Para cuantificar incertidumbre pueden considerarse:

- ensembles de redes;
- bootstrap;
- Monte Carlo dropout;
- cuantiles;
- modelos probabilísticos;
- conformal prediction;
- simulación de escenarios.

Debe distinguirse:

| Componente | Descripción |
|---|---|
| Proceso | Variabilidad futura de reclamaciones |
| Parámetros | Incertidumbre del entrenamiento |
| Modelo | Arquitectura y especificación |
| Datos | Calidad, cobertura y drift |
| Entorno | Inflación, regulación y shocks |

La variabilidad entre semillas no representa por sí sola todos estos riesgos.

## 10. Benchmarks mínimos

Antes de adoptar deep learning deben estimarse alternativas como:

- Chain Ladder;
- Mack y Bootstrap;
- Bornhuetter-Ferguson;
- GLM y GAM;
- Random Forest o gradient boosting;
- métodos PMPM o frecuencia-severidad.

Si la mejora no es material, estable y explicable, la red no está justificada para producción.

## 11. Validación temporal

La separación debe respetar la secuencia de valoración:

| Entrenamiento | Validación | Prueba |
|---|---|---|
| 2019–2022 | 2023 | 2024 |
| 2020–2023 | 2024 | 2025 |

El procedimiento debe:

1. reconstruir datos disponibles al corte;
2. ajustar preprocesamiento solo con entrenamiento;
3. elegir arquitectura con validación;
4. reservar la prueba para evaluación final;
5. repetir en varios cierres;
6. analizar cohortes y segmentos.

## 12. Métricas

Combinar precisión individual y suficiencia agregada:

- MAE y RMSE;
- sesgo total;
- error por periodo de origen;
- estabilidad entre valoraciones;
- pinball loss para cuantiles;
- cobertura de intervalos;
- calibración probabilística;
- reserva estimada frente al desarrollo real.

La métrica principal y los límites de aceptación deben definirse antes del ajuste final.

## 13. Interpretabilidad

No es necesario explicar cada peso de la red, pero sí demostrar comportamiento razonable.

Herramientas útiles:

- SHAP;
- importancia por permutación;
- partial dependence;
- accumulated local effects;
- análisis de sensibilidad;
- escenarios y stress testing;
- comparación con GLM, GAM o árboles.

También deben revisarse predicciones extremas, categorías raras y movimientos materiales entre cierres.

## 14. Aplicaciones en seguros de salud

Deep learning puede apoyar:

- pagos futuros por reclamación;
- severidad por diagnóstico o prestación;
- probabilidad y resolución de glosas;
- reclamaciones de alto costo;
- desarrollo por proveedor;
- pagos tardíos;
- reservas por contrato;
- utilización longitudinal.

Riesgos específicos incluyen cambios de red, inflación médica, estacionalidad, epidemias, codificación clínica y modificaciones tarifarias.

## 15. Contexto colombiano

Las aplicaciones deben preservar trazabilidad entre:

- prestación;
- autorización cuando aplique;
- radicación;
- factura electrónica de venta;
- RIPS;
- auditoría y glosa;
- notas de ajuste;
- contabilización y pago.

Los modelos secuenciales pueden representar estados y tiempos de resolución, pero la reserva final debe reconciliarse con saldos contables, cuentas conocidas, auditoría médica y controles internos.

## 16. Ejemplo conceptual en Python

```python
import tensorflow as tf
from tensorflow import keras

tf.keras.utils.set_random_seed(20260714)

model = keras.Sequential(
    [
        keras.layers.Input(shape=(n_features,)),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dropout(0.10),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dense(1, activation="softplus"),
    ]
)

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss="mae",
)

callbacks = [
    keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=10,
        restore_best_weights=True,
    )
]

history = model.fit(
    X_train,
    y_train,
    validation_data=(X_validation, y_validation),
    epochs=200,
    batch_size=512,
    callbacks=callbacks,
    verbose=0,
)
```

La semilla mejora reproducibilidad, pero operaciones paralelas y hardware diferente todavía pueden producir variaciones. Deben fijarse versiones y conservarse artefactos del entrenamiento.

## 17. Modelos híbridos

Una red puede complementar, no reemplazar, la estructura actuarial:

- predecir ajustes sobre un benchmark;
- estimar factores condicionados por variables;
- modelar cuentas conocidas y conservar un método agregado para no reportadas;
- combinar predicciones mediante credibilidad;
- calibrar el total a una estimación actuarial aprobada.

La combinación debe definirse antes de observar el resultado final y validarse históricamente.

## 18. Producción y monitoreo

Conservar:

1. snapshot de datos y fecha de corte;
2. código de preprocesamiento;
3. arquitectura y pesos;
4. función de pérdida;
5. semillas y dependencias;
6. resultados de validación;
7. benchmarks;
8. calibración e incertidumbre;
9. explicación de predicciones materiales;
10. aprobaciones y límites de uso.

Monitorear drift de variables, categorías desconocidas, error maduro, sesgo agregado, estabilidad y dependencia del postprocesamiento.

## 19. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Leakage temporal | Reconstrucción estricta al corte |
| Sobreajuste | Regularización y backtesting |
| Opacidad | Explicabilidad y benchmarks |
| Drift | Monitoreo y revisión periódica |
| Sesgo por segmento | Métricas segmentadas |
| Extrapolación | Límites y escenarios |
| Falsa precisión | Intervalos y comunicación clara |
| Dependencia tecnológica | Versionamiento y contingencia |

## 20. Checklist de adopción

- [ ] El objetivo está definido en términos actuariales.
- [ ] Las variables son observables al corte.
- [ ] Existe suficiente volumen y maduración.
- [ ] El benchmark clásico está documentado.
- [ ] La validación respeta el tiempo.
- [ ] La mejora es material y estable.
- [ ] El sesgo agregado está dentro del límite.
- [ ] La incertidumbre está calibrada.
- [ ] El comportamiento puede explicarse.
- [ ] Existe un modelo o procedimiento de contingencia.
- [ ] La salida se reconcilia con controles financieros.

## Conclusiones

Deep learning puede ampliar el conjunto de herramientas de reserving cuando existen datos granulares y patrones complejos. Su mayor capacidad también amplifica el costo de una mala definición del objetivo, leakage o drift.

La adopción debe ser gradual: comenzar con benchmarks, validar en varios cierres, demostrar valor incremental y conservar un proceso explicable y auditable. La red es un componente de la estimación, no la decisión actuarial completa.

## Referencias

- ASOP No. 23, *Data Quality*.
- ASOP No. 38, *Using Models Outside the Actuary’s Area of Expertise*.
- ASOP No. 41, *Actuarial Communications*.
- ASOP No. 56, *Modeling*.
- Goodfellow, I., Bengio, Y. y Courville, A. *Deep Learning*.
- Gabrielli, A., Richman, R. y Wüthrich, M. V. “Neural Network Embedding of the Over-Dispersed Poisson Reserving Model”.
- Wüthrich, M. V. y Merz, M. *Statistical Foundations of Actuarial Learning and its Applications*.

## Capítulos relacionados

Anterior: [Modelos basados en árboles para reservas actuariales](19-tree-based-models-for-loss-reserving.md).  
Siguiente: [Particularidades del reserving en seguros de salud](../part-06-health-specific/21-health-insurance-reserving-specificities.md).
