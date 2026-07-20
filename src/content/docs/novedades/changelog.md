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

---

# Vigilancia semanal de CSS — 2026-07-10

No se han detectado cambios relevantes esta semana en las fuentes vigiladas.

---

# Vigilancia semanal de CSS — 2026-07-13

## MDN Web Docs — cambios en la referencia de CSS
- [added missing word (#44698)](https://github.com/mdn/content/commit/a0b748b391f3ed7e6ef38e8eda3ecaa9efced926) (2026-07-13)

---

# Vigilancia semanal de CSS — 2026-07-20

## MDN Web Docs — cambios en la referencia de CSS
- [New pages: row-rule, *-style, and *-width (#44725)](https://github.com/mdn/content/commit/b13ef1ff1d0914617689df9074b24d41486e91b2) (2026-07-18)
- [Synchronize with BCD v8.0.7 (#44771)](https://github.com/mdn/content/commit/9cf3002bd29376c15d49df6fab2e6a264285abf6) (2026-07-18)
- [New CSS module page: `will-change` (#44210)](https://github.com/mdn/content/commit/5362c0545d8dc2a859fd2f64de41d576931d6a2e) (2026-07-18)
- [Fix scan media feature example: use interlace not interlaced (#44779)](https://github.com/mdn/content/commit/5a41c90092765ffe35958f439c2ab626714db340) (2026-07-18)
- [Change nonnegative to non-negative (#44765)](https://github.com/mdn/content/commit/0c62b082755017d0773ecaaee7e74efd5e066d0b) (2026-07-17)
- [Editorial review: Document responsive iframe sizing (#44598)](https://github.com/mdn/content/commit/04c41175b160dc00b1a1b8e4e13b2183d89fdf1a) (2026-07-17)
- [fix: auto-cleanup by bot (#44756)](https://github.com/mdn/content/commit/78291b4caa8c466d5e96480b7c0646f5f255952c) (2026-07-17)
- [fix: add note about relative URL resolution in custom properties for url() (#44751)](https://github.com/mdn/content/commit/b36b3e9dc1c4a60a4a382e57f1d3793164e2ca3f) (2026-07-16)
- [fix: soften 'never' to 'generally not' for pointer-events:none description (#44749)](https://github.com/mdn/content/commit/54363b174e87f0d2af789266d78eda0e9934bdbd) (2026-07-16)
- [Update muted HTML attribute description and examples (#44724)](https://github.com/mdn/content/commit/d1aa0dbd7441564e6ce8f6706c2022a2e1912d8c) (2026-07-16)
- [Editorial review: Document border-shape (#44191)](https://github.com/mdn/content/commit/cd0970bc03cf30a9a8089954cc542a17dbe9eba3) (2026-07-16)
- [fix: remove deprecated overflow:overlay from demo code (#44737)](https://github.com/mdn/content/commit/bd1e1e4c5979dc7b79f75dfcc787e5bff9510aef) (2026-07-16)
- [ci(deps-dev): bump prettier from 3.9.4 to 3.9.5 (#44676)](https://github.com/mdn/content/commit/4761340e600daad008747fb9aa48e28748a78422) (2026-07-15)
- [Fix simple code example oversight (#44717)](https://github.com/mdn/content/commit/7dbcde5a0aa6855447d015d99eba6fb8be6c2185) (2026-07-15)
- [New property: row-rule-color (#44549)](https://github.com/mdn/content/commit/c2b19ba089e2aa91491254bb76b9cbfcc27d7826) (2026-07-15)
- [Fix typo in Multicolumn Layout - Handling Overflow guide (#44692)](https://github.com/mdn/content/commit/fe28ff18c21cdea9ab159bafb972cc3f1e17cae7) (2026-07-13)

## CSSWG Drafts — cambios en especificaciones
- [[css-values-5] Editorial reorg of calc-size()](https://github.com/w3c/csswg-drafts/commit/c7573530343759ace8e46438a1fa2c44515b5554) (2026-07-17)
- [[css-values-5] Add WPT links](https://github.com/w3c/csswg-drafts/commit/df2c8d991cdad3582adb549bae076d7a05104ced) (2026-07-17)
- [[css-color-4] Avoid referencing "prepare for conversion", just state directly #14049](https://github.com/w3c/csswg-drafts/commit/226658f3d76cf165495b8faa92e8dfe60f7d7ae6) (2026-07-17)
- [[css-animations-2] Added `animation-delay-start`/`end` and made `animation-delay` a shorthand (#14167)](https://github.com/w3c/csswg-drafts/commit/dadb67bc264b412ff5f87cf6917912d4ae8a9c81) (2026-07-17)
- [[css-color-4] Clarified that the computed value of a deprecated system color is the color of the corresponding (non-deprecated) system color #13459](https://github.com/w3c/csswg-drafts/commit/e5e48fd957106f1f62fec295df5843583991aae3) (2026-07-16)
- [[web-animations-2] [scroll-animations] should calling play() reset the start time of a scroll-driven animation? (#14146)](https://github.com/w3c/csswg-drafts/commit/fea54cd6aa87f81e9ff7ea365366854eca28a284) (2026-07-16)
- [cleanup](https://github.com/w3c/csswg-drafts/commit/324e9d7e0fb1477bc7584d21c6862c00b1b742ae) (2026-07-15)
- [[css-color-4] Consolidated the resolution of system colors and deprecated system colors #13450](https://github.com/w3c/csswg-drafts/commit/ccbeef7edc7c0fd155a79040ec7bdc1265a4e723) (2026-07-15)
- [[css-color-4][editorial] wpt](https://github.com/w3c/csswg-drafts/commit/f91ef82ca03a91ad3c9a66a116d06405a64747c2) (2026-07-15)
- [[css-color-4][editorial] Added gradients to the hue interpolation examples to make them clearer](https://github.com/w3c/csswg-drafts/commit/7ee4e3759bd56d191668a53287c8baa4cce9247b) (2026-07-15)
- [[css-mixins-1][editorial] Update WPT paths and add missing WPTs](https://github.com/w3c/csswg-drafts/commit/0da42c8afd3a2a237be8fcfe1831b40d0d35aca4) (2026-07-14)
- [[css-values-5] Make it a little clearer that attr() matches *identically* to attribute selectors.](https://github.com/w3c/csswg-drafts/commit/c48d1b1353552913cf1c534c4d4e01f1bc3bed21) (2026-07-13)
- [[selectors-4] Fix explanation of HTML's case-matching rules. Define the default matching of document-supplied strings. #2259](https://github.com/w3c/csswg-drafts/commit/a2e88f36185c396d795f0718594c3022ea911a0d) (2026-07-13)
- [[mediaqueries-4] Remove trailing mention for speech as not deprecated. Fix #6029](https://github.com/w3c/csswg-drafts/commit/ac212bb8b373768ccf3c583bf76e0c74d35bcd50) (2026-07-14)
- [[css-values-5][editorial] fix bikeshed issues](https://github.com/w3c/csswg-drafts/commit/0222af95924db44c8e10d993b614596cd6f35cbb) (2026-07-13)
- [[web-animations-2] Auto-aligning the start time should apply a pending playback rate (#14175)](https://github.com/w3c/csswg-drafts/commit/04c3840a291d62b095845786bbfbf05f1cd421f7) (2026-07-13)
- [Tweak prose to account for ident-token](https://github.com/w3c/csswg-drafts/commit/e82303fde06dcff89f8e8e004f161ccb78d2a577) (2026-07-13)
- [function-token includes the opening (](https://github.com/w3c/csswg-drafts/commit/1c83f3a46a6cf6c6be4d71234065cd6e15108cea) (2026-07-09)
- [Add changes entry](https://github.com/w3c/csswg-drafts/commit/9f912ea85e0fdacb8ad94d82a59672fcea579e33) (2026-07-09)
- [[css-mixins-1] Make parentheses optional for mixins without parameters. #13015](https://github.com/w3c/csswg-drafts/commit/e3b81f011c571887ccc2ad850e581174cd93641a) (2026-07-09)
- [replace `contain: view-transition` with `view-transition-scope: all` (#14171)](https://github.com/w3c/csswg-drafts/commit/6ebe5ca638a909b79cc8928aae0196ef1e96d050) (2026-07-13)
