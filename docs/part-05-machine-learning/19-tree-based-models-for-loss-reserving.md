---
title: "Modelos basados en árboles para reservas actuariales"
description: "Guía práctica de árboles de decisión, Random Forest y gradient boosting para modelar reservas de seguros de salud con validación y gobierno actuarial."
status: "draft"
version: "0.1.10"
chapter: "19"
part: "part-05-machine-learning"
language: "es"
last_updated: "2026-07-14"
---

# Modelos basados en árboles para reservas actuariales

Los modelos basados en árboles dividen recursivamente el espacio de variables para formar grupos con resultados similares. Pueden capturar umbrales, interacciones y no linealidades sin especificarlas previamente, lo que los hace atractivos para datos granulares de reclamaciones de salud.

Esa flexibilidad no elimina las exigencias actuariales. Un modelo puede ajustar bien la historia y fallar ante una nueva diagonal, un cambio de red o una modificación contractual. La validación temporal, el control de sesgo agregado y la comparación con benchmarks siguen siendo obligatorios.

## Objetivos de aprendizaje

Al finalizar este capítulo, el lector podrá:

- explicar cómo se construye un árbol de regresión;
- distinguir árbol individual, bagging, Random Forest y boosting;
- seleccionar hiperparámetros con validación temporal;
- evaluar importancia y explicabilidad sin inferir causalidad;
- controlar sobreajuste, extrapolación y drift;
- implementar un pipeline reproducible;
- integrar modelos de árboles con métodos actuariales tradicionales.

## 1. Árboles de regresión

Sea un conjunto de entrenamiento con observaciones $(x_i,y_i)$. Un árbol selecciona una variable $j$ y un punto de corte $s$. Las dos regiones quedan definidas por las condiciones:

$$
R_1(j,s): x_j < s, \qquad R_2(j,s): x_j \geq s
$$

Para una pérdida cuadrática, la división busca minimizar:

$$
\sum_{x_i\in R_1(j,s)}(y_i-\bar y_1)^2 + \sum_{x_i\in R_2(j,s)}(y_i-\bar y_2)^2
$$

El procedimiento se repite en cada nodo. La predicción de una hoja es normalmente el promedio de sus observaciones:

$$
\widehat y(x)=\frac{1}{|R_m|}\sum_{x_i\in R_m}y_i, \qquad x\in R_m
$$

El resultado es una función constante por tramos.

## 2. Interpretación actuarial de una partición

Un árbol puede aprender reglas como:

```text
¿Mes de desarrollo < 4?
├── Sí: ¿la reclamación está glosada?
│   ├── Sí  → pago futuro alto y tardío
│   └── No  → pago futuro moderado
└── No: ¿pagado/incurrido > 90 %?
    ├── Sí  → pago futuro bajo
    └── No  → revisar contrato y prestador
```

Estas reglas son predictivas, no causales. Que un prestador aparezca en una partición no prueba que cause mayor reserva; puede representar mezcla de servicios, complejidad o procesos administrativos.

## 3. Profundidad y sobreajuste

Un árbol profundo produce hojas pequeñas y ajusta detalles de la muestra:

- disminuye el sesgo de entrenamiento;
- aumenta la varianza;
- crea reglas inestables;
- extrapola de forma deficiente.

Controles principales:

- `max_depth`;
- `min_samples_leaf`;
- `min_samples_split`;
- número máximo de hojas;
- poda por complejidad.

Una hoja con pocas reclamaciones de alto monto puede generar una predicción materialmente inestable.

## 4. Poda

La poda costo-complejidad equilibra ajuste y tamaño:

$$
R_\alpha(T)=R(T)+\alpha|T|
$$

donde $R(T)$ representa el error del árbol, $|T|$ el número de hojas y $\alpha$ la penalización por complejidad. El valor de $\alpha$ debe seleccionarse con datos posteriores en el tiempo, no solo con el ajuste interno.

## 5. Bagging

*Bootstrap aggregation* entrena múltiples árboles sobre muestras bootstrap y promedia sus predicciones:

$$
\widehat f_{\mathrm{bag}}(x)=\frac{1}{B}\sum_{b=1}^{B}\widehat f_b(x)
$$

El promedio reduce la varianza de un árbol individual. Sin embargo, árboles muy correlacionados producen una reducción limitada.

## 6. Random Forest

Random Forest agrega selección aleatoria de variables en cada división. Esto descorrelaciona los árboles y suele mejorar la estabilidad.

Hiperparámetros relevantes:

| Parámetro | Efecto |
|---|---|
| `n_estimators` | Número de árboles |
| `max_features` | Variables candidatas por división |
| `max_depth` | Complejidad máxima |
| `min_samples_leaf` | Suavizamiento de las hojas |
| `max_samples` | Tamaño de la muestra bootstrap |

Un mayor número de árboles reduce el error Monte Carlo del ensemble, pero no corrige sesgo, leakage ni variables mal construidas.

## 7. Error fuera de bolsa

Las observaciones no seleccionadas en una muestra bootstrap son *out-of-bag* (OOB) para ese árbol. Pueden estimar error sin una partición adicional.

En reserving, el error OOB no reemplaza la validación temporal porque el bootstrap mezcla periodos. Puede servir como diagnóstico interno, pero la decisión debe basarse en cierres posteriores.

## 8. Gradient boosting

Boosting construye árboles secuencialmente. Cada nuevo árbol aproxima el gradiente negativo de la pérdida respecto a la predicción vigente:

$$
F_m(x)=F_{m-1}(x)+\eta h_m(x)
$$

donde $h_m$ es el árbol de la iteración $m$ y $\eta$ la tasa de aprendizaje.

Una tasa pequeña con más iteraciones suele producir modelos más suaves, pero exige seleccionar el punto de parada con validación.

## 9. Familias de boosting

### Gradient Boosting clásico

Proporciona una implementación clara y útil como benchmark. Puede ser suficiente para datasets medianos.

### XGBoost

Incluye regularización, muestreo de filas y columnas, tratamiento de valores faltantes y optimizaciones computacionales.

### LightGBM

Usa histogramas y crecimiento de hojas eficiente. Es apropiado para grandes volúmenes, pero su crecimiento por hoja puede sobreajustar si no se controla.

### CatBoost

Está diseñado para variables categóricas y utiliza esquemas ordenados para reducir fuga en sus codificaciones. Puede resultar útil con prestador, diagnóstico, municipio y producto, siempre que el orden temporal se preserve.

La selección no debe basarse solo en velocidad. Deben compararse estabilidad, sesgo, interpretabilidad, dependencia tecnológica y facilidad de operación.

## 10. Función de pérdida y soporte

Las predicciones de un árbol estándar no están obligadas a ser positivas. Para montos de reserva pueden considerarse:

- transformación logarítmica;
- pérdida Gamma;
- pérdida Tweedie;
- boosting de cuantiles;
- modelos separados de frecuencia y severidad;
- calibración posterior documentada.

Si se modela $\log(1+y)$, la transformación inversa puede requerir corrección de sesgo. Aplicar únicamente $\exp(\widehat z)-1$ no siempre recupera el valor esperado en la escala original.

## 11. Hiperparámetros

| Familia | Parámetros principales |
|---|---|
| Árbol | profundidad, mínimo por hoja, poda |
| Random Forest | árboles, variables por división, tamaño bootstrap |
| Boosting | iteraciones, tasa de aprendizaje, profundidad |
| XGBoost | `subsample`, `colsample_bytree`, regularización |
| LightGBM | `num_leaves`, `min_data_in_leaf`, fracciones |
| CatBoost | profundidad, iteraciones, regularización |

La búsqueda debe realizarse dentro de una validación temporal. Usar repetidamente el periodo de prueba para elegir parámetros convierte la prueba en otra validación.

## 12. Variables y codificación

Los árboles manejan relaciones no lineales, pero no solucionan automáticamente problemas de calidad.

Controles necesarios:

- categorías nuevas y raras;
- códigos que cambian en el tiempo;
- montos extremos;
- faltantes con significado operativo;
- variables derivadas de información futura;
- alta cardinalidad de prestador o diagnóstico;
- cambios de unidad o moneda.

Las codificaciones por promedio del target deben calcularse dentro de cada ventana de entrenamiento. Calcularlas con todo el dataset produce leakage.

## 13. Validación temporal

Un diseño mínimo incluye:

1. cortes históricos reproducibles;
2. entrenamiento con datos disponibles en cada corte;
3. predicción del desarrollo posterior;
4. comparación con el resultado maduro;
5. análisis por cohorte y segmento;
6. repetición en varias fechas.

Las métricas deben incluir MAE, RMSE, sesgo agregado, estabilidad y error por origen. Para cuantiles deben evaluarse pinball loss y cobertura.

## 14. Importancia de variables

### Importancia por ganancia

Resume cuánto reduce la pérdida cada variable dentro del modelo. Puede favorecer variables continuas o de alta cardinalidad.

### Importancia por permutación

Mide cuánto empeora el desempeño cuando una variable se permuta. Debe calcularse en datos posteriores y puede diluirse entre predictores correlacionados.

### SHAP

Descompone una predicción en contribuciones relativas a un valor base:

$$
\widehat y_i=\phi_0+\sum_{j=1}^{p}\phi_{i,j}
$$

SHAP ayuda a explicar una predicción, pero no convierte asociaciones en efectos causales.

## 15. Pruebas de comportamiento

Además de métricas promedio, conviene probar:

- monotonicidad respecto al desarrollo cuando sea razonable;
- sensibilidad a pagado e incurrido;
- estabilidad ante pequeños cambios de variables;
- respuesta a categorías desconocidas;
- comportamiento fuera del rango histórico;
- coherencia entre predicción individual y total;
- movimientos entre fechas de corte.

Algunas bibliotecas permiten restricciones de monotonicidad. Deben usarse solamente cuando la relación actuarial es defendible.

## 16. Aplicaciones en seguros de salud

Los árboles son útiles para:

- pago futuro por reclamación;
- probabilidad de cierre o reapertura;
- tiempo y resultado de glosas;
- identificación de alto costo;
- segmentación de patrones de desarrollo;
- frecuencia y severidad;
- predicción de pagos por prestador;
- estimación de utilización por población.

Su capacidad para detectar interacciones puede capturar que un mismo rezago tenga significado diferente según servicio, prestador o modalidad contractual.

## 17. Contexto colombiano

Una implementación para Colombia puede incorporar:

- diferencias entre prestación, radicación, factura, RIPS y pago;
- estado de glosa, devolución o conciliación;
- modalidad contractual;
- tipo de prestador y red;
- fuente de financiación;
- grupo de servicio y alto costo;
- periodo calendario y cambios operativos.

Las categorías de prestadores y códigos deben versionarse. Un identificador no debe actuar como sustituto opaco de calidad clínica, poder contractual o complejidad sin análisis adicional.

## 18. Ejemplo reproducible en Python

El ejemplo utiliza componentes de `scikit-learn`. La partición temporal debe construirse previamente.

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
    "days_since_report",
]

categorical_features = [
    "provider_type",
    "service_group",
    "contract_type",
]

features = numeric_features + categorical_features

preprocess = ColumnTransformer(
    transformers=[
        ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ],
    remainder="passthrough",
)

pipeline = Pipeline(
    steps=[
        ("preprocess", preprocess),
        (
            "model",
            RandomForestRegressor(
                n_estimators=500,
                max_features=0.7,
                min_samples_leaf=25,
                random_state=20260714,
                n_jobs=-1,
            ),
        ),
    ]
)

pipeline.fit(train[features], train["future_paid"])
prediction = pipeline.predict(test[features])

mae = mean_absolute_error(test["future_paid"], prediction)
reserve_bias = (
    prediction.sum() - test["future_paid"].sum()
) / test["future_paid"].sum()
```

El resultado debe almacenarse con la versión de datos, el corte, las variables, los parámetros, la semilla y las dependencias.

## 19. Arquitectura híbrida

Un esquema práctico conserva una referencia actuarial:

```text
Datos al corte
      │
      ├───────────────┐
      ▼               ▼
Benchmark clásico   Modelo de árboles
      │               │
      └───────┬───────┘
              ▼
     Comparación y explicación
              ▼
     Selección o combinación
              ▼
     Reserva y monitoreo
```

El benchmark permite identificar cuándo la mejora aparente proviene de leakage, sobreajuste o una anomalía operativa.

## 20. Gobierno y producción

Conservar como mínimo:

1. definición del objetivo y fecha de corte;
2. diccionario de variables;
3. reglas de categorías y faltantes;
4. ventanas de entrenamiento y prueba;
5. hiperparámetros y semillas;
6. resultados por periodo y segmento;
7. explicaciones de movimientos materiales;
8. comparación con benchmarks;
9. límites de uso y contingencia;
10. monitoreo de drift y calendario de revisión.

## 21. Errores frecuentes

- utilizar partición aleatoria;
- tratar importancia como causalidad;
- seleccionar profundidad con el periodo de prueba;
- ignorar censura o cola;
- aceptar predicciones negativas sin política;
- incluir identificadores con leakage;
- reportar solo métricas individuales;
- desplegar sin benchmark ni reconciliación;
- reentrenar automáticamente sin análisis de cambios.

## 22. Checklist

- [ ] El target corresponde a una cantidad actuarial definida.
- [ ] Las variables estaban disponibles al corte.
- [ ] La validación es temporal.
- [ ] Se controló profundidad y tamaño de hojas.
- [ ] Se evaluó sesgo agregado.
- [ ] La importancia se calculó fuera de muestra.
- [ ] Las predicciones materiales son explicables.
- [ ] Existe comparación con Chain Ladder, GLM u otro benchmark.
- [ ] Se probaron categorías nuevas y extrapolación.
- [ ] El modelo tiene controles de producción.

## Conclusiones

Los modelos basados en árboles ofrecen una combinación potente de flexibilidad, desempeño e instrumentos de explicación. En reserving de salud pueden representar interacciones complejas entre desarrollo, servicio, prestador y contrato.

Su uso defendible requiere validación por fecha de valoración, control de hojas pequeñas, análisis de sesgo agregado y reconciliación con métodos actuariales. La complejidad del ensemble nunca debe ocultar la definición económica de la reserva.

## Referencias

- ASOP No. 23, *Data Quality*.
- ASOP No. 41, *Actuarial Communications*.
- ASOP No. 56, *Modeling*.
- Breiman, L. “Random Forests”.
- Friedman, J. H. “Greedy Function Approximation: A Gradient Boosting Machine”.
- Hastie, T., Tibshirani, R. y Friedman, J. *The Elements of Statistical Learning*.
- Wüthrich, M. V. y Merz, M. *Statistical Foundations of Actuarial Learning and its Applications*.

## Capítulos relacionados

Anterior: [Machine Learning para reservas actuariales](18-machine-learning-for-loss-reserving.md).  
Siguiente: [Deep Learning para reservas actuariales](20-deep-learning-for-loss-reserving.md).
