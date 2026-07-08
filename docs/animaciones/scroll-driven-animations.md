# Scroll-driven animations (animaciones basadas en scroll)

Durante años, cualquier animación "ligada al scroll" (una barra de progreso de lectura, una tarjeta que aparece al desplazarse, un efecto parallax) exigía un listener de `scroll` en JavaScript, calcular a mano el porcentaje desplazado y actualizar estilos en cada frame con `requestAnimationFrame`. Las **scroll-driven animations** resuelven esto de forma nativa en CSS: en lugar de que una animación avance con el tiempo (segundos), avanza con la posición del scroll. El resultado corre en el hilo de composición del navegador, no se bloquea si el hilo principal está ocupado, y elimina por completo el código de scroll a mano.

## Dos tipos de línea de tiempo: scroll progress y view progress

Toda animación en CSS necesita una *timeline* (línea de tiempo) que le diga cómo avanzar. La de toda la vida es la del documento, basada en tiempo real. Las scroll-driven animations añaden dos líneas de tiempo nuevas, ambas basadas en scroll pero midiendo cosas distintas:

| | **Scroll progress timeline** (`scroll()`) | **View progress timeline** (`view()`) |
|---|---|---|
| ¿Qué mide? | Cuánto se ha desplazado un contenedor con scroll, de principio a fin | Cuánto de un elemento concreto es visible dentro de su scrollport, según entra y sale de él |
| 0% ocurre cuando... | El contenedor está en su posición de scroll inicial | El elemento empieza a asomar por un borde del scrollport |
| 100% ocurre cuando... | El contenedor está en su posición de scroll final | El elemento ha terminado de desaparecer por el borde opuesto |
| Caso de uso típico | Barra de progreso de lectura, efectos ligados al scroll de toda la página | Revelar tarjetas, contadores o imágenes conforme entran en pantalla |

Ambas se generan con dos funciones CSS —`scroll()` y `view()`— y se conectan a una animación mediante una única propiedad: `animation-timeline`.

## `animation-timeline`: la propiedad que lo conecta todo

`animation-timeline` sustituye (o complementa) a la línea de tiempo por defecto de una animación `@keyframes`. Sus valores posibles son:

```css
.elemento {
  animation-timeline: none;              /* la animación no se ejecuta */
  animation-timeline: auto;               /* valor inicial: timeline de tiempo normal */
  animation-timeline: --mi-timeline;      /* una timeline con nombre (ver más abajo) */
  animation-timeline: scroll();           /* timeline de progreso de scroll, anónima */
  animation-timeline: view();             /* timeline de progreso de visibilidad, anónima */
}
```

El valor inicial es `auto`, que es exactamente el comportamiento de siempre: una animación gobernada por `animation-duration` en el tiempo. En cuanto le asignas `scroll()` o `view()`, la animación deja de "correr" con el reloj y pasa a mapearse sobre el 0%–100% de esa nueva línea de tiempo basada en scroll.

!!! warning "Declárala después del shorthand `animation`"

    `animation-timeline` es una subpropiedad *reset-only* del shorthand `animation`: si escribes `animation: aparecer 1s ease;` y **después** `animation-timeline: view();`, todo funciona. Pero si el shorthand `animation` va **después**, resetea `animation-timeline` de vuelta a `auto` y tu timeline de scroll deja de aplicarse silenciosamente. Es un error muy fácil de cometer al reordenar CSS.

## `scroll()`: el progreso del propio scroll de un contenedor

```css
animation-timeline: scroll( [ <scroller> ] || [ <axis> ] );
```

Ambos parámetros son opcionales y se pueden escribir en cualquier orden.

| `<scroller>` | Qué contenedor de scroll usa como referencia |
|---|---|
| `nearest` (inicial) | El ancestro desplazable más cercano en el árbol del DOM |
| `root` | El *scroller* del documento (el viewport), aunque el elemento esté anidado dentro de otro contenedor con scroll |
| `self` | El propio elemento (debe tener `overflow` con scroll) |

| `<axis>` | Dirección de scroll que controla el progreso |
|---|---|
| `block` (inicial) | Eje de bloque: vertical en modos de escritura horizontales como el español |
| `inline` | Eje en línea: horizontal en modos de escritura horizontales |
| `x` | Siempre horizontal, sea cual sea el modo de escritura |
| `y` | Siempre vertical, sea cual sea el modo de escritura |

```css
.linea-progreso {
  animation: crecer linear;
  animation-timeline: scroll(root block); /* progreso del scroll vertical de todo el documento */
}

@keyframes crecer {
  to { transform: scaleX(1); }
}
```

Aquí lo importante es que `root` fija explícitamente el scroll de **todo el documento** como referencia, sin importar en qué parte del árbol DOM viva `.linea-progreso`. Si en lugar de `root` dejas el valor por defecto `nearest`, el navegador buscará el ancestro desplazable más próximo, lo que puede darte resultados distintos si el elemento está anidado dentro de otro contenedor con su propio scroll (un modal, un panel lateral...).

## `view()`: cuánto se ve un elemento dentro de su scrollport

```css
animation-timeline: view( [ <axis> ] || [ <view-timeline-inset> ] );
```

A diferencia de `scroll()`, `view()` **no acepta un parámetro de scroller**: el "contenedor" de referencia es siempre el ancestro desplazable más cercano del propio elemento. Ojo, esto **no** es lo mismo que el comportamiento por defecto de un `IntersectionObserver`: si no le indicas `root`, un `IntersectionObserver` usa el viewport de nivel superior como referencia (aunque el elemento esté anidado dentro de otro contenedor con scroll), mientras que `view()` siempre usa el scroller más próximo en el árbol, aunque no sea el documento. Sus parámetros son:

- **`<axis>`**: igual que en `scroll()` (`block` por defecto, `inline`, `x`, `y`), pero aquí indica el eje en el que se mide la entrada/salida del elemento.
- **`<view-timeline-inset>`**: ajusta qué se considera "dentro" del scrollport, con uno o dos valores (`<length-percentage>` o `auto`, que es el inicial). Un valor positivo **encoge** la zona visible (el elemento tarda más en considerarse "en vista"); un valor negativo la **expande**. Con dos valores, el primero ajusta el borde de entrada y el segundo el de salida.

```css
.tarjeta {
  animation: aparecer linear;
  animation-timeline: view();       /* equivale a view(block auto) */
  animation-timeline: view(20%);    /* recorta 20% en ambos bordes del scrollport */
}

@keyframes aparecer {
  from { opacity: 0; }
  to   { opacity: 1; }
}
```

## Timelines con nombre: `scroll-timeline` y `view-timeline`

Las funciones `scroll()` y `view()` cubren el caso más simple: el elemento que se anima es el mismo que genera la timeline (o su propio scroller). Pero a veces necesitas separar **quién genera el progreso** de **quién se anima con él** —por ejemplo, animar un pseudo-elemento decorativo con el scroll de su contenedor padre—. Para eso existen las propiedades con nombre.

### `scroll-timeline-name` / `scroll-timeline-axis`

Se declaran en el **contenedor con scroll** (formalmente, la propiedad "aplica a *scroll containers*"):

```css
main {
  scroll-timeline-name: --main-timeline;
  scroll-timeline-axis: block; /* valor inicial */

  /* o el shorthand equivalente: */
  scroll-timeline: --main-timeline block;

  height: 90vh;
  overflow-y: scroll;
}

div::after {
  animation: mover-forma linear;
  animation-timeline: --main-timeline; /* referencia el timeline por su nombre */
}
```

El nombre debe ser un `<dashed-ident>` (empezar por `--`), igual que las custom properties, precisamente para evitar choques con palabras clave de CSS.

Para que esta referencia funcione tal cual, `div` tiene que ser descendiente de `main` en el HTML: por defecto, un timeline con nombre solo es visible dentro del árbol del elemento que lo declara (ver la nota sobre `timeline-scope` más abajo para el caso contrario).

### `view-timeline-name` / `view-timeline-axis` / `view-timeline-inset`

A diferencia de `scroll-timeline-name`, estas "aplican a todos los elementos" y se declaran sobre el propio **elemento que quieres rastrear** (el "sujeto"):

```css
.tarjeta {
  view-timeline-name: --revelar-tarjeta;
  view-timeline-axis: block;   /* valor inicial */
  view-timeline-inset: 10%;    /* valor inicial: auto */

  /* o el shorthand equivalente: */
  view-timeline: --revelar-tarjeta block 10%;
}

.tarjeta {
  animation: aparecer linear;
  animation-timeline: --revelar-tarjeta;
}
```

!!! note "Cuando el timeline con nombre necesita salir de su árbol"

    Por defecto, un timeline con nombre solo es visible para los descendientes del elemento que lo declara. Si necesitas referenciarlo desde un elemento que no desciende de él (por ejemplo, un hermano), existe la propiedad `timeline-scope`, pensada específicamente para ampliar ese alcance.

## Acotar el tramo de la animación: `animation-range`

Por defecto, una animación con `scroll()` o `view()` ocupa el **100% de la timeline**: `animation-range-start: normal` (0%) y `animation-range-end: normal` (100%). `animation-range` te deja recortar ese tramo:

```css
animation-range: normal;        /* 0% a 100% (equivalente al valor inicial: toda la timeline) */
animation-range: 20% 80%;       /* entre el 20% y el 80% de la timeline */
animation-range: entry;         /* solo durante la fase de "entrada" (ver tabla) */
animation-range: entry 25%;     /* desde el 25% de la fase "entry" hasta su final (100%) */
```

Ojo con esta última: el porcentaje no se mide sobre toda la timeline, sino **dentro del rango con nombre indicado**. `entry 25%` significa "25% de avance dentro de la fase `entry`", no "25% de la timeline completa". Y como aquí solo se da el valor de inicio, `animation-range-end` se rellena automáticamente con el mismo nombre de rango al 100% (`entry 100%`), así que el tramo animado es el último 75% de la fase `entry`, no el primer 25%.

En una *view progress timeline*, además de porcentajes, puedes usar nombres de rango predefinidos (`<timeline-range-name>`) que dividen el recorrido del elemento por el scrollport en fases con sentido:

| Nombre | Qué delimita |
|---|---|
| `cover` (por defecto) | Todo el recorrido: desde que el elemento empieza a asomar hasta que desaparece del todo |
| `contain` | El tramo en que el elemento está completamente contenido en el scrollport (o lo cubre entero, si es más grande que él) |
| `entry` | Solo la fase de entrada, mientras el elemento está apareciendo |
| `exit` | Solo la fase de salida, mientras el elemento está desapareciendo |
| `entry-crossing` | Como `entry`, pero sin recortar el tramo al tamaño del scrollport (útil con elementos mayores que el viewport) |
| `exit-crossing` | Como `exit`, sin ese recorte |

```css
.tarjeta {
  animation-timeline: view();
  animation-range: entry; /* la animación solo ocurre mientras la tarjeta entra en pantalla */
}
```

## Caso práctico: barra de progreso de lectura

Un patrón muy habitual en artículos largos: una línea fina y fija en la parte superior que crece de izquierda a derecha según el usuario avanza en la lectura.

```html
<div class="barra-progreso" aria-hidden="true"></div>

<article class="post">
  <!-- contenido largo del artículo -->
</article>
```

```css
.barra-progreso {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(to right, #6366f1, #ec4899);

  transform: scaleX(0);
  transform-origin: left; /* crece desde el borde izquierdo */

  animation: leer linear;
  animation-timeline: scroll(root block);
  animation-duration: 1ms; /* ver nota más abajo: Firefox lo necesita */
}

@keyframes leer {
  to {
    transform: scaleX(1);
  }
}
```

Puntos clave del ejemplo:

- Se anima `transform: scaleX()` en lugar de `width`, porque `transform` no dispara recálculo de layout en cada paso de scroll (el mismo motivo por el que se prefiere en cualquier animación, no solo en las basadas en scroll).
- `scroll(root block)` ata el progreso al scroll **vertical de todo el documento**, sin importar que `.barra-progreso` esté fuera del flujo normal por su `position: fixed`.
- Como el rango de la animación es el 100% de la timeline (no se ha recortado con `animation-range`), no hace falta `animation-fill-mode`: no existe un "antes" ni un "después" fuera de los límites del propio scroll del documento.

!!! tip "¿Por qué `animation-duration: 1ms`?"

    En una animación puramente gobernada por scroll, el valor en segundos de `animation-duration` no debería importar: el progreso lo marca la posición del scroll, no el reloj. De hecho, MDN documenta que el valor `auto` está pensado justo para esto ("*rellena toda la timeline con la animación*"). En la práctica, sin embargo, algunos navegadores necesitan que `animation-duration` tenga un valor explícito para aplicar la animación. La recomendación de MDN es fijarlo en `1ms`: un valor tan pequeño que no altera el resultado visual, pero evita el problema.

## Caso práctico: elementos que aparecen al hacer scroll

El otro patrón clásico: tarjetas, imágenes o bloques de texto que hacen un *fade-in* combinado con un ligero desplazamiento vertical según van entrando en el viewport.

```css
.tarjeta {
  opacity: 0;
  transform: translateY(2rem);

  animation: revelar linear;
  animation-timeline: view();
  animation-range: entry;          /* solo mientras la tarjeta está entrando */
  animation-fill-mode: both;       /* mantiene el estado final tras terminar "entry" */
  animation-duration: 1ms;
}

@keyframes revelar {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

Aquí `animation-fill-mode: both` **sí es imprescindible**: al recortar la animación a la fase `entry` con `animation-range`, en cuanto la tarjeta termina de entrar (y pasa a las fases `contain`/`exit`, donde sigue siendo visible) la animación queda "fuera de rango" dentro de una timeline que sigue activa. Sin `fill-mode: both`, el elemento volvería a su estado base (`opacity: 0`) en cuanto dejara de estar en el tramo `entry`, provocando un parpadeo indeseado.

## Progressive enhancement y accesibilidad

Como `scroll()` y `view()` no tienen soporte universal todavía (ver la nota de soporte más abajo), conviene aplicarlas como **mejora progresiva**: el contenido debe verse bien también donde no haya soporte.

La forma más segura es envolver el estado "oculto" **junto con** la animación dentro de un `@supports`, de modo que un navegador sin soporte nunca llegue a ocultar el contenido:

```css
.tarjeta {
  /* Sin @supports, la tarjeta se ve siempre: nada que "revelar" */
}

@supports (animation-timeline: view()) {
  .tarjeta {
    opacity: 0;
    transform: translateY(2rem);

    animation: revelar linear;
    animation-timeline: view();
    animation-range: entry;
    animation-fill-mode: both;
    animation-duration: 1ms;
  }
}

@keyframes revelar {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

También es razonable avisar explícitamente cuando la función no está disponible, con la variante negada de `@supports`, un patrón que la propia documentación de MDN usa en sus ejemplos:

```css
@supports not (scroll-timeline: --main-timeline) {
  body::before {
    content: "Tu navegador no soporta las scroll-driven animations.";
    display: block;
    padding: 1rem 0;
    text-align: center;
  }
}
```

Por último, no olvides `prefers-reduced-motion`: siguen siendo animaciones CSS normales por debajo, así que a las personas que prefieren menos movimiento hay que respetarles esa preferencia igual que en cualquier otra animación:

```css
@media (prefers-reduced-motion: reduce) {
  .tarjeta {
    animation: none;
  }
}
```

!!! tip "Soporte de navegadores"

    Las scroll-driven animations (`animation-timeline`, `scroll()`, `view()`, `scroll-timeline-name`, `view-timeline-name`, `animation-range`...) son soportadas en Chrome y Edge desde la versión 115 (julio de 2023) y en Safari desde la versión 26. Firefox, a mediados de 2026, todavía no las soporta por defecto en su versión estable: la bandera `layout.css.scroll-driven-animations.enabled` viene activada por defecto en Nightly, pero en la versión estable hay que activarla manualmente en `about:config`. Al ser una función relativamente reciente y sin soporte universal, trátala siempre como mejora progresiva y comprueba el estado actualizado en [caniuse: animation-timeline](https://caniuse.com/mdn-css_properties_animation-timeline).

## Ver también

- [Transform](transform.md)
- [Keyframes y animation](keyframes.md)
- [Transiciones](transiciones.md)
- [Overflow y desbordamiento](../layout/overflow.md)

## Fuentes

- [MDN: CSS scroll-driven animations (guía general)](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations)
- [MDN: animation-timeline](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline)
- [MDN: scroll()](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline/scroll)
- [MDN: view()](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline/view)
- [MDN: scroll-timeline](https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-timeline)
- [MDN: view-timeline](https://developer.mozilla.org/en-US/docs/Web/CSS/view-timeline)
- [MDN: animation-range](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-range)
- [MDN: nombres de rango de timeline (`<timeline-range-name>`)](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations/Timeline_range_names)
- [MDN: animation-duration](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-duration)
- [W3C/CSSWG: Scroll-driven Animations (borrador de especificación)](https://drafts.csswg.org/scroll-animations-1/)
- [caniuse: animation-timeline](https://caniuse.com/mdn-css_properties_animation-timeline)
