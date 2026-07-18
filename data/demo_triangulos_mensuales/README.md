# Datos del demo mensual r2

Datos sintéticos con una base de estimación de **72 x 36** y una vista tradicional **36 x 36**. El runoff completo se simula hasta edad 48; la cola 35->48 es una hipótesis conocida del generador.

- `triangulo_pagado_mensual_acumulado.csv`: base completa para estimación.
- `vista_tradicional_36x36.csv`: últimos 36 orígenes, presentación tradicional 36 x 36.
- `factores_mensuales_edad_a_edad.csv`: factores y observaciones por enlace.
- `resultados_proyeccion_pasivo_no_pagado.csv`: costo proyectado, cola y pasivo no pagado estimado.
- `prior_bornhuetter_ferguson_mensual.csv`: prior sintético para BF/Benktander.

**Alcance:** con un triángulo agregado exclusivamente pagado no se separan IBNR puro, RBNS e IBNER. El resultado es educativo y no constituye una reserva contable.
