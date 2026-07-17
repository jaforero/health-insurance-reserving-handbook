# Demo 6 · Sprint 1 — Núcleo Bornhuetter-Ferguson

## Objetivo

Agregar Bornhuetter-Ferguson como una capa determinística, modular y auditable sobre el resultado
Chain Ladder publicado en `v0.4.0`. Este sprint valida primero el contrato matemático; no cambia la
interfaz Streamlit ni los paquetes exportados.

## Contrato de entrada

El motor recibe:

1. un `ChainLadderResult` con observado, CDF, ultimate e IBNR por periodo de origen;
2. una tabla de prior con exactamente los mismos periodos;
3. un `BornhuetterFergusonConfig` que declara cómo interpretar el prior.

Se admiten dos modos:

| Modo | Columnas mínimas | Cálculo del prior |
|---|---|---|
| `expected_ultimate` | `periodo_origen`, `ultimate_esperado` | valor directo por origen |
| `exposure_rate` | `periodo_origen`, `exposicion`, `tasa_esperada` | exposición × tasa |

Los nombres de columnas pueden configurarse. El motor bloquea periodos faltantes, adicionales o
duplicados, valores no finitos y priors, exposiciones o tasas negativas.

## Cálculo

Para cada periodo de origen `i`:

```text
porcentaje_desarrollado_i = 1 / CDF_i
porcentaje_no_desarrollado_i = 1 - porcentaje_desarrollado_i
IBNR_BF_i = prior_i × porcentaje_no_desarrollado_i
Ultimate_BF_i = observado_i + IBNR_BF_i
```

No se aplica un piso implícito de cero. Un CDF menor que uno conserva el resultado matemático y
genera una advertencia para revisión actuarial.

## Salidas

`fit_bornhuetter_ferguson(...)` entrega:

- prior normalizado y reconciliado;
- resultado por periodo con madurez, BF y comparación contra Chain Ladder;
- totales reconciliados;
- sensibilidad configurable a shocks del prior;
- diagnósticos estructurados `BF01` a `BF07`;
- copia de la configuración usada.

## Ejemplo mínimo

```python
import pandas as pd

from health_reserving import (
    BornhuetterFergusonConfig,
    fit_bornhuetter_ferguson,
)

prior = pd.DataFrame(
    {
        "periodo_origen": ["2023", "2024"],
        "exposicion": [10_000, 11_000],
        "costo_esperado": [125_000, 132_000],
    }
)

config = BornhuetterFergusonConfig(
    prior_mode="exposure_rate",
    expected_rate_column="costo_esperado",
    sensitivity_shocks=(-0.10, 0.0, 0.10),
)

bf = fit_bornhuetter_ferguson(chain_ladder_result, prior, config)
print(bf.origin_summary)
print(bf.sensitivity)
```

`chain_ladder_result` corresponde al objeto ya producido por `fit_chain_ladder(...)`.

## Criterios de aceptación del Sprint 1

- reproduce el ejemplo conceptual del capítulo 11: observado 100, CDF 2 y prior 180 producen
  IBNR 90 y ultimate 190;
- los dos modos de prior producen el mismo resultado cuando su expectativa es equivalente;
- sensibilidad y totales se reconcilian con los resultados por origen;
- los periodos deben coincidir uno a uno;
- los datos de entrada no se modifican;
- los CDF menores que uno se conservan y se diagnostican;
- toda la suite, auditorías y build estricto continúan en verde.

## Alcance diferido al Sprint 2

- carga y mapeo del archivo de exposición/prior en Streamlit;
- componentes visuales BF dentro de Demo 6;
- exportación ZIP conjunta Chain Ladder + BF;
- sensibilidad visual a métodos de desarrollo;
- guía paso a paso para usuarios principiantes.
