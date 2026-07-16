---
title: "Health Insurance Reserving Handbook — Estado y continuidad"
description: "Documento de transferencia con el estado vigente, convenciones y próximos pasos del repositorio."
chapter: "project-handoff"
part: "repository"
language: "es"
status: "active"
version: "0.3.0"
last_updated: "2026-07-15"
---

# Health Insurance Reserving Handbook — Estado y continuidad

Este documento permite continuar el proyecto sin depender de inventarios o decisiones históricas ya superadas.

## 1. Repositorio y publicación

- Repositorio: <https://github.com/jaforero/health-insurance-reserving-handbook>
- Sitio: <https://actuaria.javierforero.co/>
- Rama principal: `main`
- Última versión pública: `v0.3.0`
- Estado del release: Demo 5 local publicado y validado
- Idioma principal: español
- Demos: español e inglés

## 2. Inventario vigente

| Parte | Tema | Capítulos | Cantidad |
|---:|---|---|---:|
| 1 | Fundamentos | 01–05 | 5 |
| 2 | Reservas clásicas | 06, 07 y 11–14 | 6 |
| 3 | Reservas estocásticas | 08–10 | 3 |
| 4 | Modelos estadísticos | 15–17 | 3 |
| 5 | Machine Learning | 18–20 | 3 |
| 6 | Especificidades de salud | 21–28 | 8 |
| 7 | Colombia | 29–40 | 12 |
|  | **Total** |  | **40** |

No existe actualmente una Parte 8, 9 o 10 publicada. La numeración 08–14 mantiene rutas históricas estables: no renombrar archivos de forma aislada.

## 3. Demos disponibles

### Demo 1 · Triángulos pagados simulados

```bash
python scripts/generate_demo_triangles.py
python scripts/generate_demo_triangle_visuals.py
```

Genera datos largos, triángulos incremental y acumulado, factores, ultimate, IBNR y visualizaciones.

### Demo 2 · Pagado vs. incurrido

```bash
python scripts/generate_demo_paid_incurred.py
```

Genera bases pagada e incurrida, reserva caso, factores, comparación Chain Ladder y SVG.

### Demo 3 · Triángulos mensuales pagados

```bash
python scripts/generate_demo_monthly_triangles.py
```

Genera 60 meses de origen, desarrollo mensual 0–24, factores, ultimate, IBNR, controles de suficiencia y tres visualizaciones por idioma.

### Demo 4 · Preparación de datos

Mapea campos a nombres canónicos, ejecuta controles y evalúa gates de preparación metodológica.

### Demo 5 · De datos propios a triángulos actuariales

```bash
conda env create -f environment.yml
conda activate reserving-handbook
python scripts/iniciar_asistente_triangulos.py
```

Abre una interfaz local en Streamlit para leer CSV, TXT delimitado, XLSX o Parquet, validar,
construir triángulos y exportar resultados. Este demo está en preparación para el siguiente release.

Los datos incluidos en el repositorio son sintéticos. El Demo 5 también puede procesar archivos
locales del usuario, que no deben incorporarse al control de versiones.

## 4. Validación obligatoria

Antes de integrar cambios:

```bash
rm -rf site
python scripts/audit_docs.py
python scripts/preflight_release.py
python -m unittest discover -s tests -p "test_*.py"
python -m mkdocs build --strict
```

El workflow `.github/workflows/docs.yml` ejecuta la validación y despliega GitHub Pages desde `main`.

## 5. Convenciones editoriales

- Un único H1 por documento.
- Front matter con `title`, `description`, `chapter`, `part`, `language`, `status`, `version` y `last_updated`.
- Contenido principal en español.
- Fórmulas compatibles con GitHub y MkDocs.
- Rutas de archivo estables y enlaces relativos dentro de `docs/`.
- Ejemplos numéricos reproducibles y claramente identificados como sintéticos.
- Afirmaciones regulatorias con fecha de corte y fuentes verificables.
- Métodos avanzados comparados con benchmarks actuariales transparentes.

## 6. Reglas de trabajo

- Crear una rama para demos, automatización o cambios amplios.
- Ejecutar auditorías antes del commit.
- Usar rutas explícitas con `git add`; evitar `git add .` cuando existan cambios ajenos.
- No versionar `site/`, paquetes temporales ni respaldos.
- No modificar datos generados sin ejecutar y documentar el generador correspondiente.
- No mezclar una corrección editorial con cambios metodológicos no relacionados.

## 7. Próximo hito

El objetivo recomendado es `v0.3.0`, con este orden:

1. auditoría matemática automática en CI;
2. pruebas de reproducibilidad de demos;
3. consolidar pruebas del Demo 3 mensual;
4. estabilizar y revisar el Demo 5 local con datos propios;
5. Demo 6: Chain Ladder vs. Bornhuetter-Ferguson vs. Benktander vs. Cape Cod;
6. documentación de esquemas y diccionarios de datos sintéticos;
7. changelog, citación, tag y release notes de v0.3.0.

## 8. Criterio de continuidad

La siguiente conversación o contribución debe partir del estado de `main`, revisar `CHANGELOG.md` y `docs/roadmap.md`, y confirmar que las validaciones están limpias antes de ampliar el alcance.
