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

---

# Vigilancia semanal de CSS — 2026-07-27

## MDN Web Docs — cambios en la referencia de CSS
- [Update CSS function references (#44865)](https://github.com/mdn/content/commit/d1745aaf15baa2b3d48f67a51eba881a9f4f2c33) (2026-07-26)
- [CSS properties:  intro sentence in values section (#44873)](https://github.com/mdn/content/commit/071fd0613b1b5728d2d83845ea11512cb615067a) (2026-07-26)
- [Synchronize with BCD v8.0.8 (#44914)](https://github.com/mdn/content/commit/a9dc3374034d357cbfea717fd5d641605359e3c7) (2026-07-25)
- [link parameters property & param() function (#44852)](https://github.com/mdn/content/commit/35cd8b781219157e42b289364754cff862c2dd1a) (2026-07-24)
- [CSS property: value section intro (#44867)](https://github.com/mdn/content/commit/d4dc9d899ebec0e9c22a5bb9229f39f33457d8df) (2026-07-24)
- [New data type page: line-width (#44597)](https://github.com/mdn/content/commit/e9c03ba87f9ff4123150d8f7dc457bd546bdab83) (2026-07-24)
- [CSS `repeat()` function: page rewrite (#44601)](https://github.com/mdn/content/commit/01b76b3a2afa161bd2481e3623d76f05de4b2797) (2026-07-24)
- [FF153 CSS basic shape closest-/farthest-corner (#44827)](https://github.com/mdn/content/commit/1e7ba7f0645705dcd46dd7392f09284129cf87bf) (2026-07-24)
- [Fix typo in `font-weight` at-rule descriptor reference (#44888)](https://github.com/mdn/content/commit/c66cecb0ec58ddea1bd624aa89dd355d9b90b5c3) (2026-07-24)
- [Editorial review: Document the path-length CSS property (#44563)](https://github.com/mdn/content/commit/28f2781de2dbb8e81be94c87ff81fd0442cb4736) (2026-07-24)
- [fix(css): clarify ruby-position inter-character value (#44874)](https://github.com/mdn/content/commit/a52a9cd2b661e6e51e4b600c848207140265d362) (2026-07-23)
- [columns property: add value to interactive example (#44890)](https://github.com/mdn/content/commit/ab90c79ca764c4431c7f4a078d81c02ef4bfce2e) (2026-07-23)
- [Page updates: column-rule-* (#44755)](https://github.com/mdn/content/commit/5cf8432d980cbe9b7e5611d647d8566b5c4ff3ed) (2026-07-21)
- [CSS value intro sentence position (#44833)](https://github.com/mdn/content/commit/c0c85c3dc0d6ff4247c85b0144149e584d74b625) (2026-07-21)

## CSSWG Drafts — cambios en especificaciones
- [[css-values-4][editorial] Slightly reword the automatic clamping text to make it clearer that it's often implicit/UA-defined.](https://github.com/w3c/csswg-drafts/commit/5849ec370c7edc65dcade47d25e113d8798d33b8) (2026-07-23)
- [[css-values-5][editorial] Fix markup](https://github.com/w3c/csswg-drafts/commit/6200ae897402813de98f750ca5dc80eb43cb5533) (2026-07-23)
- [[css-values-5] Specify that normal simplification *is* done on the calculation (and basis if needed), same as math functions.](https://github.com/w3c/csswg-drafts/commit/55f964529ec847328c9253ceaae1798a9f3412d4) (2026-07-23)
- [[filter-effects-1] Removed SVGURIInterface from SVGFilterElement. #13949](https://github.com/w3c/csswg-drafts/commit/65f6c90e61e89ea7c14c1196390f714d9f39b6f4) (2026-07-22)
- [[selectors-4][editorial] correct link to html a element not lab (color) a](https://github.com/w3c/csswg-drafts/commit/08f2f799da6a306e8bf5daca208683717f26d643) (2026-07-22)
- [[selectors-4][editorial] Mark some sections explicitly as non-normative, in hopes the normative reference checker is helped](https://github.com/w3c/csswg-drafts/commit/5606680f8d8141c39fd07d99331a6fea94c1293b) (2026-07-22)
- [[selectors-4][editorial] Update changes](https://github.com/w3c/csswg-drafts/commit/0319971bd0fada94b50b5f79d3ce95589c757e3e) (2026-07-22)
- [[selectors-4] Changed HTML5 references to HTML LS](https://github.com/w3c/csswg-drafts/commit/45dbb1507f09ceb9cceca5a7ab70ed33a8c74851) (2026-07-22)
- [[selectors-4][editorial] wpt](https://github.com/w3c/csswg-drafts/commit/c2f4c82b646edb4c6467354dd7e740c05d505b4f) (2026-07-22)
- [[selectors-4][editorial] Update changes](https://github.com/w3c/csswg-drafts/commit/71f240e7a761c4c0969641e9f2392c916132b8d6) (2026-07-22)
- [[css-sizing-5][editorial] Add/tweak notes in interpolation-size.](https://github.com/w3c/csswg-drafts/commit/5c21b073ea303b1331f82921ce6137336b6f102d) (2026-07-20)
- [[css-values-5][editorial] Fix example code to current syntax/rules.](https://github.com/w3c/csswg-drafts/commit/66a5b4b80962d51e44e03e8d07ed62a13c4b785f) (2026-07-20)
- [[css-values-5] Revert previous edit about simplification at specified/computed time, it's just an interpolation operation.](https://github.com/w3c/csswg-drafts/commit/63bd6aec4bb234baf896bd3307aef1753923f01f) (2026-07-20)
- [[css-values-5][editorial] Shift 'simplifying calc-size()' back to being under 'interpolating', as it only concerns interpolation.](https://github.com/w3c/csswg-drafts/commit/762e5ca4b20b0ae4cb44ca0d8a569525ee2cc13f) (2026-07-20)
- [[css-values-5][editorial] Define all the calc-basis values more explicitly in our normal list fashion; slightly rearrange surrounding text to fit.](https://github.com/w3c/csswg-drafts/commit/8c67ba03f553e5697424ac13a5d3f3188bc82bf2) (2026-07-20)
- [[css-font-loading] Add support for the new  terminology and alias the old (#14197)](https://github.com/w3c/csswg-drafts/commit/11aef64584da64cd350bd221fc598adf6ec40894) (2026-07-20)
- [[css-color-4] Changed the previous term "Required conversion" to "Conversion, if required" because the former term was misleading #14204](https://github.com/w3c/csswg-drafts/commit/553385de6177e28f6c9cbccb480caee0cdd724c9) (2026-07-20)

---

# Vigilancia semanal de CSS — 2026-08-03

## MDN Web Docs — cambios en la referencia de CSS
- [THank! docs(css): remove stale flex-basis 0% vs 0 warning on `flex` page (#44963)](https://github.com/mdn/content/commit/28839be2d5cdb1235fdd75b873c90cf491e93367) (2026-07-31)
- [Mark all legacy SVG1 writing-mode values as deprecated (#44974)](https://github.com/mdn/content/commit/52b551c479b9ab85215a05e40161013e3f285746) (2026-07-31)
- [Note the SVG rotate() center-of-rotation syntax (#44979)](https://github.com/mdn/content/commit/80ab11f9d757b49325122071a8a6210440ec6551) (2026-07-31)
- [New CSS property: rule (#44947)](https://github.com/mdn/content/commit/f4d39e4f5a6f426bff5f91cccb5b6fadff094e27) (2026-07-30)
- [CSS minor fix: added missing "flexbox" (#44955)](https://github.com/mdn/content/commit/b5c3edee358451f960799810aaed0749e5f1b2be) (2026-07-30)
- [Fix broken links, HTTP→HTTPS upgrades, and article/typo corrections (#44733)](https://github.com/mdn/content/commit/7ed7b730bf88307cc6cf34b82bb1d735b9a1aa1f) (2026-07-28)
- [fix: missing apostrophe in CSS Replaced Elements guide ('dont' -> 'don't') (#44928)](https://github.com/mdn/content/commit/7b47c1b23681675bdaaa3788d1c177ac92eb925f) (2026-07-27)

## CSSWG Drafts — cambios en especificaciones
- [[web-animations-css-integration] Drop Web Animations CSS Integration spec](https://github.com/w3c/csswg-drafts/commit/e1f921c97d8e50fb54d087f81a16b91f5d33a34f) (2026-08-03)
- [[css-backgrounds-4][editorial] Sort background-origin and background-clip values in canonical order (#14257)](https://github.com/w3c/csswg-drafts/commit/bbbe9a687b92585ad2587e2441e439e838d99fec) (2026-08-03)
- [[css-gaps-1] Update Privacy Considerations per wide review feedback.](https://github.com/w3c/csswg-drafts/commit/13b14ec48af0219c893713d670cf80d8c014a648) (2026-07-31)
- [typo](https://github.com/w3c/csswg-drafts/commit/e595770f2216380e954462fab5b54222b6c066bf) (2026-07-31)
- [[css-color-5][editorial] wpt](https://github.com/w3c/csswg-drafts/commit/34d6bf9698913d418d24dd0e29fc674a53830b7e) (2026-07-31)
- [[css-color-5][editorial] Add examples of RCD alpha() serialization, #13994](https://github.com/w3c/csswg-drafts/commit/55eb4e60ace2723c82caf2d888e09b9f3ecd512b) (2026-07-31)
- [[css-navigation-1][editorial] Update title (#14242)](https://github.com/w3c/csswg-drafts/commit/dbb54ef0c224308747560a9c6021eb0714b98c37) (2026-07-30)
- [[selectors-4][editorial] Make non-normative references more clearly marked so the normative references checker doesn't trip over them so much](https://github.com/w3c/csswg-drafts/commit/c282dbebe51162f438dcafa1a1d77634f366a6e3) (2026-07-30)
- [[css-syntax-3][editorial] Update changes](https://github.com/w3c/csswg-drafts/commit/f971255463f01fb740e2a3a7ecfe83e319cddab9) (2026-07-30)
- [better layout](https://github.com/w3c/csswg-drafts/commit/d5c592fdb6102834457b1284714b2b0f62ea9c87) (2026-07-28)
- [[css-color-hdr][editorial] Add JzCzhz prim-sec diagram to the JzCzhz section](https://github.com/w3c/csswg-drafts/commit/df2044c097c6c7769652cf289f3a7be07810fcd8) (2026-07-28)
- [[css-color-hdr][editorial] Add Jzazbz prim-sec diagram and its generator script](https://github.com/w3c/csswg-drafts/commit/7b804b8ffc2e3481a2eab7d22b25d21d25f0989b) (2026-07-28)
- [[css-color-4][editorial] Add generator script for Oklch prim-sec diagrams](https://github.com/w3c/csswg-drafts/commit/178bea27ffcffd0ef418a5c6f4184bb41b7da168) (2026-07-28)
- [[css-color-4][editorial] Add Oklab a,b plane diagrams for predefined RGB color spaces](https://github.com/w3c/csswg-drafts/commit/133fcc7e84c534a382d94519ee910840e003bd8a) (2026-07-28)
- [Remove a dangling scroll completion para from CSSOM View 1](https://github.com/w3c/csswg-drafts/commit/dc3101a1c758940d05a650bafd1cbc6e0865fabb) (2026-07-27)
- [[css-color-4][editorial] Add note to hwb about Abney effect](https://github.com/w3c/csswg-drafts/commit/4dbb2edad06e2ebc0cb47aa39d019c5fd5e0cc3f) (2026-07-24)
- [[web-animations-1] Specify handling of duration string values other than auto](https://github.com/w3c/csswg-drafts/commit/9fc6f40a056ea714a35acb9414a73f92edc8ce53) (2026-07-28)

---

# Vigilancia semanal de CSS — 2026-08-10

## MDN Web Docs — cambios en la referencia de CSS
- [Revise flex-direction property (#44956)](https://github.com/mdn/content/commit/c965bd5938085b2dab7d19734adbe3db0914ba5d) (2026-08-07)
- [[CSS] Add grid-lanes documentation to display property (#44436)](https://github.com/mdn/content/commit/24cdca6f7927df0c49c00d272f68d4a25c817af3) (2026-08-07)
- [Synchronize with BCD v8.0.10 (#45039)](https://github.com/mdn/content/commit/343ab51426f9279175b8f71fff911621d0a7da20) (2026-08-07)
- [Fix typos: withing -> within, wll -> will, bellow -> below (#45040)](https://github.com/mdn/content/commit/f49f1d49a7ea045dd1365834d8931721894c1aaf) (2026-08-07)
- [fix: resolve weekly spelling check findings (#44906)](https://github.com/mdn/content/commit/c655f38c10ba17b853b0e66b43cf4cf2b176e424) (2026-08-04)
- [Fix weekly spelling check (#44962)](https://github.com/mdn/content/commit/4b837c21d9138c61a81ac584cd4319cf22d1388c) (2026-08-04)
- [New pages: rule-* shorthand properties (#44895)](https://github.com/mdn/content/commit/e08f8e5467c3af416ca82f00bfbf19d718d6fbab) (2026-08-04)
- [Synchronize with BCD v8.0.9 (#45000)](https://github.com/mdn/content/commit/e57e3fdd4ab6fb372ddc3d78e5b428f318202426) (2026-08-04)
- [Remove outdated browser compatibility info about sideways-rl and sideways-lr (#44970)](https://github.com/mdn/content/commit/08c6d21d1e741aa3d96296edaa4964ebfcdbaded) (2026-08-03)

## CSSWG Drafts — cambios en especificaciones
- [[css-egg-1] Added random units](https://github.com/w3c/csswg-drafts/commit/f86e27657b041700249811a974f7c4a80df20d82) (2026-08-07)
- [[web-animations-1][web-animations-2] Simplify auto fill mode calculation in level 1](https://github.com/w3c/csswg-drafts/commit/914ce4bbc2b25bb3c7b50b7b844a5f1a164b6ed6) (2026-08-07)
- [Add links from drafts homepage to explainers](https://github.com/w3c/csswg-drafts/commit/6af23215645075e9e88751765ea07d0d1231c5d6) (2026-07-31)
- [Fix link](https://github.com/w3c/csswg-drafts/commit/f5170788ce7777e75ed3d2a16fb856e3c8bf10b7) (2026-08-06)
- [typo](https://github.com/w3c/csswg-drafts/commit/87b44e016626bbbf5c55953ea622e3fe1483131f) (2026-08-06)
- [stop bikeshed complaining](https://github.com/w3c/csswg-drafts/commit/b414cb076ef2364df644a2652c78e40afdeafc13) (2026-08-06)
- [[css-color-4][editorial] Update changes](https://github.com/w3c/csswg-drafts/commit/d528ec68d55e20578ef418085db37bb4a9e907bc) (2026-08-06)
- [[css-color-4][editorial] add generator for the Oklrab Lr vs L diagram](https://github.com/w3c/csswg-drafts/commit/65787fbffd3f1cbba575f744d90f15e6a6422d83) (2026-08-06)
- [[css-color-4][editorial] add a figure #14207](https://github.com/w3c/csswg-drafts/commit/c9ab944a7e7743defe9da30f382e357ace982265) (2026-08-06)
- [[css-color-4] Explain deltaE better, and add deltaEOKr2 #14207](https://github.com/w3c/csswg-drafts/commit/af8338edf72e154f05b57d4c199906358e684db0) (2026-08-06)
- [[css-text-decor-4] Added percentages to `text-decoration-inset` (#14282)](https://github.com/w3c/csswg-drafts/commit/512adad03bbc51c03b47e58c6a21b53b974ad000) (2026-08-06)
- [[web-animations-1] Add summary of relationship between play states and start/hold time](https://github.com/w3c/csswg-drafts/commit/8dc970b1eef7da4890d8c559c85ad02a8edda34e) (2026-08-06)
- [Revert "[css-text-decor-4] Updated the value for `text-decoration-inset` (#14269)"](https://github.com/w3c/csswg-drafts/commit/96dadf1df19e764ddc0fd78b728fad626e944cc6) (2026-08-05)
- [[css-text-decor-4] Updated the value for `text-decoration-inset` (#14269)](https://github.com/w3c/csswg-drafts/commit/2d923a4d630c7e396bbe0fa26bee20ff051e8e0d) (2026-08-05)
- [[web-animations-1] Update changelog](https://github.com/w3c/csswg-drafts/commit/06cc4643ee5556a8174e8d732b947ef56272a0b2) (2026-08-05)
- [[web-animations-1] Add missing closing div tag](https://github.com/w3c/csswg-drafts/commit/44b9fc8ee208dd18c7c801a0586fcd4b878fb38f) (2026-08-05)
- [[web-animations-1] Add annotations describing exceptions thrown by the API](https://github.com/w3c/csswg-drafts/commit/aafe0da6a622b9db43a38c4dd1410a0690c0a429) (2026-08-05)
- [[css-navigation-1] Apply CSSWG resolutions (#14264)](https://github.com/w3c/csswg-drafts/commit/3845cfb3fcb0ecec6ca83bbe8675a71d536f7270) (2026-08-04)
- [[css-over-flow-5] Introduce scroll-axis-lock (#14152)](https://github.com/w3c/csswg-drafts/commit/dd4d35400b94d85260de2bc4504bc08c460c865e) (2026-08-04)
- [[css-multicol] Drafting implementaion report](https://github.com/w3c/csswg-drafts/commit/f3f92fec735b6a31fd3d823a05b32200a00cdf04) (2026-08-04)
- [[css-multicol] Initial draft implementation report](https://github.com/w3c/csswg-drafts/commit/b8c37b8972e38a5bd2824f559b4ecac40959a6e6) (2026-08-04)

---

# Vigilancia semanal de CSS — 2026-08-17

## MDN Web Docs — cambios en la referencia de CSS
- [Fix stacking context hierarchy diagram (remove non-context) (#45159)](https://github.com/mdn/content/commit/d1a90acef8a6fb1f75a3e4d937f78d7038d7bfc4) (2026-08-17)
- [Fix content issues (#45143)](https://github.com/mdn/content/commit/b6de98eb9cd52ce7e37f22a340352f0af4c9d597) (2026-08-14)
- [fix: soften 'never' in pointer-events:none description (fixes #44565) (#44566)](https://github.com/mdn/content/commit/b9c07e549a6e66272c589a254ebcd5a8c91f37a5) (2026-08-14)
- [Avoid using the same id as tag name without visible HTML (#42159)](https://github.com/mdn/content/commit/6f1b699dd8891431bbfe0bc3bb803f929fa6032e) (2026-08-12)
- [fix(css): clarify wbr line breaking behavior (#45103)](https://github.com/mdn/content/commit/d4569d185ccab9b722eb849c033ef69f8f44d107) (2026-08-12)
- [Editorial review: Chrome 149 User action pseudo-class top-layer boundary (#44615)](https://github.com/mdn/content/commit/c62181855c91ac0435dea5fa759a250e1dea4f8b) (2026-08-12)
- [Make arithmetic operator formatting consistent in CSS docs (#44335)](https://github.com/mdn/content/commit/11c522da37b7469cbce26bbe220936aec1d372d0) (2026-08-12)
- [Editorial review: Add notes about web app scope system accent color (#44678)](https://github.com/mdn/content/commit/4d49c28381a2b736e205215b75388945e44a028c) (2026-08-12)
- [Added documentation that sibling combinators to the right of :scope never match (#43743)](https://github.com/mdn/content/commit/e8310a9d2806a4aebf457f75eec4671e14e47e44) (2026-08-11)
- [docs(css): rename masonry guide to grid lanes (#45049)](https://github.com/mdn/content/commit/b02c4fe0f8c485fa3fd0af10005310aaecef64ca) (2026-08-11)
- [Intro to css values (#44937)](https://github.com/mdn/content/commit/a5531a7b1fa30ab1de952ffff619a9830eb1c1a9) (2026-08-11)
- [docs(css): clarify negative lookahead analogy (#45080)](https://github.com/mdn/content/commit/ebc0a01b494e58ada6d89a5f94141cdcba7efbc7) (2026-08-11)
- [Removes reference to masonry values (#44663)](https://github.com/mdn/content/commit/2f710bc43d966483d0204330b14f841b440a6b60) (2026-08-11)

## CSSWG Drafts — cambios en especificaciones
- [[text-decor-4] Added example images for percentage insets](https://github.com/w3c/csswg-drafts/commit/015294489d1da98c14e19f09a2fa453587f352ba) (2026-08-17)
- [[css-sizing-4] Use the %-resolving ancestor, not parent. #13260](https://github.com/w3c/csswg-drafts/commit/f7ac17a5703733e920b390075e953e4850e11171) (2026-08-14)
- [[css-text-4] Post publication bump](https://github.com/w3c/csswg-drafts/commit/1d1378d18c1ff9a02e77abc3424f9f9ef330e6a5) (2026-08-14)
- [[css-text-3] Post publication bump](https://github.com/w3c/csswg-drafts/commit/e2a76bde01e77f714a8f22e9866d8c636b482a6f) (2026-08-14)
- [[css-text] Bikeshed fix](https://github.com/w3c/csswg-drafts/commit/7f20270458a3465247975f580d7c52226489d1fc) (2026-08-14)
- [[css-text-4] Be explicit that we're using the script property and its extension (#14333)](https://github.com/w3c/csswg-drafts/commit/961075636a7da7b46c3e6faf7d33bcec10d3b48f) (2026-08-14)
- [[css-text] Clarify interaction between conditionally and unconditionally hanging](https://github.com/w3c/csswg-drafts/commit/4e4398bb9783a90663b641285d2a179dfd1c54ae) (2026-08-14)
- [[css-text] Tweak example styling](https://github.com/w3c/csswg-drafts/commit/5904384b63222fa3357f36d799a1076b7f1086ca) (2026-08-14)
- [[css-text] extra visuals for example](https://github.com/w3c/csswg-drafts/commit/9883ac53f0b3a09e00707e4794972d4742c2629a) (2026-08-14)
- [Remove flex and grid from margin-trim, as resolved in #13731](https://github.com/w3c/csswg-drafts/commit/16a494b33c886b64488c5c724d5bcbcac2b55ead) (2026-08-06)
- [[css-text-4] hyphenate- properties can't accept negative integers #12517](https://github.com/w3c/csswg-drafts/commit/3bee580622d20043eb9723a942b3acf73a6d7840) (2026-08-13)
- [[css-text-4] Rename avoid-orphans to avoid-short-last-line #11283](https://github.com/w3c/csswg-drafts/commit/a36be2a3c6079aae6a6eeb61baa80bdb3e5d598e) (2026-08-13)
- [[css-overflow-3] Add text rendering example to ink overflow section. #8649 #10066](https://github.com/w3c/csswg-drafts/commit/a2269e25513e5915de6c5196029fee5d7e39ee29) (2026-08-13)
- [[css-text] Update letter-spacing example to newest spec](https://github.com/w3c/csswg-drafts/commit/0a4eb5b685fa7646d41239893427c513fd5c2754) (2026-08-13)
- [[css-text-4] Exclude Hangul (and all Wide characters) from non-ideographic letters #9979](https://github.com/w3c/csswg-drafts/commit/067ad409711bbe6dde4f401dd0b152cd766cbbf3) (2026-08-13)
- [[css-text-3][css-text-4][editorial] Fix bikeshed links](https://github.com/w3c/csswg-drafts/commit/4f8fc6966b36ff70bd9f6568b2a3b353dabce014) (2026-08-13)
- [[css-text-4] Move definitions to the section where they're used](https://github.com/w3c/csswg-drafts/commit/09edb4dd7a908d3c8e219aa9b5cbd88888f340cc) (2026-08-13)
- [[css-text] Fix markup](https://github.com/w3c/csswg-drafts/commit/8808757cbc5b4ef902cd786efc49edb93ccb372d) (2026-08-13)
- [Ensure vt scope qualifies for layout containment (#14327)](https://github.com/w3c/csswg-drafts/commit/85533a87cb020d6f2ffd6e718506a78f0902e169) (2026-08-13)
- [[css-values-5][editorial] Give an informative mention of the element-scoped behavior in functions.](https://github.com/w3c/csswg-drafts/commit/f857f237909fcde8987ff929be85eee4285ecf36) (2026-08-12)
- [[css-text-4] Add bidi example for text-autospace #10803](https://github.com/w3c/csswg-drafts/commit/2c10daaaeccb536d0b5fe77a66e2123229f07ef3) (2026-08-12)
- [[css-text-4] plain-text copy&paste and text-autospace](https://github.com/w3c/csswg-drafts/commit/45b1ed082f52e1fcd77370f83d5fde400c27ab70) (2026-08-12)
- [[css-text-4][editorial] Reorder dfns and fix wording](https://github.com/w3c/csswg-drafts/commit/531871bd9d8b81d51ac9e24d87767c35407f9cfb) (2026-08-12)
- [[css-text-3][css-text-4][editorial] Move paragraph](https://github.com/w3c/csswg-drafts/commit/9c34dbecefe8c22e612c8c338a7372b7987b5cb2) (2026-08-12)
- [[css-text-3][css-text-4] Switch letter-spacing from between letters to around letters #10193 (#14315)](https://github.com/w3c/csswg-drafts/commit/1fa76c0ae9b5f76456504caf6f373dcce84a525b) (2026-08-12)
