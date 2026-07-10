---
title: Unidades y valores en CSS
description: Guía de las unidades de medida en CSS (absolutas, relativas y de viewport) y de las funciones calc(), min(), max() y clamp() para calcular valores en lugar de fijarlos a mano.
---

Casi todas las propiedades de CSS (`width`, `font-size`, `margin`, `gap`...) necesitan un valor numérico con una unidad que le diga al navegador *a qué se refiere ese número*. Elegir bien la unidad no es un detalle cosmético: es lo que decide si tu diseño escala con el tamaño de fuente del usuario, si se adapta a la pantalla o si se rompe en cuanto alguien usa un móvil con una barra de direcciones que aparece y desaparece. Esta página repasa las unidades absolutas y relativas disponibles, cuándo conviene cada una, y las funciones `calc()`, `min()`, `max()` y `clamp()`, que permiten calcular valores en lugar de fijarlos a mano.

## Unidades absolutas

Las unidades absolutas representan una medida física fija: no cambian según el contenedor, la fuente ni el viewport. Todas se pueden convertir entre sí con una proporción constante, y en última instancia a píxeles CSS (`px`).

| Unidad | Nombre | Equivalencia |
|---|---|---|
| `px` | Píxel | Unidad de referencia (1px = 1px) |
| `in` | Pulgada | 1in = 96px |
| `cm` | Centímetro | 1cm = 96px / 2.54 ≈ 37.8px |
| `mm` | Milímetro | 1mm = 1cm / 10 ≈ 3.78px |
| `Q` | Cuarto de milímetro | 1Q = 1cm / 40 ≈ 0.945px |
| `pc` | Pica | 1pc = 1in / 6 = 16px |
| `pt` | Punto | 1pt = 1in / 72 ≈ 1.33px |

:::note[El `px` de CSS no es un píxel físico]
El `px` de CSS es un **píxel de referencia** (*reference pixel*), definido para que 1in equivalga siempre a 96px, independientemente de la densidad de píxeles real de la pantalla. Es el propio navegador quien traduce ese píxel CSS a píxeles físicos según el `dpi` del dispositivo. Por eso `1cm` mide lo mismo en una pantalla 4K que en una de baja resolución (al menos en teoría; en pantallas la corrección no siempre es perfecta), mientras que en un documento impreso sí se corresponde con un centímetro real.
:::

**¿Cuándo usarlas?**

- `px` es razonable para cosas que deben tener un tamaño físico consistente sin importar el contexto: bordes finos (`border: 1px solid`), sombras, radios de esquina pequeños o breakpoints de `media queries`.
- `cm`, `mm`, `in`, `pt`, `pc` y `Q` solo tienen sentido real en hojas de estilo pensadas para impresión (`@media print`); en pantalla no aportan nada que `px` no dé ya.

:::caution[No uses unidades absolutas para `font-size`]
Si fijas el tamaño de texto en `px`, `pt` o `cm`, el usuario no puede escalarlo con la configuración de "tamaño de fuente" del navegador en algunos navegadores (Chrome, Firefox y Safari sí permiten hacer zoom de página incluso con `px`, pero la opción de tamaño de fuente del navegador puede no afectar a unidades absolutas). Usa unidades relativas (`rem`, `em`, `%`) para que el texto respete las preferencias de accesibilidad del usuario.
:::

## Unidades relativas

Las unidades relativas se calculan en función de otra cosa: el tamaño de fuente de un elemento, el de la raíz del documento, o las dimensiones del viewport. Son la base de cualquier diseño que deba adaptarse.

### Porcentaje (`%`)

El `%` se resuelve respecto a otro valor que depende de la propiedad: en `width`/`height` es el tamaño del contenedor de referencia (normalmente el *content box* del elemento padre), en `font-size` es el tamaño de fuente heredado, en `translate` es el tamaño de la propia caja, etc. No es una unidad de longitud como tal, sino un `<percentage>` que cada propiedad interpreta a su manera.

```css
.sidebar {
  width: 25%; /* 25% del ancho del contenedor padre */
}
```

### `em` y `rem`: relativas a la fuente

- **`em`**: relativo al `font-size` *computado* del propio elemento (o, si se usa en la propiedad `font-size`, al tamaño heredado del padre). Esto significa que los `em` se **acumulan**: si un `.card` tiene `font-size: 1.2em` y dentro hay un `<strong>` con `padding: 1em`, ese padding se calcula sobre el tamaño ya multiplicado del `.card`, no sobre el tamaño raíz.
- **`rem`** (*root em*): relativo únicamente al `font-size` del elemento raíz (`<html>`), sea cual sea el nivel de anidamiento. Por defecto ese tamaño raíz es `16px` en la mayoría de navegadores, pero es configurable por el usuario, así que `rem` sigue respetando la accesibilidad.

```css
html {
  font-size: 100%; /* respeta la preferencia del navegador, normalmente 16px */
}

.card {
  font-size: 1.2em;  /* 1.2 × el tamaño heredado */
  padding: 1rem;      /* siempre relativo a <html>, no al .card */
}

.card strong {
  padding: 0.5em; /* relativo al font-size ya ampliado de .card: efecto acumulativo */
}
```

**Cuándo usar cada una**: `rem` es la opción por defecto para tamaños de fuente, márgenes y paddings a nivel de componente, porque su resultado es predecible sin importar dónde se anide el elemento. `em` es útil cuando quieres que un valor escale *junto con* el tamaño de fuente de ese elemento en concreto (por ejemplo, un icono o un `padding` que debe crecer proporcionalmente si el texto de ese botón crece).

### `ch`: el ancho de un carácter

`ch` equivale al avance (ancho) del carácter `"0"` en la fuente del elemento. Es especialmente útil para limitar la longitud de línea de un bloque de texto a un número de caracteres aproximado, algo recomendado para la legibilidad (habitualmente entre 45 y 75 caracteres por línea).

```css
p {
  max-width: 65ch; /* aprox. 65 caracteres por línea, con la fuente actual */
}
```

### `vw`, `vh`, `vmin`, `vmax`: relativas al viewport

Estas unidades se calculan como un porcentaje de las dimensiones del *viewport* (el área visible del documento):

- `1vw` = 1% del ancho del viewport.
- `1vh` = 1% del alto del viewport.
- `1vmin` = el menor entre `1vw` y `1vh`.
- `1vmax` = el mayor entre `1vw` y `1vh`.

```css
.hero {
  height: 100vh;   /* ocupa toda la altura visible */
  padding-inline: 5vw;
}
```

El problema clásico de `vh` aparece en móviles: la especificación indica que las unidades de viewport "por defecto" (`vw`, `vh`...) equivalen actualmente al **viewport grande** (*large viewport*), es decir, al tamaño que tendría la pantalla si la barra de direcciones y otras barras del navegador estuvieran ocultas. Como esas barras aparecen y desaparecen al hacer scroll, un `height: 100vh` puede quedar por debajo del borde visible real cuando la barra está desplegada, dejando una franja cortada o generando una barra de scroll indeseada. Para resolver justo ese problema existen las unidades de viewport dinámico.

### Unidades modernas de viewport: `svh`, `lvh`, `dvh` (y sus variantes de ancho)

La especificación [CSS Values and Units Module Level 4](https://www.w3.org/TR/css-values-4/#viewport-relative-lengths) define tres tamaños de viewport distintos, cada uno con su propio juego de unidades (`w`, `h`, `i`, `b`, `min`, `max`):

- **Viewport pequeño (`sv*`, *small viewport*)**: asume que las barras/interfaces del navegador que pueden expandirse están **desplegadas**. Es el tamaño más conservador: el contenido cabe siempre, pero puede dejar espacio vacío cuando esas barras se ocultan.
- **Viewport grande (`lv*`, *large viewport*)**: asume que esas barras están **retraídas/ocultas**. El contenido aprovecha toda la pantalla cuando las barras desaparecen, pero puede quedar tapado cuando reaparecen. Es el comportamiento que hoy tienen `vh`/`vw` por defecto.
- **Viewport dinámico (`dv*`, *dynamic viewport*)**: se **recalcula en tiempo real** según el estado actual de las barras del navegador, así que el contenido siempre encaja exactamente, sin importar si la barra está visible o no en cada momento.

```css
/* Vh clásico: en móvil puede quedar cortado por la barra de direcciones */
.pantalla-completa-clasica {
  height: 100vh;
}

/* Dvh: se ajusta al alto real disponible en cada momento */
.pantalla-completa-moderna {
  height: 100dvh;
}
```

El propio grupo de trabajo advierte de una contrapartida importante: como el valor de `dvh` cambia mientras el usuario hace scroll (porque la barra del navegador se expande o retrae), un elemento dimensionado con `dvh` puede **redimensionarse visiblemente durante el scroll**, lo cual puede sentirse menos fluido que un valor estable. Si tu contenido no necesita reaccionar a ese cambio en vivo, `svh` o `lvh` (que son estables mientras el viewport no cambie de tamaño) pueden ser preferibles a `dvh`.

Existen también las variantes de ancho e inline/block: `svw`/`lvw`/`dvw` (ancho), `svi`/`lvi`/`dvi` e `svb`/`lvb`/`dvb` (según el eje de escritura), y sus correspondientes `svmin`/`svmax`, `lvmin`/`lvmax`, `dvmin`/`dvmax`.

:::tip[Soporte de navegadores]
Las unidades de viewport pequeño/grande/dinámico (`svh`, `lvh`, `dvh` y el resto de variantes) tienen buen soporte en navegadores modernos, pero no existen en versiones antiguas. Comprueba la compatibilidad actualizada en [caniuse: Small, Large, and Dynamic viewport units](https://caniuse.com/viewport-unit-variants) antes de depender de ellas sin una unidad de respaldo (por ejemplo, declarando primero `height: 100vh` y después `height: 100dvh`, para que los navegadores que no reconocen `dvh` se queden con el valor anterior).
:::

## Guía rápida: qué unidad usar según el caso

| Necesitas | Unidad recomendada |
|---|---|
| Tamaño de fuente de un componente | `rem` |
| Un valor que escale con el texto local (icono junto a una palabra) | `em` |
| Ancho de un bloque de texto legible | `ch` (o `max-width` con `%`/`clamp()`) |
| Ancho/alto relativo a su contenedor | `%` |
| Sección que debe ocupar el alto de pantalla | `dvh` (con fallback a `vh`) |
| Borde, sombra o radio pequeño y fijo | `px` |
| Hoja de estilos para impresión | `cm`, `mm`, `in`, `pt` |

## Funciones de valor: calcular en lugar de fijar

CSS permite calcular un valor en el propio navegador con las funciones matemáticas `calc()`, `min()`, `max()` y `clamp()`. Son especialmente potentes combinadas con unidades relativas, porque permiten mezclar unidades distintas (por ejemplo, un porcentaje y un `px`) en una sola expresión.

### `calc()`

`calc()` evalúa una expresión matemática con `+`, `-`, `*` y `/`, siguiendo la precedencia habitual de operadores. Puede mezclar tipos de unidades siempre que el resultado tenga sentido:

- En `+` y `-`, ambos operandos deben ser del mismo tipo (dos longitudes, dos ángulos...) y **es obligatorio dejar un espacio** a cada lado del operador (`calc(100% - 30px)`, nunca `calc(100%-30px)`).
- En `*`, solo uno de los dos operandos puede llevar unidad (no se puede multiplicar `px` por `px`).
- En `/`, el divisor debe ser un número sin unidad (o ambos deben ser longitudes, devolviendo un número sin unidad).

```css
.banner {
  /* Ancho del contenedor menos un margen fijo a cada lado */
  width: calc(100% - 2 * 40px);
}

.card {
  /* Combina rem (escala con accesibilidad) y vw (escala con la pantalla) */
  font-size: calc(1rem + 0.5vw);
}
```

`calc()` también se puede anidar, y las funciones anidadas se tratan como paréntesis normales:

```css
:root {
  --gutter: 1rem;
  --gutter-doble: calc(var(--gutter) * 2);
}
```

### `min()` y `max()`

`min()` recibe una lista de valores separados por comas y devuelve **el más pequeño**; `max()` devuelve **el más grande**. Son una alternativa declarativa a escribir varias reglas con `media queries` para imponer un límite.

```css
/* La tarjeta nunca supera los 400px, aunque el contenedor sea más ancho */
.card {
  width: min(90%, 400px);
}

/* El texto nunca baja de 1rem, aunque el viewport sea muy estrecho */
.texto-legible {
  font-size: max(1rem, 2vw);
}
```

En el primer ejemplo, en pantallas donde `90%` del contenedor supera los `400px`, gana `400px`; en pantallas más estrechas, donde `90%` es menor que `400px`, gana ese `90%`. En el segundo, `2vw` gana en pantallas anchas, pero nunca se permite bajar de `1rem`.

### `clamp()`: un valor fluido con tope inferior y superior

`clamp()` recibe tres argumentos: un **mínimo**, un **valor preferido** (normalmente basado en una unidad de viewport, para que escale) y un **máximo**. Equivale a `max(mínimo, min(valor-preferido, máximo))`, y es la herramienta habitual para tipografía y espaciados fluidos sin necesidad de `media queries`.

```css
h1 {
  /* Nunca menor a 1.8rem, nunca mayor a 3rem, escala con el viewport entre medias */
  font-size: clamp(1.8rem, 4vw + 1rem, 3rem);
}

.contenedor {
  /* Padding fluido: crece con la pantalla, sin desbordar ni desaparecer */
  padding-inline: clamp(1rem, 5vw, 3rem);
}
```

Esto sustituye patrones como:

```css
/* Enfoque tradicional con media queries: varios saltos bruscos */
h1 {
  font-size: 1.8rem;
}

@media (min-width: 600px) {
  h1 {
    font-size: 2.2rem;
  }
}

@media (min-width: 1200px) {
  h1 {
    font-size: 3rem;
  }
}
```

por una única línea con transición continua entre los tamaños, en lugar de saltos discretos en cada *breakpoint*.

:::caution[Accesibilidad: cuidado con la diferencia entre el mínimo y el máximo en `clamp()` para texto]
Los navegadores no escalan las unidades de viewport (`vw`) cuando el usuario hace zoom de página: el viewport en sí no cambia de tamaño, así que la parte de la fórmula basada en `vw` se queda "congelada" mientras el resto del texto sí crece con el zoom. Si el valor máximo de tu `clamp()` es mucho mayor que el mínimo, esa parte congelada pesa más en el resultado final y puede impedir que el texto alcance el 200% de aumento exigido por el criterio de éxito 1.4.4 (*Resize Text*) de las WCAG cuando el usuario amplía el navegador. Como referencia práctica (documentada por análisis como el de Smashing Magazine sobre accesibilidad en tipografía fluida), si el máximo no supera aproximadamente 2.5 veces el mínimo, el texto seguirá pudiendo escalarse correctamente; cuanto mayor sea esa proporción, más riesgo hay de incumplir el criterio.
:::

:::tip[Soporte de navegadores]
`calc()` es compatible con todos los navegadores modernos desde hace años (incluida la antigua Internet Explorer 9+ con soporte parcial). `min()`, `max()` y `clamp()` son más recientes: consulta la compatibilidad actualizada en [caniuse: CSS math functions min(), max() and clamp()](https://caniuse.com/css-math-functions) si necesitas dar soporte a navegadores muy antiguos.
:::

## Ver también

- [El modelo de caja](modelo-de-caja)
- [Media queries](../responsive/media-queries)
- [Unidades y funciones responsivas](../responsive/unidades-y-funciones)
- [Fuentes y propiedades de texto](../tipografia/fuentes-y-texto)

## Fuentes

- [MDN: `<length>`](https://developer.mozilla.org/en-US/docs/Web/CSS/length)
- [MDN: CSS Values and Units](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Values_and_Units)
- [MDN: `calc()`](https://developer.mozilla.org/en-US/docs/Web/CSS/calc)
- [MDN: `min()`](https://developer.mozilla.org/en-US/docs/Web/CSS/min)
- [MDN: `max()`](https://developer.mozilla.org/en-US/docs/Web/CSS/max)
- [MDN: `clamp()`](https://developer.mozilla.org/en-US/docs/Web/CSS/clamp)
- [W3C CSSWG: CSS Values and Units Module Level 4 — Viewport-percentage lengths](https://www.w3.org/TR/css-values-4/#viewport-relative-lengths)
- [caniuse: Small, Large, and Dynamic viewport units](https://caniuse.com/viewport-unit-variants)
- [caniuse: CSS math functions min(), max() and clamp()](https://caniuse.com/css-math-functions)
- [Smashing Magazine: Addressing Accessibility Concerns With Using Fluid Type](https://www.smashingmagazine.com/2023/11/addressing-accessibility-concerns-fluid-type/)
