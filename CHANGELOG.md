# Changelog

## v0.6.0 Sprint 2 r2.1.2 — 2026-07-18

- Evita nombres duplicados en la tabla de sensibilidad Chain Ladder de Streamlit.
- Usa directamente las columnas actuariales precisas generadas por el motor.
- Retira la línea en blanco adicional al final del informe de investigación de ChatGPT.

## v0.6.0 Sprint 2 r2.1.1 — 2026-07-18

- Reemplaza íntegramente `bibliography/chatgpt-deep-research-report.md` con la nueva investigación.
- Normaliza espacios finales del Markdown sin alterar su contenido sustantivo.
- Alinea la advertencia visible del Demo 6 con la prueba de alcance actuarial.

Todos los cambios relevantes de este proyecto se documentan en este archivo. El formato se inspira en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y utiliza versionado semántico.

## [Unreleased]

<!-- bibliography-refresh-2026-07-18 -->
### Bibliografía

- Actualización del informe de investigación de ChatGPT e incorporación del informe de Claude
  como fuentes de descubrimiento, explícitamente subordinadas a la verificación de fuentes
  primarias.
- Registro verificable del estudio PROESA (2021) sobre planes voluntarios de salud, con alcance,
  limitaciones, páginas y SHA-256.
- Exclusión deliberada del PDF de Facecolda/PROESA del repositorio distribuible por su restricción
  expresa de reproducción; se conserva una ficha bibliográfica auditable.

<!-- demo6-actuarial-scope-v0.6.0-sprint2-r2 -->
### Corregido en r2

- Demo mensual ampliado a una base 72×36, con vista actuarial tradicional 36×36 y runoff
  sintético separado hasta la edad 48 para sustentar una cola didáctica 35→48.
- Sustitución de rótulos que prometían “IBNR” o “ultimate” por `pasivo no pagado estimado`,
  `acumulado proyectado a edad terminal` y `costo final estimado con cola`, según corresponda.
- Eliminación del piso artificial en cero del residual pagado; los resultados negativos permanecen
  visibles como diagnóstico y requieren investigación.
- Panel posterior a cada carga con inventario de información recibida, información faltante o
  deseable y alcance de cálculo soportado por los datos.
- Exportaciones con nombres precisos y manifest que aclara que un triángulo pagado agregado no
  identifica por separado IBNR puro, RBNS ni IBNER.

<!-- part-02-classical-methods-v0.6.0-sprint1 -->
### Documentación

- Profundización de diagnósticos y backtesting de Chain Ladder con cortes retrospectivos,
  métricas reconciliadas, runoff, sensibilidad y evidencia mínima.
- Especificación técnica de Bornhuetter-Ferguson, Benktander y Cape Cod con fórmulas,
  ejemplos numéricos, contratos de datos, limitaciones y criterios de prueba.
- Marco común para comparar métodos clásicos por periodo de origen y total sin confundir la
  documentación objetivo con funcionalidad ya implementada.
- Actualización de Demo 6 y del plan v0.6.0 para separar componentes disponibles y pendientes.

<!-- demo6-benktander-v0.6.0-sprint2 -->
### Agregado

- Motor Benktander modular con recurrencia y forma cerrada reconciliadas por periodo de origen.
- Iteraciones configurables, sensibilidad desde el prior inicial y pesos explícitos de prior y
  Chain Ladder.
- Comparación visual no apilada de Chain Ladder, Bornhuetter-Ferguson y Benktander.
- Diagnósticos de reconciliación, CDF, pesos, IBNR negativo y convergencia.
- Exportación conjunta con resultados, totales, sensibilidad, diagnósticos y configuración
  Benktander, sin archivos fuente originales.
- Pruebas de equivalencia con BF en una iteración, formas iterativa y cerrada, entradas inválidas,
  inmutabilidad y recorrido completo en Streamlit.

### Cambiado

- Demo 6 y el capítulo Benktander reflejan funcionalidad efectivamente implementada; Cape Cod y
  el backtesting común continúan como alcance pendiente de v0.6.0.

## [0.5.0] - 2026-07-17

### Agregado

- Núcleo modular Bornhuetter-Ferguson que consume la madurez de
  Chain Ladder sin modificar sus resultados.
- Contratos explícitos para definir el prior como ultimate esperado directo o como exposición por
  tasa esperada, con conciliación exacta por periodo de origen.
- Resultados BF por origen y totales, comparación directa con Chain Ladder, sensibilidad a shocks
  del prior y diagnósticos de CDF, priors e IBNR negativos.
- Pruebas numéricas de la fórmula del handbook, modos de prior, validaciones, sensibilidad y
  preservación de los datos de entrada.
- Sprint 2 de Demo 6: carga local de priors en CSV, TXT delimitado, XLSX o Parquet, mapeo de
  columnas y ejecución Bornhuetter-Ferguson posterior a una estimación Chain Ladder válida.
- Prior sintético reproducible por miembros-mes y costo esperado, construido de forma
  independiente del patrón observado de pagos.
- Comparación visual por periodo y total de ultimate e IBNR, sensibilidad configurable del prior,
  diagnósticos y seis KPI compactos.
- Exportación conjunta y auditable de Chain Ladder y Bornhuetter-Ferguson sin incluir los archivos
  fuente originales del triángulo ni del prior.
- Comparación visual balanceada con Chain Ladder y BF lado a lado, líneas no apiladas sobre una
  escala común y gráfico firmado `BF − CL` con referencia cero para evitar interpretaciones
  aditivas incorrectas.
- Eliminación completa de `st.bar_chart` en Demo 6 e identificador visible de la versión de la
  interfaz para detectar procesos locales que estén sirviendo una copia anterior.

## [0.4.0] - 2026-07-16

### Agregado

- Demo 6 local para estimar ultimate e IBNR mediante Chain Ladder determinístico a partir del
  ejemplo mensual o de paquetes agregados y reconciliados de Demo 5.
- Motor modular con ratios individuales, cuatro selecciones automáticas, selección manual, factor
  de cola, CDF, proyección del triángulo, sensibilidad y diagnósticos.
- Exportación ZIP en memoria y pruebas numéricas, de seguridad del paquete y de la interfaz.
- Tarjetas KPI compactas y responsivas que muestran completos los importes de Demo 6.

### Cambiado

- Sistema visual corporativo reutilizable para aplicaciones Streamlit, con IgraSans autoalojada y
  registrada nativamente mediante `theme.fontFaces`, paleta oficial, hero, sidebar, indicadores,
  botones y footer responsivo contenido dentro de la columna principal.
- Demo 5 adopta la misma identidad visual del sitio principal sin enviar fuentes ni activos a
  servicios externos.

## [0.3.0] - 2026-07-15

### Agregado

- Demo 5 local para construir triángulos actuariales con archivos CSV, TXT delimitado, XLSX o
  Parquet del usuario.
- Interfaz Streamlit ejecutada exclusivamente en `localhost`.
- Núcleo modular `health_reserving` para ingestión, mapeo, validación, triángulos y exportación.
- Distinción explícita entre ceros observados y celdas futuras mediante máscara de observación.
- Reconciliación automática entre datos canónicos y triángulo incremental.
- Gates G0, G1, G2, G3, G4, G7 y G9 aplicados al flujo de construcción.
- Ambiente reproducible de Anaconda y lanzador para principiantes.
- Paquete ZIP local con validaciones, triángulos, máscara, diagnóstico, configuración y manifiesto.
- Pruebas para fechas, negativos, duplicados, segmentación, reconciliación y privacidad del export.
- Pruebas de ingestión para TXT delimitado y conservación de tipos al leer Parquet.

### Seguridad

- Exclusión de carpetas locales de datos y resultados mediante `.gitignore`.
- Detalle canónico fila a fila excluido por defecto del paquete descargable.
- Configuración local con CORS y XSRF habilitados y estadísticas de Streamlit desactivadas.

## [0.2.4] - 2026-07-15

### Agregado

- Tipografía corporativa IgraSans autoalojada.
- Logo actuarial y favicon propios.
- Footer corporativo con enlaces a Javier Forero, CV, GitHub y LinkedIn.
- Integración nativa con Google Analytics 4 mediante `G-MQ3K8EVKV0`.

### Cambiado

- Aplicación de la identidad visual morada de Javier Forero al handbook.
- Nueva paleta principal `#4e00ff` y acento `#7c4dff`.
- Rediseño del hero de la página principal.
- Mejora de botones, navegación activa, búsqueda y modo oscuro.
- Corrección del renderizado de iconos Material.
- Títulos HTML específicos para el handbook y sus páginas internas.
- Metadata de autor y color del navegador.
- Incorporación de IgraSans como tipografía principal.
- Incorporación de identidad corporativa en encabezado y footer.

## [0.2.2] - 2026-07-15

### Cambiado

- Migración del sitio público a `https://actuaria.javierforero.co/`.
- Actualización de la URL canónica, enlaces de publicación y metadata de citación.
- Configuración del subdominio actuarial como URL pública oficial del handbook.

## [0.2.1] - 2026-07-15

### Agregado

- Marco de preparación de datos para seleccionar y comparar metodologías de reserving, publicado en dos partes.
- Taxonomía de dominios D1–D10 para alcance, fechas, importes, identificadores, historia, exposición, priors, segmentación, operación y gobierno.
- Gates G0–G9 y estados `LISTO`, `LISTO_CON_LIMITACIONES`, `EXPLORATORIO`, `BLOQUEADO` y `NO_PERTINENTE`.
- Diccionario canónico con 132 campos principales en español y alias opcionales en inglés.
- Matriz de preparación, requisitos y datos faltantes por metodología.
- Demo 4 de mapeo canónico, deduplicación y elegibilidad metodológica.
- Demo bilingüe de triángulos mensuales pagados con 60 meses de origen y desarrollo 0–24.
- Controles de suficiencia por factor, comparación con ultimate simulado y visualizaciones SVG.

### Cambiado

- Navegación de MkDocs para incorporar el marco de preparación de datos, la matriz y el Demo 4.
- Portada, README y roadmap para reflejar cuatro demos prácticos.
- Estructura principal del repositorio para incorporar configuraciones canónicas.
- Normalización de archivos CSV con terminaciones de línea LF.
- Migración del sitio público a `https://actuaria.javierforero.co/`.
- Actualización de la URL canónica, enlaces de publicación y metadata de citación.

## [0.2.0] - 2026-07-14

### Agregado

- Demo bilingüe de triángulos pagados vs. incurridos con datos sintéticos, reserva caso, comparación Chain Ladder y visualizaciones SVG.
- Capítulo 20 sobre Deep Learning para reservas actuariales.
- Capítulos 34–40 para completar el bloque colombiano hasta el capítulo 40.
- Verificadores incrementales para compatibilidad matemática y consistencia editorial.

### Cambiado

- Traducción y normalización en español de las Partes 1–7.
- Unificación de títulos, H1, front matter y navegación.
- Actualización de `README.md`, portada, roadmap, documento de transferencia y metadata de citación para reflejar 40 capítulos, siete partes y dos demos.
- Consolidación de las mejoras posteriores a v0.1.3 en una nueva versión pública.

### Corregido

- Renderizado matemático incompatible con la vista previa de GitHub.
- Delimitadores `\[...\]`, macros no admitidas, llaves problemáticas y ecuaciones fragmentadas.
- Metadatos duplicados y títulos residuales en inglés.
- Rutas y etiquetas desactualizadas en la navegación de MkDocs.

## [0.1.3] - 2026-07-14

### Agregado

- Visualización SVG del triángulo actuarial tradicional.
- Tablas Markdown de triángulos acumulados en formato actuarial.
- Generador reproducible de visualizaciones para español e inglés.

### Cambiado

- Ampliación del Demo 1 con lectura visual de la diagonal observada y celdas futuras.

## [0.1.2] - 2026-07-14

### Agregado

- Versión bilingüe del demo de triángulos simulados.
- Datos, resultados y documentación equivalentes en español e inglés.

## [0.1.1] - 2026-07-14

### Agregado

- Primer demo reproducible de triángulos pagados de salud.
- Datos sintéticos en formato largo.
- Triángulos incremental y acumulado.
- Factores edad-a-edad y estimación Chain Ladder de ultimate e IBNR.

## [0.1.0] - 2026-07-14

### Agregado

- Publicación inicial del handbook hasta el capítulo 40.
- Configuración de MkDocs Material y GitHub Pages.
- Auditoría estructural de documentación y preflight de publicación.
- Validación automática de front matter, H1, bloques de código, navegación y enlaces internos.
- Archivos de gobierno y comunidad:
  - `CONTRIBUTING.md`;
  - `CODE_OF_CONDUCT.md`;
  - `SECURITY.md`;
  - `CITATION.cff`;
  - plantillas de issues y pull requests;
  - workflow de GitHub Pages.

[Unreleased]: https://github.com/jaforero/health-insurance-reserving-handbook/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/jaforero/health-insurance-reserving-handbook/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/jaforero/health-insurance-reserving-handbook/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/jaforero/health-insurance-reserving-handbook/compare/v0.2.4...v0.3.0
[0.2.4]: https://github.com/jaforero/health-insurance-reserving-handbook/compare/v0.2.2...v0.2.4
[0.2.2]: https://github.com/jaforero/health-insurance-reserving-handbook/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/jaforero/health-insurance-reserving-handbook/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/jaforero/health-insurance-reserving-handbook/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/jaforero/health-insurance-reserving-handbook/releases/tag/v0.1.3
[0.1.2]: https://github.com/jaforero/health-insurance-reserving-handbook/releases/tag/v0.1.2
[0.1.1]: https://github.com/jaforero/health-insurance-reserving-handbook/releases/tag/v0.1.1
[0.1.0]: https://github.com/jaforero/health-insurance-reserving-handbook/releases/tag/v0.1.0
