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

---

# Vigilancia semanal de CSS — 2026-07-10

## MDN Web Docs — cambios en la referencia de CSS
- [Fix minor typos across several pages (#44674)](https://github.com/mdn/content/commit/7f138099644a02640a903b2abc39e685ca8ca7cd) (2026-07-09)
- [Remove 'border' from list of properties that can be given a 'url()' (#44671)](https://github.com/mdn/content/commit/039b9d3f05cae775b88d4bdb09c533af62246e32) (2026-07-09)
- [chore(dict): fix typos (#44653)](https://github.com/mdn/content/commit/afcdfa050626bb7eb05ee693df8997020db9ff2e) (2026-07-08)
- [add `Snap a length as a line width` (#44194)](https://github.com/mdn/content/commit/b25b4a98b757fbd05ce1fb74b1b78f3fcf917729) (2026-07-08)
- [CSS overflow property description (#44340)](https://github.com/mdn/content/commit/ef6043b9d32b240262f6a29b719c02a7f61a5066) (2026-07-08)
- [Synchronize with BCD v8.0.5 (#44639)](https://github.com/mdn/content/commit/513146a616213fee548fdcf72dc1359030eb3395) (2026-07-04)
- [New pages: *-rule-visibility-items (#44616)](https://github.com/mdn/content/commit/34838ae7d32e78bfe01dbf2c266257ef0f8305c4) (2026-07-03)
- [ci(deps-dev): bump prettier from 3.8.5 to 3.9.4 (#44606)](https://github.com/mdn/content/commit/8d9cda4e9080e9c324a521f40c7e0704ef94ce07) (2026-07-03)
- [Update fit-content() documentation for clarity (#44602)](https://github.com/mdn/content/commit/5e4520f9cd84f65d470ec57efef7a73bbe9fd686) (2026-07-03)
- [fix: auto-cleanup by bot (#44623)](https://github.com/mdn/content/commit/fb0c5c4bd92cfdc043afcfca944c658cbf592b34) (2026-07-02)
- [Document CSS `alpha()` function (#44506)](https://github.com/mdn/content/commit/1055ee79c55c33ef82e2efc27ed248a561365724) (2026-07-01)
- [fix(css): correct attr() restriction in url-taking functions (#44589)](https://github.com/mdn/content/commit/3e21789c23062f7cfffa6fd7e24bd9dfc2c38551) (2026-06-29)
- [border-image shorthand reset info (#44560)](https://github.com/mdn/content/commit/0cf00ab40deebad90225815e1881ae89bbca085b) (2026-06-23)
- [Update the description for an `image-rendering` example (#44558)](https://github.com/mdn/content/commit/d314d089e9be9ac78a91ba95ee80cad7d3cbe8c2) (2026-06-23)
- [Add `display-p3-linear` to predefined color spaces (#44496)](https://github.com/mdn/content/commit/99251a2a7cc534462d5c0ad6fbcb17905e4df826) (2026-06-23)
- [untangle `border/column-rule/outline-width` from `*-style` properties value (#44195)](https://github.com/mdn/content/commit/a06cf3dca37bb7da1d5e5ad98c5d15a10dde3e8c) (2026-06-22)
- [Fix underlying translateX value typo in `animation-composition` (#44521)](https://github.com/mdn/content/commit/68bff8f2a51944e80394307c8e5c2879c167b126) (2026-06-21)
- [Fix CSS Flex documentation on behavior of `start` with reversed `flex-direction` (#44508)](https://github.com/mdn/content/commit/170d71538522a7dc3d98e8f5c5ba0f22c47d6c7f) (2026-06-21)
- [Synchronize with BCD v8.0.4 (#44523)](https://github.com/mdn/content/commit/361dd9caf4ac5db8a73cc33e4d8ee43fa2e35fcc) (2026-06-19)
- [Editorial review: Document element-scoped view transitions (#44217)](https://github.com/mdn/content/commit/3114d1b72a4d46d314caa7f73f775a1f6f7407dc) (2026-06-19)
- [New module: CSS gaps (#44447)](https://github.com/mdn/content/commit/53745a2089268ce62bf79695d7d347bcbd0abe57) (2026-06-18)
- [Update CSS background-color (#44336)](https://github.com/mdn/content/commit/21fddb9643fae34dce16aec8eb5dd86cc29e0b7c) (2026-06-18)
- [CSS `font` semi-shorthand property (#44387)](https://github.com/mdn/content/commit/efad19be74655f7a9c78f78d81cd4fb18d551033) (2026-06-18)
- [timeline-range-name defaults (#44353)](https://github.com/mdn/content/commit/ddd76a60b6f33cf077f9fdc5d1377ff94acd5aa4) (2026-06-17)
- [Improve clarity of `animation-composition` (#44431)](https://github.com/mdn/content/commit/682dfd30caf9790bcc9b90ad90ce951373bc86af) (2026-06-17)

## CSSWG Drafts — cambios en especificaciones
- [[meta] Don't scrub raw HTML from markdown. (#14166)](https://github.com/w3c/csswg-drafts/commit/57a1abdbb57aea5e1f70b06e8fa229427011ec00) (2026-07-10)
- [[css-image-animations] Manual anchors](https://github.com/w3c/csswg-drafts/commit/ea1b6104ba265dae7b9aba95c801adf13561fd57) (2026-07-10)
- [[css-image-animation] and ids to section titles](https://github.com/w3c/csswg-drafts/commit/f33b2e36fe44c776b4eb3b34861b043e951f878f) (2026-07-10)
- [[css-color-4][editorial] fix warning about variable only used once](https://github.com/w3c/csswg-drafts/commit/94c46c67c6832f7c506d70f007b68d5a4e77406b) (2026-07-09)
- [[css-color-4][editorial] wpt](https://github.com/w3c/csswg-drafts/commit/f37938a30d65f0a8ff8da7930322c55da03dbff0) (2026-07-09)
- [[css-color-4] Clarify carry-forward in color interpolation #14134](https://github.com/w3c/csswg-drafts/commit/526bc74aef4192ff1a4b3f8f3f782b836b6ef87c) (2026-07-09)
- [[css-link-params][editorial] Prepare for FPWD](https://github.com/w3c/csswg-drafts/commit/c7d565cd958ae69e264839f4a4d750d8db3e3ad5) (2026-07-03)
- [[css-view-tranitions-2] Update two-phase view transition explainer (#14145)](https://github.com/w3c/csswg-drafts/commit/6106271c16dbb9d90e8fe1ae9fdbdd4d4d8a3378) (2026-07-08)
- [[css-navigation-1] Remove controversial parts (#14138)](https://github.com/w3c/csswg-drafts/commit/98f7294797021f48fb578fe59e9c73e12f7cdea6) (2026-07-07)
- [[css-speech-1][editorial] Enforce positive <generic-voice> variant using range notation (#14124)](https://github.com/w3c/csswg-drafts/commit/b99f0c7aabea5d3d559991aad43d3eb1866c8b6a) (2026-07-02)
- [[selectors-4][editorial] Update previous versions](https://github.com/w3c/csswg-drafts/commit/a3a7543a98003f4c218cb9e5d284ede7393d1c00) (2026-07-02)
- [[selectors-4][editorial] silence bikeshed nitpicking](https://github.com/w3c/csswg-drafts/commit/7780a1fef5eedbc2f7e32be64f071068d1dfb618) (2026-07-02)
- [[selectors-4][editorial] wpt](https://github.com/w3c/csswg-drafts/commit/aa61b2cffedd74f649515d35ab457594d7446318) (2026-07-02)
- [[selectors-4] Better description of :lang() psuedo class selector #3022.](https://github.com/w3c/csswg-drafts/commit/1ed57ea00a366c70d7f018603c4f508f67fa4fd9) (2026-07-02)
- [[css-navigation-1] Change `:trigger-link` to `:nav-source` and include submit/form (#14122)](https://github.com/w3c/csswg-drafts/commit/d554423cee00e645b8bed6c8a963094deab649f0) (2026-07-01)
- [Clarify note on ViewTransition/types manipulation. (#14110)](https://github.com/w3c/csswg-drafts/commit/14685cd7383d9a2b49d075d76c5187f6ea571aac) (2026-07-01)
- [[selectors-4] Add CanIUse panels #1193 (#14120)](https://github.com/w3c/csswg-drafts/commit/387bbced5058e37ac273c6a840dddd255bef2839) (2026-07-01)
- [[css-navigation-1] Move parameter resolution into <<route-location>> instead of `:active-navigation` (#14119)](https://github.com/w3c/csswg-drafts/commit/0aa3d4092f277e50936d17490e15b9b414f08baf) (2026-07-01)
- [Initial plan](https://github.com/w3c/csswg-drafts/commit/1df9846dc2d3d8408b6cd22111964bc17d47f25f) (2026-03-20)
- [[cssom-view-1] Per flackr feedback, not worth making quirks mode care about single-axis.](https://github.com/w3c/csswg-drafts/commit/169b4342e2a46470236aed058e829efae61692ac) (2026-06-30)
- [[css-overscroll-1] Clarify the wording to be about scrollable axis.](https://github.com/w3c/csswg-drafts/commit/d5541f207f8c7ad2f345d59b0b36b9fcdf395f4f) (2026-06-30)
- [[css-conditional-5] Clarify a little bit that we can skip containers.](https://github.com/w3c/csswg-drafts/commit/416c9715a3c063d6c9705b4e3c96e966299bdda5) (2026-06-30)
- [[css-overscroll-1] Never mind, exclude single-axis scrollers from the scroll chain in their non-scrolling axis.](https://github.com/w3c/csswg-drafts/commit/23ba67b1be61d6f455a9cf46a2732df72e1aa68a) (2026-05-14)
- [[css-nav-1] Fix up 'can be manually scrolled' to care about axises, use it in a few more places.](https://github.com/w3c/csswg-drafts/commit/8f211ee559ce6ee64d2268e94cadccabf6425610) (2026-05-14)
- [[css-nav-1] Clean up some of the bikeshed errors](https://github.com/w3c/csswg-drafts/commit/f74689996f25df8092e2c3767fa186e12e9fa399) (2026-05-14)
