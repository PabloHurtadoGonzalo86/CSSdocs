# Selectores en CSS

Un selector es la parte de una regla CSS que decide **a qué elementos del DOM se les aplica** un bloque de declaraciones. Antes de preocuparte por la cascada, la especificidad o las propiedades modernas, necesitas dominar los selectores: son la herramienta con la que apuntas tus estilos, y elegir el selector equivocado es la causa más habitual de CSS frágil, sobre-específico o difícil de mantener en un proyecto real.

Esta página cubre los selectores base del lenguaje: tipo, clase, ID, universal, atributo, las pseudo-clases y pseudo-elementos más usados, los combinadores y la agrupación con coma. Los selectores más recientes (`:is()`, `:where()`, `:has()`) tienen su propia página en [Selectores modernos](../moderno/selectores-modernos.md), porque merecen una explicación aparte.

## Selectores básicos

### Selector universal (`*`)

Selecciona **cualquier elemento** del documento.

```css
* {
  box-sizing: border-box;
}
```

Es habitual verlo en resets o en el patrón `*, *::before, *::after` para aplicar `box-sizing: border-box` a todo, incluidos los pseudo-elementos generados. Al no filtrar nada, es el selector con la especificidad más baja posible (cuenta como cero para efectos de especificidad).

### Selector de tipo (o de etiqueta)

Selecciona todos los elementos de una etiqueta HTML concreta, usando el nombre del elemento tal cual.

```css
p {
  line-height: 1.6;
}

nav {
  display: flex;
}
```

### Selector de clase (`.clase`)

Selecciona todos los elementos que tengan ese valor en su atributo `class`. Un elemento puede tener varias clases (separadas por espacios en el HTML) y puedes encadenar varios selectores de clase sin espacio para exigir que estén todas presentes a la vez:

```css
.card {
  border-radius: 8px;
}

/* Solo elementos que tengan AMBAS clases */
.card.card--highlighted {
  border-color: orange;
}
```

Es, con diferencia, el selector recomendado para el día a día: no depende de la etiqueta HTML que uses y es fácil de reutilizar y de mantener.

### Selector de ID (`#id`)

Selecciona el elemento cuyo atributo `id` coincide. Como un `id` debe ser único dentro del documento (según el estándar HTML), este selector solo debería apuntar a un único elemento.

```css
#main-nav {
  position: sticky;
  top: 0;
}
```

!!! warning "Úsalo con moderación en CSS de componentes"

    El selector de ID tiene una especificidad muy alta (más que cualquier cantidad de clases), lo que dificulta sobrescribirlo después sin recurrir a más IDs o a `!important`. En la mayoría de proyectos se reserva para anclas de navegación (`href="#seccion"`), hooks de JavaScript o casos muy puntuales, y se prefiere la clase para estilos reutilizables. El detalle de cómo se calcula esa especificidad se explica en [Cascada, especificidad y herencia](cascada-especificidad-herencia.md).

## Selectores de atributo

Seleccionan elementos en función de si tienen un atributo determinado, o de si su valor cumple un patrón concreto.

| Sintaxis | Selecciona | Ejemplo |
|---|---|---|
| `[attr]` | Elementos que tienen el atributo, sea cual sea su valor | `a[title]` — enlaces con `title` |
| `[attr=valor]` | El valor del atributo es exactamente ese | `input[type="email"]` |
| `[attr~=valor]` | El atributo contiene esa palabra dentro de una lista separada por espacios | `[class~="destacado"]` |
| `[attr\|=valor]` | El valor es exactamente ese, o empieza por ese valor seguido de un guion | `[lang\|="es"]` — coincide con `es` y `es-MX` |
| `[attr^=valor]` | El valor **empieza por** ese texto | `a[href^="https://"]` |
| `[attr$=valor]` | El valor **termina en** ese texto | `a[href$=".pdf"]` |
| `[attr*=valor]` | El valor **contiene** ese texto en cualquier posición | `a[href*="ejemplo.com"]` |

```css
/* Enlaces externos que abren PDFs */
a[href^="http"][href$=".pdf"] {
  padding-left: 1.5em;
  background: url("icon-pdf.svg") left center no-repeat;
}

/* Inputs sin atributo "required" */
input:not([required]) {
  border-color: #ccc;
}
```

Los selectores de atributo también admiten un modificador de sensibilidad a mayúsculas/minúsculas, justo antes del corchete de cierre:

```css
/* Coincide con "ejemplo", "Ejemplo", "EJEMPLO"... */
a[href*="ejemplo" i] {
  color: teal;
}

/* Fuerza sensibilidad a mayúsculas aunque el atributo sea case-insensitive por defecto */
a[href*="ABC" s] {
  color: crimson;
}
```

`i` (o `I`) fuerza la comparación **insensible** a mayúsculas/minúsculas (en el rango ASCII); `s` (o `S`) fuerza que sea **sensible**. Esto es útil porque atributos como `class`, `id` o `data-*` son sensibles a mayúsculas por defecto, mientras que algunos atributos HTML predefinidos no lo son.

!!! tip "Soporte de navegadores"

    Los selectores de atributo básicos son compatibles con todos los navegadores modernos desde hace años. El modificador `i` también tiene soporte amplio (Chrome/Edge 49+, Firefox 47+, Safari 9+); revisa [css-case-insensitive en caniuse.com](https://caniuse.com/css-case-insensitive) si necesitas dar soporte a navegadores muy antiguos. El modificador `s`, en cambio, tiene un soporte mucho más limitado: por ahora solo lo implementa Firefox (desde la versión 66); Chrome, Edge y Safari todavía no lo soportan (las peticiones de implementación siguen abiertas). Compruébalo en [el seguimiento del modificador `s` en caniuse.com](https://caniuse.com/mdn-css_selectors_attribute_case_sensitive_modifier) antes de depender de él en producción.

## Combinadores

Un combinador describe la **relación** entre dos selectores: no seleccionan un tipo de elemento nuevo, sino que filtran según su posición respecto a otro elemento.

### Combinador descendiente (espacio)

Selecciona un elemento que esté **en cualquier nivel** dentro de otro (hijo, nieto, bisnieto...).

```css
article p {
  margin-block: 1em;
}
```

Esto aplica a todos los `<p>` dentro de un `<article>`, sin importar cuántos elementos intermedios haya.

### Combinador de hijo directo (`>`)

Selecciona solo los elementos que son **hijos inmediatos** del elemento anterior, no descendientes más profundos.

```css
.menu > li {
  list-style: none;
}
```

Si un `<li>` de `.menu` contiene a su vez un submenú con más `<li>`, esos nietos **no** se ven afectados; solo los `<li>` directamente dentro de `.menu`.

### Combinador de hermano adyacente (`+`)

Selecciona un elemento que sea el **hermano inmediatamente siguiente** de otro (mismo padre, justo después).

```css
h2 + p {
  margin-top: 0;
}
```

Aquí solo el primer `<p>` que viene justo después de un `<h2>` pierde su margen superior; el resto de párrafos no se ven afectados.

### Combinador de hermano general (`~`)

Selecciona todos los elementos que sean hermanos **posteriores** a otro (mismo padre, en cualquier posición después, no necesariamente el inmediato).

```css
h2 ~ p {
  color: #444;
}
```

Todos los `<p>` que aparezcan después de un `<h2>` (dentro del mismo padre), sean o no adyacentes a él, reciben el estilo.

## Agrupación de selectores con coma

Cuando varios selectores comparten exactamente las mismas declaraciones, puedes agruparlos en una lista separada por comas para no repetir el bloque:

```css
h1,
h2,
h3 {
  font-family: "Georgia", serif;
  font-weight: 700;
}
```

Es equivalente a escribir tres reglas idénticas por separado. Cada selector de la lista conserva su propia especificidad de forma independiente (agruparlos no la suma ni la promedia); si te interesa ese detalle, está explicado en [Cascada, especificidad y herencia](cascada-especificidad-herencia.md).

!!! warning "Un selector inválido invalida todo el grupo"

    Por defecto, una lista de selectores separados por coma es "no perdonadora" (*non-forgiving*): si **uno solo** de los selectores del grupo no es válido (por ejemplo, una pseudo-clase mal escrita o no soportada), el navegador descarta **toda la regla**, incluidos los selectores que sí eran correctos. Las pseudo-clases `:is()` y `:where()` (ver [Selectores modernos](../moderno/selectores-modernos.md)) sí crean listas "perdonadoras" que ignoran solo la parte inválida.

## Pseudo-clases

Una pseudo-clase se escribe con dos puntos (`:`) y selecciona elementos según un **estado** o una **posición** que no se puede expresar con el propio marcado (por ejemplo, si el ratón está encima, o si es el primer hijo de su padre).

### Pseudo-clases de interacción

```css
a:hover {
  text-decoration: underline;
}

button:focus {
  outline: 2px solid dodgerblue;
}

button:focus-visible {
  outline: 3px solid dodgerblue;
  outline-offset: 2px;
}
```

- **`:hover`**: mientras el puntero está sobre el elemento.
- **`:focus`**: mientras el elemento tiene el foco del teclado o se ha seleccionado programáticamente, sin importar cómo se obtuvo.
- **`:focus-visible`**: coincide con el elemento enfocado solo cuando el navegador estima que ese foco debería mostrarse visualmente (típicamente navegación por teclado). Es la forma recomendada de estilizar el foco hoy en día, porque evita mostrar un anillo de foco molesto cuando el usuario hace clic con el ratón, pero lo conserva para quien navega con `Tab`.
- **`:focus-within`**: coincide con un elemento cuando él mismo o **cualquiera de sus descendientes** tiene el foco; muy útil para resaltar un `<form>` completo cuando el usuario está escribiendo en uno de sus campos.

!!! tip "Soporte de navegadores"

    `:focus-visible` es *Baseline: Widely available* (ampliamente soportado) desde marzo de 2022. Si necesitas dar soporte a navegadores más antiguos, consulta [css-focus-visible en caniuse.com](https://caniuse.com/css-focus-visible).

### Pseudo-clases estructurales

Seleccionan elementos según su posición entre sus hermanos, sin necesidad de clases adicionales en el HTML.

```css
li:first-child {
  font-weight: bold;
}

li:last-child {
  border-bottom: none;
}

li:only-child {
  list-style: none;
}

/* Filas de tabla alternas (patrón "cebra") */
tr:nth-child(odd) {
  background: #f7f7f7;
}

/* Los tres primeros elementos */
.card:nth-child(-n + 3) {
  order: -1;
}
```

`:nth-child()` acepta la notación **`An+B`** (dos enteros `A` y `B`), o las palabras clave `odd`/`even`:

| Valor | Selecciona |
|---|---|
| `:nth-child(odd)` | 1º, 3º, 5º... |
| `:nth-child(even)` | 2º, 4º, 6º... |
| `:nth-child(2n)` | Igual que `even` |
| `:nth-child(3n)` | 3º, 6º, 9º... |
| `:nth-child(n + 4)` | Desde el 4º en adelante |
| `:nth-child(-n + 3)` | Solo los 3 primeros |

Hay una diferencia importante entre `:nth-child()` y `:nth-of-type()`: el primero cuenta la posición entre **todos** los hermanos, sin importar su etiqueta; el segundo cuenta solo entre los hermanos que comparten el **mismo tipo de elemento**.

```css
/* Cuenta solo entre <p>, ignorando otros elementos hermanos */
p:nth-of-type(2) {
  color: green;
}
```

`:first-of-type` y `:last-of-type` funcionan igual que `:first-child`/`:last-child` pero también filtrando por tipo de etiqueta.

`:nth-child()` (y `:nth-last-child()`) admiten además la cláusula opcional **`of <selector>`**, que primero filtra los hermanos que cumplen ese selector y luego cuenta la posición solo entre ellos:

```css
/* El primer <li> que tenga la clase "destacado", cuente la posición que cuente */
li:nth-child(1 of .destacado) {
  color: purple;
}
```

Esto es distinto de `li.destacado:nth-child(1)`, que solo coincidiría si ese elemento destacado fuera además, literalmente, el primer hijo de su padre.

!!! tip "Soporte de navegadores"

    La cláusula `of <selector>` en `:nth-child()`/`:nth-last-child()` tiene ya soporte amplio en navegadores modernos. El caso curioso es Safari, que la soporta desde Safari 9 (WebKit se adelantó muchos años); Chrome y Edge se sumaron en la versión 111 y Firefox en la 113. Aun así, conviene comprobarlo si tu proyecto da soporte a versiones antiguas: [css-nth-child-of en caniuse.com](https://caniuse.com/css-nth-child-of).

### La pseudo-clase de negación `:not()`

`:not()` selecciona elementos que **no** coinciden con el selector (o la lista de selectores) que recibe como argumento.

```css
/* Todos los botones excepto los deshabilitados */
button:not(:disabled):hover {
  cursor: pointer;
}

/* Todos los párrafos excepto los que tengan estas dos clases */
p:not(.nota, .cita) {
  color: #222;
}
```

En CSS moderno (Selectors Level 4), `:not()` acepta una **lista de selectores separada por comas** — `:not(.a, .b)` equivale a `:not(.a):not(.b)` — mientras que en la versión anterior de la especificación solo aceptaba un único selector simple. Ten en cuenta que, como es una lista no perdonadora (igual que la agrupación con coma explicada más arriba), si uno de los selectores dentro de `:not()` no es válido, toda la regla se descarta.

## Pseudo-elementos

A diferencia de las pseudo-clases, un pseudo-elemento no selecciona un elemento existente del DOM, sino una **parte específica** de un elemento (o contenido generado que no existe en el HTML). Se escriben con doble dos puntos (`::`) para distinguirlos visualmente de las pseudo-clases.

### `::before` y `::after`

Insertan contenido generado justo antes o después del contenido real de un elemento, sin modificar el HTML.

```css
.tooltip::before {
  content: "▲";
  display: block;
}

a[href^="http"]::after {
  content: " ↗";
}
```

Estos pseudo-elementos **no aparecen** si no se les define explícitamente la propiedad `content`: el valor inicial de `content` es `normal`, y para `::before`/`::after` ese `normal` se computa como `none`, es decir, sin generar nada. Por eso siempre verás `content: ""` (aunque sea una cadena vacía, para un icono puesto por `background` o `border`) o `content: "algún texto"` acompañando a estos selectores.

### `::first-line`

Aplica estilos únicamente a la primera línea *renderizada* de un bloque de texto — no a una etiqueta HTML concreta, sino a la línea que resulta tras el ajuste de línea (*line wrap*), por lo que puede cambiar según el ancho del contenedor.

```css
p::first-line {
  font-weight: bold;
  color: darkslategray;
}
```

Solo acepta un subconjunto limitado de propiedades: las relacionadas con fuente (`font`, `font-family`, `font-size`, `font-weight`...), color y fondo (`color`, `background-*`), y algunas de texto (`text-decoration`, `text-transform`, `letter-spacing`, `word-spacing`, `line-height`, `vertical-align`). Propiedades como `padding` o `margin` no tienen efecto aquí.

Su pariente cercano, `::first-letter`, funciona igual pero afecta solo a la primera letra (útil para el clásico efecto de letra capital).

!!! tip "Doble dos puntos vs. un solo dos puntos"

    La sintaxis correcta y recomendada para pseudo-elementos es siempre con doble dos puntos (`::before`, `::after`, `::first-line`, `::first-letter`). Por compatibilidad histórica con CSS2, los navegadores también aceptan la sintaxis antigua de un solo dos puntos (`:before`, `:after`, `:first-line`, `:first-letter`) **únicamente** para estos cuatro pseudo-elementos originales; cualquier pseudo-elemento más reciente (como `::marker` o `::placeholder`) exige obligatoriamente doble dos puntos.

## Ver también

- [Cascada, especificidad y herencia](cascada-especificidad-herencia.md)
- [Selectores modernos (:has, :is, :where)](../moderno/selectores-modernos.md)
- [Cheatsheet de selectores](../cheatsheets/selectores-cheatsheet.md)

## Fuentes

- [MDN: CSS selectors](https://developer.mozilla.org/es/docs/Web/CSS/CSS_selectors)
- [MDN: Selector de estructura (combinadores y agrupación)](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors/Selector_structure)
- [MDN: Selectores de atributo](https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors)
- [MDN: Pseudo-elementos](https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-elements)
- [MDN: :nth-child()](https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-child)
- [MDN: :nth-of-type()](https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-of-type)
- [MDN: :not()](https://developer.mozilla.org/en-US/docs/Web/CSS/:not)
- [MDN: :focus-visible](https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible)
- [MDN: ::first-line](https://developer.mozilla.org/en-US/docs/Web/CSS/::first-line)
- [MDN: content](https://developer.mozilla.org/en-US/docs/Web/CSS/content)
- [caniuse: Case-insensitive CSS attribute selectors](https://caniuse.com/css-case-insensitive)
- [caniuse: Case-sensitive CSS attribute selector modifier (s)](https://caniuse.com/mdn-css_selectors_attribute_case_sensitive_modifier)
- [caniuse: :focus-visible](https://caniuse.com/css-focus-visible)
- [caniuse: selector list argument of :nth-child and :nth-last-child](https://caniuse.com/css-nth-child-of)
