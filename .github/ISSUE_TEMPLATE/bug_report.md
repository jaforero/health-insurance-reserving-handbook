---
name: Bug report
about: Reportar un error técnico, de navegación o construcción del sitio
title: "[Bug]: "
labels: bug
assignees: ""
---

## Descripción

Describe el problema.

## Archivo o sección afectada

Indica el archivo, capítulo o URL.

## Comportamiento esperado

Describe qué debería ocurrir.

## Evidencia

Incluye salida de terminal, captura o fragmento relevante.

## Validación local

Si aplica, pega el resultado de:

```bash
python scripts/audit_docs.py
python scripts/preflight_release.py
python -m mkdocs build --strict
```

