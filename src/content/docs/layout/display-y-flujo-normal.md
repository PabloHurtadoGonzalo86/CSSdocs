---
title: Display y flujo normal
description: Explica la propiedad display (tipos de display exterior e interior) y el flujo normal en CSS, junto con los valores block, inline, inline-block, none, contents, table y flex/grid.
---

La propiedad `display` es probablemente la propiedad CSS más importante de todas: decide si un elemento genera una caja de bloque o una caja en línea, y qué modelo de layout usan sus hijos (flujo normal, flexbox, grid, tabla...). Entenderla bien — junto con el **flujo normal** en el que viven todos los elementos por defecto — es la base sobre la que se apoya todo lo demás en layout: si no sabes por qué un `<div>` "rompe línea" y un `<span>` no, cualquier problema de alineación o de espaciado se vuelve mucho más difícil de depurar.

## Qué hace `display`

Según [MDN](https://developer.mozilla.org/es/docs/Web/CSS/display), `display` define dos cosas a la vez:

- El **tipo de display exterior** (`outer display type`): cómo se comporta la caja del elemento respecto a sus hermanos en el flujo normal (como bloque o como línea).
- El **tipo de display interior** (`inner display type`): cómo se organizan sus hijos (flujo normal, flexbox, grid, tabla, ruby...).

La sintaxis moderna incluso permite especificar ambos valores por separado, por ejemplo `display: block flex` en lugar del histórico `display: flex`. Son equivalentes, pero el valor de una sola palabra clave es el que funciona en todos los navegadores hoy en día, así que es el que verás en el resto de esta página y en el resto del sitio.

```css
/* Equivalentes */
.caja {
  display: flex;
}

.caja {
  display: block flex;
}
```

:::tip[Soporte de navegadores]
Los valores clásicos de una sola palabra (`block`, `inline`, `inline-block`, `flex`, `grid`, `none`, `table`...) funcionan en cualquier navegador con soporte de CSS moderno. La **sintaxis de dos valores** (`display: block flex`) es más reciente: consulta su soporte actualizado en [caniuse: CSS display multi-keyword values](https://caniuse.com/mdn-css_properties_display_multi-keyword_values).
:::

## El flujo normal (normal flow)

El **flujo normal** es el comportamiento de layout por defecto: el que se aplica a cualquier elemento que no haya sido sacado de él mediante `float`, `position: absolute`/`fixed`, o convertido en contenedor `flex`/`grid`. Dentro del flujo normal, cada caja participa en uno de estos dos contextos de formato, tal como describe la especificación CSS2.1 recogida por [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Display/Block_and_inline_layout) (esta página concreta de MDN todavía no tiene traducción al español):

- **Contexto de formato de bloque (BFC):** las cajas se apilan una debajo de otra, verticalmente, empezando por la parte superior del contenedor.
- **Contexto de formato en línea (IFC):** las cajas se colocan una junto a otra, horizontalmente, formando "cajas de línea" (line boxes) que saltan de línea cuando no queda espacio.

Una caja nunca participa en los dos contextos a la vez: o se apila con sus hermanos (comportamiento de bloque), o fluye junto a ellos en la misma línea (comportamiento en línea). Esa es la decisión que toma el valor **exterior** de `display`.

## `display: block`

Un elemento con `display: block` genera una **caja de bloque**:

- Ocupa todo el ancho disponible del contenedor (a menos que se le indique un `width` distinto).
- Fuerza un salto de línea antes y después de sí mismo, así que dos elementos de bloque nunca quedan uno junto al otro.
- Respeta por completo `width`, `height`, y todos los márgenes y paddings.
- Sus márgenes verticales pueden colapsar con los de los elementos de bloque adyacentes (el margen final entre dos párrafos es el mayor de los dos, no la suma).

```css
p {
  display: block; /* es el valor por defecto de <p> en la hoja de estilos del navegador */
  border: 2px solid green;
  width: 40%;
}
```

Aunque le pongamos un `width` del 40 %, el párrafo se sigue apilando verticalmente con el siguiente elemento de bloque: el ancho no cambia su comportamiento exterior.

Elementos como `<div>`, `<p>`, `<h1>`–`<h6>`, `<ul>` o `<section>` son de bloque por defecto en la hoja de estilos del navegador (user-agent stylesheet). `<li>` es un caso especial: su valor por defecto no es `block` sino `list-item`, un valor que genera una caja de bloque igual que `block` pero que además añade la caja del marcador (el punto o el número de la lista).

## `display: inline`

Un elemento con `display: inline` genera una o varias **cajas en línea**:

- Solo ocupa el ancho de su propio contenido, nunca todo el ancho disponible.
- No provoca salto de línea: fluye junto al texto y a otros elementos en línea, como si fuera una palabra más.
- **Ignora** `width` y `height`: no tienen ningún efecto.
- El `margin` vertical (arriba/abajo) **no tiene ningún efecto**: ni desplaza el layout ni se ve reflejado visualmente. El `padding` vertical sí se pinta (el fondo o el borde se extienden verticalmente), pero tampoco empuja a los elementos de líneas adyacentes ni afecta a la altura de la línea. Solo el `margin`/`padding` horizontal afecta al espaciado real del layout.
- Los márgenes en línea **no colapsan** entre sí.

```css
strong {
  display: inline; /* valor por defecto de <strong>, <a>, <span>... */
  font-size: 150%;
  /* width y height aquí no tendrían ningún efecto */
}
```

Elementos como `<span>`, `<a>`, `<strong>`, `<em>` o `<img>`* son en línea por defecto (*`<img>` es técnicamente un elemento reemplazado en línea, con un comportamiento algo distinto respecto a `width`/`height`, pero comparte el resto de reglas de `inline`).

### Diferencias prácticas entre `block` e `inline`

| | `block` | `inline` |
|---|---|---|
| Ancho | Ocupa todo el contenedor por defecto | Solo el ancho de su contenido |
| `width` / `height` | Se respetan | Se ignoran |
| Salto de línea | Antes y después, siempre | No, fluye con el texto |
| `margin`/`padding` vertical | Se aplican y pueden colapsar entre bloques | `margin` no tiene efecto; `padding` se pinta pero no desplaza el layout de otras líneas |
| Ejemplos por defecto | `div`, `p`, `section`, `ul` | `span`, `a`, `strong`, `em` |

## `display: inline-block`

`inline-block` es un híbrido pensado para resolver justo la limitación anterior: se comporta **por fuera** como un elemento en línea (no rompe línea, fluye junto a otros elementos) pero **por dentro** como un bloque (respeta `width`, `height`, y todo el `margin`/`padding`, incluido el vertical, sin que colapse).

```css
.chip {
  display: inline-block;
  width: 120px;
  padding: 0.5rem 1rem;
  margin: 0.25rem;
  border-radius: 999px;
  background: #eef;
}
```

Este patrón era muy común antes de Flexbox y Grid para maquetar elementos "en fila" con ancho y alto controlados (menús, badges, tarjetas pequeñas). Hoy en día, para filas o rejillas de elementos, casi siempre es mejor usar [Flexbox](flexbox) o [CSS Grid](grid), que dan control real sobre el espaciado entre elementos sin depender de trucos de `font-size`/`white-space` para eliminar espacios en blanco entre `inline-block` consecutivos. `inline-block` sigue siendo útil para casos puntuales y sencillos, como un icono o un botón que debe fluir dentro de un párrafo de texto pero necesita padding vertical.

## `display: none`

`display: none` saca al elemento completamente del flujo: no genera ninguna caja, no ocupa espacio, y no afecta al renderizado del resto del documento, como si no existiera en el DOM visual.

```css
.tooltip {
  display: none; /* no reserva espacio ni se pinta */
}

.tooltip.is-visible {
  display: block;
}
```

Un matiz importante: `display: none` también **elimina al elemento (y a todos sus descendientes) del árbol de accesibilidad**, así que lectores de pantalla y otras tecnologías asistivas lo ignoran por completo. Es lo correcto cuando el contenido debe estar realmente oculto para todo el mundo (un panel colapsado, una pestaña inactiva). Si en cambio quieres ocultar algo *solo* visualmente pero mantenerlo accesible (por ejemplo, texto para lectores de pantalla), `display: none` no es la herramienta adecuada — hace falta otra técnica (fuera del alcance de esta página).

## `display: contents`

`display: contents` hace que la caja del propio elemento "desaparezca": el elemento no genera ninguna caja propia (ni de bloque ni en línea), pero sus **hijos siguen ahí**, como si fueran hijos directos del padre del elemento. Es útil, por ejemplo, para deshacerte de un `<div>` envoltorio que solo estorba cuando quieres que sus hijos participen directamente en una rejilla de Grid o en un contenedor Flex del nivel superior.

```html
<div class="grid">
  <div class="wrapper">
    <div class="item">A</div>
    <div class="item">B</div>
  </div>
  <div class="item">C</div>
</div>
```

```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

.wrapper {
  display: contents; /* "desaparece": .item A y B pasan a ser celdas directas de .grid */
}
```

:::caution[Cuidado con la accesibilidad]
Según la propia especificación (citada en [MDN](https://developer.mozilla.org/es/docs/Web/CSS/display)), `display: contents` no debería afectar al árbol de accesibilidad de los hijos, pero durante años varios navegadores lo implementaron de forma incorrecta y eliminaban del árbol de accesibilidad información relevante (como el nombre accesible calculado a partir de ese contenedor). Verifica siempre el comportamiento real en las tecnologías asistivas que te importen antes de depender de esta propiedad en contenido crítico.
:::

:::tip[Soporte de navegadores]
El soporte base de `display: contents` es amplio en navegadores modernos, pero conviene revisar el detalle de versiones y las notas de compatibilidad (incluidas las de accesibilidad) en [caniuse: CSS display: contents](https://caniuse.com/css-display-contents).
:::

## `display: table` y compañía

`display: table` hace que un elemento se comporte como el antiguo elemento HTML `<table>`, generando una caja de bloque que organiza a sus hijos con el modelo de layout de tablas. Existen valores hermanos para reproducir el resto de la estructura de una tabla sin usar las etiquetas HTML correspondientes: `table-row` (como `<tr>`), `table-cell` (como `<td>`), `table-row-group` (como `<tbody>`), `table-column`, `table-caption`, etc.

```css
.tabla-visual {
  display: table;
}
.fila {
  display: table-row;
}
.celda {
  display: table-cell;
  vertical-align: middle; /* alineación vertical típica de las celdas de tabla */
}
```

Antes de que Flexbox y Grid estuvieran disponibles, este era el truco habitual para conseguir columnas de igual altura o centrado vertical robusto. Hoy, para maquetar layouts, [Flexbox](flexbox) y [CSS Grid](grid) son casi siempre la mejor opción: son más flexibles, más legibles y pensados específicamente para layout (en lugar de "tomar prestado" un modelo pensado para datos tabulares). `display: table` sigue teniendo su sitio cuando el contenido *es* genuinamente tabular pero, por la razón que sea, no puedes usar las etiquetas semánticas `<table>`/`<tr>`/`<td>` — aunque en ese caso conviene añadir los roles ARIA (`role="table"`, `role="row"`, `role="cell"`) para no perder semántica accesible, ya que cambiar el `display` de una tabla puede alterar cómo la anuncian los lectores de pantalla.

## `flex` y `grid` también son valores de `display`

Vale la pena remarcarlo porque a veces se pasa por alto: **Flexbox y Grid se activan poniendo `display: flex` o `display: grid`** en el contenedor. En el momento en que haces eso, ese contenedor sigue comportándose como una caja de bloque (o en línea, con `inline-flex`/`inline-grid`) de cara al resto del documento, pero sus hijos directos dejan de participar en el flujo normal — ya no forman un contexto de formato de bloque ni en línea, sino un **contexto de formato flexible** o un **contexto de formato de rejilla**, con sus propias reglas de alineación, tamaño y distribución de espacio.

```css
.contenedor-flex {
  display: flex; /* los hijos directos pasan a ser "flex items" */
}

.contenedor-grid {
  display: grid; /* los hijos directos pasan a ser "grid items" */
}
```

Esta página se centra en el flujo normal y en los valores de `display` que lo gobiernan (`block`, `inline`, `inline-block`, `none`, `contents`, `table`); para el detalle completo de cómo funcionan estos dos modelos de layout, sus propiedades y sus casos de uso, consulta las páginas dedicadas: [Flexbox](flexbox) y [CSS Grid](grid).

## Ver también

- [Flexbox](flexbox)
- [CSS Grid](grid)
- [Positioning](positioning)
- [El modelo de caja](../fundamentos/modelo-de-caja)

## Fuentes

- [MDN: display](https://developer.mozilla.org/es/docs/Web/CSS/display)
- [MDN: Block and inline layout in normal flow](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Display/Block_and_inline_layout)
- [MDN: visibility](https://developer.mozilla.org/es/docs/Web/CSS/visibility)
- [MDN: `<div>`](https://developer.mozilla.org/es/docs/Web/HTML/Reference/Elements/div)
- [MDN: `<span>`](https://developer.mozilla.org/es/docs/Web/HTML/Reference/Elements/span)
- [caniuse: CSS display: contents](https://caniuse.com/css-display-contents)
- [caniuse: CSS display multi-keyword values](https://caniuse.com/mdn-css_properties_display_multi-keyword_values)
