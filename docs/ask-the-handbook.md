---
title: "Pregúntale al Handbook — MVP"
description: "Demostración sin costo operativo de preguntas y respuestas editoriales verificadas sobre IBNR, triángulos y métodos clásicos."
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
  - mvp
---

# Pregúntale al Handbook — MVP

Esta demostración permite formular preguntas breves sobre conceptos cubiertos por el handbook y recibir una explicación editorial revisada, sus advertencias y enlaces a las secciones de soporte.

!!! info "Cómo funciona esta versión"
    La consulta se procesa íntegramente en su navegador. No utiliza IA generativa, no envía la pregunta a un servidor, no consume tokens y no almacena conversaciones.

<div
  class="handbook-qa"
  data-handbook-qa
  data-catalog="../assets/data/handbook-qa-catalog.json"
  data-sections="../assets/data/handbook-section-index.json"
  data-context="handbook mvp preguntas respuestas"
>
  <div class="handbook-qa__intro">
    <strong>Asistente contextual de conocimiento</strong>
    <span>Recuperación local y respuestas editoriales verificadas dentro del Health Insurance Reserving Handbook.</span>
  </div>

  <form class="handbook-qa__form" data-qa-form>
    <label class="handbook-qa__label" for="handbook-qa-question">
      Escriba una pregunta
    </label>
    <textarea
      id="handbook-qa-question"
      class="handbook-qa__input"
      data-qa-input
      rows="4"
      maxlength="500"
      placeholder="Ejemplo: ¿Por qué es necesario deduplicar los movimientos?"
      aria-describedby="handbook-qa-help handbook-qa-status"
    ></textarea>
    <p id="handbook-qa-help" class="handbook-qa__status">
      El MVP cubre 15 preguntas editoriales sobre datos, triángulos, Chain Ladder, Bornhuetter-Ferguson, Benktander y uso profesional.
    </p>
    <div class="handbook-qa__actions">
      <button class="md-button md-button--primary" type="submit">
        Consultar el handbook
      </button>
      <button class="md-button" type="button" data-qa-clear>
        Limpiar
      </button>
    </div>
    <p
      id="handbook-qa-status"
      class="handbook-qa__status"
      data-qa-status
      role="status"
      aria-live="polite"
    >
      Cargando catálogo local…
    </p>
  </form>

  <section class="handbook-qa__suggestions" aria-labelledby="qa-suggestions-title">
    <h2 id="qa-suggestions-title">Preguntas para probar</h2>
    <div class="qa-chip-list">
      <button
        class="qa-chip"
        type="button"
        data-qa-question="¿Por qué es necesario deduplicar los movimientos?"
      >¿Por qué deduplicar?</button>
      <button
        class="qa-chip"
        type="button"
        data-qa-question="¿Por qué una matriz 36 por 36 puede ser insuficiente?"
      >¿Por qué 36×36 puede ser insuficiente?</button>
      <button
        class="qa-chip"
        type="button"
        data-qa-question="¿Cuándo Chain Ladder puede ser poco confiable?"
      >¿Cuándo falla Chain Ladder?</button>
      <button
        class="qa-chip"
        type="button"
        data-qa-question="¿Por qué Bornhuetter-Ferguson necesita un prior independiente?"
      >¿Por qué BF necesita un prior?</button>
      <button
        class="qa-chip"
        type="button"
        data-qa-question="¿Qué aporta Benktander frente a Bornhuetter-Ferguson?"
      >¿Qué aporta Benktander?</button>
      <button
        class="qa-chip"
        type="button"
        data-qa-question="¿Cuál debe ser la reserva exacta de mi EPS este mes?"
      >Probar una consulta fuera de alcance</button>
    </div>
  </section>

  <section
    class="qa-result"
    data-qa-result
    tabindex="-1"
    aria-live="polite"
    hidden
  ></section>
</div>

<noscript>
Esta demostración requiere JavaScript para ejecutar la recuperación local. La búsqueda normal del sitio continúa disponible.
</noscript>

## Qué demuestra el Sprint 1

La prueba funcional valida que es posible:

- recibir una pregunta en lenguaje natural;
- reconocer formulaciones equivalentes y errores ortográficos leves;
- mostrar una respuesta estructurada y fuentes navegables;
- abstenerse ante cálculos, regulación específica o recomendaciones que exceden el corpus;
- operar sin APIs, backend, modelos descargables ni costos variables.

## Límites deliberados

El MVP no mantiene una conversación de múltiples turnos ni genera una respuesta nueva. Si la consulta no coincide con una respuesta editorial suficientemente precisa, muestra únicamente secciones relacionadas.

La cobertura inicial no pretende abarcar los 40 capítulos. Su propósito es probar precisión, transparencia, experiencia de usuario y mantenibilidad antes de ampliar el catálogo.

## Privacidad y costo

La pregunta permanece en el navegador durante la sesión. No se persiste, no se incorpora a Google Analytics como texto y no se transmite a un proveedor de modelos.

El costo operativo incremental esperado es **USD 0**, sujeto a los límites ordinarios del sitio estático y del repositorio público.

## Siguiente evolución

Después de validar este prototipo se podrá:

1. integrar el acceso desde capítulos específicos;
2. ampliar el catálogo usando preguntas reales y revisión editorial;
3. añadir contexto automático de página y sección;
4. evaluar búsqueda semántica local únicamente si la recuperación léxica resulta insuficiente.
