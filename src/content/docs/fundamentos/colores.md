---
title: Colores en CSS
description: Referencia de los formatos de color en CSS - palabras clave, hexadecimal, rgb(), hsl(), currentColor, los espacios de color modernos (lab, lch, oklab, oklch, color()) y la función color-mix().
---

El color es uno de los valores que más se repiten en cualquier hoja de estilos: fondos, texto, bordes, sombras, gradientes... Elegir bien el **formato** para escribir un color no es solo cuestión de gustos: afecta a si puedes usar transparencia, a si el color se anima o interpola de forma suave, o incluso a cuántos colores distintos puedes llegar a representar. En este documento repasamos todos los formatos válidos, desde las palabras clave más básicas hasta los espacios de color modernos con gamut ampliado.

## Palabras clave (`<named-color>`)

El formato más simple es escribir el nombre del color directamente. CSS define una lista larga de **colores con nombre** (`red`, `cornflowerblue`, `rebeccapurple`, `papayawhip`...) que cualquier navegador reconoce:

```css
.alerta {
  background-color: tomato;
  border-color: firebrick;
}
```

Además de los nombres "normales", existen dos palabras clave especiales que merecen su propia sección más abajo:

- `transparent`: un color totalmente transparente (equivalente a un color con canal alfa en 0).
- `currentcolor`: el color actual del elemento, heredado del `color` calculado. Lo vemos en detalle en [currentColor](#currentcolor-reutilizar-el-color-del-texto).

Las keywords son legibles y muy útiles para prototipar, pero en un proyecto real es raro que sobrevivan más allá de la fase inicial: no permiten ajustar matices ni transparencia, así que enseguida se migran a hexadecimal o a una función de color.

## Notación hexadecimal

El formato hexadecimal (`<hex-color>`) codifica los canales rojo, verde y azul (y opcionalmente alfa) como pares de dígitos hexadecimales (`00`–`ff`, es decir, 0–255 en decimal). Existen cuatro variantes:

```css
.caja {
  background-color: #ff0099;   /* #RRGGBB - 6 dígitos */
  border-color:     #f09;      /* #RGB    - 3 dígitos (atajo) */
  outline-color:    #ff0099aa; /* #RRGGBBAA - 8 dígitos, con alfa */
  box-shadow: 0 0 4px #f09a;   /* #RGBA   - 4 dígitos, con alfa (atajo) */
}
```

La clave de los atajos de 3 y 4 dígitos es que **cada dígito se duplica** para obtener el valor de 6 u 8 dígitos: `#f09` se expande a `#ff0099`, y `#f09a` se expande a `#ff0099aa`. Por eso un atajo solo puede representar 16 valores posibles por canal (`0`–`f`), no los 256 completos.

En los formatos con alfa, el último par de dígitos es el canal de transparencia: `00` es totalmente transparente y `ff` totalmente opaco. La notación es insensible a mayúsculas/minúsculas (`#00FF00` y `#00ff00` son el mismo color).

:::tip[Soporte de navegadores]
Los formatos de 6 y 3 dígitos son universales desde hace décadas. Los atajos con canal alfa (`#RGBA` y `#RRGGBBAA`) se definieron en CSS Color Module Level 4 y tienen soporte amplio (Chrome 62+, Firefox 49+, Safari 10+, Edge 79+), pero no funcionan en Internet Explorer. Consulta el detalle en [caniuse: #RRGGBBAA hex color notation](https://caniuse.com/css-rrggbbaa).
:::

## `rgb()` y `rgba()`

La función `rgb()` describe un color por sus componentes rojo, verde y azul, con un canal alfa opcional para la transparencia. Desde CSS Color 4, `rgb()` y `rgba()` son **exactamente la misma función** (alias): puedes usar cualquiera de las dos indistintamente, con o sin alfa. MDN recomienda usar `rgb()` para todo.

```css
/* Sintaxis moderna: valores separados por espacios, alfa tras "/" */
.moderno {
  color: rgb(255 0 153);
  background-color: rgb(255 0 153 / 0.5);
  border-color: rgb(100% 0% 60% / 50%);
}

/* Sintaxis "legacy": valores separados por comas (sigue siendo válida) */
.legacy {
  color: rgb(255, 0, 153);
  background-color: rgba(255, 0, 153, 0.5);
}
```

Los canales R, G y B aceptan un `<number>` de 0 a 255 o un `<percentage>` de 0% a 100%. El alfa acepta un `<number>` de 0 a 1 o un `<percentage>` de 0% a 100%. Un detalle importante: en la sintaxis **legacy** (con comas) los tres canales deben ser del mismo tipo —o los tres números, o los tres porcentajes—; no puedes mezclarlos. La sintaxis moderna es más flexible en ese sentido.

## `hsl()` y `hsla()`

`hsl()` describe el color con tres ejes más intuitivos para razonar sobre matices: **H**ue (matiz, un ángulo en la rueda de color), **S**aturation (saturación) y **L**ightness (luminosidad). Al igual que con `rgb()`/`rgba()`, desde CSS Color 4 `hsl()` y `hsla()` son alias exactos entre sí.

```css
.moderno {
  color: hsl(150 30% 60%);
  background-color: hsl(150 30% 60% / 80%);
}

.legacy {
  color: hsl(150, 30%, 60%);
  background-color: hsla(150, 30%, 60%, 0.8);
}
```

El matiz (`H`) se puede escribir como número sin unidad (interpretado en grados) o con una unidad de ángulo explícita: `deg`, `rad`, `grad` o `turn` (por ejemplo, `hsl(0.4turn 60% 45%)`). Saturación y luminosidad son porcentajes. En la sintaxis legacy con comas, el `%` en saturación y luminosidad es obligatorio y el matiz no admite la palabra clave `none`.

`hsl()` es cómodo para razonar "quiero el mismo tono pero más claro" (basta con subir `L`), aunque tiene una limitación real: su luminosidad no es perceptualmente uniforme, así que el mismo valor de `L` puede verse más o menos claro según el matiz. Los espacios de color modernos como `oklch()` resuelven justo este problema (lo vemos más abajo).

## `currentColor`: reutilizar el color del texto

`currentcolor` es una palabra clave que se resuelve al valor calculado de la propiedad `color` del elemento. Es especialmente útil en propiedades que **no heredan** `color` de forma automática, como `border-color`, `box-shadow`, `outline-color` o el `fill`/`stroke` de SVG.

```css
.tarjeta {
  color: darkslateblue;
  border: 1px solid currentColor;   /* usa darkslateblue sin repetir el valor */
  box-shadow: 0 0 0 3px currentColor;
}
```

Cuando `currentcolor` se usa en la propia propiedad `color`, no genera una referencia circular: toma el valor **heredado** de `color` del elemento padre. Su gran ventaja práctica es evitar la duplicación de valores: si cambias `color` en un solo sitio (por ejemplo, con una custom property de tema), todo lo que dependa de `currentColor` se actualiza solo.

## Espacios de color modernos: más allá de sRGB

`rgb()`, `hsl()` y el hexadecimal describen colores dentro del espacio **sRGB**, el mismo que llevan usando las pantallas desde los años 90. El problema es que sRGB es un gamut relativamente estrecho: hay colores muy saturados (sobre todo verdes y cian) que las pantallas modernas —muchas ya con soporte **Display P3**— pueden mostrar pero que sRGB no puede describir.

CSS Color Module Level 4 añade varias funciones para trabajar con espacios de color más amplios y, sobre todo, **perceptualmente uniformes**:

| Función | Espacio de color | Idea principal |
|---|---|---|
| `lab()` | CIELAB | Lightness + ejes a (verde↔rojo) y b (azul↔amarillo) |
| `lch()` | CIELAB en polar | Lightness + Chroma (intensidad) + Hue (ángulo) |
| `oklab()` | Oklab | Como `lab()`, pero con un modelo de uniformidad perceptual más moderno y preciso |
| `oklch()` | Oklab en polar | Como `lch()`, pero sobre Oklab |
| `color()` | Espacios con nombre (`srgb`, `display-p3`, `a98-rgb`, `rec2020`, `xyz`...) | Acceso explícito a gamuts amplios como Display P3 |

```css
.moderno {
  background-color: oklch(60% 0.15 250);        /* L C H */
  color: lch(30% 40 280);
  border-color: color(display-p3 1 0.5 0);       /* gamut amplio explícito */
}
```

¿Por qué importan estos formatos en un proyecto real?

- **Gamut más amplio**: `lab()`, `lch()`, `oklab()`, `oklch()` y `color()` pueden describir colores que sRGB no puede representar, aprovechando pantallas con Display P3 o Rec. 2020.
- **Mejor interpolación**: al animar o mezclar colores, sRGB y HSL suelen pasar por tonos grisáceos o apagados a mitad de camino (por ejemplo, al interpolar de azul a amarillo). Los espacios como Oklab/OkLCH producen transiciones mucho más naturales porque su distancia numérica se corresponde con la diferencia perceptual real.
- **Luminosidad predecible**: en `oklch()`, cambiar solo `L` mantiene el matiz y la saturación percibidos estables, algo que `hsl()` no garantiza. Esto hace mucho más fácil generar escalas de un color (más claro/más oscuro) de forma consistente.

Esta página cubre solo la introducción a estos formatos; el detalle de sintaxis, la sintaxis de colores relativos (`oklch(from ...)`) y ejemplos de theming están en [Color moderno (oklch, color-mix)](../moderno/color-moderno).

:::tip[Soporte de navegadores]
`lab()`, `lch()`, `oklab()`, `oklch()` y `color()` tienen **Baseline: Widely available** desde 2023 (Chrome/Edge 111+, Firefox 113+, Safari 15.4+ para `oklch()`, Safari 15+ para `color()`). No funcionan en navegadores más antiguos ni en Internet Explorer. Consulta [caniuse: oklch()](https://caniuse.com/mdn-css_types_color_oklch) y [caniuse: color()](https://caniuse.com/css-color-function).
:::

## `color-mix()`: mezclar colores directamente en CSS

`color-mix()` mezcla dos colores en un espacio de color determinado, en la proporción que indiques, sin necesidad de calcular el resultado a mano ni de recurrir a Sass:

```css
color-mix(in <color-space>, <color> [<percentage>], <color> [<percentage>])
```

```css
.boton {
  background-color: color-mix(in srgb, royalblue 80%, white);
  /* un tinte más claro de royalblue, sin definir un nuevo color a mano */
}

.boton:hover {
  background-color: color-mix(in srgb, royalblue 80%, black);
  /* un tono más oscuro para el estado hover */
}
```

Si omites los dos porcentajes, se asume 50%/50%. Si solo indicas uno, el otro se calcula para que sumen 100%. Y si la suma de ambos porcentajes es menor que 100%, el resultado se vuelve parcialmente transparente (como si se hubiera mezclado también con `transparent`).

Un uso muy práctico es combinarlo con `currentColor` para obtener una variante semitransparente de "el color que ya está en uso", sin tener que conocer su valor exacto:

```css
.aviso {
  color: darkred;
  background-color: color-mix(in srgb, currentColor 15%, transparent);
  /* fondo tenue del mismo tono que el texto, funcione con el color que funcione */
}
```

El espacio de color (`in srgb`, `in oklch`, `in hsl`, `in lab`...) determina cómo se interpolan los valores intermedios; en espacios polares como `hsl`, `hwb`, `lch` u `oklch` puedes además indicar el método de interpolación del matiz (`shorter hue`, `longer hue`, `increasing hue`, `decreasing hue`). El detalle de esas variantes queda para [Color moderno (oklch, color-mix)](../moderno/color-moderno).

:::tip[Soporte de navegadores]
`color-mix()` tiene **Baseline: Widely available** desde 2023 (Chrome/Edge 111+, Firefox 113+, Safari 16.2+). No está disponible en Internet Explorer ni en versiones de navegadores anteriores a 2023. Consulta [caniuse: color-mix()](https://caniuse.com/mdn-css_types_color_color-mix).
:::

## Ver también

- [Color moderno (oklch, color-mix)](../moderno/color-moderno): profundiza en los espacios de color modernos, la sintaxis de colores relativos y `color-mix()` con ejemplos de theming.
- [Custom properties](../moderno/custom-properties): la forma habitual de centralizar y reutilizar colores en un proyecto real.
- [Cascada, especificidad y herencia](../fundamentos/cascada-especificidad-herencia): entiende cómo hereda `color` para razonar mejor sobre `currentColor`.
- [Unidades y valores](../fundamentos/unidades): otros tipos de valores de CSS, como números, porcentajes y ángulos, que aparecen dentro de las funciones de color.

## Fuentes

- [MDN: `<color>` value](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value)
- [MDN: `<hex-color>`](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color)
- [MDN: `rgb()`](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/rgb)
- [MDN: `hsl()`](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/hsl)
- [MDN: `currentcolor`](https://developer.mozilla.org/en-US/docs/Web/CSS/currentColor)
- [MDN: `lab()`](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/lab)
- [MDN: `lch()`](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/lch)
- [MDN: `oklch()`](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch)
- [MDN: `color()`](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color)
- [MDN: `color-mix()`](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color-mix)
- [caniuse: #RRGGBBAA hex color notation](https://caniuse.com/css-rrggbbaa)
- [caniuse: oklch() color model](https://caniuse.com/mdn-css_types_color_oklch)
- [caniuse: color() function](https://caniuse.com/css-color-function)
- [caniuse: color-mix()](https://caniuse.com/mdn-css_types_color_color-mix)
