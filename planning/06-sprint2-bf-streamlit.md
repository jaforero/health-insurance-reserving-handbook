# Demo 6 · Sprint 2 — Integración Bornhuetter-Ferguson en Streamlit

## Objetivo

Convertir el núcleo Bornhuetter-Ferguson del Sprint 1 en un recorrido educativo local dentro de
Demo 6. La integración conserva Chain Ladder como primera etapa, hace explícito el origen del
prior y produce una comparación reproducible sin persistir archivos internos del usuario.

## Recorrido de usuario

1. cargar el ejemplo mensual o un paquete agregado de Demo 5;
2. seleccionar factores Chain Ladder, cola y moneda;
3. confirmar la revisión actuarial y estimar Chain Ladder;
4. cargar un prior local o usar el prior sintético incluido;
5. mapear el periodo de origen y la definición del prior;
6. documentar shocks inferior y superior;
7. confirmar fuente, fecha, unidad, independencia y ajustes;
8. comparar Chain Ladder y Bornhuetter-Ferguson;
9. descargar el paquete conjunto.

## Fuentes y contratos

El prior local puede leerse desde CSV, TXT delimitado, XLSX o Parquet. Debe contener exactamente
una fila por periodo de origen y admitir uno de estos contratos:

| Modo | Campos lógicos | Cálculo |
|---|---|---|
| Ultimate esperado | origen, ultimate esperado | prior directo |
| Exposición por tasa | origen, exposición, tasa esperada | exposición × tasa |

La interfaz permite mapear nombres internos sin renombrar el archivo. El núcleo bloquea orígenes
faltantes, adicionales o duplicados y valores no numéricos, no finitos o negativos.

## Prior sintético reproducible

El generador mensual crea un prior educativo basado en miembros-mes y costo esperado por miembro.
La expectativa utiliza tendencia y estacionalidad conocidas, pero excluye el ruido de morbilidad
usado para simular la experiencia de reclamaciones. Así se evita construir el prior a partir del
desarrollo observado que luego se pretende comparar.

## Resultados visuales

- base observada común y dos tarjetas metodológicas paralelas con ultimate, IBNR y proporción;
- líneas no apiladas para comparar el IBNR por periodo sobre la misma escala;
- barras firmadas `BF − CL` con referencia cero para aislar la diferencia;
- sensibilidad del IBNR BF a los shocks del prior;
- diagnósticos del prior, CDF y resultados negativos;
- vista del prior normalizado y reconciliado.

## Privacidad y trazabilidad

- todos los cálculos se ejecutan en la sesión local de Streamlit;
- los archivos cargados no se copian al repositorio;
- el ZIP conjunto se genera en memoria;
- el paquete excluye los archivos fuente originales;
- el manifiesto conserva hashes de las entradas agregadas, configuraciones y versiones del motor.

## Criterios de aceptación

- el ejemplo incluido completa Chain Ladder y BF sin errores;
- los cuatro formatos del prior reutilizan el lector tabular validado en Demo 5;
- un cambio en factores, prior, mapeo o shocks invalida resultados anteriores;
- la comparación concilia por periodo y total;
- ninguna visualización suma o apila estimaciones metodológicas alternativas;
- la exportación incluye resultados, sensibilidad, diagnósticos y configuraciones;
- las pruebas unitarias, de interfaz, auditoría documental, preflight y build estricto terminan
  correctamente.

## Fuera de alcance

- error de predicción e intervalos;
- Mack y bootstrap;
- calibración automática del prior con la experiencia observada;
- Benktander y Cape Cod;
- persistencia, autenticación o despliegue multiusuario.
