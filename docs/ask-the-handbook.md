---
title: "Pregúntale al Handbook — MVP"
description: "Asistente local y trazable de preguntas y respuestas editoriales, complementado con recuperación automática sobre todo el corpus publicado."
chapter: "ask-the-handbook"
part: "repository"
language: "es"
status: "review"
version: "0.2.0"
last_updated: "2026-10-27"
tags:
  - q-and-a
  - knowledge-retrieval
  - zero-cost
  - accessibility
  - reserving
  - corpus-index
---

# Pregúntale al Handbook — MVP

## Conexiones de lectura

- [Inicio](index.md): explorar la estructura completa del manual.
- [Glosario](glossary.md): precisar los términos de una consulta.
- [Guía de selección](methodology-selection-guide.md): comparar requisitos y límites de los métodos.
- [Particularidades de reservas en salud](part-06-health-specific/21-health-insurance-reserving-specificities.md): entender cómo cambia la selección metodológica en Health Insurance.
- [Demo 4 · Preparación de datos](examples/04-demo-preparacion-datos.md): llevar las explicaciones a un ejercicio reproducible.

Esta demostración permite formular preguntas en lenguaje natural y recuperar conocimiento trazable dentro del **Health Insurance Reserving Handbook**.

El asistente utiliza dos capas locales:

1. **respuestas editoriales verificadas**, para preguntas de alta importancia o formulaciones frecuentes;
2. **índice automático del corpus publicado**, generado desde todos los archivos `docs/**/*.md` y sus secciones para recuperar evidencia cuando todavía no existe una respuesta editorial curada.

Las respuestas editoriales tienen prioridad. Cuando una formulación no coincide con el catálogo pero el corpus contiene evidencia suficientemente relacionada, el asistente muestra **Evidencia encontrada en el Handbook** y enlaza las secciones fuente. Solo utiliza **Cobertura insuficiente** cuando tampoco existe evidencia documental razonable en el corpus indexado.

!!! info "Arquitectura sin costo variable"
    La consulta se procesa íntegramente en el navegador. Esta versión no utiliza IA generativa,
    APIs externas, tokens, embeddings, bases vectoriales, backend ni almacenamiento de
    conversaciones.

!!! warning "Alcance"
    El asistente no calcula reservas particulares, no interpreta regulación vigente para una
    entidad específica y no sustituye el juicio actuarial. Una coincidencia de corpus localiza
    evidencia; no sintetiza hechos ausentes ni convierte automáticamente una sección relacionada
    en una recomendación profesional para un caso particular.

<div
  class="handbook-qa"
  data-handbook-qa
  data-catalog-url="../assets/data/handbook-qa-catalog.json"
  data-sections-url="../assets/data/handbook-section-index.json"
  data-site-root="../"
>
  <div class="handbook-qa__intro">
    <p><strong>Cómo funciona:</strong> escriba una pregunta o seleccione una sugerencia.</p>
    <p>La respuesta incluye explicación, ejemplo, advertencia y enlaces a las fuentes internas.</p>
  </div>

  <form class="handbook-qa__form" data-handbook-qa-form>
    <div class="handbook-qa__field">
      <label for="handbook-qa-question">Pregunta</label>
      <input
        id="handbook-qa-question"
        class="handbook-qa__input"
        data-handbook-qa-input
        type="search"
        name="question"
        minlength="3"
        maxlength="240"
        autocomplete="off"
        placeholder="Ejemplo: Para reservas en salud, ¿cuál de los métodos es más recomendado?"
        aria-describedby="handbook-qa-help"
        required
      >
      <p id="handbook-qa-help" class="handbook-qa__help">
        La primera sugerencia explica cómo seleccionar métodos de reserving en salud. El índice de respaldo cubre automáticamente todo el corpus Markdown publicado.
      </p>
    </div>
    <button class="handbook-qa__submit" type="submit">Buscar explicación</button>
  </form>

  <div
    class="handbook-qa__suggestions"
    data-handbook-qa-suggestions
    aria-label="Preguntas sugeridas"
  ></div>

  <p class="handbook-qa__loading" data-handbook-qa-loading>
    Cargando el catálogo editorial y el índice local del corpus…
  </p>

  <div
    class="handbook-qa__output"
    data-handbook-qa-output
    tabindex="-1"
    aria-live="polite"
    hidden
  ></div>

  <p class="handbook-qa__privacy">
    La pregunta permanece en su navegador y no se transmite ni se almacena.
  </p>

  <noscript>
    <p class="handbook-qa__error">
      Esta demostración necesita JavaScript. La búsqueda estándar del sitio permanece disponible.
    </p>
  </noscript>
</div>

## Respuesta editorial prioritaria

La primera pregunta sugerida por defecto es:

> **Para reservas en salud, ¿cuál de los métodos es más recomendado?**

La respuesta editorial establece que **no existe un único método universalmente superior**. La selección depende de la obligación, la madurez de los claims, la estabilidad del patrón de desarrollo, la disponibilidad de exposición o de un prior defendible, la calidad de los datos y el propósito de la estimación.

Como marco práctico:

- con desarrollo triangular estable, **Chain Ladder** es un benchmark natural;
- para periodos inmaduros con prior o exposición confiables, **Bornhuetter-Ferguson, Cape Cod o PMPM** suelen ser candidatos más robustos;
- **Mack y Bootstrap** complementan el análisis cuando se necesita cuantificar incertidumbre bajo estructuras de desarrollo;
- si los triángulos no representan adecuadamente el fenómeno, deben considerarse **GLM/GAM, modelos granulares, supervivencia, escenarios u otros enfoques apropiados**;
- la práctica defendible es seleccionar un método central, usar challengers y validar con diagnósticos, backtesting y sensibilidad, no declarar un ganador universal.

La respuesta enlaza directamente a [Selección metodológica en reservas de salud](part-06-health-specific/21-health-insurance-reserving-specificities.md#seleccion-metodologica), su [árbol de decisión](part-06-health-specific/21-health-insurance-reserving-specificities.md#arbol-de-decision-resumido) y la [Guía de selección de metodologías](methodology-selection-guide.md#principios-de-seleccion).

## Cómo se actualiza el conocimiento

El archivo `scripts/generate_handbook_qa_knowledge.py` reconstruye el índice antes de `test`, `build` y `serve`. El proceso:

1. descubre todos los archivos Markdown publicables bajo `docs/`;
2. extrae metadatos, títulos y headings H1–H3;
3. genera términos y resúmenes breves únicamente desde el texto fuente;
4. reconstruye `handbook-section-index.json`;
5. sincroniza las respuestas editoriales prioritarias;
6. habilita el estado `corpus_match` cuando existe evidencia documental suficiente.

Por tanto, un capítulo nuevo o una sección nueva entra en la capa de recuperación en el siguiente ciclo normal de construcción del sitio, sin mantener manualmente una lista paralela de secciones.

## Qué puede demostrar este MVP

El prototipo permite validar cinco hipótesis antes de incorporar una arquitectura generativa:

1. si los lectores formulan preguntas que pueden resolverse con respuestas editoriales;
2. si las variantes y los sinónimos producen recuperación suficientemente precisa;
3. si el índice automático del corpus reduce falsos negativos de cobertura;
4. si la abstención evita respuestas que exceden el contenido disponible;
5. si las fuentes navegables mejoran la comprensión frente a una búsqueda por palabras.

## Qué no demuestra

El MVP no mantiene conversaciones de múltiples turnos, no sintetiza respuestas nuevas y no consulta información externa. **Evidencia encontrada en el Handbook** significa que el sistema localizó secciones relevantes; el lector debe revisar esas fuentes y no interpretar la coincidencia como una recomendación individual.

## Criterio de evolución

Una futura solución con RAG o un modelo generativo solo debería evaluarse después de observar preguntas reales, medir cobertura y precisión del índice automático y establecer un presupuesto explícito. El diseño conserva el contrato editorial, la trazabilidad y los enlaces aun si el motor tecnológico cambia.
