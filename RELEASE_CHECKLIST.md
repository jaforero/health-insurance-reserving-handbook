# Release checklist

Checklist para publicar la primera versión del handbook en GitHub.

## 1. Validar estructura local

Desde la raíz del repositorio:

```bash
python scripts/audit_docs.py
python scripts/preflight_release.py
python -m mkdocs build --strict
```

Resultado esperado:

- auditoría sin issues;
- preflight sin errores;
- build de MkDocs completado.

## 2. Revisar archivos que no deben subirse

Confirmar que `.gitignore` excluye:

- `.venv/`;
- `site/`;
- `_audit/`;
- `_backups/`;
- `.DS_Store`;
- caches de Python;
- archivos temporales.

## 3. Inicializar Git local

```bash
git init
git status
git add .
git status
git commit -m "Initial public version of health insurance reserving handbook"
```

## 4. Crear repositorio en GitHub

Crear un repositorio nuevo en:

```text
https://github.com/jaforero
```

Nombre recomendado:

```text
health-insurance-reserving-handbook
```

## 5. Conectar remoto y subir

Reemplaza `NOMBRE_DEL_REPOSITORIO` por el nombre elegido:

```bash
git branch -M main
git remote add origin https://github.com/jaforero/NOMBRE_DEL_REPOSITORIO.git
git push -u origin main
```

## 6. Activar GitHub Pages

En GitHub:

1. `Settings`
2. `Pages`
3. `Build and deployment`
4. Source: `GitHub Actions`

## 7. Actualizar `site_url`

Después de confirmar el nombre del repositorio, actualizar `mkdocs.yml`:

```yaml
site_url: "https://jaforero.github.io/NOMBRE_DEL_REPOSITORIO/"
```

Luego:

```bash
python -m mkdocs build --strict
git add mkdocs.yml
git commit -m "Set GitHub Pages site URL"
git push
```

## 8. Crear tag de primera versión

```bash
git tag -a v0.1.0 -m "First public version"
git push origin v0.1.0
```

