---
title: "Cheatsheet: CSS Grid"
description: Chuleta de referencia rápida con las propiedades de CSS Grid, sus valores posibles y qué hace cada uno en una línea.
---

Chuleta de referencia rápida con las propiedades de CSS Grid, sus valores posibles y qué hace cada uno en una línea. Está pensada para consultarla mientras escribes CSS —sin explicaciones largas—, no para aprender el modelo desde cero: si necesitas entender el *por qué* detrás de cada propiedad, la [guía completa de CSS Grid](../layout/grid) cubre eso en profundidad.

## Propiedades del contenedor grid

Se aplican al elemento que recibe `display: grid` (o `inline-grid`). Definen la retícula y controlan cómo se distribuyen y alinean sus hijos directos (los *grid items*).

### `display`

| Valor | Descripción |
|---|---|
| `grid` | Convierte al elemento en contenedor grid de tipo bloque; los hijos directos pasan a ser grid items |
| `inline-grid` | Igual que `grid`, pero el propio contenedor se comporta como una caja `inline` de cara al resto del documento |

### `grid-template-columns` / `grid-template-rows`

Definen los *tracks* (pistas: filas o columnas) explícitos de la retícula, separados por espacios.

| Valor | Descripción |
|---|---|
| `none` (inicial) | Sin retícula explícita en ese eje; el posicionamiento se resuelve en la retícula implícita |
| `<length>` / `<percentage>` (p. ej. `200px`, `25%`) | Tamaño fijo para ese track |
| `<flex>` (p. ej. `1fr`) | Fracción del espacio libre restante, repartida proporcionalmente entre los tracks en `fr` |
| `auto` / `min-content` / `max-content` | Tamaño según el contenido del track |
| `minmax(min, max)` | Acota el tamaño del track entre un mínimo y un máximo |
| `repeat(<n> \| auto-fill \| auto-fit, <track-size>)` | Repite un patrón de tracks; con `auto-fill`/`auto-fit` el navegador calcula cuántas repeticiones caben según el espacio disponible |
| `[<line-name>]` | Nombre de línea opcional entre corchetes, antes de un track, para referenciarlo luego en `grid-column`/`grid-row` |
| `subgrid` | El grid anidado reutiliza los tracks del grid padre en ese eje, en vez de crear tracks propios |

`auto-fill` y `auto-fit` calculan el mismo número de repeticiones, pero se comportan distinto con los tracks que quedan sin ningún item dentro: `auto-fill` los conserva con su tamaño (quedan huecos vacíos visibles), mientras que `auto-fit` los colapsa a `0px` y deja que los demás tracks —normalmente los definidos en `fr`, como en `minmax(150px, 1fr)`— absorban ese espacio sobrante. Por eso `auto-fit` es la opción habitual para columnas que deben estirarse hasta ocupar todo el ancho disponible.

### `grid-template-areas`

| Valor | Descripción |
|---|---|
| `none` (inicial) | Sin áreas nombradas |
| `"<string> <string> …"` | Cada string es una fila; cada palabra separada por espacio, una celda. Un punto (`.`) marca celda vacía. Todas las strings deben tener el mismo número de celdas, y las celdas de un mismo nombre deben formar un rectángulo perfecto |

### `gap` / `row-gap` / `column-gap`

| Sintaxis | Descripción |
|---|---|
| `gap: <valor>` | Mismo espacio entre todas las filas y todas las columnas |
| `gap: <fila> <columna>` | Define `row-gap` y `column-gap` por separado, en ese orden |
| `row-gap: <valor>` | Solo el espacio entre filas (inicial `normal`, equivale a `0`) |
| `column-gap: <valor>` | Solo el espacio entre columnas (inicial `normal`, equivale a `0`) |

No añade espacio en los bordes exteriores del grid; se resta del espacio disponible antes de repartir los tracks en `fr`.

### `justify-items` / `align-items`

Alinean **cada item dentro de su propia celda o área**. `justify-items` actúa en el eje en línea (horizontal, en modo de escritura habitual); `align-items`, en el eje de bloque (vertical).

| Valor | Descripción |
|---|---|
| `normal` (inicial de `align-items`) | En grid se comporta como `stretch`, salvo en cajas con `aspect-ratio` o tamaño intrínseco, donde se comporta como `start` |
| `stretch` | El item ocupa todo el ancho/alto de su celda (si no tiene tamaño explícito) |
| `start` / `end` | Alinea el item al inicio/final de su celda en ese eje |
| `center` | Centra el item dentro de su celda |
| `self-start` / `self-end` | Alinea respecto al borde de inicio/final propio del item, según su modo de escritura individual |
| `left` / `right` (solo `justify-items`) | Alinea hacia el lado físico izquierdo/derecho de la celda |
| `baseline` / `first baseline` / `last baseline` | Alinea los items por la línea base de su contenido |
| `legacy` (inicial formal de `justify-items`) | Valor de compatibilidad pensado para replicar el comportamiento histórico del atributo HTML `align` y del elemento `<center>`; usado solo (sin `left`/`right`/`center`) se comporta igual que `normal`. Combinado (`legacy left`/`right`/`center`) además hace que ese valor se transmita a los descendientes que usen `justify-self: auto`, algo que no ocurre con la herencia normal de CSS |

### `justify-content` / `align-content`

Distribuyen el espacio libre **de toda la retícula** dentro del contenedor, cuando el tamaño total de los tracks es menor que el del contenedor. `justify-content` reparte las columnas; `align-content`, las filas.

| Valor | Descripción |
|---|---|
| `normal` (inicial) | En grid equivale a `stretch` (solo afecta a tracks con tamaño `auto`); si ningún track es `auto` —el caso más común, con `fr`, `px`, `minmax()`, etc.— no hay tracks que estirar y el resultado visual es como `start` |
| `start` / `end` | Agrupa los tracks al inicio/final de ese eje |
| `center` | Agrupa los tracks en el centro |
| `stretch` | Los tracks con tamaño `auto` se estiran para repartirse todo el espacio disponible |
| `space-between` | Primer y último track pegados a los extremos; el resto del espacio se reparte igual entre huecos |
| `space-around` | Cada track recibe el mismo espacio a su alrededor |
| `space-evenly` | Todos los huecos, incluidos los extremos, quedan exactamente iguales |
| `left` / `right` (solo `justify-content`) | Agrupa los tracks hacia el lado físico izquierdo/derecho |
| `baseline` / `first baseline` / `last baseline` | Alinea por la línea base (poco habitual en grid) |

### `place-items` (shorthand)

Combina `align-items` y `justify-items` en una sola declaración.

| Sintaxis | Descripción |
|---|---|
| `place-items: <align-items>` | Aplica el mismo valor a `align-items` y `justify-items` |
| `place-items: <align-items> <justify-items>` | Primer valor para `align-items` (eje de bloque), segundo para `justify-items` (eje en línea) |

### `place-content` (shorthand)

Combina `align-content` y `justify-content` en una sola declaración.

| Sintaxis | Descripción |
|---|---|
| `place-content: <align-content>` | Aplica el mismo valor a `align-content` y `justify-content`, siempre que ese valor sea válido para ambas propiedades |
| `place-content: <align-content> <justify-content>` | Primer valor para `align-content` (eje de bloque), segundo para `justify-content` (eje en línea) |

### `grid-auto-flow`

Controla en qué dirección se generan y rellenan los tracks **implícitos** (los que el navegador crea automáticamente cuando hay más items de los que caben en la retícula explícita).

| Valor | Descripción |
|---|---|
| `row` (inicial) | Coloca los items rellenando cada fila; añade filas nuevas si hace falta |
| `column` | Coloca los items rellenando cada columna; añade columnas nuevas si hace falta |
| `dense` (combinable: `row dense`, `column dense`) | Activa el empaquetado denso: rellena huecos anteriores con items posteriores más pequeños, aunque altere el orden visual respecto al DOM |

### `grid-auto-rows` / `grid-auto-columns`

Definen el tamaño de los tracks **implícitos** generados por `grid-auto-flow` (o por un item posicionado fuera de la retícula explícita).

| Valor | Descripción |
|---|---|
| `auto` (inicial) | El track implícito se dimensiona según su contenido |
| `<length>` / `<percentage>` / `<flex>` | Tamaño fijo, porcentual o en `fr` para todo track implícito |
| `min-content` / `max-content` | Tamaño según el contenido mínimo/máximo |
| `minmax(min, max)` | Acota el tamaño del track implícito entre dos límites |
| `<track-size> <track-size> …` | Varios valores definen un patrón que se repite en cada track implícito sucesivo |

## Propiedades de los items grid

Se aplican a los hijos directos de un contenedor grid y controlan su posición y alineación individual.

### `grid-column` / `grid-row`

Shorthands de `grid-column-start`/`grid-column-end` y `grid-row-start`/`grid-row-end`. Posicionan el item por número de línea.

| Valor | Descripción |
|---|---|
| `auto` (inicial) | Colocación automática según el algoritmo de flujo del grid (`grid-auto-flow`) |
| `<línea>` (p. ej. `grid-column: 2`) | El item empieza en esa línea; si no se indica el final, ocupa un único track |
| `<línea-inicio> / <línea-fin>` (p. ej. `1 / 4`) | El item se extiende desde una línea hasta la otra (sin incluir la línea final) |
| `span <n>` (p. ej. `span 2`) | El item ocupa `n` tracks a partir de donde se colocaría automáticamente, en vez de indicar la línea final |
| `<línea> / span <n>` | Empieza en una línea concreta y se extiende `n` tracks |
| `-1`, `-2`… | Números negativos cuentan las líneas desde el final de la retícula explícita (`-1` es siempre la última línea) |
| `<line-name>` | Nombre de línea definido con corchetes en `grid-template-columns`/`rows`, en vez de un número |

### `grid-area`

| Sintaxis | Descripción |
|---|---|
| `grid-area: <nombre>` | Asigna el item a una región nombrada en `grid-template-areas`; el nombre debe coincidir exactamente |
| `grid-area: <fila-inicio> / <col-inicio> / <fila-fin> / <col-fin>` | Shorthand de cuatro valores equivalente a `grid-row-start`/`grid-column-start`/`grid-row-end`/`grid-column-end`, en ese orden |
| `auto` (inicial) | Sin área asignada; el item se posiciona según `grid-column`/`grid-row` o de forma automática |

### `justify-self` / `align-self`

Sobrescriben, para un item concreto, el valor de `justify-items`/`align-items` heredado del contenedor.

| Valor | Descripción |
|---|---|
| `auto` (inicial) | Usa el valor de `justify-items`/`align-items` del contenedor padre |
| `normal` | En grid, se comporta como `stretch` salvo en cajas con `aspect-ratio` o tamaño intrínseco, donde se comporta como `start` |
| `stretch` | El item ocupa todo el ancho/alto de su celda (si no tiene tamaño explícito) |
| `start` / `end` | Alinea el item al inicio/final de su celda |
| `center` | Centra el item dentro de su celda |
| `self-start` / `self-end` | Alinea respecto al borde de inicio/final propio del item |
| `left` / `right` (solo `justify-self`) | Alinea hacia el lado físico izquierdo/derecho de la celda |
| `baseline` / `first baseline` / `last baseline` | Alinea el item por la línea base de su contenido |

### `place-self` (shorthand)

Combina `align-self` y `justify-self` en una sola declaración.

| Sintaxis | Descripción |
|---|---|
| `place-self: <align-self>` | Aplica el mismo valor a `align-self` y `justify-self` |
| `place-self: <align-self> <justify-self>` | Primer valor para `align-self` (eje de bloque), segundo para `justify-self` (eje en línea) |

## Ejemplo combinado

```css
.wrapper {
  display: grid;
  grid-template-columns: 200px repeat(auto-fit, minmax(150px, 1fr));
  grid-template-rows: 80px 1fr 60px;
  grid-template-areas:
    "sidebar head head"
    "sidebar main main"
    "sidebar foot foot";
  gap: 1rem;
  justify-items: stretch;
  align-content: start;
}

.sidebar { grid-area: sidebar; }
.header  { grid-area: head; }
.main    { grid-area: main; }
.footer  { grid-area: foot; }

.destacado {
  grid-column: span 2; /* ocupa 2 columnas a partir de su posición automática */
  justify-self: center;
  align-self: start;
}
```

`.wrapper` combina una columna fija (`200px`) con columnas flexibles que se autoajustan (`repeat(auto-fit, minmax(150px, 1fr))`), y usa `grid-template-areas` para nombrar cada región en lugar de contar líneas. `.destacado` no participa del mapa de áreas: se posiciona por líneas (`grid-column: span 2`) y ajusta su propia alineación con `justify-self`/`align-self`, sin afectar al resto de items.

:::tip[Soporte de navegadores]
El núcleo de CSS Grid (`display: grid`, `grid-template-columns`/`rows`, `grid-template-areas`, `gap`, posicionamiento por líneas, `justify-*`/`align-*`) tiene un **95.36 %** de soporte global, disponible en Chrome 57+, Firefox 52+, Safari 10.1+ y Edge 16+; Internet Explorer 10/11 solo implementó una versión previa y parcial de la especificación. Los shorthands `place-items`/`place-content`/`place-self` llegaron algo después (Chrome 59+, Firefox 45+, Safari 11+, Edge 79+), con un **94.96 %** de soporte global. Consulta el detalle en [caniuse.com/css-grid](https://caniuse.com/css-grid) y [caniuse.com/mdn-css_properties_place-items](https://caniuse.com/mdn-css_properties_place-items).
:::

:::tip[Soporte de navegadores: `subgrid`]
El valor `subgrid` para `grid-template-columns`/`grid-template-rows` tiene un soporte más limitado (**90.49 %** global): Firefox 71+, Safari 16+ y Chrome/Edge 117+ (en Chrome 114-116 existía tras una flag experimental). Si necesitas dar soporte a versiones anteriores, revisa [caniuse.com/css-subgrid](https://caniuse.com/css-subgrid) antes de depender de él sin alternativa.
:::

## Ver también

- [CSS Grid: guía completa](../layout/grid)
- [Cheatsheet: Flexbox](flexbox-cheatsheet)
- [Display y flujo normal](../layout/display-y-flujo-normal)
- [El modelo de caja](../fundamentos/modelo-de-caja)

## Fuentes

- [MDN: display](https://developer.mozilla.org/en-US/docs/Web/CSS/display)
- [MDN: grid-template-columns](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-template-columns)
- [MDN: grid-template-rows](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-template-rows)
- [MDN: grid-template-areas](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-template-areas)
- [MDN: gap](https://developer.mozilla.org/en-US/docs/Web/CSS/gap)
- [MDN: justify-items](https://developer.mozilla.org/en-US/docs/Web/CSS/justify-items)
- [MDN: align-items](https://developer.mozilla.org/en-US/docs/Web/CSS/align-items)
- [MDN: justify-content](https://developer.mozilla.org/en-US/docs/Web/CSS/justify-content)
- [MDN: align-content](https://developer.mozilla.org/en-US/docs/Web/CSS/align-content)
- [MDN: place-items](https://developer.mozilla.org/en-US/docs/Web/CSS/place-items)
- [MDN: place-content](https://developer.mozilla.org/en-US/docs/Web/CSS/place-content)
- [MDN: place-self](https://developer.mozilla.org/en-US/docs/Web/CSS/place-self)
- [MDN: grid-auto-flow](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-auto-flow)
- [MDN: grid-auto-rows](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-auto-rows)
- [MDN: grid-auto-columns](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-auto-columns)
- [MDN: grid-column](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-column)
- [MDN: grid-row](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-row)
- [MDN: grid-area](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-area)
- [MDN: justify-self](https://developer.mozilla.org/en-US/docs/Web/CSS/justify-self)
- [MDN: align-self](https://developer.mozilla.org/en-US/docs/Web/CSS/align-self)
- [MDN: Subgrid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Subgrid)
- [W3C: CSS Grid Layout Module Level 1](https://www.w3.org/TR/css-grid-1/)
- [W3C: CSS Box Alignment Module Level 3](https://www.w3.org/TR/css-align-3/)
- [caniuse: CSS Grid Layout](https://caniuse.com/css-grid)
- [caniuse: CSS Subgrid](https://caniuse.com/css-subgrid)
- [caniuse: place-items](https://caniuse.com/mdn-css_properties_place-items)
