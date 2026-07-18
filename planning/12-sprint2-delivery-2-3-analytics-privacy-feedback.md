# Ask the Handbook · Sprint 2.3 — Analítica agregada, privacidad y feedback

## Estado

- **Iniciativa:** Ask the Handbook
- **Entrega:** Sprint 2.3
- **Dependencias:** Sprint 2.1 y Sprint 2.2 fusionados en `main`
- **Modelo operativo:** aplicación estática ejecutada en el navegador
- **Costo incremental esperado:** USD 0
- **Fecha:** 2026-07-18

## 1. Objetivo

Cerrar Sprint 2 con una capa de observabilidad y retroalimentación que permita evaluar la utilidad del asistente sin capturar, persistir ni transmitir el texto libre escrito por el lector.

La entrega incorpora:

1. eventos agregados mediante `gtag`, únicamente cuando la función ya está disponible en el sitio;
2. una lista cerrada de eventos y parámetros;
3. sanitización antes de cualquier emisión;
4. seguimiento de apertura, sugerencias, resultados, fuentes y cierre;
5. enlace de feedback para cobertura insuficiente;
6. creación de issues sin copiar automáticamente la pregunta;
7. pruebas automáticas de privacidad y regresión.

## 2. Principio de minimización

La telemetría responde preguntas de producto, no preguntas sobre el lector.

Puede observarse:

- qué páginas abren el panel;
- cuántas interacciones usan sugerencias o texto libre;
- qué clase de cobertura devuelve el motor;
- si se consultan fuentes;
- dónde se reportan brechas editoriales.

No puede observarse:

- qué escribió el lector;
- nombres, correos o identificadores;
- datos actuariales particulares;
- reservas, siniestros o resultados privados;
- hashes o representaciones de la consulta;
- sesiones o conversaciones reconstruibles.

## 3. Contrato de eventos

| Evento | Propósito |
|---|---|
| `handbook_qa_open` | Apertura del panel |
| `handbook_qa_suggestion_selected` | Selección de pregunta editorial |
| `handbook_qa_search_submitted` | Envío de pregunta libre, sin su contenido |
| `handbook_qa_result` | Clase de cobertura obtenida |
| `handbook_qa_source_opened` | Apertura de fuente o sección relacionada |
| `handbook_qa_closed` | Cierre del panel |
| `handbook_qa_unresolved_report` | Apertura del reporte de brecha |

## 4. Allowlist de parámetros

Los únicos parámetros aceptados son:

```text
page_path
section_anchor
answer_id
coverage_class
suggestion_position
interaction_type
catalog_version
```

Cualquier otro campo se descarta antes de invocar `gtag`.

## 5. Clases de cobertura

```text
verified
probable
insufficient
out_of_scope
```

No se envían puntajes continuos, texto de respuesta ni conceptos inferidos.

## 6. Emisión tolerante a fallos

La función de analítica:

- valida el nombre del evento;
- sanitiza el payload;
- comprueba que `gtag` exista;
- captura errores del proveedor;
- devuelve un booleano;
- no afecta el resultado del asistente.

La ausencia de Google Analytics no cambia ninguna funcionalidad.

## 7. Feedback de cobertura insuficiente

Cuando el motor devuelve `insufficient`, la interfaz muestra una invitación opcional para reportar una brecha editorial.

El enlace preconfigurado incluye únicamente:

- ruta;
- anchor;
- cobertura;
- respuesta candidata, cuando exista;
- versión del catálogo.

El cuerpo aclara que la pregunta no fue incorporada y que el lector decide qué contexto compartir manualmente.

## 8. Controles de privacidad

- sin `localStorage`;
- sin `sessionStorage`;
- sin IndexedDB;
- sin cookies propias;
- sin query string que contenga la pregunta;
- sin endpoints de IA;
- sin hashes del texto;
- sin identificador persistente del lector.

## 9. Archivos

### Modificados

```text
docs/assets/javascripts/handbook-qa.js
docs/assets/stylesheets/handbook-qa.css
overrides/partials/handbook-qa-panel.html
```

### Nuevos

```text
planning/12-sprint2-delivery-2-3-analytics-privacy-feedback.md
tests/js/test_handbook_qa_privacy.js
tests/test_handbook_qa_privacy.py
```

## 10. Pruebas

Las pruebas verifican:

- allowlist exacta;
- descarte de `query`, `question`, `text`, `search_term` y correo;
- operación cuando `gtag` no existe;
- bloqueo de eventos desconocidos;
- URL de feedback sin texto libre;
- ausencia de almacenamiento;
- ausencia de endpoints de IA;
- tags de fuentes y feedback;
- preservación de las regresiones anteriores.

## 11. Validación obligatoria

```bash
python -m unittest discover -s tests -p "test_*.py"
node tests/js/test_handbook_qa_engine.js
node tests/js/test_handbook_qa_context.js
node tests/js/test_handbook_qa_panel.js
node tests/js/test_handbook_qa_privacy.js
node --check docs/assets/javascripts/handbook-qa.js
python scripts/audit_docs.py
python scripts/preflight_release.py
python -m mkdocs build --strict
git diff --check
```

## 12. Prueba manual

- abrir el panel;
- seleccionar una sugerencia;
- enviar una pregunta libre;
- abrir una fuente;
- provocar cobertura insuficiente;
- abrir el reporte de brecha;
- confirmar que el issue no contiene la pregunta;
- verificar que el panel funciona cuando `gtag` no existe;
- revisar modo oscuro y móvil.

## 13. Criterios de aceptación

- [ ] Todos los eventos pertenecen a la lista cerrada.
- [ ] Todos los parámetros pertenecen a la allowlist.
- [ ] Ningún evento contiene texto libre.
- [ ] El feedback no copia la pregunta.
- [ ] La ausencia de Analytics no rompe el panel.
- [ ] Las fuentes emiten eventos agregados.
- [ ] No se usa almacenamiento del navegador.
- [ ] Todos los tests pasan.
- [ ] Auditoría y preflight pasan.
- [ ] Build estricto pasa.
- [ ] Prueba pública satisfactoria.

## 14. Riesgos y controles

| Riesgo | Control |
|---|---|
| Captura accidental de texto | Allowlist y sanitización centralizada |
| Nueva propiedad enviada sin revisión | Campos desconocidos descartados |
| Analytics bloqueado | Emisión opcional y tolerante a fallos |
| Issue con datos sensibles | Pregunta excluida automáticamente |
| Métricas interpretadas como exactitud | Revisión editorial separada |
| Duplicación por navegación instantánea | Inicialización idempotente existente |

## 15. Bibliografía interna comentada

- `planning/09-sprint2-ask-handbook-contextual.md`: define el alcance completo y la prohibición de registrar preguntas.
- `planning/10-sprint2-delivery-2-1-context-suggestions.md`: establece contexto y ranking.
- `planning/11-sprint2-delivery-2-2-global-panel.md`: documenta el panel global y su accesibilidad.
- `docs/assets/javascripts/handbook-qa.js`: implementación ejecutable y fuente de verdad del contrato.

## 16. Checklist práctico

- [ ] Crear rama desde `main` actualizado.
- [ ] Aplicar paquete.
- [ ] Ejecutar pruebas.
- [ ] Probar issue de feedback.
- [ ] Inspeccionar Network y Analytics.
- [ ] Confirmar ausencia de texto libre.
- [ ] Commit y push.
- [ ] Abrir PR borrador.
- [ ] Revisar checks.
- [ ] Marcar listo y fusionar solo al completar la prueba pública.
