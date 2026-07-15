# Datos demo: triángulos simulados de reclamaciones pagadas de salud

Esta carpeta contiene datos sintéticos reproducibles generados con:

```bash
python scripts/generate_demo_triangles.py --language es
```

Archivos:

- `reclamaciones_pagadas_largo.csv`: pagos sintéticos observados por año de origen y edad de desarrollo.
- `triangulo_pagado_incremental.csv`: triángulo pagado incremental.
- `triangulo_pagado_acumulado.csv`: triángulo pagado acumulado.
- `factores_edad_a_edad.csv`: factores de desarrollo seleccionados, ponderados por volumen.
- `resultados_chain_ladder.csv`: pagado observado, CDF seleccionado, ultimate e IBNR por año de origen.
- `resumen_ejecucion.txt`: resumen de ejecución.

Los datos son sintéticos y no deben interpretarse como experiencia real de un portafolio.
