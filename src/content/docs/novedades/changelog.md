---
title: Changelog automático de CSS
description: Página que se actualiza automáticamente cada semana con cambios reales detectados en CSS a través de MDN Web Docs, CSSWG Drafts y caniuse.
---

Esta página se actualiza automáticamente cada semana mediante el workflow
[`weekly-css-watch.yml`](https://github.com/PabloHurtadoGonzalo86/CSSdocs/blob/main/.github/workflows/weekly-css-watch.yml).

Cada entrada enlaza cambios **reales** detectados en tres fuentes oficiales — nunca contenido inventado:

- **MDN Web Docs** (`mdn/content`): commits recientes que tocan la referencia de CSS.
- **CSSWG Drafts** (`w3c/csswg-drafts`): commits recientes en las especificaciones en desarrollo.
- **caniuse**: cambios de madurez (`status`) en un listado vigilado de características modernas de CSS.

Cuando aparece una entrada relevante aquí, es una señal de que alguna página de esta
documentación podría necesitar una revisión manual.

---

*Todavía no se ha ejecutado ninguna vigilancia semanal. La primera ejecución programada
sentará la base de comparación (ver `.github/scripts/state.json`).*

---

# Vigilancia semanal de CSS — 2026-07-10

Primera ejecucion: se ha guardado el estado inicial (commits de referencia y estados de madurez de caniuse). A partir de la proxima ejecucion semanal se compararan los cambios reales frente a este punto de partida.
