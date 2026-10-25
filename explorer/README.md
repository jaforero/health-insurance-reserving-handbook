# Explorador de conocimiento

Un explorador al estilo Obsidian para el **Health Insurance Reserving Handbook**. Convierte las notas Markdown de `docs/` en una base de conocimiento navegable: lista de notas, nota abierta con fórmulas renderizadas, grafo de relaciones y backlinks.

Se publica junto al sitio en **`https://actuaria.javierforero.co/explorador/`** y se regenera solo en cada despliegue.

---

## Espacio de investigación

El explorador abre con el grafo como vista principal. La cabecera mantiene la identidad del Handbook, IgraSans y el acceso al manual.

- **Grafo / Grafo + lectura / Lectura:** vistas con atajos `G`, `D` y `L`. En móvil, la vista dividida abre la lectura a ancho completo.
- **Ficha de nota:** seleccionar un nodo muestra título, descripción y número de notas entrantes/salientes; permite leer, consultar referencias o explorar sus vecinos.
- **Índice, filtros y calidad bajo demanda:** dejan el espacio principal al grafo. `Escape` cierra los paneles; `/` busca. Restablecer muestra todos los idiomas y tipos de enlace.
- **Enlace compartible:** `?note=ruta.md&view=graph` abre una nota publicada; «Copiar enlace» conserva la nota y la vista. Las carpetas locales no se comparten mediante URL.
- **Accesibilidad:** nodos activables con Enter/Espacio, controles de zoom, movimiento reducido y temas ES/EN claro/oscuro.

La ficha cuenta notas distintas en todo el corpus; el grafo aplica el filtro de idioma y tipos activos. Sus conexiones agrupan referencias entre pares de notas, por lo que no equivalen al total de referencias documentales.

## Qué hace

**Para quien visita el sitio**

- **Grafo global.** Cada nota es un nodo, coloreado por parte del manual y con tamaño según cuántas notas la enlazan. Las dos notas eje (portada y guía de metodologías) aparecen como rombos fijos encima del grafo, para que no lo colapsen.
- **Grafo local.** Muestra la nota abierta y sus vecinas hasta 2 saltos.
- **Filtros.** Por tipo de enlace (texto, prerrequisito, relacionado, traducción), estado, etiqueta e idioma. La búsqueda resalta las coincidencias en la lista y en el grafo.
- **Nota abierta.** Markdown renderizado con fórmulas LaTeX, tablas, admoniciones, diagramas Mermaid e imágenes. El frontmatter aparece como propiedades. Los enlaces internos abren la nota destino y el botón «Ver en el manual» lleva a la página publicada.
- **Enlaces de esta nota.** Lista las notas que enlazan aquí, con la frase donde aparece cada enlace, y las notas a las que esta enlaza.
- **Salud de la bóveda.** Lista las notas huérfanas y los enlaces rotos.
- **«Abrir tu carpeta».** Un investigador elige una carpeta propia de archivos `.md` y el explorador la reconstruye con las mismas reglas. Sus archivos se procesan en su navegador y no se suben a ningún servidor.
- **Idiomas.** La interfaz está en español, con un botón para pasarla a inglés. Las notas que tienen versión en otro idioma muestran «Leer en English».

**Para ti, como mantenedor**

- **Sin pasos manuales.** Cada `mkdocs build` vuelve a generar el explorador con las notas actuales. Si agregas, renombras o enlazas notas, el grafo se actualiza solo.
- **Control de calidad opcional.** Un paso de CI hace fallar el despliegue si aparece un enlace roto, una imagen faltante o una nota huérfana, e indica el archivo exacto.

---

## Qué hay en este paquete

```
explorador-conocimiento/
├── README.md                  este archivo
├── hooks/
│   └── explorer.py            se ejecuta durante el build de MkDocs y genera explorador/
├── explorer/
│   ├── template.html          estructura y estilos de la página
│   ├── app.js                 la interfaz: grafo, nota, backlinks, filtros, «Abrir tu carpeta»
│   ├── vault-parser.js        el analizador de notas y enlaces (lo usan el navegador y el CI)
│   └── check_vault.js         revisión de enlaces para CI (opcional)
└── tests/
    └── test_explorer.py       6 pruebas en el mismo estilo unittest de tu repo
```

---

## Instalación (unos 10 minutos)

### 1. Copia las carpetas a la raíz del repo

En `health-insurance-reserving-handbook/`:

- `hooks/` → `hooks/` (carpeta nueva)
- `explorer/` → `explorer/` (carpeta nueva)
- `tests/test_explorer.py` → `tests/test_explorer.py`
- este `README.md` → `explorer/README.md`

Ninguno de estos archivos va dentro de `docs/`. El explorador se genera durante el build y no toca tus notas.

### 2. Edita `mkdocs.yml`

Agrega estas líneas **antes** de `plugins:`:

```yaml
hooks:
  - hooks/explorer.py

watch:
  - explorer
```

`hooks` activa el generador. `watch` hace que `mkdocs serve` recargue cuando cambias algo en `explorer/`.

Agrega la entrada al menú dentro de `nav:`. Por ejemplo, después de «Pregúntale al Handbook»:

```yaml
nav:
  - Inicio: index.md
  - Pregúntale al Handbook: ask-the-handbook.md
  - Explorador de conocimiento: explorador/index.html
```

### 3. Agrega `node_modules/` a `.gitignore`

Solo es necesario si vas a usar el control de calidad (paso 5) en tu computador:

```
node_modules/
```

### 4. Prueba en tu computador

```bash
python -m unittest discover -s tests -p "test_*.py"
python -m mkdocs build --strict
python -m mkdocs serve
```

Abre `http://127.0.0.1:8000/explorador/`, o entra desde el menú.

> Abre siempre la página desde `mkdocs serve` o desde el sitio publicado. Si haces doble clic en `site/explorador/index.html`, el navegador bloquea la lectura de `vault.json` y la página lo indica con un mensaje.

### 5. (Opcional, recomendado) Control de calidad en CI

En `.github/workflows/docs.yml`, agrega este paso **después de «Audit documentation» y antes de «Build MkDocs site»**:

```yaml
      - name: Check knowledge graph
        run: |
          npm install --no-save js-yaml@4.1.0
          node explorer/check_vault.js docs
```

Los runners de GitHub ya traen Node, así que no hace falta otro paso de instalación.

- Si quieres que fallen solo los enlaces rotos y no las notas huérfanas, usa `node explorer/check_vault.js docs --allow-orphans`.
- Puedes correr lo mismo en tu computador antes de hacer push.

### 6. Commit y push

```bash
git add hooks/ explorer/ tests/test_explorer.py mkdocs.yml .gitignore .github/workflows/docs.yml
git commit -m "feat: explorador de conocimiento con grafo de notas"
git push
```

El workflow existente construye y publica el sitio. El explorador queda en `/explorador/`.

---

## Cómo funciona

```
mkdocs build
   │
   ├─ hooks/explorer.py (evento on_files)
   │     ├─ lee todas las notas .md de docs/
   │     ├─ escribe  explorador/vault.json    texto de las notas + URL publicada de cada una
   │     └─ escribe  explorador/index.html    template.html + vault-parser.js + app.js
   │
   └─ el sitio se publica con lo demás

En el navegador del visitante
   index.html carga vault.json → vault-parser.js encuentra notas y enlaces → app.js dibuja todo
```

El análisis no se hace en Python sino en `vault-parser.js`. Ese mismo archivo lo usan el sitio, «Abrir tu carpeta» y el control de CI, así que las tres partes siguen siempre las mismas reglas.

### Reglas de análisis

Todo sale del texto de los archivos. No hay nada inferido.

- **Notas.** Cada archivo `.md`. Del frontmatter se toman `title`, `part`, `chapter`, `status`, `tags` y `language`. Si una nota no tiene `title`, se usa su primer `# Título`; si tampoco lo tiene, el nombre del archivo.
- **Enlaces.** Cada fuente queda como un tipo de enlace propio:
  - **Texto:** enlaces Markdown `[texto](ruta.md)` y `[texto](ruta.md#seccion)`.
  - **Wikilink:** `[[nota]]`, `[[nota|alias]]`, `[[nota#sección]]`.
  - **Prerrequisito:** el campo `prerequisites` del frontmatter.
  - **Relacionado:** el campo `related_chapters` del frontmatter.
  - **Traducción:** un enlace en una línea que empieza con `**Idioma:**` o `**Language:**`, como en tus demos 01–03.
- **Resolución de rutas.** Cada ruta se busca primero relativa a la nota. Si no existe, se busca relativa a `docs/` y se marca como «root-relative». Los wikilinks además buscan un nombre de archivo único en toda la carpeta, igual que Obsidian. Lo que no aparece queda como «roto».
- **Bloques de código.** Los enlaces dentro de bloques de código se ignoran.
- **Normalización solo para colores y filtros.** `part` se normaliza (por ejemplo, `Repository Governance` → `repository-governance`) y `status` se pasa a minúsculas. Las propiedades de cada nota muestran el valor original tal como está escrito.

---

## Configuración

Todo está al inicio de `hooks/explorer.py`:

| Constante | Para qué sirve |
|---|---|
| `OUTPUT_DIR` | Carpeta y URL del explorador (por defecto `explorador`) |
| `VAULT_NAME` | Nombre en la barra superior |
| `HUBS` | Notas eje que se fijan encima del grafo. Si renombras una, `test_hubs_exist` te avisa |
| `DEFAULT_LANG` | Idioma de notas que se muestra al abrir (`es`) |
| `GROUP_LABELS` | Nombre visible de cada parte, en español e inglés |
| `BRAND_FONT` | Ruta de la fuente IgraSans dentro de `docs/` |

**Mantenimiento habitual**

- **Nota nueva o enlace nuevo:** no tienes que hacer nada.
- **Parte nueva del manual** (por ejemplo `part-08-...`): agrega su nombre a `GROUP_LABELS`. Si no lo haces, el explorador muestra un nombre generado a partir de la carpeta.
- **Cambio de nota eje:** edita `HUBS`.

---

## Requisitos y límites

- **MkDocs 1.6 o superior.** Tu `requirements.txt` ya lo exige.
- **No agrega dependencias de Python.** Node solo hace falta para el control de CI opcional.
- **Internet en el navegador.** Las librerías (d3 7.9.0, marked 12.0.2, js-yaml 4.1.0, MathJax 3.2.2 y Mermaid 10.9.1) se cargan desde jsDelivr con versión fija, igual que hoy tu sitio carga MathJax y Mermaid. Sin conexión, la página no funciona.
- **Peso.** `index.html` pesa unos 110 KB. `vault.json` pesa unos 1,1 MB y GitHub Pages lo sirve comprimido. Las imágenes no se duplican: el explorador usa las que el sitio ya publica.
- **«Elegir carpeta».** Funciona en Chrome, Edge, Firefox y Safari de escritorio. En el celular está «Elegir archivos .md», que avisa que se pierde la estructura de subcarpetas. Arrastrar una carpeta sobre la página funciona en todos los navegadores de escritorio.
- **Privacidad.** Los archivos que un visitante abre con «Abrir tu carpeta» nunca salen de su navegador. La página no envía datos a ningún servidor.

---

## Verificación declarada por el paquete original

Probado sobre una copia de tu repo en el commit `e50612b`, con este paquete instalado:

- `python -m mkdocs build --strict`: termina sin errores. La entrada del menú enlaza a `explorador/`.
- `python -m unittest discover -s tests`: 100 pruebas OK (tus 94 más las 6 nuevas).
- `scripts/audit_docs.py` y `scripts/preflight_release.py`: sin problemas.
- `node explorer/check_vault.js docs`: 58 notas, 375 enlaces, 0 rotos, 0 huérfanas, 16 imágenes encontradas. Al romper un enlace a propósito, el paso falla con código 1 y señala el archivo.
- En Chromium, sirviendo el sitio construido:
  - el explorador abre desde el menú y las 16 fórmulas de Chain Ladder se renderizan;
  - la fuente de marca y las imágenes cargan desde el sitio;
  - «Ver en el manual» lleva a la página correcta.

---

## Solución de problemas

| Síntoma | Causa y solución |
|---|---|
| `/explorador/` da 404 | Falta `hooks: - hooks/explorer.py` en `mkdocs.yml` |
| `no contiene el marcador /*__...*/` al construir | `explorer/template.html` quedó incompleto o se editó un marcador; vuelve a copiarlo |
| La página dice que no pudo cargar las notas | Se abrió como archivo local; usa `mkdocs serve` o el sitio publicado |
| Las fórmulas se ven como LaTeX | El navegador no pudo cargar MathJax desde jsDelivr (red o bloqueador) |
| `test_hubs_exist` falla | Renombraste o moviste una nota eje; actualiza `HUBS` |
| El CI falla en «Check knowledge graph» | Hay un enlace roto, una imagen faltante o una nota huérfana; el log indica el archivo |

---

## Si lo instalas con Claude Code

Puedes pedírselo así, con este paquete descomprimido junto al repo:

> Integra el paquete `explorador-conocimiento/` en este repo siguiendo su README: copia `hooks/`, `explorer/` y `tests/test_explorer.py`; agrega `hooks`, `watch` y la entrada «Explorador de conocimiento» en `mkdocs.yml`; agrega `node_modules/` a `.gitignore` y el paso «Check knowledge graph» en `.github/workflows/docs.yml`. Luego corre los tests, `mkdocs build --strict` y `node explorer/check_vault.js docs`, y muéstrame el diff antes de hacer commit.

---

Licencia: MIT, la misma del repositorio.

## Integración mantenida en este repositorio

El hook incluye solo archivos publicables según MkDocs (`is_included`): excluye
`exclude_docs` y `draft_docs`, y conserva las páginas publicadas fuera del menú.
El estado editorial del frontmatter se muestra como filtro, no decide la publicación.
El CI revisa tanto `docs/` como el `vault.json` generado antes de subir el artefacto.
Una página abierta conserva su instantánea: al recargar obtiene el último despliegue
publicado mediante una petición con revalidación de caché. No hay sondeo en tiempo real.

El lector limpia el HTML con DOMPurify 3.3.1 antes de insertarlo en el documento.
IgraSans se carga desde los recursos del manual; se eliminaron las fuentes de Google.
Las bibliotecas JavaScript siguen requiriendo acceso a jsDelivr.

Comprobaciones adicionales:

```bash
python -m unittest discover -s tests -p 'test_*.py'
python -m mkdocs build --strict
node explorer/check_vault.js site/explorador/vault.json
```

Las pruebas del hook comprueban también exclusiones y regeneración tras añadir,
editar o eliminar notas. Los enlaces representan referencias explícitas, no similitud
semántica calculada ni evidencia de causalidad.

La integración añade 8 pruebas Python (102 totales en la versión integrada) y
`tests/js/test_explorer_ui.js`, ejecutado en CI con jsdom. Comprueba carga,
navegación, marcado matemático, enlaces, búsqueda, grafo local, idioma, tema
y limpieza de HTML. MathJax y Mermaid se simulan en este test: no valida su
representación visual. La revisión visual en navegador queda como comprobación
manual; jsdom no evalúa layout ni sustituye Chromium.
