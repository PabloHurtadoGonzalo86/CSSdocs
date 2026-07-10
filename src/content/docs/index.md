---
title: CSSdocs
description: Documentación personal y viva sobre CSS, con una referencia estructurada basada en fuentes oficiales, el curso de midulive y un vigilante semanal automático que la mantiene actualizada.
---

Documentación personal y viva sobre **CSS**, escrita para dominarlo a nivel profesional
en desarrollo Frontend.

## Qué es esto

Una referencia estructurada, precisa y didáctica que combina:

- **Fuentes oficiales**: [MDN Web Docs](https://developer.mozilla.org/es/docs/Web/CSS), las
  especificaciones del [CSS Working Group (W3C)](https://www.w3.org/Style/CSS/) y datos de
  soporte de [caniuse](https://caniuse.com/).
- El curso en vídeo ["Curso de CSS desde cero completo y GRATIS"](https://www.youtube.com/playlist?list=PLUofhDIg_38q7l8gV4IVCz_pjUeyD99_j)
  de [midulive](https://www.youtube.com/@midulive) — ver [Curso de midulive](curso-midulive/index).
- Un **vigilante semanal automático** (GitHub Actions) que revisa esas fuentes oficiales y
  registra los cambios detectados en [Novedades](novedades/changelog), para que esta
  documentación no se quede obsoleta.

## Cómo está organizada

| Sección | Contenido |
|---|---|
| [Fundamentos](fundamentos/que-es-css) | Sintaxis, cascada, especificidad, herencia, selectores, unidades, colores, modelo de caja |
| [Layout](layout/display-y-flujo-normal) | Display, flujo normal, overflow, positioning, Flexbox, Grid, multi-columna |
| [Diseño responsivo](responsive/media-queries) | Media queries, container queries, unidades y funciones responsivas |
| [Tipografía](tipografia/fuentes-y-texto) | Fuentes web y propiedades de texto |
| [Animaciones](animaciones/transiciones) | Transiciones, `@keyframes`, transform, scroll-driven animations |
| [CSS moderno](moderno/custom-properties) | Custom properties, `:has()`/`:is()`/`:where()`, nesting, `@layer`, `@scope`, color moderno |
| [Arquitectura CSS](arquitectura/metodologias-y-organizacion) | Metodologías y organización a escala |
| [Cheatsheets](cheatsheets/flexbox-cheatsheet) | Chuletas rápidas de Flexbox, Grid y selectores |
| [Curso de midulive](curso-midulive/index) | Notas y enlaces a los resúmenes del curso en Google Docs |
| [Novedades](novedades/changelog) | Changelog automático generado por el vigilante semanal |

## Filosofía de esta documentación

- **Nada inventado.** Todo lo técnico está verificado contra documentación oficial.
- **Explicada, no solo listada.** Cada página busca que se entienda el *porqué*, no solo el *qué*.
- **Viva.** Se actualiza semanalmente de forma automática a partir de fuentes oficiales.
