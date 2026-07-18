# Ask the Handbook · Sprint 1 — Prototipo funcional sin costo

## 1. Objetivo

Implementar una prueba pública y aislada de **Pregúntale al Handbook** sobre MkDocs y GitHub Pages, manteniendo las restricciones aprobadas en Sprint 0:

- costo operativo incremental esperado de USD 0;
- cero consumo de tokens;
- cero APIs de IA;
- cero backend;
- procesamiento local en el navegador;
- respuestas editoriales y fuentes verificables;
- abstención explícita fuera del alcance.

## 2. Alcance entregado

El Sprint 1 incorpora:

1. una página demostrativa navegable;
2. un catálogo editorial con 15 preguntas;
3. un índice estático de 15 secciones;
4. normalización local de consultas;
5. coincidencia exacta, por variantes y con error ortográfico leve;
6. puntuación por términos, conceptos, pregunta y contexto;
7. tres estados cualitativos de cobertura;
8. respuestas con explicación, ejemplo, advertencia y fuentes;
9. consultas relacionadas;
10. abstención ante cálculos, regulación específica y prompt injection;
11. estilos responsivos para modos claro y oscuro;
12. pruebas automáticas del contrato estático.

## 3. Archivos

```text
docs/
├── ask-the-handbook.md
├── assets/data/
│   ├── handbook-qa-catalog.json
│   └── handbook-section-index.json
├── javascripts/
│   └── handbook-qa.js
└── stylesheets/
    └── handbook-qa.css

tests/
└── test_ask_handbook_static.py
```

Además, `mkdocs.yml` registra la página, JavaScript y CSS.

## 4. Recorrido de usuario

1. abrir `Pregúntale al Handbook — MVP`;
2. escribir una pregunta o seleccionar un ejemplo;
3. procesar la consulta localmente;
4. recibir:
   - respuesta verificada;
   - coincidencia probable; o
   - cobertura insuficiente;
5. navegar a las fuentes;
6. explorar preguntas relacionadas;
7. limpiar la consulta.

## 5. Motor de recuperación

La versión inicial utiliza:

- normalización de mayúsculas, tildes, signos y espacios;
- eliminación limitada de palabras funcionales;
- conservación de términos actuariales;
- coincidencia difusa para errores leves;
- comparación contra pregunta canónica, variantes y conceptos;
- contexto opcional de ruta y etiquetas.

La puntuación conserva la especificación del Sprint 0:

\[
S(q,d)=0.35S_{términos}+0.25S_{sinónimos}+0.15S_{contexto}+0.25S_{pregunta}.
\]

Las coincidencias exactas con una pregunta canónica o variante reciben puntuación 1.

## 6. Umbrales

| Puntaje | Resultado |
|---:|---|
| `S ≥ 0.80` | Respuesta verificada |
| `0.55 ≤ S < 0.80` | Coincidencia probable |
| `S < 0.55` | Cobertura insuficiente y secciones relacionadas |

Los umbrales siguen siendo hipótesis del MVP y deberán calibrarse con consultas reales.

## 7. Abstención

El motor bloquea respuestas aparentes para consultas como:

- reserva exacta de una entidad;
- cálculo de IBNR sin datos;
- metodología exigida por regulación específica;
- método universalmente superior;
- instrucciones para ignorar fuentes;
- solicitud de búsqueda abierta en Internet.

La respuesta informa que se requieren propósito, datos, obligaciones, contratos, regulación aplicable y fecha de valoración.

## 8. Pruebas

`tests/test_ask_handbook_static.py` valida:

- 15 respuestas editoriales;
- identificadores únicos;
- campos obligatorios;
- fechas y versiones;
- relaciones válidas;
- existencia de documentos y anchors;
- resolución de preguntas de referencia;
- tolerancia a un error ortográfico leve;
- límites de tamaño;
- ausencia de endpoints de IA o secretos;
- declaración de procesamiento local en la página.

## 9. Criterios de aceptación

- [ ] el build estricto de MkDocs finaliza correctamente;
- [ ] todos los tests terminan correctamente;
- [ ] las cinco preguntas de demostración recuperan la respuesta esperada;
- [ ] la consulta fuera de alcance produce abstención;
- [ ] todas las fuentes navegan al anchor correcto;
- [ ] no existen solicitudes de red fuera de los dos archivos JSON estáticos;
- [ ] la interfaz funciona con teclado y en viewport móvil;
- [ ] el JavaScript permanece por debajo de 100 KB;
- [ ] cada índice permanece por debajo de 500 KB.

## 10. Fuera de alcance

- botón flotante global;
- detección automática del encabezado visible;
- historial conversacional;
- persistencia de feedback;
- analítica del texto de preguntas;
- embeddings locales;
- modelos generativos;
- documentos cargados por usuarios;
- soporte bilingüe;
- cobertura completa de los 40 capítulos.

## 11. Riesgos observables

### Falso positivo léxico

Una pregunta ambigua puede coincidir con una respuesta cercana pero incorrecta.

**Control:** umbral probable, advertencia visible y fuentes obligatorias.

### Falsa percepción de inteligencia generativa

El usuario puede asumir que el sistema crea respuestas dinámicas.

**Control:** aviso explícito de respuestas editoriales y procesamiento local.

### Cobertura inicial limitada

Quince preguntas no cubren todo el handbook.

**Control:** abstención y secciones relacionadas; expansión basada en evidencia de uso.

### Deriva editorial

Un capítulo puede cambiar sin actualizar el catálogo.

**Control:** pruebas automáticas de rutas y anchors; revisión de versión y fecha.

## 12. Decisión para el siguiente sprint

Sprint 2 solo debe comenzar después de validar el prototipo. Su foco recomendado sería integrar acceso contextual desde capítulos seleccionados, no ampliar aún a IA generativa.
