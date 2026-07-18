# Ask the Handbook · Sprint 1 — Prototipo local sin costo

## 1. Objetivo

Implementar una página aislada y funcional para **Pregúntale al Handbook** usando únicamente
archivos estáticos servidos por MkDocs y GitHub Pages.

La implementación conserva las restricciones del Sprint 0:

- sin modelos generativos;
- sin consumo de tokens;
- sin APIs externas;
- sin backend;
- sin embeddings ni base vectorial;
- sin almacenamiento de preguntas;
- sin carga de archivos del usuario.

## 2. Entregables

```text
docs/ask-the-handbook.md
docs/assets/data/handbook-qa-catalog.json
docs/assets/data/handbook-section-index.json
docs/assets/javascripts/handbook-qa.js
docs/assets/stylesheets/handbook-qa.css
tests/test_handbook_qa.py
tests/js/test_handbook_qa_engine.js
```

`mkdocs.yml` registra la página, la hoja de estilo y el motor JavaScript.

## 3. Cobertura editorial

El catálogo inicial contiene 15 respuestas sobre:

1. deduplicación;
2. identificación de duplicados técnicos;
3. llave económica y archivo fuente;
4. rezagos negativos;
5. importes negativos;
6. incrementales y acumulados;
7. madurez;
8. elegibilidad de Chain Ladder;
9. efecto de duplicados en factores;
10. historia mensual;
11. riesgos de Chain Ladder;
12. independencia del prior BF;
13. diferencia entre CL y BF;
14. aporte de Benktander;
15. alcance profesional de los demos.

Cada respuesta contiene explicación directa, relevancia actuarial, ejemplo, advertencia, fuentes y
preguntas relacionadas.

## 4. Motor de recuperación

El motor normaliza tildes y signos, elimina palabras funcionales, tolera un error ortográfico leve,
expande grupos editoriales de sinónimos y combina cuatro componentes:

\[
S(q,d)
=
0.35S_{terminos}
+
0.25S_{sinonimos}
+
0.15S_{contexto}
+
0.25S_{pregunta}.
\]

Los estados implementados son:

| Estado | Regla inicial | Comportamiento |
|---|---:|---|
| Respuesta verificada | coincidencia exacta o \(S\geq0.78\) | respuesta completa |
| Coincidencia probable | \(0.52\leq S<0.78\) | respuesta con advertencia |
| Cobertura insuficiente | \(S<0.52\) | solo secciones relacionadas |
| Fuera de alcance | patrón bloqueado | abstención explícita |

Los umbrales siguen siendo parámetros experimentales y deben revisarse con preguntas reales.

## 5. Seguridad y privacidad

La pregunta permanece en el navegador. El motor solo realiza `fetch` de dos archivos JSON del
mismo sitio. No existe endpoint público, clave API, cookie propia, persistencia ni telemetría de
contenido.

Las solicitudes de cálculo particular, interpretación regulatoria específica, omisión de fuentes o
búsqueda externa activan una respuesta de abstención.

## 6. Accesibilidad

La página incluye:

- formulario operable por teclado;
- etiqueta vinculada al campo;
- foco visible;
- región de resultados con `aria-live`;
- estados expresados mediante texto y no solo color;
- diseño adaptable a móvil;
- respeto por `prefers-reduced-motion`;
- alternativa `noscript`.

## 7. Pruebas

`tests/test_handbook_qa.py` valida:

- estructura y unicidad del catálogo;
- campos editoriales obligatorios;
- relaciones internas;
- existencia de rutas y anchors;
- ausencia de endpoints de IA;
- presupuestos de tamaño;
- contrato de la página;
- registro en MkDocs;
- ejecución de la regresión JavaScript mediante Node.js.

`tests/js/test_handbook_qa_engine.js` valida las 15 preguntas canónicas, todas sus variantes,
errores ortográficos leves, consultas fuera de alcance, abstención y construcción de enlaces.

## 8. Criterios de salida

El Sprint 1 puede cerrarse cuando terminen correctamente:

```bash
python -m unittest discover -s tests -p "test_*.py"
python scripts/audit_docs.py
python scripts/preflight_release.py
python -m mkdocs build --strict
git diff --check
```

Además, la página debe probarse manualmente en vista de escritorio, móvil y modos claro y oscuro.

## 9. Riesgos pendientes

- El catálogo todavía tiene cobertura limitada.
- La similitud léxica no comprende razonamiento nuevo.
- Los umbrales pueden producir falsos positivos o abstenciones excesivas.
- Los anchors deben permanecer sincronizados con los capítulos.
- La incorporación futura de analítica de preguntas requerirá una decisión explícita de privacidad.

## 10. Decisión para Sprint 2

Sprint 2 debería integrar un botón contextual únicamente después de revisar la precisión de la página
aislada. La integración global no debe preceder a la calibración del motor ni a la prueba de
accesibilidad.
