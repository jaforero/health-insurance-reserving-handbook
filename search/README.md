# Búsqueda híbrida estática del Handbook

Este componente añade recuperación por significado a **Pregúntale al Handbook**, conservando el asistente editorial anterior. La interfaz aislada se publica en `pregunta/`; funciona también bajo `/health-insurance-reserving-handbook/pregunta/`. No hereda la analítica, MathJax ni Mermaid externos de la plantilla MkDocs existente.

## Arquitectura y corpus

`docs/**/*.md` versionados en Git → secciones Markdown y líneas originales → E5 ONNX cuantizado → vectores Float32 normalizados + postings BM25 → Web Worker local → coseno y RRF → cinco fragmentos literales con citas al SHA exacto.

Se indexa el corpus publicado: 58 Markdown, 1.07 MB al inicio de esta implementación. Los archivos de planificación, código, PDF, bibliografía externa y los productos generados no son fuentes de respuestas. La selección se obtiene de `git ls-files`: detecta automáticamente adiciones, modificaciones y eliminaciones. Los documentos fuente no se reescriben. No se utiliza un LLM generativo.

Los bloques H2 conservan sus H3–H6 para no perder contexto. Se respetan front matter, títulos Setext, fences y bloques matemáticos LaTeX; los encabezados dentro de código no crean secciones. La subdivisión utiliza el tokenizer real, con máximo 512 tokens incluyendo prefijo y contexto. Una línea individual excesivamente larga provoca un error visible en CI en lugar de truncamiento silencioso. Los fragmentos son intervalos contiguos exactos de la fuente; no se inventan extractos ni se renderiza HTML de los documentos.

## Modelo y distribución

- `Xenova/multilingual-e5-small`, revisión fija en `config.json`, 384 dimensiones, ONNX `model_quantized.onnx` (q8).
- Modelo upstream `intfloat/multilingual-e5-small`, licencia MIT según su model card fijada a revisión. El despliegue incluye esa ficha y licencias Apache-2.0 de Transformers.js y MIT de ONNX Runtime.
- Transformers.js 3.8.1; dependencias exactas y transitivas bloqueadas con `package-lock.json`.
- Preprocesamiento compartido: `passage: ` para documentos, `query: ` para preguntas; mean pooling y normalización L2. Node y navegador usan el mismo ONNX WASM de un hilo. `embedding-node.mjs` utiliza el hook de inyección de runtime presente en la versión fijada de Transformers.js. Se verifica equivalencia con dos probes bilingües y las 20 preguntas de evaluación (coseno > 0.999). El primer prototipo con CPU nativo mostró discrepancias y fue descartado.
- `prepare.mjs` descarga **solo durante compilación** pesos/tokenizer de la revisión fija; valida SHA-256 contra `model-assets.lock.json`; copia JS, WASM, licencias y recursos a Pages. La ruta del modelo incluye la revisión para evitar reutilizar pesos antiguos en la caché del navegador.
- No hay CDN, inferencia remota, clave, endpoint de consultas, fuente web ni analítica en esta interfaz. Su CSP restringe conexiones a su propio origen. Los enlaces a GitHub solo navegan al seleccionarlos.
- El modelo se descarga al consultar por primera vez. El worker reutiliza la instancia y Transformers.js usa Cache Storage cuando está disponible. No hay promesa de persistencia si el navegador elimina su caché.

## Construcción y mantenimiento

Desde la raíz del repositorio, con Node 22 y las dependencias Python habituales del proyecto:

```sh
npm ci --prefix search
node search/prepare.mjs
node search/build.mjs
node search/evaluate.mjs
node --test search/test.mjs
node search/incremental-test.mjs
python scripts/generate_handbook_qa_knowledge.py
python -m mkdocs build --strict
cd search
npx playwright install --with-deps chromium
cd ..
SEARCH_SITE_ROOT=site node search/browser-test.mjs
node search/size-check.mjs
```

El workflow existente `.github/workflows/docs.yml` realiza estos pasos antes de publicar con las acciones oficiales de Pages. Un error de descarga, integridad, prueba o compilación impide el despliegue. Solo el job de despliegue recibe permisos `pages:write` e `id-token:write`; el build usa `contents:read`. Los PR se validan sin desplegar. Push a main y ejecuciones manuales despliegan tras validación.

Para reconstruir: **Actions → Build and deploy MkDocs site → Run workflow → rebuild_search = true**. Localmente: `node search/build.mjs --full` y repetir evaluación/build/pruebas. No se necesitan secretos nuevos.

La caché `.cache/semantic/` contiene embeddings por hash de contenido e identidad de modelo/preprocesamiento. También conserva fragmentos por hash de documento para evitar tokenizar documentos intactos. Se valida la dimensión, finitud y norma de cada vector reutilizado. JSON corrupto o firma incompatible provoca reconstrucción. Los documentos eliminados desaparecen del manifiesto y del índice final; el cache de salida conserva solo entradas vigentes. Un cache ausente es una optimización perdida, nunca un índice incompleto.

`retrieval-settings.json` permite desactivar `calibrateFusion` para fijar manualmente los pesos y controla BM25 (`k1`, `b`), pesos RRF, constante y candidatos. Cambiar estos parámetros no requiere nuevos embeddings. Se ejecuta `evaluate.mjs` para producir el nuevo `retrieval.json`; en un sitio estático sigue siendo necesario publicar el archivo actualizado. El navegador verifica que calibración e índice corresponden al mismo commit y firma.

Para cambiar de modelo: revisar licencia y compatibilidad, fijar revisión y archivos, actualizar hashes de `model-assets.lock.json` mediante descarga inspeccionada, reconstruir completamente y repetir equivalencia Node/WASM, calibración y evaluación. No cambiar el modelo silenciosamente ni quitar el prefijo E5.

## Evaluación y abstención

- `evaluation.json`: 20 consultas diagnósticas, incluidas 18 etiquetas revisadas del benchmark P1 existente y dos variantes (paráfrasis y formulación ambigua). 14 tienen evidencia etiquetada, seis requieren abstención.
- `calibration.json`: 12 preguntas distintas (seis respaldadas por fuentes, seis fuera de alcance). El umbral semántico maximiza exactitud balanceada en esta muestra; el peso léxico RRF se selecciona por MRR@5 documental en las seis preguntas positivas de calibración; el benchmark de 20 no se usa para ajustar ese umbral. BM25 tiene su propio umbral calibrado para comparación.
- Las solicitudes de importes privados, datos actuales externos o información ajena al manual tienen reglas explícitas de alcance. No se confunde un cosine elevado con suficiencia para calcular una reserva individual.
- Recall@5 estricto mide recuperar el fragmento que contiene el extracto de referencia. Se informa por separado Recall@5 documental, ya que un capítulo correcto no equivale a evidencia exacta. Las etiquetas no son juicios exhaustivos: otros pasajes pueden ser pertinentes. Calidad de citas significa aquí correspondencia íntegra con fuente/versión/líneas, no una revisión actuarial independiente de cada respuesta.
- `evaluate.mjs` escribe métricas por pregunta y latencias reales de Node. `browser-test.mjs` prueba WASM, navegación con prefijo, móvil, citas, abstención, ausencia de requests externos y reutilización del modelo. No se simulan métricas ni se confunde tiempo de Node con latencia móvil.
- Los tests de 20 preguntas se usaron para diagnosticar segmentación: son una evaluación exploratoria y de regresión, **no una validación independiente ciega**. La muestra es pequeña; conservar o ampliar revisión humana antes de afirmar generalización.

El mensaje de abstención es: «No encontré información suficiente en los documentos para responder esta pregunta.» La abstención automática sigue siendo imperfecta; una nueva pregunta fuera de alcance que comparta vocabulario actuarial puede superar el umbral. El resultado siempre se presenta como evidencia recuperada, nunca como asesoría particular ni respuesta sintetizada.

## Límites y costo

Las consultas no invocan servicios facturables: descargas estáticas y cómputo en el dispositivo del lector. Se utilizan runners estándar Ubuntu en un repositorio público, no larger runners. No se habilitan sobrecostos, suscripciones, bases externas ni credenciales pagas.

La primera descarga es grande: aproximadamente 160 MB entre modelo, tokenizer y runtime; el modelo q8 ocupa unos 118 MB. El sitio completo se controla con un presupuesto conservador de 900 MB. Esto cabe bajo el límite publicado de 1 GB de Pages, pero no implica capacidad ilimitada. Con 160 MB por visitante sin caché, unos 625 visitantes nuevos consumirían aproximadamente 100 GB; es una estimación sin contar otros activos ni compresión HTTP, no una cuota garantizada.

GitHub documenta 100 GB/mes de transferencia flexible, timeout de despliegue de 10 minutos y restricciones de uso comercial/SaaS. El manual educativo no procesa transacciones. GitHub puede limitar tráfico. Los runners estándar de repositorios públicos son gratuitos; cachés y artefactos tienen límites propios. No aumentar el límite de caché por encima de los 10 GB gratuitos; mantener artefactos de diagnóstico con retención corta y revisar el consumo total de la cuenta. El componente no puede garantizar la factura de otros repositorios o servicios de la cuenta.

Optimización adoptada: carga diferida, ONNX q8, caché, vectores binarios (~3–4 MB con el corpus actual) y ejecución incremental. No se eligió un modelo menor: el despliegue actual cabe en Pages y se verificó E5. Si la descarga o RAM móvil resulta inaceptable, comparar con el mismo benchmark una cuantización q4 y un modelo multilingüe menor **antes** de sustituir E5; no hay resultados medidos de esas alternativas en esta entrega. No se sustituye semántica por BM25 cuando falla el modelo: se muestra un error explícito.

## Fuentes verificadas (2026-11-10)

- [GitHub Pages: límites y condiciones](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits): tamaño, transferencia, timeout y uso permitido.
- [GitHub Actions: facturación](https://docs.github.com/en/billing/concepts/product-billing/github-actions): runners públicos gratuitos; artefactos y cachés tienen límites.
- [E5 original](https://huggingface.co/intfloat/multilingual-e5-small): MIT, prefijos, pooling, normalización y límite de tokens.
- [Conversión ONNX fijada](https://huggingface.co/Xenova/multilingual-e5-small/tree/761b726dd34fb83930e26aab4e9ac3899aa1fa78): archivos distribuidos.

Los detalles por pregunta y navegador se publican como artefacto de Actions `semantic-search-validation`, junto con el diagnóstico P1 preexistente.
