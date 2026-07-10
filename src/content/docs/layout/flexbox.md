---
title: "Flexbox: guía completa"
description: Guía completa de Flexbox en CSS, con el concepto de eje principal y transversal, las propiedades del contenedor y de los elementos flex, y casos de uso prácticos como centrado, barras de navegación y tarjetas de igual altura.
---

Flexbox (*CSS Flexible Box Layout*) es el modelo de layout pensado para distribuir elementos **en una sola dimensión**: una fila o una columna. Es la herramienta que usarás a diario para centrar contenido, construir barras de navegación, alinear botones, repartir espacio entre tarjetas o resolver ese "necesito que estos tres elementos ocupen el mismo alto" que antes obligaba a trucos con `float`, `table-cell` o posicionamiento absoluto. Entenderlo bien —sobre todo la diferencia entre eje principal y eje transversal— evita el 90% de los "por qué no se centra esto" que aparecen en el día a día del Frontend.

## El concepto clave: eje principal y eje transversal

Cuando conviertes un elemento en contenedor flex, todo su comportamiento gira en torno a dos ejes:

- **Eje principal** (*main axis*): la dirección en la que se colocan los elementos por defecto (horizontal, de izquierda a derecha). La controla `flex-direction`.
- **Eje transversal** (*cross axis*): el eje perpendicular al principal.

Casi todas las propiedades de Flexbox se dividen según a qué eje afectan: `justify-content` trabaja sobre el eje principal, `align-items` y `align-content` sobre el transversal. Si cambias `flex-direction` a `column`, los ejes rotan 90° y con ellos el significado práctico de esas propiedades.

## Activar Flexbox: `display: flex`

```css
.contenedor {
  display: flex;
}
```

Esto convierte a `.contenedor` en un **contenedor flex** y a todos sus hijos directos en **elementos flex** (*flex items*). Efectos inmediatos, aunque no cambies nada más:

- Los hijos se colocan en fila, uno junto a otro (comportamiento por defecto de `flex-direction: row`).
- Los `float`, `clear` y `vertical-align` dejan de tener efecto sobre los elementos flex.
- Los elementos flex ya no generan una caja de bloque independiente para el cálculo de márgenes: no hay colapso de márgenes entre ellos.

También existe `display: inline-flex`, que crea un contenedor flex que se comporta como una caja `inline` de cara al resto del documento (no ocupa todo el ancho disponible), pero cuyos hijos siguen distribuyéndose con las reglas de Flexbox.

## El eje principal: `flex-direction`

```css
.contenedor {
  display: flex;
  flex-direction: row; /* valor inicial */
}
```

| Valor | Efecto |
|---|---|
| `row` (inicial) | Eje principal horizontal, en la dirección del texto (izquierda→derecha en `dir="ltr"`) |
| `row-reverse` | Igual que `row` pero invirtiendo el orden visual |
| `column` | Eje principal vertical, de arriba hacia abajo |
| `column-reverse` | Igual que `column` pero invirtiendo el orden visual |

:::caution[`row-reverse` y `column-reverse` afectan a la accesibilidad]
Estos valores invierten el **orden visual** sin tocar el orden del DOM. Un usuario de lector de pantalla o que navega con teclado seguirá recibiendo el contenido en el orden original del HTML, que ya no coincidirá con lo que ve en pantalla. Úsalos solo cuando el orden de lectura lógico siga teniendo sentido invertido.
:::

## Controlar el salto de línea: `flex-wrap`

Por defecto, Flexbox intenta colocar **todos** los elementos en una sola línea, aunque eso implique encogerlos de forma agresiva o desbordar el contenedor. `flex-wrap` cambia ese comportamiento:

```css
.contenedor {
  display: flex;
  flex-wrap: wrap; /* valor inicial: nowrap */
}
```

| Valor | Efecto |
|---|---|
| `nowrap` (inicial) | Todo en una sola línea, aunque desborde |
| `wrap` | Los elementos saltan a nuevas líneas cuando no caben |
| `wrap-reverse` | Igual que `wrap`, pero apilando las líneas en orden inverso en el eje transversal |

Existe además el atajo `flex-flow`, que combina `flex-direction` y `flex-wrap` en una sola declaración:

```css
.contenedor {
  flex-flow: row wrap; /* equivalente a flex-direction: row; flex-wrap: wrap; */
}
```

:::tip[Novedad en el radar: `flex-wrap: balance`]
La especificación [CSS Flexible Box Layout Module Level 2](https://drafts.csswg.org/css-flexbox-2/) añade un valor `balance` para `flex-wrap`, que busca repartir los elementos de forma más equilibrada entre líneas (similar a lo que hace `text-wrap: balance` con el texto). A mediados de 2026 es una función muy reciente, sin soporte extendido todavía: trátala como experimental y verifica su estado en [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-wrap) antes de usarla en producción.
:::

## Alinear en el eje principal: `justify-content`

Distribuye el espacio sobrante **a lo largo del eje principal**. Solo tiene efecto visible cuando los elementos flex no ocupan todo el espacio disponible en ese eje.

```css
.contenedor {
  display: flex;
  justify-content: space-between;
}
```

| Valor | Efecto |
|---|---|
| `flex-start` (comportamiento inicial) | Elementos pegados al inicio del eje principal |
| `flex-end` | Elementos pegados al final |
| `center` | Elementos agrupados en el centro |
| `space-between` | Primer y último elemento pegados a los bordes; el resto del espacio se reparte igual entre ellos |
| `space-around` | Cada elemento recibe el mismo espacio a su alrededor (el hueco entre dos elementos es el doble que el de los extremos) |
| `space-evenly` | Todos los huecos —incluidos los extremos— quedan exactamente iguales |

El valor inicial real de la propiedad es `normal`, que según MDN y la especificación de alineación de cajas se comporta como `start` en un contenedor flex. En el caso habitual de `flex-direction: row` (o `column`) esto coincide visualmente con `flex-start`, pero conviene recordar que `start` siempre respeta la dirección de escritura, mientras que `flex-start`/`flex-end` siguen el eje principal tal como lo define `flex-direction` —por eso pueden diferir cuando usas `row-reverse` o `column-reverse`. La especificación también define `end`, `left` y `right`, pero en la práctica diaria los seis valores de la tabla cubren la inmensa mayoría de los casos.

## Alinear en el eje transversal: `align-items`

Mientras `justify-content` reparte espacio en el eje principal, `align-items` alinea los elementos **en el eje transversal**, dentro de su línea.

```css
.contenedor {
  display: flex;
  align-items: center;
}
```

| Valor | Efecto |
|---|---|
| `stretch` (comportamiento inicial) | Los elementos se estiran para ocupar todo el alto (o ancho) disponible de la línea, salvo que tengan un tamaño explícito |
| `flex-start` | Alineados al inicio del eje transversal |
| `flex-end` | Alineados al final |
| `center` | Centrados en el eje transversal |
| `baseline` | Alineados por la línea base del texto de cada elemento |

Igual que `justify-content`, el valor inicial formal es `normal`, pero en los elementos flex `normal` se comporta como `stretch`. Esto explica un comportamiento que sorprende a mucha gente: **por defecto, todos los elementos flex de una fila tienen el mismo alto**, aunque su contenido sea distinto. Esta es precisamente la base del caso práctico de tarjetas de igual altura que veremos más abajo.

## Alinear líneas completas: `align-content`

`align-content` se confunde a menudo con `align-items`, pero resuelve un problema distinto: cómo se reparte el espacio sobrante **entre las líneas** cuando hay varias (es decir, cuando `flex-wrap: wrap` ha generado más de una línea) y sobra espacio en el eje transversal.

```css
.contenedor {
  display: flex;
  flex-wrap: wrap;
  align-content: space-between;
}
```

Valores disponibles: `flex-start`, `flex-end`, `center`, `space-between`, `space-around`, `space-evenly` y `stretch` (además del valor inicial `normal`, que la propia especificación define como equivalente a `stretch` en un contenedor flex, cuando hay espacio libre en el eje transversal).

:::note[`align-content` no hace nada en una sola línea]
Si el contenedor tiene una única línea de elementos (el caso por defecto, con `flex-wrap: nowrap`), `align-content` no tiene ningún efecto visible. Necesitas `flex-wrap: wrap` (o `wrap-reverse`) **y** que sobre espacio en el eje transversal para que se note.
:::

## El espacio entre elementos: `gap`

Antes de `gap`, separar elementos flex obligaba a usar márgenes y luego "cancelar" el margen sobrante del primer o último elemento. `gap` (junto a sus componentes `row-gap` y `column-gap`) resuelve esto de forma nativa:

```css
.contenedor {
  display: flex;
  gap: 1rem;        /* separación igual en ambos ejes */
  gap: 1rem 2rem;    /* row-gap: 1rem; column-gap: 2rem; */
}
```

La ventaja frente a usar `margin` en los hijos es que `gap` **solo** aplica espacio *entre* elementos, nunca antes del primero ni después del último, sin necesidad de selectores como `:last-child` para corregirlo.

:::tip[Soporte de navegadores]
`gap` en contenedores flex tiene buen soporte en navegadores modernos (Chrome/Edge 84+, Firefox 63+, Safari 14.1+), pero llegó **más tarde** a Flexbox que a Grid, así que si necesitas dar soporte a versiones antiguas de Safari (anteriores a 14.1, de abril de 2021) comprueba antes el detalle en [caniuse.com/flexbox-gap](https://caniuse.com/flexbox-gap).
:::

## Controlar los elementos individuales

Hasta ahora todas las propiedades se aplican al **contenedor**. Las siguientes se aplican a los **elementos flex** (los hijos) y controlan su comportamiento individual.

### `flex-grow`: cómo crece cada elemento

Define la proporción de espacio sobrante que absorbe un elemento cuando el contenedor tiene más espacio del que ocupan sus hijos.

```css
.item {
  flex-grow: 1; /* valor inicial: 0 (no crece) */
}
```

El valor inicial es `0`: por defecto los elementos flex **no crecen**, aunque sobre espacio. Cuando varios elementos tienen `flex-grow` distinto de cero, el espacio libre se reparte proporcionalmente entre ellos. Por ejemplo, con tres elementos de 100px en un contenedor de 600px (300px libres, ya que los tres elementos ocupan 300px en total) y `flex-grow` de `1`, `2` y `3` respectivamente: se suman los factores (1+2+3=6), se divide el espacio libre entre ese total (300/6=50px por unidad) y cada elemento recibe su parte (50px, 100px y 150px extra).

### `flex-shrink`: cómo se encoge cada elemento

Es el opuesto de `flex-grow`: define cuánto se encoge un elemento cuando el contenedor **no tiene** espacio suficiente para todos.

```css
.item {
  flex-shrink: 0; /* valor inicial: 1 (sí se encoge) */
}
```

El valor inicial es `1`, así que, a diferencia del crecimiento, **por defecto todos los elementos flex sí se encogen** cuando hace falta. Poner `flex-shrink: 0` en un elemento evita que se comprima, aunque el resto de la fila sí lo haga.

### `flex-basis`: el tamaño de partida

Establece el tamaño base de un elemento en el eje principal **antes** de que se apliquen `flex-grow` o `flex-shrink`.

```css
.item {
  flex-basis: 200px;
}
```

Su valor inicial es `auto`, que significa: usa el valor de `width` (en `flex-direction: row`) o `height` (en `column`); y si ese valor también es `auto`, usa el tamaño del propio contenido (`content`). Admite longitudes, porcentajes y las mismas palabras clave que `width` (`max-content`, `min-content`, `fit-content`).

### El atajo `flex`

En la práctica, casi nunca se escriben `flex-grow`, `flex-shrink` y `flex-basis` por separado: se usa el atajo `flex`, que además fija valores por defecto más útiles que los que tendrían las propiedades por separado.

```css
.item {
  flex: 1 1 0%; /* flex-grow | flex-shrink | flex-basis */
}
```

| Atajo | Equivale a | Cuándo usarlo |
|---|---|---|
| `flex: initial` (o no declarar `flex`) | `0 1 auto` | Comportamiento por defecto: no crece, se encoge si hace falta, tamaño según contenido/`width` |
| `flex: auto` | `1 1 auto` | Crece y se encoge libremente partiendo del tamaño de su contenido |
| `flex: none` | `0 0 auto` | Tamaño completamente rígido: ni crece ni se encoge |
| `flex: <número>` (p. ej. `flex: 1`) | `<número> 1 0%` | El caso más habitual: reparte el espacio proporcionalmente ignorando el tamaño del contenido como base |

:::tip[Por qué preferir el atajo `flex` a las propiedades sueltas]
MDN recomienda explícitamente usar `flex` con sus valores por palabra clave (`auto`, `initial`, `none`) en lugar de fijar `flex-basis` de forma aislada, porque esos atajos combinan los tres valores en combinaciones ya probadas y coherentes entre sí, evitando resultados inesperados al mezclar un `flex-grow` de un sitio con un `flex-basis` de otro.
:::

### `align-self`: sobrescribir la alineación de un elemento concreto

Permite que un elemento individual ignore el `align-items` del contenedor y se alinee de otra forma en el eje transversal.

```css
.item--destacado {
  align-self: center;
}
```

Acepta los mismos valores que `align-items` (`flex-start`, `flex-end`, `center`, `baseline`, `stretch`...) más el valor inicial `auto`, que significa "usa el valor de `align-items` heredado del contenedor padre".

### `order`: reordenar visualmente sin tocar el HTML

Cambia la posición en la que se pinta un elemento dentro del contenedor flex, independientemente de su posición en el HTML.

```css
.item--primero {
  order: -1; /* valor inicial: 0 */
}
```

Los elementos se ordenan de menor a mayor valor de `order`; ante empates (el caso más común, ya que todos parten de `0`), se respeta el orden del documento.

:::caution[`order` no cambia el orden de lectura ni de tabulación]
`order` solo afecta al **orden visual**. El orden en el que un lector de pantalla anuncia el contenido, y el orden en el que el foco se mueve al pulsar Tab, siguen el orden del DOM. Si reordenas visualmente con `order`, puedes crear una experiencia incoherente para quien navega sin ratón. Úsalo con moderación y, siempre que puedas, ajusta el orden real en el HTML en lugar de maquillarlo con CSS.
:::

## Casos de uso prácticos

### Centrar contenido perfectamente

El caso de uso más buscado de Flexbox: centrar un elemento horizontal y verticalmente sin conocer sus dimensiones ni recurrir a `position: absolute` con márgenes negativos.

```css
.contenedor {
  display: flex;
  justify-content: center; /* centra en el eje principal (horizontal) */
  align-items: center;     /* centra en el eje transversal (vertical) */
  min-height: 100vh;
}
```

Con solo tres declaraciones el hijo queda centrado en ambos ejes, y sigue estándolo aunque cambie su tamaño de contenido dinámicamente: no hace falta calcular anchos ni altos, que era el problema real de las técnicas antiguas.

### Barra de navegación

Un patrón habitual: logotipo a la izquierda, enlaces de navegación a la derecha, todo alineado verticalmente al centro.

```css
.navbar {
  display: flex;
  justify-content: space-between; /* logo a un extremo, enlaces al otro */
  align-items: center;            /* todo centrado verticalmente */
  gap: 1rem;
  padding: 1rem 1.5rem;
}

.navbar__links {
  display: flex;       /* un segundo contenedor flex anidado */
  align-items: center;
  gap: 1.5rem;
}
```

Aquí se combinan dos contenedores flex anidados: el externo separa el bloque del logo del bloque de enlaces con `space-between`, y el interno (`.navbar__links`) usa `gap` para espaciar los enlaces entre sí sin necesidad de márgenes manuales.

### Tarjetas de igual altura

Uno de los problemas clásicos que Flexbox resuelve "gratis": si tienes varias tarjetas en una fila con contenido de longitud distinta, por defecto **todas quedan con la misma altura**, porque el valor inicial de `align-items` es `stretch`.

```css
.tarjetas {
  display: flex;
  gap: 1.5rem;
  align-items: stretch; /* es el valor inicial: se puede omitir */
}

.tarjeta {
  flex: 1;              /* todas crecen/reparten el ancho por igual */
  display: flex;
  flex-direction: column; /* dentro de la tarjeta, apilar en columna */
}

.tarjeta__cuerpo {
  flex-grow: 1; /* empuja el footer hacia abajo, ocupando el espacio libre */
}
```

El truco tiene dos capas: la fila de `.tarjetas` estira cada `.tarjeta` a la altura de la más alta (comportamiento por defecto de `align-items: stretch`), y dentro de cada tarjeta se vuelve a usar Flexbox en columna con `flex-grow: 1` en el cuerpo, para que el pie de tarjeta quede siempre pegado abajo sin importar cuánto texto tenga el cuerpo.

:::tip[Soporte de navegadores]
El modelo de caja flexible en la sintaxis moderna que se usa en esta guía (sin prefijos de proveedor) tiene soporte prácticamente universal desde hace años: Chrome 29+, Firefox 28+, Safari 9+ y Edge 12+. Versiones algo anteriores (Chrome 21-28, Safari 6.1-8) ya soportaban Flexbox, pero solo con el prefijo `-webkit-` y una sintaxis ligeramente distinta. Solo Internet Explorer 10-11 lo implementan de forma parcial, con una sintaxis y un comportamiento antiguos de la especificación. Consulta el detalle actualizado en [caniuse.com/flexbox](https://caniuse.com/flexbox).
:::

## Ver también

- [Display y flujo normal](display-y-flujo-normal)
- [CSS Grid](grid)
- [El modelo de caja](../fundamentos/modelo-de-caja)
- [Cheatsheet de Flexbox](../cheatsheets/flexbox-cheatsheet)

## Fuentes

- [MDN: flex-direction](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-direction)
- [MDN: flex-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-wrap)
- [MDN: flex-flow](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-flow)
- [MDN: justify-content](https://developer.mozilla.org/en-US/docs/Web/CSS/justify-content)
- [MDN: align-items](https://developer.mozilla.org/en-US/docs/Web/CSS/align-items)
- [MDN: align-content](https://developer.mozilla.org/en-US/docs/Web/CSS/align-content)
- [MDN: align-self](https://developer.mozilla.org/en-US/docs/Web/CSS/align-self)
- [MDN: gap](https://developer.mozilla.org/en-US/docs/Web/CSS/gap)
- [MDN: flex-grow](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-grow)
- [MDN: flex-shrink](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-shrink)
- [MDN: flex-basis](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-basis)
- [MDN: flex (shorthand)](https://developer.mozilla.org/en-US/docs/Web/CSS/flex)
- [MDN: order](https://developer.mozilla.org/en-US/docs/Web/CSS/order)
- [W3C: CSS Flexible Box Layout Module Level 1](https://www.w3.org/TR/css-flexbox-1/)
- [W3C: CSS Flexible Box Layout Module Level 2 (borrador, valor `balance`)](https://drafts.csswg.org/css-flexbox-2/)
- [caniuse: Flexbox](https://caniuse.com/flexbox)
- [caniuse: gap property for flexbox](https://caniuse.com/flexbox-gap)
