---
title: "Deep Learning for Loss Reserving"
part: "Parte V · Machine Learning"
chapter: 20
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

# Deep Learning for Loss Reserving

Este capítulo introduce el uso de deep learning en reserving actuarial. El objetivo no es reemplazar automáticamente los métodos clásicos, sino ubicar las redes neuronales dentro de una arquitectura metodológica controlada, comparable y auditable.

En seguros de salud, deep learning puede ser útil cuando existen datos granulares, alta dimensionalidad, patrones no lineales e historias longitudinales de reclamaciones. También puede ser inapropiado cuando el portafolio es pequeño, la calidad de datos es débil, la trazabilidad regulatoria es prioritaria o la mejora frente a métodos más simples no compensa el riesgo de modelo.

## Objetivos de aprendizaje

Al terminar este capítulo, el lector debería poder:

- Identificar cuándo deep learning agrega valor frente a GLM, GAM, árboles, boosting o métodos clásicos.
- Formular problemas de reserving como predicción supervisada, predicción secuencial, supervivencia o transición de estados.
- Reconocer arquitecturas relevantes: redes densas, embeddings, redes recurrentes, convoluciones temporales y transformers.
- Diseñar variables y targets evitando leakage temporal.
- Evaluar incertidumbre, calibración y estabilidad.
- Integrar deep learning dentro de un marco de gobierno actuarial.

## 1. Rol de deep learning en reserving

Deep learning es una familia de modelos de alta capacidad. Esa capacidad permite capturar relaciones complejas, pero también aumenta el riesgo de sobreajuste, inestabilidad y opacidad.

En reserving, puede apoyar cuatro problemas principales:

| Problema | Ejemplo | Salida |
|---|---|---|
| Predicción de monto | Valor final esperado de una reclamación | Media, cuantiles o distribución |
| Predicción de desarrollo | Pagos futuros por periodo | Trayectoria esperada |
| Predicción de estado | Pago, glosa, cierre o reapertura | Probabilidades |
| Predicción agregada | Reserva por cohorte o segmento | Reserva esperada e intervalo |

La pregunta actuarial relevante no es si la red neuronal ajusta bien in-sample. La pregunta es si mejora la estimación fuera de muestra, con estabilidad, explicabilidad y gobierno suficientes.

## 2. Cuándo considerar deep learning

Deep learning puede ser razonable cuando se cumplen varias condiciones:

- Volumen suficiente de datos históricos granulares.
- Múltiples fuentes: reclamaciones, afiliados, prestadores, contratos, autorizaciones, facturación y pagos.
- Relaciones no lineales fuertes.
- Interacciones entre edad, diagnóstico, servicio, proveedor, contrato y calendario.
- Necesidad de modelar trayectorias o secuencias.
- Capacidad de validación, monitoreo y documentación.

No debería ser la primera opción cuando:

- El portafolio tiene pocos años de experiencia.
- Hay cambios regulatorios recientes no representados en los datos.
- La operación de facturación o pago cambió materialmente.
- El modelo no puede explicarse suficientemente.
- Un GLM, GAM o boosting ofrece desempeño similar con mayor trazabilidad.

## 3. Formulaciones del problema

### Predicción claim-level

Cada reclamación se modela como unidad individual. El objetivo puede ser:

- monto final permitido;
- monto final pagado;
- probabilidad de pago;
- probabilidad de glosa;
- tiempo hasta cierre;
- monto pendiente condicional al estado actual.

Esta formulación es natural en salud porque permite usar variables clínicas, contractuales y operativas.

### Predicción por celda de triángulo

Cada observación representa una celda origen-desarrollo-calendario. El modelo predice pagos incrementales, incurridos o conteos.

Esta formulación preserva la lógica actuarial tradicional y facilita comparación contra Chain Ladder, Mack, Bootstrap, GLM y GAM.

### Predicción secuencial

Cada reclamación o cohorte tiene una historia temporal:

$$
x_{i,1}, x_{i,2}, \ldots, x_{i,t}
$$

El modelo aprende cómo evoluciona la reclamación o cohorte en el tiempo. Es útil cuando los eventos de autorización, radicación, glosa, respuesta y pago tienen orden informativo.

### Modelos multiestado

Las redes neuronales también pueden estimar probabilidades de transición entre estados:

$$
\Pr(S_{t+1}=j \mid S_t=i, X_t)
$$

Esto es especialmente relevante para glosas, devoluciones, pagos parciales, cierres y reaperturas.

## 4. Variables explicativas

Las variables deben estar disponibles al momento de valoración. Incluir información futura produce leakage y puede invalidar el modelo.

| Dimensión | Variables |
|---|---|
| Afiliado | edad, sexo, región, grupo de riesgo |
| Prestación | tipo de servicio, código, complejidad, ámbito |
| Prestador | tipo de prestador, red, histórico observado |
| Contrato | modalidad de pago, tarifa, capitación, paquete |
| Tiempo | mes de ocurrencia, mes de reporte, rezago |
| Operación | canal, estado de auditoría, días desde radicación |
| Historia | pagos observados, ajustes, estado actual |

Variables no admisibles al corte:

- monto final observado;
- pagos posteriores a la fecha de valoración;
- estado de cierre futuro;
- glosas resueltas después del corte;
- cualquier variable creada con información futura.

## 5. Arquitecturas principales

### Redes densas

Una red densa es adecuada para datos tabulares con variables numéricas y categóricas codificadas:

$$
\hat{y}=f_\theta(X)
$$

Ventajas:

- flexible;
- compatible con datos tabulares;
- puede modelar relaciones no lineales.

Limitaciones:

- puede sobreajustar;
- requiere validación temporal estricta;
- suele ser menos interpretable que GLM, GAM o árboles.

### Embeddings categóricos

Los embeddings permiten representar variables categóricas de alta cardinalidad, como prestador, diagnóstico, municipio o producto:

$$
e_c \in \mathbb{R}^k
$$

Esto puede mejorar la representación de categorías, pero requiere controles para categorías raras, cambios de codificación y nuevos prestadores.

### Redes recurrentes

Las redes recurrentes, incluyendo LSTM y GRU, procesan secuencias. Son útiles cuando el orden de eventos importa:

- secuencia de estados de una reclamación;
- pagos mensuales observados;
- historial de autorizaciones;
- cambios en glosas y respuestas.

### Convoluciones temporales

Las convoluciones temporales capturan patrones locales en series de desarrollo:

$$
(P_{t-3}, P_{t-2}, P_{t-1}, P_t) \rightarrow P_{t+1}
$$

Pueden ser más estables y eficientes que redes recurrentes en algunos problemas.

### Transformers

Los transformers pueden modelar dependencias largas y atención entre eventos. En reserving, podrían aplicarse a historiales granulares de reclamaciones o prestadores.

Su adopción debe ser conservadora. Requieren volumen significativo, infraestructura y pruebas sólidas de estabilidad.

## 6. Funciones de pérdida

La función de pérdida debe reflejar el objetivo actuarial.

| Objetivo | Función de pérdida |
|---|---|
| Monto esperado | MAE, MSE, Huber |
| Conteos | Poisson, binomial negativa |
| Severidad positiva | Gamma, lognormal |
| Frecuencia-severidad | Tweedie |
| Cuantiles | Pinball loss |
| Distribución predictiva | Negative log-likelihood |
| Clasificación de estado | Cross-entropy |
| Tiempo hasta evento | Pérdida de supervivencia |

Para reserving no basta optimizar error individual. También importan sesgo agregado, estabilidad por cohorte, calibración y desempeño en periodos recientes.

## 7. Incertidumbre predictiva

Deep learning no produce automáticamente incertidumbre actuarial confiable. Se requieren métodos adicionales:

- ensembles;
- bootstrap;
- Monte Carlo dropout;
- redes bayesianas aproximadas;
- modelos de cuantiles;
- conformal prediction;
- simulación predictiva.

La incertidumbre debe analizarse por componente:

| Componente | Descripción |
|---|---|
| Riesgo de proceso | Variabilidad futura |
| Riesgo de parámetro | Incertidumbre de estimación |
| Riesgo de modelo | Arquitectura y supuestos |
| Riesgo operacional | Cambios de datos o procesos |
| Riesgo externo | Regulación, inflación médica, shocks |

## 8. Benchmarks mínimos

Todo modelo de deep learning debe compararse contra métodos más simples:

- Chain Ladder;
- Mack Chain Ladder;
- Bootstrap Chain Ladder;
- Bornhuetter-Ferguson;
- Cape Cod;
- GLM;
- GAM;
- árboles y boosting;
- métodos PMPM o frecuencia-severidad en salud.

Si la mejora no es material y estable, deep learning no está justificado para producción.

## 9. Validación temporal

La validación debe respetar el tiempo. Un split aleatorio puede generar leakage.

Estrategia recomendada:

1. Entrenar con periodos antiguos.
2. Validar con periodos posteriores.
3. Probar con periodos aún más recientes.
4. Hacer backtesting rolling-origin.
5. Evaluar por cohorte, producto, prestador y segmento.
6. Comparar contra cierres reales.

Ejemplo:

| Train | Validation | Test |
|---|---|---|
| 2019–2022 | 2023 | 2024 |
| 2020–2023 | 2024 | 2025 |

## 10. Métricas de evaluación

Las métricas deben combinar precisión individual y suficiencia agregada.

| Métrica | Uso |
|---|---|
| MAE | Error absoluto robusto |
| RMSE | Penaliza errores grandes |
| Bias agregado | Control de suficiencia |
| Error por cohorte | Diagnóstico actuarial |
| Pinball loss | Cuantiles |
| Coverage | Cobertura de intervalos |
| Calibration plots | Calibración probabilística |
| Reserve-to-actual | Evaluación final de reservas |

La métrica principal debe definirse antes del entrenamiento.

## 11. Interpretabilidad

La interpretabilidad es obligatoria para adopción práctica. Métodos útiles:

- importancia por permutación;
- SHAP;
- partial dependence;
- accumulated local effects;
- análisis de sensibilidad;
- stress testing por segmento;
- comparación contra GLM o GAM.

El objetivo no es explicar cada peso de la red. El objetivo es demostrar que el comportamiento del modelo es razonable, estable y consistente con conocimiento actuarial.

## 12. Restricciones actuariales

Los modelos pueden violar restricciones naturales si no se controlan:

- predicciones negativas;
- reservas decrecientes sin justificación;
- sensibilidad extrema a variables marginales;
- discontinuidades por categorías raras;
- extrapolación no controlada.

Controles posibles:

- transformación logarítmica;
- distribuciones positivas;
- clipping documentado;
- calibración posterior;
- restricciones de monotonicidad;
- reglas de negocio posteriores al modelo.

## 13. Aplicaciones en seguros de salud

En salud, deep learning puede apoyar:

- predicción de cuentas pendientes;
- severidad por diagnóstico o prestación;
- probabilidad de glosa;
- tiempo de resolución;
- detección de prestadores atípicos;
- patrones de alto costo;
- desarrollo por canal de facturación;
- reservas para contratos prospectivos;
- estimación de pagos tardíos.

Pero salud introduce riesgos específicos:

- cambios en redes;
- inflación médica;
- estacionalidad;
- epidemias;
- cambios de codificación;
- modificaciones tarifarias;
- comportamiento administrativo de prestadores;
- cambios regulatorios.

## 14. Aplicación al contexto colombiano

En Colombia, las aplicaciones deben considerar:

- trazabilidad entre prestación, factura, RIPS, FEV y pago;
- glosas, devoluciones y controversias;
- cuentas conocidas pendientes;
- contratos capitados y pagos prospectivos;
- alto costo;
- mecanismos especiales de financiación;
- diferencias entre fecha de prestación, radicación, contabilización y pago.

Deep learning puede ser útil para modelar estados y tiempos de resolución, pero la reserva final debe reconciliarse con saldos contables, auditoría médica y controles regulatorios internos.

## 15. Flujo de implementación

Un flujo mínimo incluye:

1. Definir objetivo actuarial.
2. Definir fecha de corte.
3. Definir variables admisibles.
4. Construir dataset reproducible.
5. Separar train, validation y test temporalmente.
6. Entrenar benchmarks simples.
7. Entrenar deep learning.
8. Evaluar desempeño y estabilidad.
9. Analizar interpretabilidad.
10. Calibrar incertidumbre.
11. Ejecutar backtesting.
12. Documentar supuestos.
13. Aprobar uso.
14. Monitorear drift.

## 16. Ejemplo conceptual en Python

```python
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

features = [
    "development_month",
    "claim_age_days",
    "paid_to_date",
    "provider_type",
    "service_group",
    "contract_type",
]

target = "future_paid_amount"

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False,
)
```

En producción debe usarse split temporal explícito, control de leakage, versionamiento de datos y comparación contra benchmarks.

## 17. Ejemplo conceptual de red neuronal

```python
import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Input(shape=(n_features,)),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dropout(0.10),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dense(1, activation="softplus"),
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss="mae",
)
```

La activación `softplus` evita predicciones negativas. Aun así, el modelo requiere validación actuarial y calibración.

## 18. Gobierno del modelo

La documentación mínima debe incluir:

- objetivo de negocio y objetivo actuarial;
- población cubierta;
- variables utilizadas y excluidas;
- fecha de corte;
- definición del target;
- arquitectura;
- función de pérdida;
- benchmarks;
- validación temporal;
- resultados por segmento;
- limitaciones;
- plan de monitoreo;
- responsables de aprobación.

## 19. Riesgos principales

| Riesgo | Mitigación |
|---|---|
| Leakage temporal | Variables observables al corte |
| Sobreajuste | Regularización y backtesting |
| Opacidad | Interpretabilidad y documentación |
| Drift | Monitoreo periódico |
| Sesgo por segmento | Métricas segmentadas |
| Extrapolación | Límites y reglas de negocio |
| Falsa precisión | Intervalos y escenarios |

## 20. Checklist de adopción

Antes de usar deep learning para una reserva oficial, confirmar:

- El objetivo está definido en términos actuariales.
- Las variables son observables al corte.
- Existe benchmark clásico documentado.
- El split de validación respeta el tiempo.
- El modelo mejora de forma material y estable.
- Los errores agregados son aceptables.
- Los intervalos están calibrados.
- El comportamiento es explicable.
- El modelo está documentado.
- Existe plan de monitoreo.
- La reserva se reconcilia con saldos y controles financieros.

## 21. Conclusiones

Deep learning puede ampliar el conjunto de herramientas de reserving, especialmente cuando existen datos granulares y patrones complejos. Sin embargo, su uso debe ser disciplinado.

En seguros de salud, el potencial más relevante está en modelos claim-level, modelos de estados, predicción de glosas, pagos tardíos y patrones de desarrollo por proveedor o contrato. Aun así, la reserva final debe integrarse con criterios actuariales, contables, regulatorios y operativos.

## Referencias

- ASOP No. 1, Introductory Actuarial Standard of Practice.
- ASOP No. 23, Data Quality.
- ASOP No. 38, Using Models Outside the Actuary's Area of Expertise.
- ASOP No. 43, Property/Casualty Unpaid Claim Estimates.
- ASOP No. 56, Modeling.
- Wüthrich, M. V. Machine Learning in Individual Claims Reserving.
- Gabrielli, A., Richman, R., and Wüthrich, M. Neural Network Embedding of the Over-Dispersed Poisson Reserving Model.
- Richman, R. AI in Actuarial Science.

## Próximo capítulo

➡️ **[Health Insurance Reserving Specificities](../part-06-health-specific/21-health-insurance-reserving-specificities.md)**
