# Color moderno: oklch, color-mix() y sintaxis de color relativo

En [Colores](../fundamentos/colores.md) vimos que `oklch()`, `oklab()` y `color-mix()` existen y para qué sirven a grandes rasgos. Esta página va al grano de por qué merece la pena migrar tus tokens de color a estas funciones: cómo `oklch()` resuelve un problema real de `hsl()` que probablemente ya te ha mordido alguna vez, cómo `color-mix()` sustituye a funciones de Sass como `lighten()` o `mix()` sin salir de CSS, y cómo la **sintaxis de color relativo** (`oklch(from ...)`) te permite derivar toda una paleta de estados (hover, disabled, fondos tenues) a partir de un único color base, sin duplicar valores ni recalcular nada a mano.

## El problema que resuelve oklch(): luminosidad perceptual

`hsl()` describe la luminosidad (`L`) de forma puramente matemática: es una media entre el canal más claro y el más oscuro del color en sRGB. El problema es que esa media **no se corresponde con lo que el ojo humano percibe como brillo**. Dos colores con el mismo `L` en HSL pueden verse muy distintos en luminosidad:

```css
.amarillo { background: hsl(60 100% 50%); }  /* se percibe muy claro */
.azul     { background: hsl(240 100% 50%); } /* se percibe mucho más oscuro */
```

Ambos tienen `L: 50%`, pero si los pones uno junto al otro el amarillo parece notablemente más luminoso que el azul. Esto no es un defecto puntual: es inherente a cómo HSL deriva la luminosidad directamente de los valores RGB, sin tener en cuenta que el ojo humano no percibe el rojo, el verde y el azul con el mismo brillo aparente.

`oklch()` (y su equivalente cartesiano `oklab()`) usan el espacio de color **Oklab**, diseñado específicamente para que la distancia numérica entre dos colores se corresponda con la diferencia perceptual real entre ellos. En la práctica, esto significa que **el mismo valor de `L` se percibe igual de claro u oscuro sea cual sea el matiz**:

```css
.a { background: oklch(70% 0.15 30);  }  /* rojo anaranjado, L=70% */
.b { background: oklch(70% 0.15 145); }  /* verde,           L=70% */
.c { background: oklch(70% 0.15 260); }  /* azul violeta,    L=70% */
```

Los tres colores anteriores tienen chroma (`C`) y luminosidad (`L`) idénticos y solo cambia el matiz (`H`); al verlos juntos, su brillo percibido es consistente. Esa propiedad —**uniformidad perceptual**— es la razón principal por la que oklch se ha convertido en el estándar recomendado para construir escalas de color (paletas de 50 a 900, por ejemplo) y para animaciones de color: subir o bajar `L` en una cantidad fija produce un cambio de brillo equivalente sea cual sea el color de partida, algo que con `hsl()` no puedes dar por hecho.

!!! tip "Por qué importa en un design system"

    Si generas una paleta con `hsl()` variando solo `L` (por ejemplo, para los tonos 100–900 de un color de marca), es habitual que algunos escalones "se queden cortos" o "se pasen" de claros/oscuros según el matiz de partida, obligando a ajustar cada rama a mano. Con `oklch()` el mismo incremento de `L` mantiene un salto de brillo comparable en cualquier matiz, lo que hace que las escalas generadas por fórmula (o por `color-mix()` y color relativo, como veremos abajo) se vean consistentes sin retoques manuales.

### Sintaxis de oklch() y oklab()

```css
oklch(L C H)          /* sin alfa */
oklch(L C H / A)      /* con canal alfa */
```

- **`L` (lightness)**: `<number>` de `0` a `1`, o `<percentage>` de `0%` a `100%` (`0%` = `0`, `100%` = `1`). Es la luminosidad percibida, no comparativa como en `hsl()`.
- **`C` (chroma)**: `<number>` sin límite superior estricto, o `<percentage>` donde `100%` equivale a `0.4`. En la práctica los colores dentro de gamuts habituales rara vez superan `0.4`; `0` es completamente acromático (gris).
- **`H` (hue)**: un ángulo (`<number>` interpretado en grados, o `<angle>` explícito con `deg`/`rad`/`grad`/`turn`). Importante: **los grados de `oklch()` no significan lo mismo que los de `hsl()`**, porque cada uno mide el ángulo sobre un espacio de color distinto. En `hsl()`, `0deg` es rojo; en Oklab, `0deg` corresponde aproximadamente a un rosa/magenta, y el rojo está cerca de `29deg`. No puedes reutilizar un ángulo de `hsl()` en `oklch()` esperando el mismo matiz.
- **`A` (alfa)**, opcional tras `/`: `<number>` de `0` a `1` o `<percentage>`, igual que en el resto de funciones de color.

`oklab()` es la versión cartesiana del mismo espacio: en vez de chroma y matiz usa dos ejes, `a` (verde↔rojo) y `b` (azul↔amarillo), cada uno con rango práctico de `-0.4` a `0.4`:

```css
.rosa-oklab { background: oklab(70% 0.15 -0.02); }
.rosa-oklch { background: oklch(70% 0.151 352); } /* mismo color, notación polar */
```

Usa `oklch()` cuando quieras razonar en términos de "más saturado/menos saturado" o "gira el matiz", y `oklab()` cuando necesites interpolar directamente sobre los ejes `a`/`b` (por ejemplo, en cálculos programáticos). En CSS de autor, `oklch()` suele ser más legible porque el matiz es un ángulo intuitivo.

!!! tip "Soporte de navegadores"

    `oklch()` y `oklab()` tienen **Baseline: Widely available** desde 2023: Chrome/Edge 111+, Firefox 113+ y Safari 15.4+. No están disponibles en Internet Explorer ni en versiones de navegadores anteriores a esas. Consulta [caniuse: oklch() color model](https://caniuse.com/mdn-css_types_color_oklch).

## color-mix(): mezclar colores sin salir de CSS

`color-mix()` toma dos colores y devuelve el resultado de mezclarlos en un espacio de color concreto, en la proporción que indiques. Es el reemplazo directo de funciones que antes solo existían en preprocesadores como Sass (`mix()`, `lighten()`, `darken()`):

```css
color-mix(in <color-space>, <color> [<percentage>], <color> [<percentage>])
```

```css
:root {
  --marca: royalblue;
}

.boton {
  background-color: var(--marca);
}

.boton:hover {
  background-color: color-mix(in oklch, var(--marca) 85%, black);
}

.boton:disabled {
  background-color: color-mix(in oklch, var(--marca) 40%, white);
}
```

### Reglas de los porcentajes

- Si omites los dos porcentajes, se asume `50%`/`50%`.
- Si solo indicas uno, el otro se calcula para que sumen `100%` (`color-mix(in srgb, red 30%, blue)` mezcla 30% rojo / 70% azul).
- Si la suma de ambos porcentajes es **menor que 100%**, el resultado se vuelve parcialmente transparente: por ejemplo, `color-mix(in srgb, red 30%, blue 40%)` produce 30% rojo + 40% azul, y como la suma es 70%, el color final lleva además un 30% de transparencia añadida.
- Los dos porcentajes al `0%` a la vez (`color-mix(in srgb, red 0%, blue 0%)`) es un valor inválido.

### El espacio de color cambia el resultado

El espacio indicado tras `in` no es un detalle menor: determina la trayectoria que siguen los valores intermedios. Puedes mezclar en espacios rectangulares (`srgb`, `srgb-linear`, `display-p3`, `lab`, `oklab`, `xyz`...) o en espacios polares (`hsl`, `hwb`, `lch`, `oklch`), y en estos últimos puedes además elegir cómo interpola el matiz:

```css
color-mix(in oklch, hsl(200 50% 80%), coral);                  /* shorter hue (por defecto) */
color-mix(in oklch longer hue, hsl(200 50% 80%), coral);        /* da la vuelta larga */
color-mix(in oklch increasing hue, hsl(200 50% 80%) 44%, coral 16%);
color-mix(in oklch decreasing hue, yellow, blue);
```

Mezclar en `srgb` suele producir tonos apagados o grisáceos a mitad de camino cuando los colores de partida están en lados opuestos de la rueda de color; mezclar en `oklch` u `oklab` da transiciones más vivas y naturales porque la distancia numérica en esos espacios se corresponde con la diferencia perceptual. Ojo con dar por hecho cuál es el espacio "por defecto": la gramática actual permite omitir `in <espacio>` por completo, y en ese caso la especificación indica que el resultado se calcula en Oklab, no en `srgb`. Como el soporte de esa forma abreviada todavía es desigual entre navegadores, lo más seguro es declarar siempre el espacio explícitamente, como en todos los ejemplos de esta página. Para generar escalas de marca (tints/shades) o transiciones de color en animaciones, `oklch`/`oklab` suele ser la opción recomendada.

Un patrón muy práctico es combinarlo con `currentColor` para conseguir un fondo tenue que siempre combine con el texto, sin conocer su valor exacto:

```css
.aviso {
  color: darkred;
  background-color: color-mix(in oklch, currentColor 12%, transparent);
}
```

!!! tip "Soporte de navegadores"

    `color-mix()` tiene **Baseline: Widely available** desde 2023: Chrome/Edge 111+, Firefox 113+ y Safari 16.2+. Consulta [caniuse: color-mix()](https://caniuse.com/mdn-css_types_color_color-mix).

## Sintaxis de color relativo: derivar un color a partir de otro

La **sintaxis de color relativo** (*relative color syntax*, definida en CSS Color Module Level 5) añade un `from <color>` al principio de cualquier función de color moderna (`rgb()`, `hsl()`, `hwb()`, `lab()`, `lch()`, `oklab()`, `oklch()`, `color()`). Ese `from` "abre" el color de origen y expone sus canales como palabras clave que puedes reutilizar, modificar con `calc()` o ignorar:

```css
oklch(from <color> L C H)
oklch(from <color> L C H / A)
```

Cada función expone los nombres de canal que le corresponden:

| Función | Canales disponibles |
|---|---|
| `rgb()` | `r`, `g`, `b`, `alpha` |
| `hsl()` | `h`, `s`, `l`, `alpha` |
| `hwb()` | `h`, `w`, `b`, `alpha` |
| `lab()` | `l`, `a`, `b`, `alpha` |
| `lch()` | `l`, `c`, `h`, `alpha` |
| `oklab()` | `l`, `a`, `b`, `alpha` |
| `oklch()` | `l`, `c`, `h`, `alpha` |

El caso de uso más habitual: partir de un color base guardado en una custom property y derivar variantes más claras, más oscuras o más transparentes sin volver a escribir el color completo:

```css
:root {
  --color-marca: oklch(60% 0.15 250);
}

.boton {
  background-color: var(--color-marca);
}

.boton:hover {
  /* misma H y C, un poco más oscuro */
  background-color: oklch(from var(--color-marca) calc(l - 0.1) c h);
}

.boton:focus-visible {
  /* mismo color, más saturado */
  background-color: oklch(from var(--color-marca) l calc(c + 0.05) h);
}

.boton[disabled] {
  /* mismo color, mucho más claro */
  background-color: oklch(from var(--color-marca) 0.9 c h);
}
```

Y el ejemplo que da título a esta sección —una variante semitransparente del color base, útil para fondos sutiles, overlays o anillos de foco—:

```css
.tarjeta {
  --color-marca: oklch(55% 0.18 260);
  border: 1px solid oklch(from var(--color-marca) l c h / 0.5);
  background-color: oklch(from var(--color-marca) l c h / 0.08);
}
```

Aquí `l`, `c` y `h` simplemente reutilizan los valores del color de origen sin cambiarlos, y solo el canal alfa se sobrescribe. Si omites el canal alfa por completo (`oklch(from var(--color-marca) l c h)`), el resultado hereda el alfa del color de origen en vez de asumir opacidad total, al contrario que en la sintaxis absoluta.

### Puntos importantes

- **Los canales se resuelven como `<number>`**, no como porcentajes ni ángulos con unidad, aunque el color de origen se escribiera con `%` o `deg`. Por eso `calc(l + 0.1)` funciona directamente sin necesidad de convertir unidades.
- **El navegador convierte el color de origen al espacio de la función de salida** antes de destructurarlo en canales. Puedes partir de un color en cualquier notación (`from red`, `from #123456`, `from hsl(180 100% 50%)`, `from var(--lo-que-sea)`) y expresar el resultado en otra función distinta:

  ```css
  .desde-hex-a-oklch {
    background-color: oklch(from #ff6b00 l c h);
  }
  ```

- **El valor `none`** se puede usar para descartar explícitamente un canal (por ejemplo, `oklch(from var(--color) l none h)` fuerza el chroma a `0`, produciendo un gris con la misma luminosidad).
- **Los canales no se recortan (clamp) al rango habitual**: si con `calc()` te sales del rango representable (por ejemplo, una `L` mayor que `1` o negativa), el valor se conserva tal cual lo especificaste; será el motor de renderizado el que, al pintar, ajuste el color al gamut disponible de la pantalla.
- El color de origen puede ser **otro color relativo**, lo que permite encadenar transformaciones paso a paso si lo necesitas, aunque en la práctica suele ser más legible resolverlo todo en una sola expresión.

### Generar una escala completa a partir de un solo color

Combinando `oklch(from ...)` con custom properties puedes definir toda una escala tonal de marca (por ejemplo, para fondos, hover y texto) a partir de un único valor fuente, sin tocar más que un sitio si cambias el color de marca:

```css
:root {
  --marca: oklch(58% 0.17 255);

  --marca-100: oklch(from var(--marca) 0.95 c h);
  --marca-300: oklch(from var(--marca) 0.8  c h);
  --marca-500: var(--marca);
  --marca-700: oklch(from var(--marca) 0.42 c h);
  --marca-900: oklch(from var(--marca) 0.25 c h);
}
```

Gracias a la uniformidad perceptual de Oklab, los saltos de `L` (`0.95`, `0.8`, `0.58`, `0.42`, `0.25`) producen una progresión de brillo consistente, algo que replicar con `hsl()` habría exigido tantear valores distintos de `L` para cada escalón según el matiz de partida.

!!! tip "Soporte de navegadores"

    La sintaxis de color relativo es más reciente que `oklch()` y `color-mix()`: alcanzó **Baseline: Newly available** en septiembre de 2024 (Chrome/Edge 125+, Firefox 128+, Safari 18+), tras un soporte inicial parcial desde 2023 en Chrome/Edge 119 y Safari 16.4 (esa primera versión de Safari exigía la unidad `deg` explícita dentro de `calc()` para el canal de matiz). Al no ser todavía "Widely available", conviene comprobar el estado real en [caniuse: CSS relative colors](https://caniuse.com/css-relative-colors) antes de depender de ella sin una alternativa para navegadores desactualizados, y usar `@supports (color: oklch(from red l c h))` para detectarla si necesitas un plan B.

## Ver también

- [Colores](../fundamentos/colores.md): repaso de todos los formatos de color de CSS, incluida la introducción a `oklch()`, `lab()`, `lch()` y `color()`.
- [Custom properties](../moderno/custom-properties.md): la pieza que hace prácticas las paletas derivadas de este documento, guardando el color base una sola vez.
- [Transiciones](../animaciones/transiciones.md): cómo se interpola un color al animarlo y por qué el espacio de color también afecta a las transiciones.
- [Unidades y valores](../fundamentos/unidades.md): detalle de las unidades de ángulo (`deg`, `turn`...) que aparecen en el canal `H` de `oklch()`.

## Fuentes

- [MDN: `oklch()`](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch)
- [MDN: `oklab()`](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklab)
- [MDN: `color-mix()`](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color-mix)
- [MDN: Using relative colors](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Colors/Using_relative_colors)
- [W3C: CSS Color Module Level 5 (sintaxis de color relativo)](https://www.w3.org/TR/css-color-5/)
- [W3C: CSS Color Module Level 4 (oklch, oklab, color-mix)](https://www.w3.org/TR/css-color-4/)
- [caniuse: oklch() color model](https://caniuse.com/mdn-css_types_color_oklch)
- [caniuse: color-mix()](https://caniuse.com/mdn-css_types_color_color-mix)
- [caniuse: CSS relative colors](https://caniuse.com/css-relative-colors)
