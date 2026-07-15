---
title: "Machine Learning para reservas actuariales"
description: "Marco práctico para diseñar, validar, explicar y gobernar modelos de aprendizaje automático aplicados a reservas de seguros de salud."
status: "draft"
version: "0.1.10"
chapter: "18"
part: "part-05-machine-learning"
language: "es"
last_updated: "2026-07-14"
---

# Machine Learning para reservas actuariales

El aprendizaje automático, o *machine learning* (ML), amplía las herramientas de reserving cuando existen datos granulares, relaciones no lineales y suficiente historia para validar el desempeño fuera de muestra. Su valor no consiste en sustituir el juicio actuarial, sino en estimar componentes de la obligación futura con información que un triángulo agregado no conserva.

Un modelo predictivo puede ser técnicamente preciso y aun así resultar inadecuado para una reserva oficial. Debe respetar la fecha de corte, evitar fuga de información, producir resultados reconciliables y demostrar estabilidad frente a cambios operativos, contractuales y regulatorios.

## Objetivos de aprendizaje

Al finalizar este capítulo, el lector podrá:

- distinguir predicción, inferencia y estimación actuarial;
- formular objetivos de ML compatibles con una fecha de valoración;
- construir variables sin utilizar información futura;
- seleccionar familias de modelos y funciones de pérdida;
- diseñar validación temporal y backtesting;
- evaluar precisión individual, suficiencia agregada y estabilidad;
- incorporar explicabilidad e incertidumbre;
- integrar modelos de ML con benchmarks actuariales y controles de producción.

## 1. Papel de ML en reserving

Los métodos tradicionales resumen el desarrollo histórico en factores, curvas o parámetros. ML permite usar simultáneamente variables como:

- edad de desarrollo;
- monto pagado e incurrido a la fecha;
- diagnóstico, procedimiento y tipo de servicio;
- prestador, red y modalidad contractual;
- características del afiliado y exposición;
- estado de auditoría, glosa o devolución;
- periodo calendario, inflación médica y estacionalidad.

Esta flexibilidad es útil cuando el portafolio es grande y heterogéneo. También aumenta el riesgo de sobreajuste, relaciones espurias y resultados difíciles de explicar.

## 2. Predicción frente a inferencia

La inferencia estadística se interesa por parámetros, supuestos y relaciones estructurales. La predicción prioriza el desempeño en observaciones futuras. En reserving se necesitan ambas perspectivas:

| Pregunta | Enfoque dominante |
|---|---|
| ¿Qué variables explican el retraso? | Inferencia y diagnóstico |
| ¿Cuánto se pagará después del corte? | Predicción |
| ¿Qué reserva debe registrarse? | Decisión actuarial y financiera |
| ¿Qué incertidumbre rodea la estimación? | Modelación predictiva y escenarios |

Una buena predicción no determina por sí sola la reserva registrada. La selección final debe considerar materialidad, incertidumbre, consistencia contable y conocimiento del negocio.

## 3. Unidades de modelación

### Nivel de reclamación

Cada fila representa una reclamación, factura o episodio. Los objetivos pueden ser:

- pago futuro;
- monto final permitido;
- probabilidad de cierre;
- tiempo hasta pago;
- probabilidad y monto de glosa;
- severidad condicional a un estado.

La reserva agregada puede construirse como:

$$
\widehat R = \sum_{k \in \mathcal{O}} \widehat Y_k^{\mathrm{futuro}} + \widehat R_{\mathrm{no\ reportado}}
$$

donde $\mathcal{O}$ representa obligaciones conocidas al corte. Debe evitarse confundir la predicción de cuentas conocidas con el IBNR puro de eventos todavía no reportados.

### Nivel de celda

Cada observación corresponde a una celda origen-desarrollo-calendario. El modelo estima pagos incrementales, incurridos o conteos. Esta estructura facilita la comparación con Chain Ladder, GLM y GAM.

### Nivel de segmento

El objetivo puede ser PMPM, frecuencia, severidad o costo agregado por producto, región, contrato o cohorte. Es útil cuando los datos individuales no están disponibles o cuando la decisión se toma a nivel de portafolio.

## 4. Fecha de corte y fuga de información

Una variable es admisible solamente si estaba disponible en la fecha de valoración que se pretende reconstruir. La fuga de información (*data leakage*) ocurre cuando el entrenamiento utiliza información conocida después del corte.

Ejemplos de fuga:

- estado final de una reclamación aún abierta;
- pago total observado al cierre definitivo;
- glosa resuelta después de la valoración;
- variables calculadas con diagonales futuras;
- codificaciones corregidas retrospectivamente sin reconstruir su versión histórica;
- imputaciones realizadas con todo el periodo de prueba.

El dataset debe reconstruirse como una fotografía histórica:

```text
Fecha de valoración
        │
        ├── Información observable al corte → variables
        └── Desarrollo posterior            → objetivo
```

## 5. Definición del objetivo

El objetivo debe corresponder a una cantidad económica y temporal precisa.

| Objetivo | Definición posible | Riesgo principal |
|---|---|---|
| Pago futuro | Pagos posteriores al corte | Cuentas no conocidas |
| Ultimate | Pago total al cierre | Censura y cola |
| IBNR | Ultimate menos observado | Mezcla de componentes |
| Tiempo hasta cierre | Duración restante | Censura |
| Probabilidad de pago | Evento dentro de un horizonte | Desbalance de clases |
| Cuantil de costo | Percentil condicional | Calibración |

Cuando existe censura, excluir observaciones incompletas introduce sesgo. Deben considerarse técnicas de supervivencia, ventanas de maduración o ponderación adecuada.

## 6. Ingeniería de variables

Las variables deben tener significado operativo y mantenerse reproducibles.

### Variables de desarrollo

- meses desde ocurrencia;
- días desde radicación;
- pagos acumulados;
- número de movimientos;
- relación pagado/incurrido;
- tiempo desde último movimiento;
- estado actual.

### Variables clínicas y de exposición

- grupo diagnóstico;
- procedimiento o tipo de servicio;
- edad y grupo de riesgo;
- condición crónica;
- exposición o afiliados equivalentes;
- utilización histórica observable.

### Variables contractuales y operativas

- modalidad de pago;
- prestador y red;
- canal de facturación;
- estado de auditoría;
- glosa o devolución vigente;
- lote, plataforma o proceso de recepción.

Las categorías de alta cardinalidad requieren tratamiento explícito para valores raros y categorías nuevas. El historial del prestador debe calcularse únicamente con información anterior al corte.

## 7. Partición temporal

Una partición aleatoria suele sobreestimar el desempeño porque mezcla periodos de valoración.

La separación recomendada respeta el tiempo:

```text
Entrenamiento        Validación          Prueba
periodos antiguos    periodo posterior   periodo más reciente
```

El backtesting *rolling-origin* repite la estimación en varios cierres:

| Iteración | Entrenamiento | Validación |
|---|---|---|
| 1 | hasta 2022 | 2023 |
| 2 | hasta 2023 | 2024 |
| 3 | hasta 2024 | 2025 |

Cada iteración debe reconstruir variables, transformaciones y universos como habrían existido en ese momento.

## 8. Familias de modelos

### Modelos lineales regularizados

Ridge, Lasso y Elastic Net ofrecen benchmarks transparentes y controlan colinealidad. Son útiles antes de adoptar modelos más complejos.

### Árboles y boosting

Random Forest, Gradient Boosting, XGBoost, LightGBM y CatBoost capturan no linealidades e interacciones. Se estudian con detalle en el [capítulo 19](19-tree-based-models-for-loss-reserving.md).

### Redes neuronales

Pueden modelar datos de alta dimensionalidad y secuencias, pero requieren mayor volumen, control y capacidad de cómputo. Se desarrollan en el [capítulo 20](20-deep-learning-for-loss-reserving.md).

### Supervivencia y modelos multiestado

Son apropiados para tiempo hasta reporte, pago, cierre o transición entre estados. En muchos problemas de salud resultan más naturales que una regresión directa del monto final.

## 9. Funciones de pérdida

La función de pérdida debe ser coherente con el objetivo y su soporte.

| Objetivo | Pérdida o distribución |
|---|---|
| Monto continuo | MAE, MSE, Huber |
| Severidad positiva | Gamma o lognormal |
| Frecuencia | Poisson o binomial negativa |
| Frecuencia-severidad | Tweedie |
| Cuantiles | Pinball loss |
| Clasificación | Log loss |
| Tiempo hasta evento | Pérdida de supervivencia |

Minimizar MSE individual no garantiza una reserva agregada sin sesgo. Puede ser necesario ponderar por exposición, monto o segmento y calibrar posteriormente el total.

## 10. Métricas actuariales

Las métricas individuales deben complementarse con medidas agregadas.

$$
\mathrm{MAE} = \frac{1}{n}\sum_{i=1}^{n}|y_i-\widehat y_i|
$$

$$
\mathrm{RMSE} = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\widehat y_i)^2}
$$

$$
\mathrm{Sesgo\ agregado} = \frac{\sum_i \widehat y_i-\sum_i y_i}{\sum_i y_i}
$$

También deben revisarse:

- error por cohorte de origen;
- error por fecha de valoración;
- suficiencia acumulada;
- estabilidad de la reserva entre cierres;
- desempeño por producto, prestador y nivel de riesgo;
- cobertura de intervalos;
- impacto financiero de errores extremos.

## 11. Benchmarks y valor incremental

Todo modelo de ML debe compararse contra alternativas más simples:

- Chain Ladder;
- Bornhuetter-Ferguson;
- métodos PMPM;
- frecuencia-severidad;
- GLM o GAM;
- una predicción histórica simple.

La complejidad se justifica cuando la mejora es material, estable, reproducible y útil para la decisión. Ganar una métrica promedio mientras aumenta el sesgo de reserva no constituye una mejora.

## 12. Incertidumbre predictiva

Una predicción puntual no representa la distribución de la obligación. Entre las alternativas se encuentran:

- bootstrap;
- ensembles;
- regresión cuantílica;
- conformal prediction;
- modelos probabilísticos;
- simulación de frecuencia y severidad;
- escenarios de inflación, cola y cambios operativos.

Debe distinguirse riesgo de proceso, parámetros, modelo, datos y entorno externo. Ninguna técnica automática captura por sí sola todos estos componentes.

## 13. Explicabilidad

La explicabilidad debe responder preguntas concretas:

- ¿por qué cambió la reserva respecto al cierre anterior?;
- ¿qué variables impulsan una predicción material?;
- ¿el modelo responde razonablemente a cambios de exposición o desarrollo?;
- ¿existen segmentos con comportamiento inestable?;

Herramientas frecuentes:

- importancia por permutación;
- SHAP;
- partial dependence;
- accumulated local effects;
- análisis de sensibilidad;
- comparación contra un modelo interpretable.

La importancia predictiva no demuestra causalidad.

## 14. Aplicación a seguros de salud

ML puede apoyar:

- estimación de cuentas conocidas pendientes;
- predicción de pagos tardíos;
- detección de reclamaciones de alto costo;
- desarrollo por prestador o contrato;
- frecuencia y severidad por población;
- probabilidad de glosa o devolución;
- conciliación entre pagado e incurrido.

Los modelos deben capturar o someterse a escenarios para inflación médica, estacionalidad, cambios de red, epidemias, actualizaciones tarifarias y variaciones en la mezcla de afiliados.

## 15. Consideraciones para Colombia

En el contexto colombiano deben preservarse, cuando apliquen:

- fecha de prestación;
- fecha de radicación;
- factura electrónica de venta;
- registros RIPS;
- estados de auditoría y glosa;
- pagos y notas de ajuste;
- modalidad contractual;
- fuente y periodo de exposición.

La salida debe reconciliarse con cuentas conocidas, provisiones contables, saldos por prestador y reglas internas de reconocimiento. El modelo no sustituye la trazabilidad entre prestación, factura, auditoría y pago.

## 16. Ejemplo conceptual en Python

El siguiente ejemplo muestra una estructura reproducible. Los nombres de variables deben adaptarse al dataset real.

```python
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

numeric_features = [
    "development_month",
    "paid_to_date",
    "case_reserve",
    "claim_age_days",
]

categorical_features = [
    "service_group",
    "provider_type",
    "contract_type",
]

preprocess = ColumnTransformer(
    transformers=[
        ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ],
    remainder="passthrough",
)

model = Pipeline(
    steps=[
        ("preprocess", preprocess),
        (
            "regressor",
            RandomForestRegressor(
                n_estimators=500,
                min_samples_leaf=20,
                random_state=20260714,
                n_jobs=-1,
            ),
        ),
    ]
)

model.fit(train[numeric_features + categorical_features], train["future_paid"])
prediction = model.predict(test[numeric_features + categorical_features])

mae = mean_absolute_error(test["future_paid"], prediction)
bias = (prediction.sum() - test["future_paid"].sum()) / test["future_paid"].sum()
```

La partición `train` y `test` debe construirse por fecha de valoración, no mediante muestreo aleatorio.

## 17. Producción y monitoreo

Un flujo de producción mínimo incluye:

```text
Fuentes versionadas
        ↓
Validación de datos
        ↓
Construcción de variables al corte
        ↓
Modelo y calibración
        ↓
Agregación y reconciliación
        ↓
Reporte, aprobación y monitoreo
```

Monitorear como mínimo:

- cambios de esquema y categorías;
- distribución de variables;
- error observado cuando madura el desarrollo;
- sesgo por segmento;
- estabilidad entre cierres;
- desviación frente al benchmark;
- frecuencia de reglas posteriores al modelo.

## 18. Gobierno del modelo

La documentación debe incluir:

1. objetivo actuarial y población;
2. fecha de corte y definición del target;
3. fuentes, transformaciones y variables excluidas;
4. arquitectura e hiperparámetros;
5. benchmarks y criterios de selección;
6. validación temporal y backtesting;
7. incertidumbre y escenarios;
8. explicabilidad y pruebas de razonabilidad;
9. limitaciones y usos no permitidos;
10. responsables, aprobaciones y monitoreo.

Este marco es consistente con la atención que ASOP 23 presta a la calidad de datos, ASOP 41 a la comunicación y ASOP 56 al gobierno de modelos.

## 19. Checklist de adopción

Antes de utilizar ML en una reserva oficial, confirmar:

- [ ] El objetivo está definido en términos económicos y temporales.
- [ ] Todas las variables eran observables al corte.
- [ ] La validación respeta el tiempo.
- [ ] Existe un benchmark actuarial reproducible.
- [ ] La mejora es material y estable.
- [ ] El sesgo agregado es aceptable.
- [ ] La incertidumbre está cuantificada.
- [ ] Los movimientos materiales pueden explicarse.
- [ ] La salida se reconcilia con controles financieros.
- [ ] Existe monitoreo y un procedimiento de contingencia.

## Conclusiones

Machine Learning puede aportar granularidad y capacidad predictiva al reserving de salud, especialmente en portafolios grandes y heterogéneos. Su adopción debe comenzar con una formulación actuarial clara, datos reconstruidos al corte y benchmarks simples.

El modelo más complejo no es necesariamente el mejor. La alternativa adecuada es aquella que combina precisión, estabilidad, explicabilidad, incertidumbre y capacidad de operación dentro de un proceso gobernado.

## Referencias

- ASOP No. 5, *Incurred Health and Disability Claims*.
- ASOP No. 23, *Data Quality*.
- ASOP No. 41, *Actuarial Communications*.
- ASOP No. 56, *Modeling*.
- Hastie, T., Tibshirani, R. y Friedman, J. *The Elements of Statistical Learning*.
- Wüthrich, M. V. y Merz, M. *Statistical Foundations of Actuarial Learning and its Applications*.

## Capítulos relacionados

Anterior: [Reserving bayesiano](../part-04-statistical-models/17-bayesian-loss-reserving.md).  
Siguiente: [Modelos basados en árboles para reservas actuariales](19-tree-based-models-for-loss-reserving.md).
