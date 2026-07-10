---
title: Overflow y desbordamiento
description: Guía sobre cómo controlar el desbordamiento de contenido con overflow, overflow-x/overflow-y, text-overflow y el estilizado de la barra de scroll.
---

Cuando el contenido de un elemento no cabe en el espacio que le has asignado, el navegador tiene que decidir qué hacer con ese sobrante: dejarlo salir, recortarlo o darte una barra de scroll para acceder a él. A ese fenómeno se le llama **desbordamiento** (*overflow*), y saber controlarlo es lo que separa una interfaz que se rompe visualmente en cuanto el contenido es un poco más largo de lo esperado de una que se comporta con elegancia ante textos dinámicos, listas que crecen o imágenes de tamaños distintos.

## Qué es el desbordamiento de contenido

El desbordamiento ocurre cuando el contenido de un elemento (texto, imágenes, elementos hijos) es más grande que la caja que lo contiene. Esto pasa, por ejemplo, cuando:

- Fijas una `height` o `max-height` y el contenido crece más allá de ese límite.
- Una palabra larga sin espacios (una URL, un identificador) no cabe en el ancho disponible.
- Aplicas `white-space: nowrap` y el texto, al no poder saltar de línea, se extiende más allá del ancho de la caja.

Por defecto, el navegador **no recorta nada**: el contenido que no cabe simplemente se sigue renderizando fuera de la caja, pudiendo solaparse con otros elementos. Es un comportamiento poco intuitivo cuando vienes de otros lenguajes, así que conviene decidir explícitamente qué debe pasar con ese sobrante.

```css
.card {
  width: 250px;
  height: 120px;
  border: 1px solid #ccc;
  padding: 1rem;
}
```

Si el texto dentro de `.card` no cabe en 120px de alto, con el comportamiento por defecto se derramará por debajo del borde inferior, invadiendo visualmente lo que venga después en el documento. Aquí es donde entra la propiedad `overflow`.

## La propiedad `overflow`: visible, hidden, scroll y auto

`overflow` es una propiedad *shorthand* que fija el comportamiento del contenido desbordado tanto en el eje horizontal como en el vertical. Si le pasas un solo valor, se aplica a ambos ejes (equivale a fijar `overflow-x` y `overflow-y` con ese mismo valor). Su **valor inicial es `visible`** y se aplica a contenedores de bloque, contenedores flex y contenedores grid (no tiene efecto en elementos `inline`).

| Valor | Qué hace |
|---|---|
| `visible` | El contenido que no cabe **no se recorta** y puede pintarse fuera de la caja. Es el valor por defecto y no convierte al elemento en un "contenedor de scroll". |
| `hidden` | El sobrante se recorta en el borde del *padding box*. No aparece ninguna barra de scroll: el contenido oculto sigue existiendo en el DOM y puede desplazarse por JavaScript (`scrollTop`, `scrollTo()`) o llegar por tabulación si contiene elementos enfocables. |
| `scroll` | El sobrante se recorta y el navegador **muestra siempre** las barras de scroll en ese eje, haga falta o no. Es útil cuando quieres reservar el espacio de la barra de forma constante y evitar que el layout salte al aparecer o desaparecer. |
| `auto` | El sobrante se recorta y la barra de scroll **solo aparece si realmente hace falta**. Es, en la práctica, el valor más usado para paneles con scroll. |

```css
.box {
  width: 200px;
  height: 150px;
  border: 1px solid #888;
}

.box--visible { overflow: visible; } /* por defecto: el texto se derrama fuera de la caja */
.box--hidden  { overflow: hidden; }  /* el sobrante desaparece, sin barra de scroll */
.box--scroll  { overflow: scroll; }  /* barra de scroll siempre visible, haga falta o no */
.box--auto    { overflow: auto; }    /* barra de scroll solo si el contenido no cabe */
```

:::note[Un efecto secundario importante]
Los valores `hidden`, `scroll` y `auto` convierten al elemento en un **contenedor de scroll** y generan un nuevo contexto de formato de bloque (la excepción es el valor `clip` —una variante más estricta de `hidden`, con menos soporte y sin `overflow-clip-margin` por defecto— que recorta el contenido pero no crea contenedor de scroll ni nuevo contexto de formato). Este contexto de formato de bloque es necesario porque, de lo contrario, los `float` que intersectan con un elemento con scroll obligarían a recalcular el ajuste de línea en cada paso de scroll. Es un efecto colateral a tener en cuenta si usas `overflow: hidden` como truco para contener flotantes (ver [Display y flujo normal](display-y-flujo-normal)).
:::

## `overflow-x` y `overflow-y` por separado

`overflow` es cómodo, pero a veces necesitas controlar cada eje de forma independiente: por ejemplo, permitir scroll vertical mientras impides cualquier desbordamiento horizontal. Para eso existen `overflow-x` (eje horizontal, bordes izquierdo y derecho) y `overflow-y` (eje vertical, bordes superior e inferior), cada una con el mismo valor inicial `visible` y los mismos valores `visible` / `hidden` / `scroll` / `auto`.

```css
.chat-panel {
  overflow-x: hidden; /* nunca scroll horizontal */
  overflow-y: auto;   /* scroll vertical solo si hace falta */
}

/* Equivalente usando el shorthand con dos valores:
   el primero es overflow-x, el segundo overflow-y */
.chat-panel {
  overflow: hidden auto;
}
```

Hay una regla de interdependencia entre ambos ejes que conviene conocer: si `overflow-y` tiene un valor distinto de `visible` (por ejemplo `hidden`, `scroll` o `auto`) y `overflow-x` se deja en `visible`, el navegador **computa `overflow-x` como `auto`** en lugar de respetar `visible` literalmente. La razón es que no tiene sentido dejar que el contenido se derrame libremente en horizontal mientras en vertical está contenido dentro de una caja con scroll: el resultado sería visualmente inconsistente e imposible de renderizar de forma coherente.

```css
.panel {
  overflow-y: scroll;
  /* overflow-x no se especifica → su valor inicial es "visible",
     pero el navegador lo computa como "auto" por la regla anterior */
}
```

## `text-overflow` y la elipsis de truncado

`text-overflow` controla **cómo se señala al usuario** que hay texto oculto por el desbordamiento; su valor inicial es `clip`, que corta el texto justo en el límite del área de contenido (incluso a mitad de un carácter). El valor `ellipsis` sustituye ese corte por el carácter de elipsis (`…`), y también admite una cadena de texto personalizada entre comillas.

Lo importante —y lo que más se olvida— es que **`text-overflow` no provoca por sí solo ningún desbordamiento**: solo decide qué hacer con un desbordamiento que ya existe. Para que `ellipsis` tenga efecto necesitas combinarlo con otras dos propiedades:

1. `white-space: nowrap`, para impedir que el texto salte de línea (si el texto puede envolver, nunca desborda en horizontal y `ellipsis` no llega a activarse).
2. `overflow: hidden`, para recortar el sobrante (sin esto no hay nada que `text-overflow` pueda "señalar").

```css
.filename {
  max-width: 220px;
  white-space: nowrap;    /* el texto no salta de línea */
  overflow: hidden;       /* se recorta lo que no cabe */
  text-overflow: ellipsis; /* se muestra "…" en el punto de corte */
}
```

```html
<span class="filename">informe-financiero-trimestre-cuarto-2026.pdf</span>
```

Con estas tres líneas, un nombre de archivo largo se trunca en algo como `informe-financiero-trimestre-cuar…` en lugar de desbordar la caja o partirse en varias líneas.

:::tip[Truncar varias líneas, no solo una]
Si necesitas cortar un párrafo tras N líneas (no solo una), `text-overflow: ellipsis` no es suficiente. La vía con más soporte histórico sigue siendo la combinación con prefijo `display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3;` junto con `overflow: hidden`. Existe también la propiedad estándar `line-clamp`, pero su soporte todavía es limitado, así que en producción conviene seguir apoyándose en la variante `-webkit-line-clamp`.
:::

## Estilizado de la scrollbar

Personalizar el aspecto de la barra de scroll es uno de esos detalles que marcan la diferencia entre un panel que "hereda" el scrollbar genérico del sistema operativo y uno que encaja con el diseño. Hay dos caminos, y conviene combinarlos porque cubren navegadores distintos.

### El camino estándar: `scrollbar-width` y `scrollbar-color`

Estas dos propiedades forman parte de la especificación CSS Scrollbars Styling y funcionan igual en cualquier navegador que las soporte, sin prefijos.

- **`scrollbar-width`** fija el grosor de la barra: `auto` (grosor por defecto de la plataforma, valor inicial), `thin` (una variante más estrecha) o `none` (oculta la barra, aunque el elemento sigue siendo desplazable).
- **`scrollbar-color`** fija los colores del *thumb* (el "pulgar" que arrastras) y del *track* (la pista sobre la que se desliza), en ese orden: `scrollbar-color: <color-del-thumb> <color-del-track>`. Su valor inicial es `auto` (colores por defecto de la plataforma).

```css
.scroll-panel {
  max-height: 300px;
  overflow-y: auto;

  scrollbar-width: thin;
  scrollbar-color: #888 transparent; /* thumb: gris, track: transparente */
}
```

:::caution[Cuidado con `scrollbar-width: none`]
Ocultar la barra de scroll perjudica la accesibilidad: deja de ser visible que el contenido es desplazable y complica el scroll por teclado o táctil. Si lo que quieres es un elemento que solo se desplace mediante JavaScript (no por interacción directa del usuario), usa `overflow: hidden` en su lugar en vez de esconder la barra con `scrollbar-width: none`.
:::

### El camino no estándar: `::-webkit-scrollbar`

Antes de que `scrollbar-width`/`scrollbar-color` existieran, los navegadores basados en WebKit/Blink (Chrome, Edge, Safari, Opera) ya permitían estilizar la scrollbar mediante una familia de **pseudo-elementos no estándar**: `::-webkit-scrollbar`, `::-webkit-scrollbar-track`, `::-webkit-scrollbar-thumb`, `::-webkit-scrollbar-button` y `::-webkit-scrollbar-corner`, entre otros. No forman parte de ninguna especificación W3C, pero siguen siendo la única forma de lograr ciertos efectos (como grosores muy concretos o esquinas redondeadas en el *thumb*) en esos navegadores.

```css
.scroll-panel::-webkit-scrollbar {
  width: 8px;
}

.scroll-panel::-webkit-scrollbar-track {
  background: transparent;
}

.scroll-panel::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 4px;
}
```

En la práctica, lo recomendable es declarar **ambos** enfoques a la vez: donde el navegador soporte `scrollbar-width`/`scrollbar-color` con un valor distinto de `auto`, esas propiedades tienen prioridad sobre los pseudo-elementos `::-webkit-scrollbar-*`; donde no las soporte (o donde solo entienda los pseudo-elementos), caerá en el estilo WebKit como resultado visual equivalente.

:::tip[Soporte de navegadores]
`scrollbar-width` y `scrollbar-color` son relativamente recientes en Chromium (Chrome/Edge 121) y llegaron a Safari en versiones distintas (Safari 18.2 para `scrollbar-width`, Safari 26.2 para `scrollbar-color`), mientras que Firefox las soporta desde hace años (Firefox 64). Los pseudo-elementos `::-webkit-scrollbar-*` no son estándar y no funcionan en Firefox. Consulta el soporte actualizado en [caniuse: scrollbar-width](https://caniuse.com/mdn-css_properties_scrollbar-width) y [caniuse: scrollbar-color](https://caniuse.com/mdn-css_properties_scrollbar-color).
:::

## Ver también

- [Display y flujo normal](display-y-flujo-normal)
- [Positioning](positioning)
- [Flexbox](flexbox)
- [El modelo de caja](../fundamentos/modelo-de-caja)

## Fuentes

- [MDN: overflow](https://developer.mozilla.org/es/docs/Web/CSS/overflow)
- [MDN: overflow-x](https://developer.mozilla.org/es/docs/Web/CSS/overflow-x)
- [MDN: overflow-y](https://developer.mozilla.org/es/docs/Web/CSS/overflow-y)
- [MDN: text-overflow](https://developer.mozilla.org/es/docs/Web/CSS/text-overflow)
- [MDN: white-space](https://developer.mozilla.org/es/docs/Web/CSS/white-space)
- [MDN: scrollbar-width](https://developer.mozilla.org/es/docs/Web/CSS/scrollbar-width)
- [MDN: scrollbar-color](https://developer.mozilla.org/es/docs/Web/CSS/scrollbar-color)
- [MDN: ::-webkit-scrollbar](https://developer.mozilla.org/en-US/docs/Web/CSS/::-webkit-scrollbar)
- [MDN: line-clamp](https://developer.mozilla.org/en-US/docs/Web/CSS/line-clamp)
- [caniuse: scrollbar-width](https://caniuse.com/mdn-css_properties_scrollbar-width)
- [caniuse: scrollbar-color](https://caniuse.com/mdn-css_properties_scrollbar-color)
