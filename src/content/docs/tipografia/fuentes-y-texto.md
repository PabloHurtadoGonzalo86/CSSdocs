---
title: "Tipografía: fuentes y propiedades de texto"
description: Guía sobre cómo cargar fuentes propias con @font-face, construir pilas de font-family con fallback robustas y ajustar tamaño, peso, interlineado, alineación y corte de línea del texto en CSS.
---

La tipografía es, probablemente, el elemento que más tiempo pasa bajo los ojos de quien usa tu web: se lee mucho más de lo que se mira un botón o un icono. Por eso cómo cargas las fuentes, qué pila de *fallback* defines, y cómo ajustas tamaño, peso, interlineado y corte de línea no es un detalle estético menor, sino algo que afecta directamente a la legibilidad, al rendimiento de carga (una fuente mal cargada puede bloquear el renderizado del texto) y a la accesibilidad. Esta página repasa cómo declarar fuentes propias con `@font-face`, cómo construir pilas de fuentes robustas, las propiedades básicas de texto y las más recientes para controlar el corte de línea.

## `@font-face`: cargar tus propias fuentes

Por defecto, el navegador solo puede usar las fuentes instaladas en el sistema del usuario. La regla `@font-face` permite declarar una fuente personalizada (alojada en tu servidor o en un CDN) y darle un nombre que luego usarás en `font-family`.

```css
@font-face {
  font-family: "Inter";
  src:
    url("/fonts/inter-variable.woff2") format("woff2");
  font-weight: 100 900; /* rango de pesos: es una fuente variable */
  font-style: normal;
  font-display: swap;
}

body {
  font-family: "Inter", system-ui, sans-serif;
}
```

Los descriptores más relevantes dentro de `@font-face` son:

- **`font-family`** (obligatorio): el nombre que le das a esta fuente para referenciarla luego. No tiene que coincidir con el nombre real del archivo.
- **`src`** (obligatorio): una lista de fuentes candidatas, separadas por comas. Puede combinar `local()` (busca una fuente ya instalada en el sistema, evitando la descarga) y `url()` con `format()` indicando el formato del archivo:

    ```css
    @font-face {
      font-family: "Lora";
      src:
        local("Lora"),
        url("/fonts/lora.woff2") format("woff2"),
        url("/fonts/lora.woff") format("woff");
    }
    ```

    El navegador recorre la lista y usa el primer recurso que sea capaz de cargar, así que conviene poner primero los formatos más eficientes (`woff2`) y dejar formatos más antiguos (`woff`, `truetype`) como último recurso para navegadores muy antiguos.

- **`font-weight`, `font-style`, `font-stretch`**: además de un valor único, aceptan un **rango** (`font-weight: 100 900`) cuando el archivo es una **fuente variable** (*variable font*), es decir, un único archivo que contiene un eje continuo de pesos (u otros ejes, como el ancho) en lugar de un archivo por cada peso.
- **`unicode-range`**: limita qué caracteres Unicode debe cubrir ese `@font-face` concreto, útil para cargar solo el subconjunto de glifos que necesitas (por ejemplo, separar el alfabeto latino del cirílico en archivos distintos) y ahorrar peso de descarga.

:::tip[Soporte de navegadores]
`@font-face` en sí es una funcionalidad *Baseline: ampliamente disponible* desde 2015, soportada en todos los navegadores modernos. Consulta el detalle de formatos y descriptores concretos (como `unicode-range` o los rangos de `font-weight`/`font-stretch` para fuentes variables) en [caniuse: @font-face](https://caniuse.com/fontface) y [caniuse: WOFF 2.0](https://caniuse.com/woff2).
:::

### `font-display`: qué mostrar mientras la fuente carga

Descargar una fuente lleva tiempo, y el navegador tiene que decidir qué hacer con el texto mientras tanto: ¿lo deja invisible hasta que la fuente esté lista (provocando un destello de texto invisible, *FOIT*), o muestra ya una fuente de respaldo y la cambia luego (un destello de texto sin estilo, *FOUT*)? El descriptor `font-display` te deja elegir ese comportamiento explícitamente, en lugar de dejarlo a criterio del navegador.

El ciclo de carga se divide conceptualmente en tres periodos: el **periodo de bloqueo** (si la fuente no ha cargado, el texto se pinta invisible), el **periodo de intercambio** (si la fuente no ha cargado, se pinta ya con una fuente de respaldo, lista para sustituirse en cuanto la fuente personalizada esté disponible) y el **periodo de fallo** (pasado este punto, el navegador da la carga por fallida y se queda con la fuente de respaldo de forma definitiva).

| Valor | Bloqueo | Intercambio | Cuándo usarlo |
|---|---|---|---|
| `auto` | El que decida el navegador | El que decida el navegador | Valor por defecto; deja el criterio al navegador. |
| `block` | Corto | Infinito | Cuando el icono/glifo personalizado es imprescindible (p. ej. una fuente de iconos) y prefieres un breve parpadeo invisible antes que ver el fallback. |
| `swap` | Extremadamente corto | Infinito | El más habitual para texto de contenido: se ve algo de inmediato (con la fuente de respaldo) y se sustituye en cuanto la fuente personalizada esté lista, sin límite de espera. |
| `fallback` | Extremadamente corto | Corto | Un término medio: si la fuente tarda demasiado, se queda con el fallback y ya no cambia, para evitar un salto de maquetación tardío. |
| `optional` | Extremadamente corto | Ninguno | Prioriza el rendimiento por encima de la fuente personalizada: si no está ya en caché, ni siquiera espera a que termine de descargar en esa visita. |

```css
@font-face {
  font-family: "Inter";
  src: url("/fonts/inter-variable.woff2") format("woff2");
  font-display: swap; /* muestra el fallback ya, sustituye cuando cargue */
}
```

:::tip[Soporte de navegadores]
`font-display` es *Baseline: ampliamente disponible* desde 2020 (Chrome 60+, Firefox 58+, Safari 11.1+, Edge 79+). Revisa la compatibilidad detallada en [caniuse: font-display](https://caniuse.com/css-font-rendering-controls).
:::

## `font-family`: pilas de fuentes con `fallback`

`font-family` acepta una lista separada por comas de nombres de fuente y/o palabras clave genéricas. El navegador prueba cada nombre **de izquierda a derecha** y, además, lo hace **carácter por carácter**: si la primera fuente de la lista no tiene el glifo de un carácter concreto (por ejemplo, un emoji o una letra acentuada), el navegador prueba con la siguiente fuente de la lista solo para ese carácter, no para todo el texto.

```css
body {
  font-family: "Inter", "Helvetica Neue", Arial, sans-serif;
}

code, pre {
  font-family: "Fira Code", "Cascadia Code", ui-monospace, monospace;
}
```

Reglas prácticas para construir la pila:

- **Termina siempre con una palabra clave genérica** (`serif`, `sans-serif`, `monospace`, `cursive`, `fantasy`, `system-ui`...): es la red de seguridad si ninguna de las fuentes anteriores está disponible.
- **Entrecomilla los nombres compuestos** por varias palabras, que empiecen por un número o que contengan símbolos: `"Gill Sans Extrabold"`, `"Goudy Bookletter 1911"`. Un nombre de una sola palabra sin caracteres especiales (`Arial`) no necesita comillas, aunque añadirlas nunca es incorrecto.
- **`system-ui`** apunta a la fuente por defecto que usa el sistema operativo para su propia interfaz (San Francisco en macOS/iOS, Segoe UI en Windows, Roboto en Android...); es una forma barata de conseguir una tipografía nativa y ya cacheada sin declarar ningún `@font-face`.

```css
/* Pila típica "system font stack": sin ninguna descarga de fuente */
body {
  font-family:
    system-ui,
    -apple-system,
    "Segoe UI",
    Roboto,
    Arial,
    sans-serif;
}
```

## Tamaño, peso e interlineado: `font-size`, `font-weight`, `line-height`

### `font-size`

Además de longitudes (`1rem`, `16px`) y porcentajes (relativos al tamaño heredado del padre), `font-size` acepta palabras clave absolutas (`medium`, que es el valor inicial, `small`, `large`, `x-large`, `xx-large`, `xxx-large`...) y relativas (`larger`, `smaller`, respecto al tamaño heredado).

```css
html {
  font-size: 100%; /* respeta la preferencia de tamaño del navegador (normalmente 16px) */
}

p {
  font-size: 1rem;
}

h1 {
  font-size: 2rem;
}
```

:::caution[Evita fijar `font-size` en `px`]
Usar `px` para el tamaño de texto puede impedir que algunas personas usuarias amplíen el tamaño de fuente desde los ajustes de accesibilidad del navegador (no el zoom de página general, que sí suele funcionar con `px`, sino la opción específica de "tamaño de fuente"). Usar `rem`, `em` o `%` mantiene el texto flexible frente a esas preferencias. Puedes combinarlo con `clamp()` para tipografía fluida entre un mínimo y un máximo; lo vemos en detalle en [Unidades y valores en CSS](../fundamentos/unidades).
:::

### `font-weight`

Acepta las palabras clave `normal` (equivalente a `400`, valor inicial) y `bold` (equivalente a `700`), las palabras clave relativas `bolder`/`lighter` (un peso más grueso/fino que el heredado del padre), y valores numéricos de **1 a 1000**.

```css
p { font-weight: normal; }   /* 400 */
strong { font-weight: bold; } /* 700 */

.titulo {
  font-weight: 600; /* semibold, si la familia tipográfica incluye ese peso */
}
```

Con fuentes estáticas, lo que ocurre al pedir un peso concreto depende de cuántos archivos hayas registrado para esa familia. Si has declarado varias fuentes estáticas en pesos distintos (por ejemplo, un `@font-face` para `400` y otro para `700`) y pides un peso intermedio que ninguno cubre exactamente (pongamos, `600`), el navegador aplica el algoritmo de emparejamiento de `font-weight` de la especificación y usa, sin inventar nada, el peso registrado más cercano al solicitado. Pero si la familia solo tiene registrado un único peso (por ejemplo, únicamente `400`) y pides `bold`/`700`, el navegador recurre por defecto a una **negrita sintética** (*faux bold*): engorda artificialmente los trazos del único peso disponible para simular el efecto. Este comportamiento lo controla la propiedad `font-synthesis`, cuyo valor inicial lo permite; puedes desactivarlo con `font-synthesis: none` cuando el resultado no te convenza, algo especialmente recomendable en escrituras CJK, donde una negrita o cursiva falsas pueden llegar a dificultar la lectura. Con una **fuente variable** declarada con un rango en `@font-face` (`font-weight: 100 900`), en cambio, puedes pedir cualquier valor entero dentro de ese rango y obtener el trazo real correspondiente, no una aproximación ni una síntesis:

```css
.titulo-fino {
  font-family: "Inter"; /* fuente variable con rango 100–900 */
  font-weight: 350; /* valor intermedio real, no una aproximación */
}
```

:::caution[Accesibilidad de los pesos muy finos]
Pesos de `100`/`200` pueden ser difíciles de leer para personas con baja visión, especialmente si además el contraste de color es bajo. Resérvalos para títulos grandes, no para párrafos de lectura.
:::

### `line-height`

Controla la altura de la caja de línea, es decir, el espacio vertical entre líneas de texto. El valor inicial es `normal`, que en la mayoría de navegadores de escritorio se traduce en, aproximadamente, `1.2` veces el tamaño de fuente (el valor exacto depende de las métricas internas de la fuente usada).

```css
p {
  line-height: 1.5; /* número sin unidad: recomendado */
}
```

El detalle importante es **usar un número sin unidad** en lugar de `em` o `%`. Con un número sin unidad, cada elemento hijo calcula el interlineado multiplicando ese número por *su propio* `font-size`. Con `em` o `%`, en cambio, el valor se calcula una vez en el elemento donde se declara y ese resultado ya fijo es lo que heredan los hijos, lo que produce interlineados inesperados si un hijo tiene un `font-size` distinto:

```css
/* Con número sin unidad: cada hijo recalcula sobre su propio font-size */
.card { font-size: 16px; line-height: 1.4; }
.card .titulo { font-size: 24px; } /* line-height efectivo: 24 * 1.4 = 33.6px, correcto */

/* Con em: el hijo hereda el PX ya calculado en el padre, no el multiplicador */
.card-em { font-size: 16px; line-height: 1.4em; } /* se fija en 22.4px */
.card-em .titulo { font-size: 24px; } /* hereda 22.4px, no 24 * 1.4 = 33.6px */
```

:::tip[Accesibilidad: interlineado mínimo recomendado]
Las pautas WCAG recomiendan un `line-height` de al menos `1.5` para bloques de texto de lectura continua (párrafos), ya que facilita la lectura a personas con baja visión o dificultades cognitivas como la dislexia.
:::

### `letter-spacing`

Ajusta el espacio horizontal entre caracteres. Acepta `normal` (valor inicial, deja que el navegador ajuste el espaciado al justificar texto) o una longitud (`0.05em`, `1px`), que puede ser negativa para juntar caracteres.

```css
.titulo-mayusculas {
  text-transform: uppercase;
  letter-spacing: 0.05em; /* un poco de aire extra, típico en mayúsculas grandes */
}
```

:::caution[No abuses de `letter-spacing`]
Valores muy grandes (positivos o negativos) pueden romper la legibilidad, y en escrituras conectadas como el árabe pueden llegar a desconectar visualmente las letras que deberían ir unidas. Además, al aplicar un `letter-spacing` distinto de cero, el navegador desactiva por defecto ligaduras tipográficas del tipo `liga`/`clig` (si la fuente las incluye).
:::

## Alineación, decoración y transformación de texto

### `text-align`

Controla la alineación horizontal del contenido dentro de su caja de línea.

| Valor | Efecto |
|---|---|
| `left` / `right` | Alinea a la izquierda o derecha de la caja de línea, sin tener en cuenta la dirección de escritura. |
| `center` | Centra el contenido. |
| `justify` | Justifica el texto: reparte el espacio para que los bordes izquierdo y derecho coincidan con los de la caja de línea, excepto en la última línea del párrafo. |
| `start` / `end` | Equivalentes a `left`/`right` (en `direction: ltr`) o a `right`/`left` (en `direction: rtl`); se adaptan automáticamente a la dirección de escritura. |
| `match-parent` | Como `inherit`, pero resolviendo `start`/`end` según la `direction` real del padre. |

```css
.parrafo { text-align: start; } /* preferible a "left" si el sitio soporta RTL */
.centrado { text-align: center; }
```

:::caution[Accesibilidad de `justify`]
`text-align: justify` puede generar espacios muy irregulares entre palabras (sobre todo en columnas estrechas), lo que dificulta la lectura a personas con dislexia. Úsalo con cautela, o combínalo con `hyphens: auto` para reducir esos huecos.
:::

### `text-decoration`

Es la propiedad abreviada de cuatro propiedades: `text-decoration-line` (`underline`, `overline`, `line-through`, o combinaciones; `none` es el valor inicial), `text-decoration-color`, `text-decoration-style` (`solid` por defecto, `double`, `dotted`, `dashed`, `wavy`) y `text-decoration-thickness` (`auto` por defecto, `from-font` para usar el grosor que sugiera el propio archivo de fuente, o una longitud/porcentaje explícitos). Los valores pueden ir en cualquier orden:

```css
a {
  text-decoration: underline dotted;
}

a:hover {
  text-decoration: underline solid currentcolor 2px;
}

.tachado {
  text-decoration-line: line-through;
  text-decoration-color: crimson;
}
```

:::tip[Soporte de navegadores]
`text-decoration-style` y `text-decoration-color` son *Baseline: ampliamente disponibles*. `text-decoration-thickness` (y la posibilidad de fijar varios valores en el shorthand `text-decoration` a la vez) es *Baseline: ampliamente disponible* desde marzo de 2021; revisa el detalle en [caniuse: text-decoration-style](https://caniuse.com/text-decoration-style) y [caniuse: text-decoration-thickness / text-underline-offset](https://caniuse.com/mdn-css_properties_text-decoration-thickness).
:::

### `text-transform`

Cambia la capitalización del texto **visualmente**, sin alterar el contenido real del documento (el texto seleccionado o copiado conserva su capitalización original en el HTML).

```css
.etiqueta { text-transform: uppercase; }   /* TODO EN MAYÚSCULAS */
.nombre-propio { text-transform: capitalize; } /* Primera Letra De Cada Palabra */
.slug { text-transform: lowercase; }        /* todo en minúsculas */
```

`capitalize` pone en mayúscula la primera *letra* de cada palabra (según las categorías Unicode de letra/número), ignorando signos de puntuación o símbolos al inicio de la palabra. También existen `none` (valor inicial, sin cambios) y valores más especializados para tipografía no latina (`full-width`, `full-size-kana`).

:::caution[Accesibilidad de `uppercase` en bloques largos]
Convertir párrafos completos a mayúsculas con `text-transform: uppercase` dificulta la lectura a personas con dislexia, porque se pierde la silueta característica de cada palabra. Resérvalo para etiquetas cortas (botones, badges, kickers) y no para texto de lectura continua.
:::

## Cuando el texto no cabe: `word-break` y `overflow-wrap`

Ambas propiedades deciden qué hacer cuando una "palabra" (una secuencia sin espacios) es más larga que el contenedor, pero con una diferencia clave: **`overflow-wrap` solo rompe la palabra como último recurso**, cuando no cabe entera en su propia línea; **`word-break: break-all` rompe en el punto exacto del desbordamiento**, aunque poner la palabra completa en la línea siguiente hubiera evitado el corte.

```css
/* overflow-wrap: rompe solo si la palabra no cabe ni en una línea propia */
.direccion-url {
  overflow-wrap: break-word; /* o "anywhere", ver diferencia abajo */
}

/* word-break: rompe agresivamente en el límite del contenedor */
.celda-estrecha {
  word-break: break-all;
}
```

- **`word-break: normal`** (valor inicial): solo rompe en los puntos habituales del idioma (espacios, guiones).
- **`word-break: keep-all`**: para texto chino/japonés/coreano (CJK), impide romper entre caracteres CJK (que por defecto sí pueden partirse); en el resto de idiomas se comporta como `normal`.
- **`word-break: break-all`**: rompe entre cualquier par de caracteres (excepto en CJK) para evitar el desbordamiento, sin esperar a que la palabra completa no quepa.
- **`overflow-wrap: normal`** (valor inicial): solo permite los puntos de ruptura habituales.
- **`overflow-wrap: break-word`**: permite romper una palabra sin puntos de ruptura normales, pero **solo si de verdad no cabe** en su propia línea; a efectos de cálculo del tamaño mínimo de contenido (*min-content*), esa posible ruptura no cuenta.
- **`overflow-wrap: anywhere`**: igual que `break-word` en cuanto al resultado visual, pero esa posible ruptura **sí se tiene en cuenta** al calcular el tamaño mínimo de contenido; es la opción recomendada si necesitas que, por ejemplo, un `grid` o un `flex` puedan encoger la columna por debajo del ancho de la palabra más larga.

```css
/* Ejemplo típico: una URL o un correo muy largo dentro de una tarjeta */
.card p {
  overflow-wrap: anywhere;
}
```

:::tip[Soporte de navegadores]
`word-break` es *Baseline: ampliamente disponible* desde 2015. `overflow-wrap` (antes conocida como `word-wrap`, que se mantiene como alias) tiene soporte consistente desde hace más tiempo, pero su valor `anywhere` es más reciente: por eso MDN sitúa el *Baseline: ampliamente disponible* de la propiedad completa en octubre de 2018. Consulta el detalle en [caniuse: word-break](https://caniuse.com/word-break) y [caniuse: overflow-wrap / word-wrap](https://caniuse.com/wordwrap).
:::

## `text-wrap`: `balance` y `pretty` para un corte de línea más cuidado

`text-wrap` decide **cómo** se distribuye el texto entre líneas cuando ya sabemos que va a envolver (a diferencia de `word-break`/`overflow-wrap`, que deciden si se puede partir una palabra concreta). Además de `wrap` (el comportamiento normal, y valor inicial) y `nowrap` (equivalente a impedir el salto de línea), la especificación añade dos valores pensados específicamente para mejorar la tipografía:

```css
/* Titulares: evita títulos con una única palabra huérfana en la última línea */
h1, h2, h3 {
  text-wrap: balance;
}

/* Párrafos largos: evita huérfanas y mejora el reparto general, sin límite de líneas */
article p {
  text-wrap: pretty;
}
```

- **`balance`**: reparte el texto entre líneas para que todas tengan una anchura lo más parecida posible, en lugar de llenar cada línea al máximo y dejar el resto en la última (el clásico título con una sola palabra suelta al final). Por su coste de cálculo, los navegadores lo limitan a bloques cortos: Chromium lo aplica como máximo a 6 líneas, y Firefox a 10; por eso está pensado sobre todo para **titulares**, no para párrafos largos.
- **`pretty`**: produce el mismo resultado visual que `wrap`, pero usando un algoritmo más lento que prioriza la calidad tipográfica sobre la velocidad (por ejemplo, evitando palabras huérfanas sueltas al final de un párrafo). Al no tener el límite de líneas de `balance`, es la opción pensada para **cuerpos de texto largos**.
- **`stable`**: pensado para contenido editable (`contenteditable`); evita que las líneas ya escritas se recoloquen mientras se sigue escribiendo justo después de ellas.

```css
.editor[contenteditable] {
  text-wrap: stable;
}
```

:::tip[Soporte de navegadores]
`text-wrap` (con `wrap`/`nowrap`) es *Baseline 2024* (disponible en los navegadores principales desde marzo de 2024). El valor `balance` tiene buen soporte: Chrome/Edge 130+ (parcial desde 114), Firefox 121+ y Safari 17.5+; consulta [caniuse: text-wrap: balance](https://caniuse.com/css-text-wrap-balance). El valor `pretty`, en cambio, todavía **no tiene soporte en Firefox** (sí en Chrome/Edge 117+ y Safari 26+); revisa el estado actualizado en [caniuse: text-wrap: pretty](https://caniuse.com/wf-text-wrap-pretty) antes de depender de él como único mecanismo. En ambos casos, al ser mejoras progresivas de la envoltura normal de texto, un navegador sin soporte simplemente aplica `wrap` y el texto sigue siendo perfectamente legible.
:::

## Ver también

- [Unidades y valores en CSS](../fundamentos/unidades)
- [Colores en CSS](../fundamentos/colores)
- [Overflow y desbordamiento](../layout/overflow)
- [Unidades y funciones responsivas](../responsive/unidades-y-funciones)

## Fuentes

- [MDN: `@font-face`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face)
- [MDN: `@font-face` / `src`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/src)
- [MDN: `font-display`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display)
- [MDN: `font-family`](https://developer.mozilla.org/en-US/docs/Web/CSS/font-family)
- [MDN: `font-size`](https://developer.mozilla.org/en-US/docs/Web/CSS/font-size)
- [MDN: `font-weight`](https://developer.mozilla.org/en-US/docs/Web/CSS/font-weight)
- [MDN: `font-synthesis`](https://developer.mozilla.org/en-US/docs/Web/CSS/font-synthesis)
- [MDN: `line-height`](https://developer.mozilla.org/en-US/docs/Web/CSS/line-height)
- [MDN: `letter-spacing`](https://developer.mozilla.org/en-US/docs/Web/CSS/letter-spacing)
- [MDN: `text-align`](https://developer.mozilla.org/en-US/docs/Web/CSS/text-align)
- [MDN: `text-decoration`](https://developer.mozilla.org/en-US/docs/Web/CSS/text-decoration)
- [MDN: `text-decoration-thickness`](https://developer.mozilla.org/en-US/docs/Web/CSS/text-decoration-thickness)
- [MDN: `text-transform`](https://developer.mozilla.org/en-US/docs/Web/CSS/text-transform)
- [MDN: `word-break`](https://developer.mozilla.org/en-US/docs/Web/CSS/word-break)
- [MDN: `overflow-wrap`](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-wrap)
- [MDN: `text-wrap`](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap)
- [W3C CSSWG: CSS Fonts Module Level 4 — descriptor `font-display`](https://drafts.csswg.org/css-fonts-4/#font-display-desc)
- [caniuse: @font-face](https://caniuse.com/fontface)
- [caniuse: WOFF 2.0](https://caniuse.com/woff2)
- [caniuse: font-display](https://caniuse.com/css-font-rendering-controls)
- [caniuse: text-decoration-style](https://caniuse.com/text-decoration-style)
- [caniuse: text-decoration-thickness](https://caniuse.com/mdn-css_properties_text-decoration-thickness)
- [caniuse: word-break](https://caniuse.com/word-break)
- [caniuse: overflow-wrap / word-wrap](https://caniuse.com/wordwrap)
- [caniuse: text-wrap: balance](https://caniuse.com/css-text-wrap-balance)
- [caniuse: text-wrap: pretty](https://caniuse.com/wf-text-wrap-pretty)
