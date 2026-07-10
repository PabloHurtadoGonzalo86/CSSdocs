---
title: "Transiciones CSS (transition)"
description: Guía sobre transition y sus longhands (property, duration, delay, timing-function, behavior), las funciones de temporización, qué propiedades son animables y las buenas prácticas de rendimiento al animar transform y opacity.
---

Las transiciones son la forma más sencilla de decirle al navegador: "cuando el valor de esta propiedad cambie, no saltes de golpe, interpola suavemente entre el valor viejo y el nuevo". Con una sola línea de CSS conviertes un cambio de estado brusco (un `:hover`, un `:focus`, una clase añadida por JavaScript) en un movimiento con principio y final, sin escribir ni una línea de JavaScript ni depender de una librería de animación. Es la herramienta que usarás a diario para dar feedback visual en botones, desplegar menús, aparecer/desaparecer overlays o suavizar cualquier interacción, y entender bien sus piezas evita el clásico "por qué esto no se anima" cuando una propiedad no responde como se espera.

## Qué problema resuelven

Sin transición, cualquier cambio de valor en CSS es instantáneo:

```css
.boton {
  background-color: royalblue;
}

.boton:hover {
  background-color: darkblue; /* el color cambia de golpe, en un único frame */
}
```

Añadir `transition` no cambia los valores inicial y final: sigue siendo `royalblue` en reposo y `darkblue` en `:hover`. Lo que cambia es *cómo* se recorre el camino entre ambos:

```css
.boton {
  background-color: royalblue;
  transition: background-color 0.3s ease;
}

.boton:hover {
  background-color: darkblue; /* ahora el cambio se recorre en 0.3s */
}
```

La transición necesita siempre un **disparador**: un cambio real en el valor computado de la propiedad, ya sea por una pseudoclase (`:hover`, `:focus`, `:active`), por una clase añadida/quitada con JavaScript, por un cambio de media query o por cualquier otra causa. Sin ese cambio de valor no hay nada que animar.

## El atajo `transition` y sus longhands

`transition` es un shorthand que agrupa cinco propiedades independientes:

| Longhand | Qué controla | Valor inicial |
|---|---|---|
| `transition-property` | Qué propiedad(es) se anima(n) | `all` |
| `transition-duration` | Cuánto dura la animación | `0s` |
| `transition-timing-function` | Cómo se acelera/desacelera a lo largo del tiempo | `ease` |
| `transition-delay` | Cuánto se espera antes de empezar | `0s` |
| `transition-behavior` | Si se permite animar propiedades de tipo discreto (como `display`) | `normal` |

```css
.tarjeta {
  transition-property: transform, box-shadow;
  transition-duration: 0.25s;
  transition-timing-function: ease-out;
  transition-delay: 0s;
}

/* La misma declaración usando el atajo */
.tarjeta {
  transition: transform 0.25s ease-out, box-shadow 0.25s ease-out;
}
```

Cuando se escriben dos valores de tiempo en la forma abreviada, el orden es fijo: **el primero es siempre `transition-duration` y el segundo `transition-delay`**.

```css
.tarjeta {
  transition: transform 0.25s 0.1s; /* duración: 0.25s, retraso: 0.1s */
}
```

:::tip[`transition` no es una propiedad animable]
La propia propiedad `transition` (y cada una de sus longhands) tiene `animation type: not animatable`: no tiene sentido "animar" la configuración de la animación. Lo que se anima siempre es la propiedad de destino declarada en `transition-property` (`background-color`, `transform`, etc.).
:::

## `transition-property`: qué se anima

Acepta `all` (valor inicial: intenta animar cualquier propiedad que cambie y sea animable), `none` (desactiva cualquier transición) o una lista de nombres de propiedad separados por comas:

```css
.elemento {
  transition-property: all;                    /* valor inicial */
  transition-property: opacity, transform;      /* lista explícita */
  transition-property: none;                    /* sin transiciones */
}
```

Usar `all` es cómodo mientras se prototipa, pero tiene un coste real en un proyecto mantenible: el navegador evalúa **todas** las propiedades animables del elemento en cada cambio de estado, incluidas las que no pretendías animar, lo que puede producir transiciones inesperadas cuando otra regla CSS cambia una propiedad que no habías previsto. La práctica recomendada es declarar explícitamente la lista de propiedades que realmente quieres animar.

## `transition-duration` y `transition-delay`

Ambas aceptan valores de tiempo (`s` o `ms`) y admiten una lista separada por comas para asignar una duración o un retraso distinto a cada propiedad de `transition-property`:

```css
.elemento {
  transition-property: transform, opacity;
  transition-duration: 0.3s, 0.6s;   /* transform: 0.3s / opacity: 0.6s */
  transition-delay: 0s, 0.1s;        /* opacity espera 0.1s antes de arrancar */
}
```

Si alguna de estas listas tiene **menos** valores que `transition-property`, la especificación indica que se repite desde el principio hasta completar el número de propiedades necesario; si tiene **más**, los valores sobrantes al final simplemente se ignoran. Por ejemplo, con tres propiedades y solo dos duraciones, la tercera propiedad reutiliza la primera duración de la lista.

:::note[`transition-delay` también acepta valores negativos]
Un valor negativo hace que la transición arranque inmediatamente pero **a mitad de recorrido**, como si ya llevara corriendo ese tiempo. Es un recurso poco habitual, pero útil para sincronizar varias transiciones que deben "encontrarse" en un punto intermedio concreto.
:::

## Funciones de temporización: `transition-timing-function`

Esta longhand define la curva de aceleración: cómo se reparte el progreso de la animación a lo largo del tiempo. No es lo mismo un movimiento a velocidad constante que uno que arranca despacio y termina rápido.

### Palabras clave basadas en curvas de Bézier

| Valor | Equivale a | Comportamiento |
|---|---|---|
| `ease` (valor inicial) | `cubic-bezier(0.25, 0.1, 0.25, 1)` | Arranca despacio, acelera y vuelve a frenar hacia el final |
| `linear` | `cubic-bezier(0, 0, 1, 1)` | Velocidad constante, sin aceleración ni frenado |
| `ease-in` | `cubic-bezier(0.42, 0, 1, 1)` | Arranca despacio y acelera hasta terminar de golpe |
| `ease-out` | `cubic-bezier(0, 0, 0.58, 1)` | Arranca de golpe y frena progresivamente |
| `ease-in-out` | `cubic-bezier(0.42, 0, 0.58, 1)` | Combina `ease-in` al principio y `ease-out` al final |

```css
.elemento {
  transition: transform 0.4s linear;      /* velocidad constante, un poco "robótica" */
  transition: transform 0.4s ease-out;    /* arranque brusco, llegada suave: la más natural para elementos que "entran" */
}
```

### `cubic-bezier()`: tu propia curva

Cuando las palabras clave no bastan, `cubic-bezier()` permite definir una curva de Bézier cúbica propia a partir de dos puntos de control:

```css
.elemento {
  transition-timing-function: cubic-bezier(0.68, -0.55, 0.27, 1.55);
}
```

La función recibe cuatro números: `cubic-bezier(x1, y1, x2, y2)`. Las coordenadas `x1` y `x2` están restringidas al rango `[0, 1]` (definen el progreso en el tiempo, que siempre avanza hacia adelante), mientras que `y1` e `y2` pueden salirse de ese rango, incluso ser negativos: eso es precisamente lo que permite crear efectos de "rebote" o "exceso" (*overshoot*), donde el valor animado se pasa momentáneamente de su destino antes de asentarse.

### `steps()`: interpolación por saltos discretos

A diferencia de las curvas de Bézier (que interpolan de forma continua), `steps()` divide la animación en un número fijo de tramos iguales y salta de uno a otro sin transición intermedia:

```css
.spinner {
  transition-timing-function: steps(4, jump-end);
}
```

- El primer argumento es un entero: el número de intervalos en los que se divide la animación.
- El segundo argumento, opcional, es la posición del salto: `jump-start` (salta al principio de cada intervalo), `jump-end` (salta al final; es el valor por defecto si se omite), `jump-none` (no hay salto ni al principio ni al final, todos los intervalos son intermedios) o `jump-both` (hay salto tanto al principio como al final).

Este comportamiento es el mismo que usan los *keywords* `step-start` (equivalente a `steps(1, jump-start)`) y `step-end` (equivalente a `steps(1, jump-end)`). `steps()` es la base de efectos como animaciones tipo *sprite sheet*, relojes o indicadores de carga con "ticks" perceptibles, donde quieres estados claramente diferenciados en lugar de un movimiento fluido.

:::tip[Novedad: `linear()` para curvas personalizadas sin adivinar coordenadas]
Además de `cubic-bezier()`, existe la función [`linear()`](https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function), que define la curva a partir de una lista de puntos de progreso (por ejemplo, `linear(0, 0.5, 1)`), útil para reproducir efectos de rebote o muelle con más control que una curva de Bézier de un solo tramo. Tiene soporte más reciente (Chrome/Edge 113+, Firefox 112+, Safari 17.2+): comprueba el estado actualizado en [caniuse.com](https://caniuse.com/mdn-css_types_easing-function_linear-function) antes de depender de ella sin alternativa.
:::

## `transition-behavior`: animar propiedades discretas

No todas las propiedades interpolan valores intermedios. Propiedades como `display` o `visibility` tienen un **tipo de animación discreto**: no existe un "`display` a medias", así que el navegador no lo transiciona gradualmente, sino que cambia el valor en un punto concreto del recorrido. Para una propiedad discreta genérica (por ejemplo, `border-style`) ese cambio ocurre exactamente a mitad de camino, al 50% de la duración. `display` y `visibility`, sin embargo, tienen cada una un comportamiento especial documentado aparte en MDN, pensado justo para no arruinar un fundido: cuando `display` anima hacia o desde `none`, el salto ocurre al 0% o al 100% del recorrido (nunca a mitad), de modo que el contenido permanece renderizado durante toda la transición; `visibility` favorece de forma parecida el valor `visible` durante prácticamente todo el recorrido, y solo se comporta como "no visible" justo en el extremo que corresponde.

Aun con eso, por defecto (`transition-behavior: normal`) los navegadores directamente **no inician ninguna transición** sobre una propiedad de tipo discreto: el valor cambia de forma instantánea en cuanto se actualiza, sin recorrer ningún punto intermedio. Por eso, hasta hace poco, era imposible combinar `display: none` con una transición de `opacity` para lograr un fundido de salida real: en cuanto `display` pasaba a `none`, el elemento desaparecía del render de inmediato, antes de que `opacity` terminara de animarse. La longhand `transition-behavior: allow-discrete` (y su atajo, el keyword `allow-discrete` dentro de `transition`) resuelve esto habilitando la transición sobre la propiedad discreta:

```css
.overlay {
  opacity: 0;
  display: none;
  transition:
    opacity 0.3s,
    display 0.3s allow-discrete;
}

.overlay.visible {
  opacity: 1;
  display: block;
}

@starting-style {
  .overlay.visible {
    opacity: 0;
  }
}
```

Con `allow-discrete`, el navegador mantiene el elemento visible (`display: block`) durante toda la duración de la transición y solo aplica `display: none` al final, permitiendo que `opacity` complete su recorrido. La regla `@starting-style` es necesaria para definir el estado "de partida" (`opacity: 0`) cuando el elemento pasa de no estar renderizado a estarlo, ya que en ese caso no hay un valor previo del que partir.

:::tip[Soporte de navegadores: `transition-behavior`]
Es una incorporación relativamente reciente: Chrome/Edge 117+, Firefox 129+ y Safari 17.4+. Revisa el estado actualizado en [caniuse.com](https://caniuse.com/mdn-css_properties_transition-behavior) antes de depender de ella sin una alternativa para navegadores más antiguos.
:::

## Qué propiedades se pueden animar

La regla general, según la especificación de Web Animations que usa CSS, es que **toda propiedad CSS es animable salvo que se indique explícitamente lo contrario**, pero no todas se comportan igual al hacerlo. MDN clasifica el comportamiento en varios tipos de animación:

- **No animable** (`not animatable`): la propiedad nunca interpola; ejemplos típicos son propiedades estructurales como `transition` misma o `transition-property`.
- **Discreta** (`discrete`): salta de un valor a otro sin estados intermedios; por defecto ese salto ocurre al 50% del recorrido, sea cual sea la curva de temporización usada. Propiedades como `border-style`, `cursor` o `list-style-type` son ejemplos directos de esta regla genérica. `display` y `visibility` también son discretas en esencia, pero —como ya se explicó arriba— tienen cada una reglas de salto especiales (0%/100%, o favorecer `visible`) en vez del reparto genérico al 50%.
- **Por valor computado** (`by computed value`): interpola numéricamente sus componentes; es el caso de la mayoría de propiedades útiles para animar: `opacity`, `color`, `background-color`, `width`.
- **Lista repetible** (`repeatable list`): como la anterior, pero pensada para propiedades cuyo valor es una lista separada por comas. Si la lista de partida y la de llegada tienen longitudes distintas, ambas se repiten hasta alcanzar el **mínimo común múltiplo** de sus longitudes (no simplemente hasta igualar la más larga: una lista de 2 elementos y otra de 3 se repiten hasta 6) y luego cada elemento se combina por valor computado. MDN documenta este tipo exacto en propiedades como `background-position`, `background-size` o `mask-position`. `box-shadow`, por su parte, usa un mecanismo emparentado pero registrado con su propio nombre en la especificación (*a shadow list*): si una lista de sombras es más corta, se rellena con sombras transparentes de longitud cero en vez de repetirse. `transform` tiene a su vez su propio tipo (*a transform*): si ambas listas de funciones coinciden en tipo y cantidad, cada función se interpola por separado; si no coinciden, el navegador recurre a descomponer la matriz resultante para interpolar igualmente.

Puedes consultar el tipo de animación exacto de cualquier propiedad en la tabla "Definición formal" de su página en MDN.

:::caution[Evita animar hacia o desde `auto`]
La especificación recomienda explícitamente **no** animar propiedades hacia o desde el valor `auto` (por ejemplo, `height: auto`), porque no define un procedimiento de interpolación fiable para ese caso. Distintos navegadores lo resuelven de forma distinta y el resultado puede ser inconsistente. Si necesitas animar una altura desconocida, las alternativas habituales son animar `max-height` hacia un valor suficientemente grande, medir la altura real con JavaScript antes de animar, o usar `calc-size()`/`interpolate-size` donde ya haya soporte.
:::

## Buenas prácticas de rendimiento: prefiere `transform` y `opacity`

No todas las propiedades cuestan lo mismo de animar. Cuando el navegador pinta una página sigue, a grandes rasgos, tres fases: **layout** (calcula tamaño y posición de cada caja), **paint** (rasteriza el contenido en píxeles) y **composite** (combina las distintas capas en la pantalla final).

Animar propiedades como `width`, `height`, `top`, `left`, `margin` o `padding` obliga al navegador a recalcular el layout **en cada frame** de la transición, y ese recálculo se propaga a los elementos vecinos y, potencialmente, a toda la página. En cambio, `transform` y `opacity` pueden gestionarse casi siempre solo en la fase de composición: el navegador puede promocionar el elemento a su propia capa y mover/desvanecer esa capa sin volver a calcular layout ni repintar el resto del documento, a menudo delegando el trabajo a la GPU. El resultado práctico es una animación notablemente más fluida, sobre todo en dispositivos móviles o de gama baja.

```css
/* Evitar: anima top/left, dispara layout en cada frame */
.tooltip {
  position: absolute;
  top: 0;
  transition: top 0.2s ease-out;
}
.tooltip.desplazado {
  top: 20px;
}

/* Preferible: mismo efecto visual, animando transform */
.tooltip {
  position: absolute;
  top: 0;
  transition: transform 0.2s ease-out;
}
.tooltip.desplazado {
  transform: translateY(20px);
}
```

Ambos fragmentos producen el mismo desplazamiento visual de 20px, pero el segundo evita que el navegador recalcule el layout del documento en cada frame de la animación.

:::tip[`will-change`: un recurso puntual, no una solución por defecto]
`will-change` permite avisar al navegador con antelación de que una propiedad va a cambiar, para que prepare optimizaciones antes de que ocurra el cambio. MDN es explícito: debe usarse **como último recurso** ante un problema de rendimiento real ya detectado, no de forma preventiva ni aplicado de forma permanente a muchos elementos, porque reservar esas optimizaciones tiene un coste de memoria propio. El patrón recomendado es activarlo justo antes de que empiece la interacción (por ejemplo, en `mouseenter`) y quitarlo (`will-change: auto`) cuando la animación termina, en lugar de declararlo fijo en la hoja de estilos.
:::

:::tip[Soporte de navegadores]
Las transiciones CSS (`transition` y todas sus longhands clásicas: `transition-property`, `transition-duration`, `transition-timing-function`, `transition-delay`) tienen soporte prácticamente universal desde hace más de una década en todos los navegadores modernos. Consulta el detalle actualizado en [caniuse.com/css-transitions](https://caniuse.com/css-transitions).
:::

## Ver también

- [Keyframes y animation](keyframes)
- [Transform](transform)
- [Positioning](../layout/positioning)
- [El modelo de caja](../fundamentos/modelo-de-caja)

## Fuentes

- [MDN: transition](https://developer.mozilla.org/en-US/docs/Web/CSS/transition)
- [MDN: transition-property](https://developer.mozilla.org/en-US/docs/Web/CSS/transition-property)
- [MDN: transition-duration](https://developer.mozilla.org/en-US/docs/Web/CSS/transition-duration)
- [MDN: transition-delay](https://developer.mozilla.org/en-US/docs/Web/CSS/transition-delay)
- [MDN: transition-timing-function](https://developer.mozilla.org/en-US/docs/Web/CSS/transition-timing-function)
- [MDN: transition-behavior](https://developer.mozilla.org/en-US/docs/Web/CSS/transition-behavior)
- [MDN: easing-function (tipo de dato)](https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function)
- [MDN: Using CSS transitions](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_transitions/Using_CSS_transitions)
- [MDN: CSS animated properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animated_properties)
- [MDN: will-change](https://developer.mozilla.org/en-US/docs/Web/CSS/will-change)
- [MDN: @starting-style](https://developer.mozilla.org/en-US/docs/Web/CSS/@starting-style)
- [W3C: CSS Transitions Level 1](https://www.w3.org/TR/css-transitions-1/)
- [caniuse: CSS Transitions](https://caniuse.com/css-transitions)
- [caniuse: transition-behavior](https://caniuse.com/mdn-css_properties_transition-behavior)
- [caniuse: linear() easing function](https://caniuse.com/mdn-css_types_easing-function_linear-function)
