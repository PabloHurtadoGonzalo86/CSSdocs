# CSS Grid: guía completa

CSS Grid Layout es el sistema de maquetación **bidimensional** de CSS: a diferencia de Flexbox, que resuelve una sola dimensión (fila *o* columna) a la vez, Grid te permite definir filas y columnas simultáneamente y colocar elementos en cualquier punto de esa retícula. Es la herramienta natural para estructuras de página completas (cabecera, barra lateral, contenido, pie) y para cualquier componente donde el alineado entre filas y columnas importa más que el orden de los elementos en el HTML.

## Activar Grid: `display: grid`

Un contenedor de grid se crea aplicando `display: grid` (o `display: inline-grid`, que genera una caja de tipo *inline* en lugar de *block*) a un elemento. En cuanto lo haces, **todos sus hijos directos** pasan a ser *grid items*, sin necesidad de ninguna otra declaración:

```css
.wrapper {
  display: grid;
}
```

Los descendientes de esos hijos (nietos del contenedor) siguen fluyendo en flujo normal, salvo que ese hijo se convierta a su vez en un contenedor de grid o flex.

## Definir columnas y filas: `grid-template-columns` / `grid-template-rows`

Sin más declaraciones, un contenedor `grid` genera una única columna y coloca cada hijo en su propia fila implícita. Para definir una retícula explícita, usas `grid-template-columns` y `grid-template-rows`, indicando el tamaño de cada *track* (pista, es decir, cada fila o columna) separado por espacios:

```css
.wrapper {
  display: grid;
  grid-template-columns: 200px 200px 200px; /* 3 columnas de 200px */
  grid-template-rows: 100px 300px;          /* 2 filas */
}
```

El valor inicial de ambas propiedades es `none`: sin retícula explícita, todo el posicionamiento ocurre en la retícula implícita (lo vemos más abajo).

### La unidad `fr`: repartir el espacio disponible

`fr` es una unidad especial de Grid que representa una **fracción del espacio libre** del contenedor. No es un tamaño fijo: el navegador primero reserva el espacio para los tracks de tamaño fijo (`px`, `%`, contenido...) y reparte lo que sobra entre los tracks en `fr`, proporcionalmente a su factor:

```css
.wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr; /* 3 columnas iguales, repartiendo el 100% del ancho */
}
```

```css
.wrapper {
  display: grid;
  grid-template-columns: 500px 1fr 2fr; /* fija + dos flexibles en proporción 1:2 */
}
```

Puedes mezclar unidades libremente en la misma declaración. Un detalle que conviene tener claro: cuando `fr` aparece fuera de `minmax()`, MDN señala que implica un mínimo automático equivalente a `minmax(auto, <flex>)`; en la práctica esto significa que un track en `fr` nunca se encogerá por debajo del contenido mínimo que contiene, aunque matemáticamente le "tocara" menos espacio.

!!! tip "`fr` no es lo mismo que `%`"

    Un porcentaje se calcula sobre el tamaño total del contenedor; `fr` se calcula sobre el espacio que **queda libre** después de restar los tracks de tamaño fijo y los gaps. Por eso `grid-template-columns: 100px 1fr` reparte en la segunda columna todo el ancho menos esos 100px, mientras que un `%` tendría que calcularse manualmente.

### `repeat()`: evitar repetición manual

Cuando varios tracks comparten el mismo tamaño (o un mismo patrón se repite), `repeat()` evita escribirlo a mano:

```css
.wrapper {
  grid-template-columns: repeat(3, 1fr); /* equivalente a: 1fr 1fr 1fr */
}

.wrapper {
  /* un patrón que se repite: 1fr 2fr 1fr 2fr 1fr 2fr */
  grid-template-columns: repeat(3, 1fr 2fr);
}
```

`repeat()` acepta también dos palabras clave especiales en lugar de un número fijo de repeticiones, muy útiles para retículas responsivas sin media queries:

- **`auto-fill`**: crea tantos tracks del tamaño indicado como quepan en el contenedor, dejando tracks vacíos (pero reservando su espacio) si sobra sitio.
- **`auto-fit`**: igual que `auto-fill`, pero los tracks vacíos se colapsan a `0`, permitiendo que los tracks con contenido se expandan para ocupar ese espacio.

```css
.wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}
```

Este patrón —`repeat(auto-fit, minmax(...))`— es probablemente el idioma más usado de Grid para crear una cuadrícula de tarjetas que se reacomoda sola según el ancho disponible, sin escribir ni un solo `@media`.

### `minmax()`: un rango de tamaño para el track

`minmax(min, max)` define un track cuyo tamaño estará siempre entre esos dos límites: nunca más pequeño que `min` ni más grande que `max`.

```css
.wrapper {
  display: grid;
  grid-template-columns: minmax(150px, 1fr) 3fr;
}
```

Aquí la primera columna nunca bajará de 150px (evitando que el contenido se aplaste), pero podrá crecer como `1fr` si hay espacio de sobra. Como valor de `max` también puedes usar `auto`, `max-content` o `min-content`:

```css
.wrapper {
  grid-auto-rows: minmax(100px, auto); /* filas de al menos 100px, que crecen con el contenido */
}
```

!!! tip "Soporte de navegadores"

    `display: grid`, `fr`, `repeat()` y `minmax()` forman parte del núcleo de CSS Grid Layout, con un **95.36 %** de soporte global y compatibilidad en todos los navegadores modernos (Chrome 57+, Firefox 52+, Safari 10.1+, Edge 16+). Internet Explorer 10/11 solo implementó una versión previa y parcial de la especificación. Consulta la tabla completa en [caniuse.com/css-grid](https://caniuse.com/css-grid).

## Espaciado entre tracks: `gap`

`gap` (con sus longhands `row-gap` y `column-gap`) define el espacio entre filas y columnas, **sin añadir espacio en los bordes exteriores** del grid (a diferencia de un margin en cada item):

```css
.wrapper {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  row-gap: 1rem;    /* espacio entre filas */
  column-gap: 2rem; /* espacio entre columnas */
  /* o el shorthand, en orden row-gap / column-gap: */
  gap: 1rem 2rem;
  /* con un solo valor se aplica a ambos ejes */
  gap: 1rem;
}
```

El valor inicial de `row-gap`/`column-gap` es `normal`, que en Grid se resuelve como `0`. Estos gaps se comportan como si fueran tracks vacíos a efectos de reparto de espacio: se restan del espacio disponible **antes** de calcular cuánto ocupa cada `fr`.

!!! tip "Soporte de navegadores"

    `gap` (junto a `row-gap`/`column-gap`) es hoy una propiedad general de layout: funciona en Grid, Flexbox y en el layout multi-columna. En versiones antiguas de la especificación esta propiedad se llamaba `grid-gap`, y por compatibilidad los navegadores siguen aceptando `grid-gap`, `grid-row-gap` y `grid-column-gap` como alias de `gap`, `row-gap` y `column-gap`. En Grid el soporte es universal desde los mismos navegadores que soportan Grid; para su uso en Flexbox conviene revisar [caniuse.com/flexbox-gap](https://caniuse.com/flexbox-gap) si necesitas dar soporte a navegadores muy antiguos (ahí `gap` llegó más tarde: Chrome/Edge 84, Firefox 63, Safari 14.1).

## Áreas nombradas: `grid-template-areas` y `grid-area`

`grid-template-areas` permite "dibujar" la retícula con nombres, directamente en el CSS, lo que hace el layout mucho más legible que razonar solo con números de línea. Cada string es una fila, y cada palabra separada por espacios dentro del string es una celda de esa fila:

```css
.page {
  display: grid;
  grid-template-columns: 150px 1fr;
  grid-template-rows: 50px 1fr 30px;
  grid-template-areas:
    "head head"
    "nav  main"
    ".    foot";
}

header { grid-area: head; }
nav    { grid-area: nav; }
main   { grid-area: main; }
footer { grid-area: foot; }
```

Reglas clave que hay que respetar:

- Todas las strings deben tener **el mismo número de columnas** (el mismo número de palabras).
- Las celdas que comparten un mismo nombre deben formar **un rectángulo perfecto**; si no es así (por ejemplo, una forma en L), la declaración completa se considera inválida y se ignora.
- Un punto (`.`) representa una celda vacía, sin nombre; puedes repetirlo (`...`) y sigue contando como una única celda vacía.
- Cada hijo se asigna a un área con `grid-area: <nombre>`, y ese nombre debe coincidir **exactamente** con el usado en `grid-template-areas`.

```css
.wrapper {
  display: grid;
  grid-template-areas:
    "a a ."
    "a a ."
    ".  b c";
}
```

`grid-template-areas` es especialmente útil para reordenar visualmente un layout en distintos breakpoints sin tocar el HTML: basta con redefinir el "mapa" de áreas dentro de una media query.

## Posicionamiento por líneas: `grid-column` / `grid-row`

Además de las áreas nombradas, Grid numera automáticamente las **líneas** que separan los tracks (en un grid de 3 columnas hay 4 líneas de columna), empezando en 1. Puedes colocar un elemento indicando entre qué líneas debe extenderse con `grid-column` y `grid-row` (shorthands de `grid-column-start`/`grid-column-end` y `grid-row-start`/`grid-row-end`):

```css
.item {
  grid-column: 1 / 4; /* desde la línea 1 hasta la línea 4: ocupa 3 columnas */
  grid-row: 1 / 3;     /* desde la línea 1 hasta la línea 3: ocupa 2 filas */
}
```

La palabra clave **`span`** indica "extiéndete N tracks" en lugar de dar la línea final explícita, lo que suele ser más fácil de leer y mantener:

```css
.item {
  grid-column: span 2; /* ocupa 2 columnas a partir de donde se colocaría automáticamente */
  grid-row: 1 / span 3; /* desde la línea 1, extendiéndose 3 filas */
}
```

También puedes contar líneas **desde el final** con números negativos: `-1` es siempre la última línea de la retícula explícita, `-2` la penúltima, etc. Es muy práctico para "hasta el final" sin saber cuántas columnas hay:

```css
.item {
  grid-column: 2 / -1; /* desde la segunda línea hasta la última */
}
```

Si solo defines el inicio, el final se calcula como `auto` (el item ocupa un único track). El valor inicial de las cuatro longhands es `auto`, es decir, colocación automática según el algoritmo de flujo del grid.

`grid-area` también admite una forma abreviada de cuatro valores equivalente a estas cuatro propiedades, en el orden `grid-row-start / grid-column-start / grid-row-end / grid-column-end`:

```css
.item {
  grid-area: 2 / 1 / 3 / 3; /* fila 2→3, columna 1→3 */
}
```

## Grid explícito vs. implícito

El **grid explícito** es el que defines tú con `grid-template-columns`/`grid-template-rows` (o `grid-template-areas`). Pero en cuanto colocas más elementos de los que caben en esa retícula —o posicionas un item fuera de sus límites, por ejemplo con `grid-row: 5`—, el navegador genera automáticamente **tracks implícitos** para acomodarlos. Por defecto, esos tracks implícitos se dimensionan automáticamente según su contenido (`auto`), pero puedes controlarlo con `grid-auto-rows` y `grid-auto-columns`:

```css
.wrapper {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* explícito: 3 columnas */
  grid-auto-rows: 150px; /* toda fila implícita medirá 150px */
}
```

```css
.wrapper {
  display: grid;
  grid-auto-rows: minmax(100px, auto); /* filas implícitas: mínimo 100px, crecen con el contenido */
}
```

Por su parte, `grid-auto-flow` controla **en qué dirección** se generan y rellenan esos tracks implícitos cuando un item no tiene una posición explícita:

```css
.wrapper {
  grid-auto-flow: row;    /* valor inicial: rellena por filas, añadiendo filas nuevas si hace falta */
  grid-auto-flow: column; /* rellena por columnas, añadiendo columnas nuevas */
  grid-auto-flow: row dense; /* con "dense", rellena huecos anteriores aunque altere el orden visual */
}
```

El modificador `dense` activa un algoritmo de empaquetado denso: en lugar de avanzar siempre hacia delante (dejando huecos si un item grande no cabe), el navegador retrocede para rellenar huecos con items posteriores más pequeños. Esto puede producir un layout más compacto, pero también puede alterar el orden visual respecto al orden del DOM, lo que tiene implicaciones de accesibilidad (el orden de foco/lectura sigue el DOM, no el visual) y conviene usarlo con cuidado.

## Alineación: items vs. contenido

Grid separa claramente dos preguntas distintas, y confundirlas es una fuente habitual de bugs:

1. **¿Cómo se alinea cada item dentro de su propia celda/área?** → `justify-items`, `align-items` (en el contenedor, para todos los items) y `justify-self`, `align-self` (en un item concreto, sobrescribiendo lo anterior).
2. **¿Cómo se alinea la retícula completa dentro del contenedor, cuando sobra espacio?** → `justify-content`, `align-content` (en el contenedor).

```css
.wrapper {
  display: grid;
  grid-template-columns: repeat(3, 100px);
  justify-items: center; /* cada item se centra horizontalmente en su celda */
  align-items: start;    /* cada item se alinea arriba en su celda */
}

.item-destacado {
  justify-self: end;  /* este item, en concreto, se pega a la derecha de su celda */
  align-self: stretch;
}
```

`align-items` vale `normal` por defecto; el valor inicial formal de `justify-items` es `legacy` (una palabra clave heredada por compatibilidad que, salvo en casos muy concretos, se comporta igual que `normal`). En ambos casos, `normal` se resuelve en un contexto de grid como `stretch` —los items ocupan todo el ancho/alto de su celda—, **excepto** en cajas con `aspect-ratio` o con un tamaño intrínseco (por ejemplo, una imagen), donde se comportan como `start`. Esto explica por qué, si colocas una `<img>` directamente como grid item, no se estira sola para llenar la celda aunque no hayas tocado la alineación. `justify-self`/`align-self` valen `auto` por defecto, lo que significa "usa el valor heredado de `justify-items`/`align-items`".

```css
.wrapper {
  display: grid;
  grid-template-columns: repeat(3, 100px);
  grid-template-rows: repeat(3, 100px);
  width: 500px; /* el grid mide menos que el contenedor: sobra espacio */
  justify-content: space-between; /* reparte los tracks horizontalmente */
  align-content: center;          /* centra el bloque de tracks verticalmente */
}
```

`justify-content`/`align-content` solo tienen efecto visible cuando el tamaño total de los tracks es **menor** que el del contenedor (si no sobra espacio, no hay nada que redistribuir). Ambas aceptan, entre otros, los valores `start`, `end`, `center`, `stretch`, `space-between`, `space-around` y `space-evenly`.

Para los casos más frecuentes existen los shorthands `place-items` (combina `align-items` y `justify-items`) y `place-content` (combina `align-content` y `justify-content`), además de `place-self` para un item concreto:

```css
.wrapper {
  display: grid;
  place-items: center; /* centra cada item en su celda, en ambos ejes, en una sola línea */
}
```

`place-items: center;` en un contenedor de una sola celda es, de hecho, una de las formas más citadas de centrar un elemento en CSS moderno.

## Introducción a subgrid

Cuando conviertes un grid item en un grid container anidado (`display: grid` dentro de otro `display: grid`), por defecto ese grid interno es **completamente independiente**: define sus propios tracks, sin relación con los del grid exterior. Esto dificulta alinear el contenido anidado con el resto de la página —por ejemplo, que las tarjetas de una cuadrícula compartan las mismas líneas verticales que la cabecera de la página, aunque tengan alturas de contenido distintas.

El valor `subgrid` para `grid-template-columns` y/o `grid-template-rows` resuelve justo eso: en lugar de crear tracks nuevos, el grid anidado **reutiliza los tracks del grid padre** en el rango de líneas que ocupa.

```css
.grid {
  display: grid;
  grid-template-columns: repeat(9, 1fr);
  grid-template-rows: repeat(4, minmax(100px, auto));
}

.item {
  display: grid;
  grid-column: 2 / 7; /* ocupa 5 columnas del grid padre */
  grid-row: 2 / 4;
  grid-template-columns: subgrid; /* hereda esas 5 columnas del padre */
  grid-template-rows: subgrid;
}

.subitem {
  grid-column: 3 / 6; /* se alinea con las líneas del grid padre, no con líneas propias */
}
```

Un par de matices importantes:

- La numeración de líneas **se reinicia** dentro del subgrid: la línea 1 del subgrid es la primera línea del rango que ocupa, no la línea 1 del grid padre (aunque los nombres de línea definidos en el padre sí se heredan y se pueden usar).
- Un subgrid **no genera tracks implícitos** en la dimensión subgrideada: si colocas más items de los que caben en el rango heredado, se desbordarán en el último track en lugar de crear filas/columnas nuevas. Si necesitas autoubicación con un número de items desconocido, usa `grid-template-rows`/`columns` normal (con `grid-auto-rows`) en vez de `subgrid` en esa dimensión.

!!! tip "Soporte de navegadores"

    `subgrid` alcanza ya un **90.49 %** de soporte global: disponible en Firefox desde la versión 71, en Safari desde la 16.0 y en Chrome/Edge desde la versión 117 (en Chrome 114-116 existía tras una flag experimental). Antes de usarlo como base de un layout crítico, comprueba el estado actual y el desglose por versión en [caniuse.com/css-subgrid](https://caniuse.com/css-subgrid).

## Ver también

- [Flexbox](flexbox.md)
- [Display y flujo normal](display-y-flujo-normal.md)
- [Unidades y valores](../fundamentos/unidades.md)
- [Grid — cheatsheet](../cheatsheets/grid-cheatsheet.md)

## Fuentes

- [Basic concepts of grid layout - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Basic_concepts_of_grid_layout)
- [grid-template-columns - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-template-columns)
- [grid-template-rows - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-template-rows)
- [grid-template-areas - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-template-areas)
- [grid-area - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-area)
- [grid-column - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-column)
- [gap - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/gap)
- [grid-auto-flow - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-auto-flow)
- [Aligning items in CSS grid layout - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Box_alignment_in_grid_layout)
- [Subgrid - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Subgrid)
- [CSS Grid Layout - Can I use](https://caniuse.com/css-grid)
- [CSS Subgrid - Can I use](https://caniuse.com/css-subgrid)
