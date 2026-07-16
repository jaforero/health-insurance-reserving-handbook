# Changelog

Todos los cambios relevantes de este proyecto se documentan en este archivo. El formato se inspira en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y utiliza versionado semántico.

## [Unreleased]

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

[Unreleased]: https://github.com/jaforero/health-insurance-reserving-handbook/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/jaforero/health-insurance-reserving-handbook/compare/v0.2.4...v0.3.0
[0.2.4]: https://github.com/jaforero/health-insurance-reserving-handbook/compare/v0.2.2...v0.2.4
[0.2.2]: https://github.com/jaforero/health-insurance-reserving-handbook/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/jaforero/health-insurance-reserving-handbook/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/jaforero/health-insurance-reserving-handbook/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/jaforero/health-insurance-reserving-handbook/releases/tag/v0.1.3
[0.1.2]: https://github.com/jaforero/health-insurance-reserving-handbook/releases/tag/v0.1.2
[0.1.1]: https://github.com/jaforero/health-insurance-reserving-handbook/releases/tag/v0.1.1
[0.1.0]: https://github.com/jaforero/health-insurance-reserving-handbook/releases/tag/v0.1.0
