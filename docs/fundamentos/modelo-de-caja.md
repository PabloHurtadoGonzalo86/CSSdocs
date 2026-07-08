# El modelo de caja (Box Model)

Todo elemento HTML se renderiza como una caja rectangular, y esa caja se compone siempre de las mismas cuatro capas: contenido, padding, border y margin. Entender el modelo de caja no es un detalle académico: es la base para calcular anchos y altos correctamente, para depurar por qué dos elementos "no encajan" como esperabas, y para evitar horas de confusión con espacios verticales que aparecen o desaparecen solos (el famoso colapso de márgenes). Casi cualquier bug de "esto mide más de lo que debería" o "hay un hueco que no puse yo" se explica desde aquí.

## Las cuatro capas de la caja

Según la especificación y la documentación de MDN, cada elemento en flujo normal genera, de dentro hacia fuera, estas áreas:

| Capa | Qué es | Propiedades relacionadas |
| --- | --- | --- |
| **Content box** | El contenido real: texto, imagen, elementos hijos | `width`, `height`, `min-width`, `max-width`, `min-height`, `max-height` |
| **Padding box** | Espacio interior entre el contenido y el borde. El fondo del elemento se extiende también por aquí | `padding`, `padding-top/right/bottom/left` |
| **Border box** | La línea (o franja) que envuelve el padding y el contenido | `border`, `border-width/style/color` |
| **Margin box** | Espacio exterior transparente que separa la caja de sus vecinas | `margin`, `margin-top/right/bottom/left` |

```css
.tarjeta {
  width: 320px;
  padding: 24px;
  border: 2px solid #d0d0d0;
  margin: 16px;
  background-color: #f7f7f7; /* se pinta hasta el borde, no en el margin */
}
```

Un detalle que suele pasar desapercibido: por defecto (`background-clip: border-box`, su valor inicial), el `background` de un elemento se extiende hasta el borde **exterior** de la caja, es decir, se pinta también por debajo del `border` (content box + padding box + border box). Como el borde normalmente es opaco y se dibuja encima, en la práctica el fondo parece detenerse justo donde empieza el borde — pero si usas un borde con huecos (`dashed`, `dotted`) o con transparencia, verás el fondo asomando por debajo de él. Lo que el fondo nunca cubre es el margin box: por eso el margin siempre se ve "transparente", dejando ver el fondo del contenedor padre o de la página.

## `box-sizing`: content-box vs border-box

Aquí es donde más confusión genera el modelo de caja, porque `width` y `height` **no siempre significan lo mismo**. La propiedad `box-sizing` decide qué incluye ese `width`/`height` que declaras.

### `content-box` (valor inicial)

Es el comportamiento por defecto de la mayoría de elementos: `width` y `height` se aplican **solo al contenido**. El padding y el border se suman por fuera, aumentando el tamaño final de la caja.

```css
.caja-content-box {
  box-sizing: content-box; /* valor inicial, no haría falta escribirlo */
  width: 300px;
  padding: 20px;
  border: 10px solid #333;
}
/* Ancho total renderizado (border box):
   300 (content) + 20 + 20 (padding) + 10 + 10 (border) = 360px */
```

Esto significa que si añades padding o border a un elemento con `width: 300px`, su tamaño real crece por encima de esos 300px, algo muy poco intuitivo cuando estás maquetando con anchos fijos o porcentuales.

### `border-box`

Con `border-box`, `width` y `height` representan el tamaño **final** de la caja (contenido + padding + border incluidos). El navegador resta el padding y el border para calcular cuánto espacio le queda al contenido.

```css
.caja-border-box {
  box-sizing: border-box;
  width: 300px;
  padding: 20px;
  border: 10px solid #333;
}
/* Ancho total renderizado: 300px (fijo).
   Ancho disponible para el contenido: 300 - 20 - 20 - 10 - 10 = 240px */
```

### Por qué casi siempre conviene `border-box`

Con `content-box`, cualquier padding o border que añadas obliga a recalcular a mano el ancho total, y eso se vuelve especialmente molesto en layouts con `width: 100%`, grids de columnas o componentes reutilizables donde no controlas si alguien añadirá padding después. Con `border-box`, el ancho que declaras es el ancho que ocupa el elemento en pantalla, punto. Por eso es la convención casi universal en proyectos modernos: se declara `width` una vez y se puede tocar padding/border libremente sin que el layout se rompa.

El reset habitual para aplicarlo a todo el documento es:

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}
```

Se incluyen explícitamente `*::before` y `*::after` porque `box-sizing` **no es una propiedad heredable** (su valor inicial es `content-box` y cada elemento lo recibe de forma independiente si no se especifica algo distinto), y los pseudo-elementos generados no heredan automáticamente el valor puesto en `*` salvo que también se seleccionen.

Una variante más flexible, popularizada porque permite que un componente de terceros con `box-sizing` propio no se vea forzado:

```css
html {
  box-sizing: border-box;
}

*,
*::before,
*::after {
  box-sizing: inherit;
}
```

!!! tip "Dato útil"

    Varios elementos de formulario ya usan `border-box` por defecto en la hoja de estilos del navegador (el *user-agent stylesheet*): `<table>`, `<select>`, `<button>` y ciertos tipos de `<input>` como `checkbox`, `radio`, `reset`, `submit`, `button`, `color` y `search`. El reset universal simplemente extiende ese mismo comportamiento, más predecible, a todo lo demás.

!!! tip "Soporte de navegadores"

    `box-sizing` con los valores `content-box` y `border-box` está disponible en todos los navegadores modernos desde hace más de una década (Baseline, ampliamente disponible desde 2015). Puedes usarlo sin ninguna capa de compatibilidad adicional. Consulta el detalle en [caniuse.com/css3-boxsizing](https://caniuse.com/css3-boxsizing).

## Colapso de márgenes (margin collapsing)

El colapso de márgenes es un comportamiento del flujo normal de bloque en el que **dos márgenes verticales adyacentes no se suman, sino que se funden en uno solo**, cuyo tamaño es el mayor de los dos (o el valor común si son iguales). Es una de las causas más habituales de "este espacio no mide lo que debería" para quien no lo conoce, pero tiene una lógica: los márgenes representan espacio entre bloques de texto, y sumar dos márgenes contiguos duplicaría visualmente ese espaciado en la mayoría de los documentos de texto.

### Cuándo colapsa

**1. Entre hermanos adyacentes.** El `margin-bottom` de un elemento y el `margin-top` del siguiente hermano se funden en uno solo:

```css
p {
  margin: 0.4rem 0 1.2rem 0;
}
```

```html
<p>Primer párrafo.</p>
<p>Segundo párrafo.</p>
```

Entre ambos párrafos el espacio resultante es `1.2rem` (el mayor de los dos), **no** `0.4rem + 1.2rem = 1.6rem`.

**2. Entre un contenedor y su primer/último hijo.** Si no hay nada que los separe, el `margin-top` del padre colapsa con el `margin-top` de su primer hijo, y lo mismo ocurre con el `margin-bottom` del padre y el de su último hijo. Lo que cuenta como "separación" no es idéntico en ambos lados: el margen superior deja de colapsar si el padre tiene `padding-top`, `border-top`, contenido en línea antes del hijo o si el hijo tiene `clearance`; el margen inferior deja de colapsar, además, si el padre tiene `padding-bottom`, `border-bottom`, **o un `height`/`min-height` explícitos** (distintos de `auto`):

```css
.contenedor { margin-top: 2rem; }
.contenedor > p:first-child { margin-top: 1rem; }
```

```html
<div class="contenedor">
  <p>Este párrafo "empuja" el margen del contenedor hacia fuera.</p>
</div>
```

Resultado: el espacio por encima de `.contenedor` es `2rem` (el mayor de 2rem y 1rem), no `3rem`. Visualmente, el margen del hijo "se escapa" fuera del padre.

**3. Márgenes de una caja vacía.** Si un elemento no tiene contenido, padding, border, `height` ni `min-height` que separen su propio `margin-top` de su `margin-bottom`, ambos colapsan entre sí:

```css
.vacio {
  margin-top: 1rem;
  margin-bottom: 2rem;
  /* sin contenido, padding ni border: el margen resultante es 2rem, no 3rem */
}
```

**Con márgenes negativos**, la regla se ajusta así: se toma el mayor de los márgenes positivos y el más negativo de los márgenes negativos, y se suman ambos resultados; si todos son negativos, se usa el más negativo de todos.

### Cuándo NO colapsa

- Entre márgenes **horizontales** (`margin-left`/`margin-right`): el colapso solo afecta a márgenes verticales en flujo de bloque normal.
- Cuando hay `padding` o `border` interpuesto en la dirección correspondiente (por ejemplo, `padding-top` en el padre impide que su `margin-top` colapse con el de su primer hijo).
- En elementos **flotados** (`float` distinto de `none`).
- En elementos con **posicionamiento absoluto o fijo** (`position: absolute` o `fixed`).
- En los **hijos directos de un contenedor flex o grid** (`display: flex`, `grid`, `inline-flex`, `inline-grid`): estos usan sus propios algoritmos de espaciado (y `gap`) y sus márgenes nunca colapsan entre sí ni con el contenedor.
- En cualquier elemento que establezca su propio **contexto de formato de bloque (BFC)**: por ejemplo con `overflow` distinto de `visible` **y de `clip`** (este último tampoco genera BFC), `display: flow-root`, `display: inline-block`, `contain: layout`, etc. Un BFC "contiene" el colapso dentro de sus propios límites y evita que se propague hacia fuera.

### Cómo evitarlo cuando no lo quieres

La forma más limpia y sin efectos secundarios de impedir que el margen de un contenedor colapse con el de sus hijos es crear un nuevo contexto de formato de bloque con `display: flow-root`, pensado específicamente para esto:

```css
.contenedor {
  display: flow-root; /* crea un BFC: el margin-top del hijo ya no se escapa */
}
```

Otras alternativas también válidas, aunque con efectos colaterales a tener en cuenta:

```css
.contenedor {
  overflow: auto; /* crea BFC, pero puede generar barras de scroll no deseadas */
}

.contenedor {
  padding-top: 1px; /* rompe el colapso interponiendo espacio real */
}
```

Y para el colapso entre hermanos, si estás maquetando listas de tarjetas o secciones, casi siempre es preferible pasar a `display: flex` con `gap` (o `display: grid` con `gap`) en el contenedor: el espaciado entre elementos se controla en un único lugar y no depende en absoluto del colapso de márgenes.

!!! tip "Soporte de navegadores"

    `display: flow-root` es la herramienta recomendada hoy para crear un BFC sin efectos secundarios. Tiene soporte amplio en navegadores modernos (Chrome, Firefox, Safari y Edge), aunque no existe en versiones antiguas de Internet Explorer. Revisa el detalle en [caniuse.com/flow-root](https://caniuse.com/flow-root).

## `outline` vs `border`

Aunque a simple vista dibujan algo parecido (una línea alrededor del elemento), `outline` y `border` son conceptualmente distintos y no deberían confundirse:

| | `border` | `outline` |
| --- | --- | --- |
| ¿Forma parte del box model? | Sí: es una de las cuatro capas de la caja | No: se dibuja *fuera* de la caja, sin afectarla |
| ¿Afecta al tamaño/layout? | Sí, ocupa espacio (salvo con `box-sizing: border-box`) | No, nunca desplaza a otros elementos |
| ¿Puede tener esquinas independientes / `border-radius`? | Sí, cada lado es configurable por separado | Es una única propiedad shorthand alrededor de todo el elemento |
| ¿Puede ser no rectangular? | No, siempre delimita la caja rectangular (por línea, en inline) | En elementos en línea que ocupan varias líneas, algunos navegadores dibujan un contorno único que envuelve todas las líneas en lugar de una caja por línea |
| Separación configurable del elemento | No existe algo equivalente | `outline-offset` permite alejarlo de la caja sin tocar el layout |

```css
.boton {
  border: 1px solid #444;
  border-radius: 6px;
  padding: 8px 16px;
}

.boton:focus-visible {
  outline: 3px solid #2684ff;
  outline-offset: 2px; /* separa el contorno del borde sin mover nada */
}
```

`outline` es el shorthand de `outline-width`, `outline-style` (por defecto `none`, por eso es invisible si no lo defines explícitamente) y `outline-color`. Al no ocupar espacio en el layout, es la herramienta correcta para indicadores de foco y accesibilidad: puedes mostrar un contorno llamativo al enfocar un elemento con teclado sin que el resto de la página se desplace ni un píxel, algo que sí ocurriría si usaras `border` para el mismo propósito.

!!! warning "No elimines el outline sin reemplazo"

    Quitar el indicador de foco por defecto con `outline: none` (o `outline: 0`) sin poner un estilo de foco visible alternativo es un problema serio de accesibilidad para quien navega con teclado. Si necesitas personalizar el foco, sustitúyelo por otro `outline` (o `box-shadow`) visible, idealmente usando el pseudo-clase `:focus-visible` para no mostrarlo en clics de ratón.

!!! tip "Soporte de navegadores"

    Las propiedades `outline` y `outline-offset` tienen soporte amplio en todos los navegadores modernos. Consulta el detalle en [caniuse.com/outline](https://caniuse.com/outline).

## Ver también

- [Display y flujo normal](../layout/display-y-flujo-normal.md)
- [Overflow y desbordamiento](../layout/overflow.md)
- [Positioning](../layout/positioning.md)
- [Unidades y valores](unidades.md)

## Fuentes

- [box-sizing - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/box-sizing)
- [Introduction to the CSS box model - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_box_model/Introduction_to_the_CSS_box_model)
- [Mastering margin collapsing - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_box_model/Mastering_margin_collapsing)
- [Block formatting context - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_display/Block_formatting_context)
- [outline - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/outline)
- [CSS3 Box-sizing - caniuse.com](https://caniuse.com/css3-boxsizing)
- [flow-root - caniuse.com](https://caniuse.com/flow-root)
- [CSS outline properties - caniuse.com](https://caniuse.com/outline)
