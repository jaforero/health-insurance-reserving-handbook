# Contributing

Gracias por considerar contribuir al Health Insurance Reserving Handbook.

Este proyecto combina documentación técnica, criterios actuariales, referencias normativas y ejemplos reproducibles. Las contribuciones deben priorizar claridad, trazabilidad y consistencia metodológica.

## Tipos de contribución

Se aceptan contribuciones como:

- corrección de errores tipográficos o conceptuales;
- mejoras de redacción técnica;
- ampliación de capítulos existentes;
- nuevos ejemplos reproducibles;
- mejoras a la navegación o estructura del handbook;
- mejoras a scripts de auditoría;
- referencias bibliográficas adicionales;
- issues con observaciones metodológicas o regulatorias.

## Reglas de contenido

Antes de proponer cambios:

1. Mantén el contenido en español técnico claro.
2. Evita afirmaciones regulatorias sin fuente o sin advertir alcance.
3. Distingue entre:
   - práctica actuarial general;
   - práctica aplicable a seguros de salud;
   - particularidades del sistema colombiano;
   - criterio profesional del autor.
4. No incluyas datos confidenciales, datos personales, datos de pacientes ni información propietaria.
5. Cuando uses ejemplos numéricos, deja claro si son sintéticos.

## Validación local

Ejecuta antes de abrir un pull request:

```bash
python scripts/audit_docs.py
python scripts/preflight_release.py
python -m mkdocs build --strict
```

La contribución debe pasar sin errores.

## Convenciones para capítulos

- Un solo H1 por archivo.
- Front matter YAML al inicio de cada capítulo.
- Títulos de archivo en minúscula, con guiones.
- Prefijo numérico de capítulo cuando aplique.
- No agregar enlaces a capítulos futuros si el archivo destino aún no existe.
- Mantener la navegación en `mkdocs.yml` sincronizada con los archivos bajo `docs/`.

## Pull requests

Todo pull request debe incluir:

- resumen claro del cambio;
- archivos modificados;
- resultado de validación local;
- notas sobre cambios metodológicos, regulatorios o de alcance.

