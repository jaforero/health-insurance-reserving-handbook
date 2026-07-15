# Datos del demo de triángulos mensuales

Datos enteramente sintéticos para 60 meses de origen y edades de desarrollo 0–24.

## Reproducción

```bash
python scripts/generate_demo_monthly_triangles.py --language es
```

## Archivos

- `reclamaciones_pagadas_mensuales_largo.csv`: datos observados en formato largo.
- `triangulo_pagado_mensual_incremental.csv` y `triangulo_pagado_mensual_acumulado.csv`: triángulos tradicionales.
- `factores_mensuales_edad_a_edad.csv`: factores mensuales y número de observaciones.
- `resultados_chain_ladder_mensual.csv`: ultimate, IBNR y comparación con la verdad simulada.
- `diagnostico_suficiencia.csv`: controles de suficiencia del diseño.

Los datos no representan experiencia de una entidad ni una metodología prescrita.
