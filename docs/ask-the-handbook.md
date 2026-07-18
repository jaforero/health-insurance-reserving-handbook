---
title: "Pregúntale al Handbook — MVP"
description: "Demostración sin costo operativo de preguntas y respuestas editoriales verificadas mediante recuperación local en el navegador."
chapter: "ask-the-handbook"
part: "repository"
language: "es"
status: "review"
version: "0.1.0"
last_updated: "2026-07-18"
tags:
  - q-and-a
  - knowledge-retrieval
  - zero-cost
  - accessibility
  - reserving
---

# Pregúntale al Handbook — MVP

Esta demostración permite formular preguntas en lenguaje natural y recuperar explicaciones
editoriales verificadas dentro del **Health Insurance Reserving Handbook**.

!!! info "Arquitectura sin costo variable"
    La consulta se procesa íntegramente en el navegador. Esta versión no utiliza IA generativa,
    APIs externas, tokens, embeddings, bases vectoriales, backend ni almacenamiento de
    conversaciones.

!!! warning "Alcance"
    El asistente no calcula reservas particulares, no interpreta regulación vigente para una
    entidad específica y no sustituye el juicio actuarial. Cuando la evidencia disponible es
    insuficiente, debe abstenerse y mostrar únicamente contenido relacionado.

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
        placeholder="Ejemplo: ¿Por qué es necesario deduplicar?"
        aria-describedby="handbook-qa-help"
        required
      >
      <p id="handbook-qa-help" class="handbook-qa__help">
        El catálogo inicial cubre datos, triángulos, Chain Ladder, Bornhuetter-Ferguson,
        Benktander y alcance profesional.
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
    Cargando el catálogo editorial local…
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

## Qué puede demostrar este MVP

El prototipo permite validar cuatro hipótesis antes de incorporar una arquitectura generativa:

1. si los lectores formulan preguntas que pueden resolverse con respuestas editoriales;
2. si las variantes y los sinónimos producen recuperación suficientemente precisa;
3. si la abstención evita respuestas que exceden el contenido disponible;
4. si las fuentes navegables mejoran la comprensión frente a una búsqueda por palabras.

## Qué no demuestra

El MVP no mantiene conversaciones de múltiples turnos, no sintetiza respuestas nuevas y no
consulta información externa. La cobertura depende del catálogo versionado de preguntas y de
las secciones indexadas.

## Criterio de evolución

Una futura solución con RAG o un modelo generativo solo debería evaluarse después de observar
preguntas reales, medir cobertura y establecer un presupuesto explícito. El prototipo está
diseñado para conservar el contrato editorial y los enlaces aun si el motor tecnológico cambia.
