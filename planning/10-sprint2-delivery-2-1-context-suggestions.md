# Ask the Handbook · Sprint 2.1 — Contexto y sugerencias

## 1. Objetivo

Implementar la primera entrega funcional del Sprint 2 sin activar todavía el botón global ni el panel contextual. Esta entrega amplía el motor local de Sprint 1 para que pueda:

- normalizar rutas publicadas por MkDocs;
- identificar la parte temática de la página;
- utilizar ruta, anchor, título y heading como señales de contexto;
- seleccionar entre tres y cinco preguntas editoriales pertinentes;
- mantener la consulta escrita por el lector como evidencia principal;
- abrir una respuesta editorial directamente por identificador;
- conservar abstención y bloqueo de consultas fuera de alcance.

El costo operativo incremental continúa siendo **USD 0**. La implementación no incorpora modelos generativos, APIs de IA, embeddings, base vectorial, backend ni persistencia.

## 2. Alcance implementado

### 2.1 Contrato contextual del catálogo

Cada respuesta editorial incorpora el objeto `contexts`:

```json
{
  "paths": ["/examples/04-demo-preparacion-datos/"],
  "anchors": ["deduplicacion"],
  "parts": ["examples"],
  "tags": ["deduplicacion", "calidad-de-datos"],
  "priority": 1.0
}
```

Los campos tienen funciones diferentes:

| Campo | Función |
|---|---|
| `paths` | páginas donde la pregunta es directamente pertinente |
| `anchors` | secciones donde debe recibir mayor prioridad |
| `parts` | afinidad temática amplia |
| `tags` | conceptos contextuales para comparación con título y heading |
| `priority` | desempate editorial entre preguntas igualmente pertinentes |
| `general` | identifica una pregunta apta como respaldo general |

Las fuentes continúan siendo la evidencia de la respuesta. `contexts` solo afecta el ranking y las sugerencias.

## 3. Normalización de rutas

La función `normalizePath` convierte variantes equivalentes en una ruta canónica.

Ejemplo:

```text
https://actuaria.javierforero.co/examples/04-demo-preparacion-datos/index.html?x=1#deduplicacion
```

se convierte en:

```text
/examples/04-demo-preparacion-datos/
```

La normalización:

1. retira dominio, query string y fragmento;
2. decodifica caracteres cuando es posible;
3. reemplaza barras invertidas;
4. colapsa barras repetidas;
5. elimina `index.html`;
6. transforma rutas Markdown a rutas renderizadas;
7. garantiza barra inicial y final.

La función `renderedPath` transforma una fuente del repositorio en la ruta pública esperada.

## 4. Contexto de página y sección

El puntaje contextual se separa en dos componentes.

### 4.1 Página


definimos:

\[
S_{página}(d,c) \in [0,1]
\]

con la siguiente jerarquía:

| Relación | Puntaje |
|---|---:|
| ruta exacta | 1,00 |
| misma parte temática | 0,55 |
| afinidad por tags | hasta 0,35 |
| sin relación | 0,00 |

### 4.2 Sección

\[
S_{sección}(d,c) \in [0,1]
\]

| Relación | Puntaje |
|---|---:|
| anchor exacto | 1,00 |
| heading equivalente | 0,90 |
| afinidad por tags | hasta 0,60 |
| página relacionada sin sección exacta | 0,30 |
| sin relación | 0,00 |

El contexto combinado se conserva como diagnóstico, pero el ranking utiliza página y sección por separado.

## 5. Ranking contextual

La puntuación de una respuesta candidata es:

\[
S(q,d,c)
=
0.30S_{términos}
+0.20S_{sinónimos}
+0.20S_{pregunta}
+0.20S_{página}
+0.10S_{sección}.
\]

La modificación redistribuye el 15% contextual de Sprint 1 y hace explícitas las señales de página y sección.

### 5.1 Evidencia léxica mínima

El contexto no puede producir por sí solo una respuesta completa. Se exige:

\[
S_{términos}>0
\quad\text{o}\quad
S_{sinónimos}>0
\quad\text{o}\quad
S_{pregunta}\geq0.40.
\]

Una pregunta sin contenido actuarial pertinente permanece en `Cobertura insuficiente`, aunque se formule desde una página altamente relacionada.

### 5.2 Umbrales

La recalibración conserva:

| Estado | Regla |
|---|---|
| `Respuesta verificada` | coincidencia exacta o puntaje ≥ 0,78 |
| `Coincidencia probable` | puntaje ≥ 0,48 con evidencia léxica |
| `Cobertura insuficiente` | puntaje inferior o sin evidencia léxica |
| `Fuera de alcance` | patrón bloqueado antes del ranking |

El umbral probable se ajusta de 0,52 a 0,48 porque el peso no contextual disminuyó de 0,85 a 0,70. Las pruebas de regresión confirman que las consultas previamente aceptadas conservan su clasificación.

## 6. Selección de sugerencias

La puntuación de sugerencia es:

\[
S_{sugerencia}(d,c)
=
0.65S_{página}
+0.25S_{sección}
+0.10P_{editorial}.
\]

Las sugerencias:

- se limitan a cinco;
- no repiten identificadores;
- favorecen diversidad mediante el primer tag contextual;
- solo incluyen respuestas con relación de página o sección;
- usan preguntas generales únicamente cuando no existe cobertura contextual;
- mantienen una selección amplia en la página aislada `/ask-the-handbook/`.

Ejemplo esperado en Demo 4, sección Deduplicación:

1. ¿Por qué es necesario deduplicar los movimientos?
2. ¿Cómo sé si dos filas repetidas son realmente duplicados?
3. ¿Por qué `archivo_fuente` no debe formar parte de la llave económica?

## 7. Selección directa por identificador

La función `answerById` permite que una sugerencia editorial abra la respuesta correcta sin reinterpretar su texto.

Esta distinción es importante:

- una pregunta libre debe pasar ranking y umbrales;
- una sugerencia fue seleccionada previamente por el motor contextual y puede recuperar su entrada canónica por `id`.

Un identificador inexistente produce `Cobertura insuficiente` y no una excepción no controlada.

## 8. Detección del heading activo

`detectActiveHeading` recibe una colección ordenable de headings con posición vertical y selecciona:

1. el último heading ubicado antes del umbral visual; o
2. el primer heading cuando ninguno ha cruzado el umbral.

La función es independiente del DOM y puede probarse con datos sintéticos. La adaptación del navegador obtiene los headings visibles y entrega sus posiciones.

La gestión completa del panel y la actualización continua del contexto durante scroll pertenecen a la Entrega 2.2.

## 9. Índice de secciones

Cada sección añade:

- `part`;
- `rendered_path`;
- `tags`.

Ejemplo:

```json
{
  "path": "part-02-classical-reserving/06-chain-ladder-method.md",
  "rendered_path": "/part-02-classical-reserving/06-chain-ladder-method/",
  "part": "part-02-classical-reserving"
}
```

Esto evita recalcular repetidamente la ruta pública y facilita pruebas de consistencia.

## 10. Pruebas implementadas

### 10.1 JavaScript

`tests/js/test_handbook_qa_context.js` verifica:

- normalización de URL completa;
- equivalencia de `.md` e `index.html`;
- normalización de anchors;
- orden de sugerencias en Demo 4;
- prioridad de Chain Ladder, BF y Benktander;
- preservación de una pregunta exacta aun desde otra página;
- abstención frente a contenido desconocido;
- bloqueo de consultas particulares;
- selección por identificador;
- detección de heading;
- ausencia de duplicados;
- límite de cinco sugerencias;
- respaldo general en páginas sin cobertura;
- funcionamiento de la página aislada.

### 10.2 Python

`tests/test_handbook_qa_context.py` verifica:

- versión `1.1.0` del catálogo e índice;
- presencia y rango de todos los metadatos contextuales;
- existencia de rutas;
- existencia de anchors;
- metadatos renderizados del índice;
- exportación del contrato JavaScript;
- regla de evidencia léxica;
- ejecución del conjunto JavaScript contextual.

## 11. Riesgos controlados

| Riesgo | Control incorporado |
|---|---|
| el contexto domina una consulta irrelevante | evidencia léxica mínima |
| sugerencias repetitivas | diversidad por tag e identificador único |
| ruta con formatos diferentes | normalización canónica |
| anchor con tildes | normalización separada de texto y anchor |
| sugerencia inexistente | selección segura por identificador |
| ruptura de Sprint 1 | ejecución conjunta de regresión anterior y nueva |
| cobertura ficticia en páginas no modeladas | solo preguntas generales como respaldo |

## 12. Fuera de alcance de esta entrega

No se implementa todavía:

- botón flotante global;
- partial HTML;
- diálogo modal;
- ciclo de foco;
- cierre con `Escape`;
- eventos de Analytics;
- reporte de pregunta no resuelta;
- actualización dinámica por scroll;
- integración pública en todas las páginas.

Estos elementos pertenecen a las Entregas 2.2 y 2.3.

## 13. Validación requerida

```bash
python -m unittest discover -s tests -p "test_*.py"
node tests/js/test_handbook_qa_engine.js
node tests/js/test_handbook_qa_context.js
python scripts/audit_docs.py
python scripts/preflight_release.py
python -m mkdocs build --strict
git diff --check
```

## 14. Criterios de aceptación

- [x] Todas las respuestas tienen metadatos contextuales.
- [x] Las rutas se normalizan de forma determinística.
- [x] Página y sección tienen puntajes separados.
- [x] El contexto no sustituye evidencia léxica.
- [x] Demo 4 prioriza las tres preguntas de deduplicación esperadas.
- [x] Chain Ladder prioriza supuestos y elegibilidad.
- [x] BF prioriza independencia del prior.
- [x] Benktander prioriza su explicación metodológica.
- [x] Una consulta desconocida conserva abstención.
- [x] Una consulta fuera de alcance conserva bloqueo.
- [x] La página aislada conserva sugerencias.
- [x] Los tests de Sprint 1 siguen pasando.
- [ ] Auditoría del repositorio completo aprobada.
- [ ] Preflight del repositorio completo aprobado.
- [ ] Build estricto del repositorio completo aprobado.
- [ ] PR de Entrega 2.1 revisado.

## 15. Bibliografía y referencias comentadas

- `planning/09-sprint2-ask-handbook-contextual.md`: especifica la arquitectura contextual, los pesos, la privacidad y la secuencia de entregas.
- `planning/08-sprint1-ask-handbook-zero-cost.md`: fija el contrato editorial y la arquitectura local sobre la que se construye esta entrega.
- `docs/assets/data/handbook-qa-catalog.json`: fuente canónica de preguntas, respuestas y nuevos contextos.
- `docs/assets/data/handbook-section-index.json`: inventario canónico de secciones y rutas publicadas.
- `docs/assets/javascripts/handbook-qa.js`: implementación reproducible del ranking, abstención y selección contextual.
- `tests/js/test_handbook_qa_engine.js`: regresión del comportamiento de Sprint 1.
- `tests/js/test_handbook_qa_context.js`: especificación ejecutable del nuevo comportamiento contextual.
- `tests/test_handbook_qa.py` y `tests/test_handbook_qa_context.py`: controles estructurales, editoriales y de integración.

## 16. Checklist práctico para Entrega 2.2

Antes de crear el panel global:

- [ ] fusionar o aprobar la Entrega 2.1;
- [ ] confirmar todos los checks remotos en verde;
- [ ] probar sugerencias desde la página aislada con contexto simulado;
- [ ] definir el partial semántico del diálogo;
- [ ] definir el punto de montaje en `overrides/main.html`;
- [ ] diseñar gestión de foco y `Escape` antes de estilos;
- [ ] definir degradación segura cuando falle un JSON;
- [ ] mantener el panel desactivado hasta completar pruebas de accesibilidad.
