# Cheatsheet: Flexbox

Chuleta de referencia rápida con todas las propiedades de Flexbox, sus valores posibles y qué hace cada uno en una línea. Está pensada para consultarla mientras escribes CSS —sin explicaciones largas—, no para aprender el modelo desde cero: si necesitas entender el *por qué* detrás de cada propiedad, la [guía completa de Flexbox](../layout/flexbox.md) cubre eso en profundidad.

## Propiedades del contenedor flex

Se aplican al elemento padre (el que recibe `display: flex`). Afectan a cómo se distribuyen y alinean sus hijos directos.

### `display`

| Valor | Descripción |
|---|---|
| `flex` | Convierte al elemento en contenedor flex de tipo bloque; los hijos directos pasan a ser flex items |
| `inline-flex` | Igual que `flex`, pero el propio contenedor se comporta como una caja `inline` de cara al resto del documento |

### `flex-direction`

Define el eje principal: la dirección en la que se colocan los elementos por defecto.

| Valor | Descripción |
|---|---|
| `row` (inicial) | Eje principal horizontal, en la dirección del texto (izquierda→derecha en `dir="ltr"`) |
| `row-reverse` | Eje principal horizontal, pero invirtiendo el orden visual de los elementos |
| `column` | Eje principal vertical, de arriba hacia abajo |
| `column-reverse` | Eje principal vertical, pero invirtiendo el orden visual de los elementos |

### `flex-wrap`

Controla si los elementos deben caber en una sola línea o pueden saltar a varias.

| Valor | Descripción |
|---|---|
| `nowrap` (inicial) | Todos los elementos en una sola línea, aunque desborden el contenedor |
| `wrap` | Los elementos saltan a nuevas líneas cuando no caben en el ancho/alto disponible |
| `wrap-reverse` | Igual que `wrap`, pero las líneas se apilan en orden inverso sobre el eje transversal |

### `justify-content`

Distribuye el espacio libre **a lo largo del eje principal**. Solo tiene un efecto visible cuando **ningún** elemento tiene `flex-grow` mayor que 0: si al menos uno lo tiene, ese elemento absorbe todo el espacio libre disponible y no queda nada que `justify-content` pueda repartir.

| Valor | Descripción |
|---|---|
| `normal` (inicial) | Sin distribución especial; en un contenedor flex se comporta como `flex-start` |
| `flex-start` | Agrupa los elementos al inicio del eje principal |
| `flex-end` | Agrupa los elementos al final del eje principal |
| `start` / `end` | Igual que `flex-start`/`flex-end`, pero referidos al inicio/final lógico del contenedor en vez de al eje principal del flex |
| `left` / `right` | Agrupan los elementos hacia el lado físico izquierdo/derecho (utilidad limitada si el eje principal no es horizontal) |
| `center` | Agrupa los elementos en el centro del eje principal |
| `space-between` | Primer y último elemento pegados a los extremos; el resto del espacio se reparte igual entre los huecos intermedios |
| `space-around` | Cada elemento recibe el mismo espacio a su alrededor (el hueco entre dos elementos es el doble que el de los extremos) |
| `space-evenly` | Todos los huecos, incluidos los extremos, quedan exactamente iguales |
| `stretch` | En un contenedor flex se comporta igual que `flex-start`/`start` (no estira nada): el reparto de espacio en el eje principal lo controla `flex-grow`, no `justify-content` |

!!! note "Modificadores `safe` / `unsafe`"

    Los valores posicionales (`center`, `start`, `end`, `flex-start`, `flex-end`) admiten los prefijos `safe` y `unsafe` (p. ej. `justify-content: safe center`) para decidir qué ocurre si el contenido es más grande que el espacio disponible: `safe` cae de nuevo a `start` para evitar que el contenido se salga y quede inaccesible, mientras que `unsafe` mantiene la alineación pedida aunque provoque overflow. Vienen definidos en el [CSS Box Alignment Module](https://developer.mozilla.org/en-US/docs/Web/CSS/justify-content) y ya tienen buen soporte en navegadores actuales (Chrome/Edge 115+, Firefox 63+, Safari 17.6+); si necesitas cubrir versiones más antiguas, comprueba antes la [tabla de compatibilidad en caniuse](https://caniuse.com/mdn-css_properties_justify-content_flex_context_safe_unsafe).

### `align-items`

Alinea los elementos **en el eje transversal**, dentro de su línea. Es al eje transversal lo que `justify-content` es al principal.

| Valor | Descripción |
|---|---|
| `normal` (inicial) | Sin alineación especial; en un contenedor flex se comporta como `stretch` |
| `stretch` | Estira los elementos para ocupar todo el alto (o ancho) de la línea, salvo que tengan un tamaño explícito |
| `flex-start` | Alinea los elementos al inicio del eje transversal |
| `flex-end` | Alinea los elementos al final del eje transversal |
| `start` / `end` | Igual que `flex-start`/`flex-end`, pero referidos al inicio/final lógico en vez de al eje transversal del flex |
| `self-start` / `self-end` | Alinean respecto al borde de inicio/final propio de cada elemento, según su modo de escritura individual |
| `center` | Centra los elementos en el eje transversal |
| `baseline` (equivale a `first baseline`) | Alinea los elementos por la línea base del texto de su primera línea de contenido |
| `last baseline` | Alinea los elementos por la línea base de la última línea de contenido |

### `align-content`

Distribuye el espacio libre **entre líneas completas** cuando hay más de una (requiere `flex-wrap: wrap` o `wrap-reverse`). No tiene ningún efecto con una sola línea.

| Valor | Descripción |
|---|---|
| `normal` (inicial) | Sin distribución especial; se comporta como `stretch` cuando sobra espacio en el eje transversal |
| `flex-start` / `start` | Agrupa las líneas al inicio del eje transversal |
| `flex-end` / `end` | Agrupa las líneas al final del eje transversal |
| `center` | Agrupa las líneas en el centro del eje transversal |
| `space-between` | Primera y última línea pegadas a los extremos; el resto del espacio se reparte igual entre huecos |
| `space-around` | Cada línea recibe el mismo espacio a su alrededor |
| `space-evenly` | Todos los huecos entre líneas, incluidos los extremos, quedan exactamente iguales |
| `stretch` | Las líneas se estiran para repartirse todo el espacio disponible del eje transversal |
| `baseline` / `first baseline` / `last baseline` | Alinea las líneas por la línea base de su contenido (poco habitual en la práctica) |

### `gap`

Shorthand de `row-gap` y `column-gap`: define la separación entre elementos, aplicada **solo entre** ellos (nunca antes del primero ni después del último).

| Sintaxis | Descripción |
|---|---|
| `gap: <valor>` | Aplica el mismo espacio entre filas y entre columnas |
| `gap: <fila> <columna>` | Define `row-gap` y `column-gap` por separado, en ese orden |
| `row-gap: <valor>` | Solo el espacio entre líneas del eje transversal (filas, en `flex-direction: row`) |
| `column-gap: <valor>` | Solo el espacio entre elementos dentro de cada línea (columnas, en `flex-direction: row`) |

El valor inicial de `row-gap`/`column-gap` es `normal`, que en contenedores flex y grid equivale a `0` (sin espacio).

## Propiedades de los elementos flex (flex items)

Se aplican a los hijos directos de un contenedor flex y controlan su comportamiento individual dentro de él.

### `order`

| Valor | Descripción |
|---|---|
| `<entero>` (inicial `0`) | Posición relativa del elemento en el **orden visual** de disposición dentro del contenedor; los elementos se colocan de menor a mayor valor y, en caso de empate, se respeta el orden del documento |

`order` solo cambia el orden *visual*: no altera el orden del DOM ni el orden de tabulación (`tab`), por lo que un uso descuidado puede desincronizar lo que se ve de lo que recorren los lectores de pantalla o la navegación por teclado.

### `flex-grow`

| Valor | Descripción |
|---|---|
| `<número>` sin unidad, ≥ 0 (inicial `0`) | Proporción de espacio libre que absorbe el elemento cuando sobra espacio en el eje principal; `0` significa que no crece |

### `flex-shrink`

| Valor | Descripción |
|---|---|
| `<número>` sin unidad, ≥ 0 (inicial `1`) | Proporción en la que se encoge el elemento cuando falta espacio en el eje principal; `0` evita que se comprima |

### `flex-basis`

| Valor | Descripción |
|---|---|
| `auto` (inicial) | Usa el valor de `width` (en `row`) o `height` (en `column`); si también es `auto`, usa `content` |
| `content` | El tamaño se calcula a partir del contenido del elemento |
| `<longitud>` (p. ej. `200px`, `10rem`) | Tamaño de partida fijo, antes de aplicar `flex-grow`/`flex-shrink` |
| `<porcentaje>` (p. ej. `50%`) | Porcentaje del tamaño interno del eje principal del contenedor |
| `max-content` | Tamaño de partida igual al ancho/alto intrínseco máximo del contenido (sin saltos de línea evitables) |
| `min-content` | Tamaño de partida igual al ancho/alto intrínseco mínimo del contenido |
| `fit-content` | Tamaño de partida acotado entre `min-content` y `max-content`, ajustado al espacio disponible |

### `flex` (shorthand)

Combina `flex-grow`, `flex-shrink` y `flex-basis`, en ese orden, y es la forma recomendada de usarlas frente a las propiedades sueltas.

| Valor | Equivale a | Descripción |
|---|---|---|
| `flex: initial` (o no declarar `flex`) | `0 1 auto` | Comportamiento por defecto: no crece, se encoge si hace falta, tamaño según contenido/`width` |
| `flex: auto` | `1 1 auto` | Crece y se encoge libremente partiendo del tamaño de su contenido |
| `flex: none` | `0 0 auto` | Tamaño rígido: ni crece ni se encoge |
| `flex: <número>` (p. ej. `flex: 1`) | `<número> 1 0%` | Reparte el espacio proporcionalmente, ignorando el contenido como base de tamaño |
| `flex: <grow> <shrink>` | — | Fija crecimiento y encogimiento, con `flex-basis: 0%` implícito |
| `flex: <grow> <shrink> <basis>` | — | Forma completa, un valor para cada componente |

### `align-self`

Sobrescribe, para un elemento concreto, el valor de `align-items` heredado del contenedor. Acepta los mismos valores que `align-items` más `auto`.

| Valor | Descripción |
|---|---|
| `auto` (inicial) | Usa el valor de `align-items` del contenedor padre |
| `stretch` | Estira el elemento para ocupar el alto/ancho disponible de la línea |
| `flex-start` / `flex-end` | Alinea el elemento al inicio/final del eje transversal |
| `start` / `end` | Igual que `flex-start`/`flex-end`, pero referidos al inicio/final lógico |
| `self-start` / `self-end` | Alinean respecto al borde de inicio/final propio del elemento |
| `center` | Centra el elemento en el eje transversal |
| `baseline` / `first baseline` / `last baseline` | Alinea el elemento por la línea base de su contenido |

## Ejemplo combinado

```css
.contenedor {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  align-content: space-between;
  gap: 1rem;
}

.item {
  order: 0;
  flex: 1 1 200px; /* flex-grow | flex-shrink | flex-basis */
  align-self: auto;
}

.item--fijo {
  flex: none;      /* no crece ni se encoge: tamaño fijo */
  align-self: flex-start;
}
```

`.contenedor` reparte sus hijos en filas que envuelven (`flex-wrap: wrap`), separadas por `gap`, con espacio distribuido tanto en el eje principal (`justify-content`) como entre líneas (`align-content`). Cada `.item` parte de 200px y puede crecer o encogerse por igual (`flex: 1 1 200px`), salvo `.item--fijo`, que se excluye de ese reparto (`flex: none`) y se alinea de forma independiente en el eje transversal (`align-self: flex-start`).

!!! tip "Soporte de navegadores"

    El modelo Flexbox moderno tiene soporte prácticamente universal (Chrome 29+, Firefox 28+, Safari 9+, Edge 12+); solo Internet Explorer 10-11 lo implementan de forma parcial con sintaxis antigua. La propiedad `gap` aplicada a contenedores flex llegó más tarde (Chrome/Edge 84+, Firefox 63+, Safari 14.1+): si necesitas dar soporte a Safari anterior a abril de 2021, revisa el detalle en [caniuse.com/flexbox-gap](https://caniuse.com/flexbox-gap) antes de depender de ella sin alternativa. Consulta el estado general en [caniuse.com/flexbox](https://caniuse.com/flexbox).

## Ver también

- [Flexbox: guía completa](../layout/flexbox.md)
- [CSS Grid](../layout/grid.md)
- [Display y flujo normal](../layout/display-y-flujo-normal.md)
- [El modelo de caja](../fundamentos/modelo-de-caja.md)

## Fuentes

- [MDN: display](https://developer.mozilla.org/en-US/docs/Web/CSS/display)
- [MDN: flex-direction](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-direction)
- [MDN: flex-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-wrap)
- [MDN: justify-content](https://developer.mozilla.org/en-US/docs/Web/CSS/justify-content)
- [MDN: align-items](https://developer.mozilla.org/en-US/docs/Web/CSS/align-items)
- [MDN: align-content](https://developer.mozilla.org/en-US/docs/Web/CSS/align-content)
- [MDN: align-self](https://developer.mozilla.org/en-US/docs/Web/CSS/align-self)
- [MDN: gap](https://developer.mozilla.org/en-US/docs/Web/CSS/gap)
- [MDN: order](https://developer.mozilla.org/en-US/docs/Web/CSS/order)
- [MDN: flex-grow](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-grow)
- [MDN: flex-shrink](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-shrink)
- [MDN: flex-basis](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-basis)
- [MDN: flex (shorthand)](https://developer.mozilla.org/en-US/docs/Web/CSS/flex)
- [W3C: CSS Flexible Box Layout Module Level 1](https://www.w3.org/TR/css-flexbox-1/)
- [W3C: CSS Box Alignment Module Level 3](https://www.w3.org/TR/css-align-3/)
- [caniuse: Flexbox](https://caniuse.com/flexbox)
- [caniuse: gap property for flexbox](https://caniuse.com/flexbox-gap)
