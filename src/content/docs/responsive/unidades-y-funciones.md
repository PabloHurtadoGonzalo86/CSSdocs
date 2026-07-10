---
title: "Unidades y funciones para diseño responsivo"
description: "Cómo combinar clamp(), min() y max() con las unidades de viewport (vw, vh, dvh, svh, lvh) para lograr tipografía fluida, límites responsivos y evitar el scroll horizontal no deseado."
---

Diseñar para "todas las pantallas" ya no depende solo de acumular `media queries`: depende de combinar funciones que **calculan** un valor (`clamp()`, `min()`, `max()`) con unidades que **responden al viewport** (`vw`, `vh` y sus variantes modernas `dvh`, `svh`, `lvh`). Bien combinadas, son lo que permite que un titular, un padding o una sección a pantalla completa se adapten de forma continua entre un móvil y un monitor ultra-wide sin escribir un solo `@media`. Mal combinadas —sobre todo las unidades de viewport sin límites— son también la causa más habitual de dos problemas muy visibles en producción: secciones que "saltan" al hacer scroll en móvil, y barras de scroll horizontal que no deberían existir. Esta página se centra en cómo aplicar estas piezas juntas, en patrones reales; para el repaso completo de qué es cada unidad y cada función por separado, consulta [Unidades y valores en CSS](../fundamentos/unidades).

## Tipografía fluida: `clamp()` en la práctica

`clamp(MÍNIMO, PREFERIDO, MÁXIMO)` devuelve el valor preferido siempre que esté entre el mínimo y el máximo, y se ajusta a uno de esos dos límites en cuanto se sale del rango (equivale a `max(MÍNIMO, min(PREFERIDO, MÁXIMO))`). Para tipografía fluida, el patrón habitual es:

- **Mínimo y máximo**, en `rem`, para que nunca dependan solo del viewport y respeten la configuración de accesibilidad del usuario.
- **Valor preferido**, combinando un término fijo en `rem` con un término en `vw`, en lugar de usar `vw` a solas.

```css
h1 {
  /* Nunca baja de 1rem ni sube de 2rem; entre esos límites, crece con el viewport */
  font-size: clamp(1rem, 0.667rem + 1.667vw, 2rem);
}
```

¿Por qué no un simple `font-size: 4vw`? Porque un valor puramente en `vw` no tiene suelo ni techo: en un móvil estrecho el texto puede volverse ilegible, y en un monitor de 3000px puede volverse gigantesco. `clamp()` resuelve justo eso sin necesidad de `media queries` intermedias.

### Cómo se calcula el término "preferido"

El término preferido no se elige a ojo: sale de una interpolación lineal entre dos parejas (tamaño, ancho de viewport) que tú decides. Por ejemplo, si quieres que el `h1` mida `1rem` (16px) en un viewport de `320px` y `2rem` (32px) en un viewport de `1280px`:

```text
pendiente = (32px - 16px) / (1280px - 320px) = 16 / 960 ≈ 0.0167 px por px de viewport
          → expresado en vw: 0.0167 × 100 ≈ 1.667vw

término fijo = 16px - (0.0167 × 320px) ≈ 10.67px ≈ 0.667rem
```

De ahí sale exactamente el `clamp(1rem, 0.667rem + 1.667vw, 2rem)` del ejemplo anterior (valores redondeados a tres decimales). No hace falta repetir este cálculo a mano cada vez —hay generadores de "fluid type scale" que lo hacen por ti—, pero entender de dónde sale el número ayuda a ajustar la curva cuando el resultado no "se siente" bien en algún ancho intermedio.

```css
/* Una pequeña escala fluida, sin una sola media query */
h1   { font-size: clamp(2rem, 1.2rem + 3vw, 4rem); }
h2   { font-size: clamp(1.5rem, 1rem + 1.8vw, 3rem); }
p    { font-size: clamp(1rem, 0.9rem + 0.3vw, 2rem); }

.contenedor {
  /* Espaciado fluido: crece con la pantalla, sin desbordar ni desaparecer */
  padding-inline: clamp(1rem, 5vw, 3rem);
}
```

Fíjate en que, en las tres líneas de texto (`h1`, `h2`, `p`), el máximo es al menos el doble del mínimo (`4rem`/`2rem`, `3rem`/`1.5rem`, `2rem`/`1rem`): es el mismo criterio de accesibilidad para tamaño de texto que se explica en el aviso siguiente, no solo aplicable al titular del primer ejemplo. La regla no aplica a `.contenedor`, porque ahí `clamp()` controla un `padding`, no un `font-size`.

:::caution[Accesibilidad: el máximo debe ser al menos el doble del mínimo]
Según la propia documentación de `clamp()` en MDN, cuando se usa para controlar el tamaño de texto, **el valor máximo permitido debe ser una unidad relativa que no sea menor que el doble del mínimo**. Esto es lo que garantiza que el texto pueda seguir escalando hasta al menos el 200% si el usuario hace zoom sobre la página, tal y como exige el criterio de éxito 1.4.4 (*Resize Text*) de las WCAG. En el ejemplo `clamp(1rem, 0.667rem + 1.667vw, 2rem)`, el máximo (`2rem`) es exactamente el doble del mínimo (`1rem`), así que cumple la recomendación.

Además, procura que el mínimo y el máximo sean siempre unidades relativas (`rem`, no `px`), y que el término preferido combine `rem` con `vw` en lugar de usar solo `vw`: así el resultado sigue respondiendo tanto al ancho de la pantalla como a la preferencia de tamaño de fuente del usuario, en vez de depender únicamente del viewport.
:::

:::tip[Soporte de navegadores]
`clamp()`, junto con `min()` y `max()`, forma parte de las funciones matemáticas de CSS. Tienen soporte amplio desde 2020 (Chrome/Edge 79+, Firefox 75+, Safari 13.1+, con soporte parcial en Safari 11.1–13), pero no existen en Internet Explorer. Consulta el detalle actualizado en [caniuse: CSS math functions min(), max() and clamp()](https://caniuse.com/css-math-functions).
:::

## `min()` y `max()` para poner límites responsivos

`min()` devuelve el valor más pequeño de una lista separada por comas; `max()`, el más grande. Son una alternativa declarativa a escribir varias reglas con `media queries` solo para imponer un tope, y aceptan expresiones matemáticas (con distintas unidades) directamente como argumentos, sin necesidad de envolverlas en `calc()`.

### Techo: usa `min()` para que algo nunca crezca de más

```css
.contenedor {
  /* Ocupa casi todo el ancho disponible, pero nunca más de 70rem,
     por grande que sea la pantalla */
  width: min(100% - 2rem, 70rem);
  margin-inline: auto;
}
```

Aquí `100% - 2rem` dará un valor menor que `70rem` en pantallas normales (gana ese término), pero en un monitor muy ancho `100% - 2rem` superará los `70rem` y entonces gana el tope fijo. El resultado: un contenedor centrado que respira en pantallas pequeñas y no se estira sin límite en pantallas enormes.

### Suelo: usa `max()` para que algo nunca se encoja de más

```css
.tarjeta {
  /* El padding crece con el viewport, pero nunca baja de 1rem */
  padding: max(1rem, 3vw);
}
```

En una pantalla estrecha, `3vw` puede ser menor que `1rem`, así que `max()` impone el suelo de `1rem`. En una pantalla ancha, `3vw` supera `1rem` y gana el término fluido.

### `min()` y `max()` anidados: así funciona `clamp()` por dentro

```css
/* Equivalente manual a clamp(1.5rem, 4vw, 3rem) */
.titulo {
  font-size: max(1.5rem, min(4vw, 3rem));
}
```

Ver esta equivalencia ayuda a razonar `clamp()` cuando el resultado no es el esperado: primero se resuelve el `min()` interior (el techo), y ese resultado se compara con el `max()` exterior (el suelo).

:::note[No lo confundas con `minmax()`]
`minmax(mínimo, máximo)` es una función distinta, exclusiva de CSS Grid: solo se usa dentro de `grid-template-columns`, `grid-template-rows`, `grid-auto-columns` o `grid-auto-rows` para definir el rango de tamaño de una pista de la cuadrícula, y no es intercambiable con las funciones matemáticas genéricas `min()`/`max()` que se usan en cualquier propiedad numérica. Más detalle en [Flexbox](../layout/flexbox) y en [CSS Grid: guía completa](../layout/grid).
:::

## Unidades de viewport: `vw`, `vh` y el problema histórico en móvil

`1vw` equivale al 1% del ancho del viewport y `1vh` al 1% de su alto. El problema aparece con `vh` en móvil: la especificación indica que, por defecto, estas unidades se calculan sobre el **viewport grande** (el tamaño que tendría la pantalla si las barras del navegador estuvieran completamente ocultas). Como esas barras (dirección, pestañas, teclado) aparecen y desaparecen al hacer scroll o al enfocar un campo, un `height: 100vh` puede quedar por debajo del borde visible real cuando la barra está desplegada —dejando una franja cortada en un hero a pantalla completa, o generando una barra de scroll vertical que no debería estar ahí—, y ese salto se nota especialmente en menús de navegación a pantalla completa o modales de móvil.

Para resolver justo eso, [CSS Values and Units Module Level 4](https://www.w3.org/TR/css-values-4/#viewport-relative-lengths) define tres tamaños de viewport distintos, cada uno con su propio juego de unidades:

| Familia | Asume que las barras del navegador están... | Cuándo conviene |
|---|---|---|
| `sv*` (*small viewport*) | Desplegadas (el escenario más conservador) | Contenido que nunca debe quedar cortado, aunque deje un hueco vacío cuando las barras se ocultan |
| `lv*` (*large viewport*) | Ocultas/retraídas (es el comportamiento heredado de `vh`/`vw`) | Aprovechar toda la pantalla cuando las barras desaparecen, a costa de poder quedar tapado cuando reaparecen |
| `dv*` (*dynamic viewport*) | Se recalculan en tiempo real, según el estado actual | Contenido que debe encajar exactamente en todo momento, asumiendo que puede redimensionarse mientras el usuario hace scroll |

```css
.pantalla-completa {
  height: 100vh;   /* fallback: navegadores sin soporte de dvh se quedan aquí */
  height: 100dvh;  /* se ajusta al alto real disponible en cada momento */
}
```

Declarar primero `vh` y después `dvh` es el patrón de *fallback* recomendado: los navegadores que no reconocen `dvh` ignoran esa línea y conservan la anterior, sin necesidad de *feature queries*.

`dvh` no es una solución mágica sin coste: como su valor cambia mientras el usuario hace scroll (porque la barra del navegador se expande o retrae en vivo), un elemento dimensionado con `dvh` puede **redimensionarse visiblemente durante el scroll**, lo que en algunos casos se nota como un pequeño "salto" o incluso afecta al rendimiento de scroll. Si tu sección no necesita reaccionar a ese cambio en vivo —por ejemplo, un bloque que solo se ve una vez al cargar la página—, `svh` o `lvh` (estables mientras el viewport no cambie de tamaño real) suelen ser preferibles a `dvh`.

También existen las variantes de ancho (`svw`, `lvw`, `dvw`) y las de eje lógico (`svi`/`lvi`/`dvi`, `svb`/`lvb`/`dvb`), con sus correspondientes `min`/`max`, pero el problema histórico de la barra del navegador afecta casi siempre al alto, no al ancho.

:::tip[Soporte de navegadores]
Las unidades de viewport pequeño/grande/dinámico llegaron después que `vw`/`vh`: Chrome/Edge 108+, Firefox 101+, Safari 15.4+ y Opera 94+. No existen en versiones anteriores ni en Internet Explorer. Si necesitas dar soporte a navegadores más antiguos, mantén siempre el `height: 100vh` como línea previa a `height: 100dvh` (como en el ejemplo anterior). Consulta el detalle actualizado en [caniuse: Small, Large, and Dynamic viewport units](https://caniuse.com/viewport-unit-variants).
:::

## Buenas prácticas para evitar el scroll horizontal no deseado

Una barra de scroll horizontal que aparece "de la nada" es uno de los fallos de responsive design más frecuentes y más visibles para el usuario, sobre todo en móvil, donde además suele impedir hacer scroll vertical con comodidad. Casi siempre viene de la combinación de las herramientas anteriores usadas sin un límite.

### Causas más comunes

- **`width: 100vw` en presencia de una scrollbar vertical.** La especificación es explícita: por defecto, las unidades de viewport se calculan **asumiendo que las barras de scroll no existen**, salvo que el elemento raíz fuerce su aparición con `overflow` o `scrollbar-gutter`, en cuyo caso el navegador sí debe descontar su ancho. Como en la mayoría de páginas el `<body>` no fuerza esa reserva de espacio, `100vw` termina siendo unos cuantos píxeles más ancho que el área realmente visible (el ancho de la scrollbar), y ese elemento sobresale generando scroll horizontal. La solución más simple es preferir `width: 100%` (que sí descuenta la scrollbar, porque se calcula sobre el contenedor ya reducido) y reservar `100vw` solo para efectos de "sangrado" a pantalla completa que de verdad lo necesiten.
- **Unidades de viewport sin límite superior.** Un `font-size: 10vw` o un `padding: 5vw` sin `min()`/`max()`/`clamp()` alrededor crecen sin freno en monitores muy anchos, empujando contenido fuera del viewport. La corrección va directamente ligada a las secciones anteriores: acota siempre esos valores con `clamp()` o con `min(valor, tope)`.
- **Elementos con un ancho fijo mayor que el viewport más pequeño soportado**, o contenido "no rompible": imágenes sin `max-width`, tablas anchas, bloques `<pre>`/`<code>` con líneas largas, o una URL sin espacios dentro de un párrafo.
- **`box-sizing` por defecto (`content-box`)** en un elemento con `width` fijo más `padding` o `border`: el ancho final resulta ser `width + padding + border`, que puede superar el contenedor sin que lo parezca a simple vista en el código.
- **Márgenes negativos o elementos posicionados en absoluto** que se desplazan fuera del flujo normal sin que nada limite su posición final.

### Prácticas defensivas

```css
/* 1. Box-sizing predecible en todo el proyecto */
*,
*::before,
*::after {
  box-sizing: border-box;
}

/* 2. Los elementos reemplazados nunca deben superar a su contenedor */
img,
picture,
video,
svg {
  max-width: 100%;
  height: auto;
}

/* 3. Texto no rompible (URLs, identificadores largos) que se ajuste en vez de desbordar */
p,
.texto-usuario {
  overflow-wrap: break-word;
}
```

- El primer bloque evita el clásico "se me sale 20px por culpa del padding" descrito arriba (más detalle en [El modelo de caja](../fundamentos/modelo-de-caja)).
- El segundo evita que una imagen subida a mayor resolución de la esperada reviente su contenedor.
- El tercero deja que una palabra larga sin espacios salte de línea en lugar de forzar el ancho de su contenedor hacia la derecha.

```css
/* Red de seguridad, no la solución raíz */
body {
  overflow-x: hidden;
}
```

:::caution[`overflow-x: hidden` es un parche, no un diagnóstico]
Aplicar `overflow-x: hidden` al `<body>` esconde el síntoma (la barra de scroll), pero no arregla la causa: el elemento que sobresale sigue ahí, solo que recortado. Además, un valor de `overflow` igual a `hidden`, `scroll`, `auto` u `overlay` en un ancestro (así lo describe MDN sobre `position`) convierte a ese elemento en el "contenedor de scroll" de referencia para los elementos con `position: sticky` que tenga dentro, lo que en algunos layouts puede hacer que una cabecera pegajosa deje de comportarse como se espera; `overflow: clip`, en cambio, no genera este efecto colateral sobre `sticky`. Úsalo como red de seguridad temporal mientras localizas el elemento culpable, no como solución definitiva; evita aplicarlo al `<html>` si puedes limitarlo al `<body>`.

Para encontrar al culpable rápido, en la consola del navegador puedes comparar el ancho real del documento con el del viewport:

```js
document.documentElement.scrollWidth > document.documentElement.clientWidth
// true → algo se está saliendo por la derecha
```

y luego, con las herramientas de desarrollo, ir aplicando `outline: 1px solid red` a contenedores sucesivos hasta encontrar cuál de ellos tiene un `scrollWidth` mayor que su `clientWidth`.
:::

## Ver también

- [Unidades y valores en CSS](../fundamentos/unidades)
- [Media queries](media-queries)
- [Container queries](container-queries)
- [Overflow y desbordamiento](../layout/overflow)
- [CSS Grid: guía completa](../layout/grid)

## Fuentes

- [MDN: `clamp()`](https://developer.mozilla.org/en-US/docs/Web/CSS/clamp)
- [MDN: `min()`](https://developer.mozilla.org/en-US/docs/Web/CSS/min)
- [MDN: `max()`](https://developer.mozilla.org/en-US/docs/Web/CSS/max)
- [MDN: `minmax()`](https://developer.mozilla.org/en-US/docs/Web/CSS/minmax)
- [MDN: `<length>` (unidades relativas al viewport)](https://developer.mozilla.org/en-US/docs/Web/CSS/length)
- [MDN: `position` (contenedor de scroll y `sticky`)](https://developer.mozilla.org/en-US/docs/Web/CSS/position)
- [MDN: `overflow-wrap`](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-wrap)
- [W3C CSSWG: CSS Values and Units Module Level 4 — Viewport-percentage lengths](https://www.w3.org/TR/css-values-4/#viewport-relative-lengths)
- [caniuse: CSS math functions min(), max() and clamp()](https://caniuse.com/css-math-functions)
- [caniuse: Small, Large, and Dynamic viewport units](https://caniuse.com/viewport-unit-variants)
