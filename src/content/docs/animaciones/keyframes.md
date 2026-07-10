---
title: "@keyframes y animation"
description: Explica la at-rule @keyframes para definir fotogramas clave de una animación CSS y la propiedad animation con sus longhands, comparándolas con transition para saber cuándo usar cada una.
---

Las transiciones resuelven bien el caso de "de un estado A a un estado B", pero se quedan cortas en cuanto necesitas una secuencia con varios puntos intermedios, que se repita sola o que arranque sin que nadie interactúe con la página. Para eso existen las **animaciones CSS**: la at-rule `@keyframes`, que define la coreografía (qué valores toma cada propiedad en cada punto del tiempo), y la propiedad `animation`, que conecta esa coreografía con un elemento y controla cómo se reproduce. Dominar ambas piezas —y saber cuándo conviene una animación y cuándo una simple transición— es una de esas habilidades que separan un CSS que "más o menos funciona" de uno que se comporta con precisión.

## La at-rule `@keyframes`

`@keyframes` define los fotogramas clave de una animación: un nombre y una lista de "paradas" en el tiempo, cada una con los valores que deben tener ciertas propiedades en ese punto.

```css
@keyframes aparecer {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
```

El nombre (`aparecer` en este caso) es un `<custom-ident>` —o una cadena entre comillas— que luego se referencia desde `animation-name`. Ese nombre es lo único que conecta la at-rule con el elemento: `@keyframes` por sí sola no anima nada, solo describe la secuencia.

### Selectores de fotograma: porcentajes, o `from`/`to`

Cada bloque dentro de `@keyframes` empieza con un selector de porcentaje (de `0%` a `100%`) que indica en qué punto de la duración total se aplican esos estilos:

```css
@keyframes rebote {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
  100% {
    transform: translateY(0);
  }
}
```

Para el caso más simple —solo un punto de inicio y uno de fin— existen los alias `from` (equivalente a `0%`) y `to` (equivalente a `100%`), que resultan más legibles:

```css
@keyframes mostrar {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
```

*(Nota: aquí se usa un nombre distinto, `mostrar`, a propósito. Si hubiéramos vuelto a llamarlo `aparecer` —el nombre usado en el ejemplo introductorio y en el resto del artículo—, esta segunda definición habría reemplazado silenciosamente a la primera en cualquier hoja de estilos donde convivieran ambas, tal como se explica en "Nombres duplicados" más abajo.)*

También puedes agrupar varios porcentajes en un mismo bloque separándolos por comas, útil cuando varios instantes comparten los mismos valores:

```css
@keyframes parpadeo {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}
```

:::note[Qué pasa si omites `0%` o `100%`]
Si no defines el fotograma inicial (`0%`/`from`) o el final (`100%`/`to`), el navegador usa como valor de ese extremo **el estilo computado que el elemento ya tenía** antes de que empezara la animación. Esto es exactamente lo que aprovecha el ejemplo de `parpadeo`-sin-extremos: puedes escribir solo `50% { opacity: 0.5; }` y dejar que el propio valor actual del elemento actúe como los bordes 0% y 100%.
:::

### Interpolación de propiedades no definidas en todos los fotogramas

No hace falta repetir todas las propiedades en cada porcentaje. Si una propiedad solo aparece en algunos fotogramas, el navegador la interpola usando únicamente esos puntos como referencia; el resto de propiedades sigue su propio conjunto de paradas de forma independiente:

```css
@keyframes desplazamiento {
  0% {
    top: 0;
    left: 0;
  }
  30% {
    top: 50px; /* left no se menciona: se sigue interpolando entre 0% y 68% */
  }
  68%, 72% {
    left: 50px;
  }
  100% {
    top: 100px;
    left: 100%;
  }
}
```

Aquí `top` se anima usando las paradas 0%, 30% y 100%, mientras que `left` usa 0%, 68%/72% y 100%, cada una de forma independiente.

### Reglas prácticas que conviene conocer

- **Nombres duplicados**: si defines dos `@keyframes` con el mismo nombre, gana la **última** en el orden del documento (no hay fusión ni cascada entre ellas).
- **Porcentajes duplicados dentro del mismo bloque**: si repites, por ejemplo, dos veces `50% { ... }` con propiedades distintas, todas se combinan como si fuera una cascada normal dentro de ese punto.
- **`!important` se ignora**: cualquier declaración con `!important` dentro de un fotograma se descarta por completo; las animaciones nunca pueden usar `!important` para ganarle a otras reglas.
- **Solo se animan propiedades animables**: si incluyes una propiedad que no admite interpolación (por ejemplo, `display` en navegadores que no soportan su animación discreta), esa propiedad concreta se ignora dentro de la animación, sin romper el resto.

## La propiedad `animation` y sus longhands

`@keyframes` describe la coreografía; `animation` (y sus longhands) la aplican a un elemento y controlan el reproductor: velocidad, repeticiones, dirección, qué pasa antes/después, etc.

### `animation-name`: qué `@keyframes` usar

```css
.tarjeta {
  animation-name: aparecer;
}
```

Acepta el nombre de una o varias reglas `@keyframes` (separadas por comas para animar el mismo elemento con varias secuencias a la vez), o `none`, que es su valor inicial y significa "sin animación". Si el nombre no coincide con ningún `@keyframes` existente, la animación **no se ejecuta en absoluto**: ninguna propiedad se anima y tampoco se disparan los eventos de animación (`animationstart`, `animationend`), exactamente igual que si `animation-name` valiera `none`. El resto de longhands que hayas declarado (`animation-delay`, `animation-fill-mode`, etc.) quedan sin efecto práctico mientras no exista un `@keyframes` con ese nombre.

### `animation-duration`: cuánto dura un ciclo

```css
.tarjeta {
  animation-duration: 0.6s;
}
```

Su valor inicial es `0s`. Con duración cero la animación se ejecuta instantáneamente: no hay transición visible, pero los eventos (`animationstart`, `animationend`) sí se disparan. Acepta segundos (`s`) o milisegundos (`ms`).

### `animation-timing-function`: la curva de aceleración

Controla cómo varía la velocidad dentro de cada ciclo. Su valor inicial es `ease`.

```css
.tarjeta {
  animation-timing-function: ease-out;
}
```

| Valor | Comportamiento |
|---|---|
| `ease` (inicial) | Empieza algo lenta, acelera con fuerza y luego desacelera hacia el final |
| `linear` | Velocidad constante durante todo el ciclo |
| `ease-in` | Empieza lenta, termina rápida |
| `ease-out` | Empieza rápida, termina lenta |
| `ease-in-out` | Lenta al inicio y al final, rápida en el medio |
| `steps(n, <step-position>)` | Divide el ciclo en `n` saltos discretos (con `jump-start`, `jump-end`, `jump-both`, `jump-none`, `start` o `end`) en lugar de una curva continua |
| `cubic-bezier(x1, y1, x2, y2)` | Curva de Bézier personalizada |
| `linear(...)` | Interpolación lineal por puntos de parada, para curvas personalizadas sin Bézier |

Un detalle poco conocido: puedes declarar `animation-timing-function` **dentro de cada fotograma** de `@keyframes`, y esa curva se aplicará solo al tramo entre ese fotograma y el siguiente:

```css
@keyframes desplazar {
  0% {
    animation-timing-function: ease-in; /* rige el tramo 0% → 50% */
    margin-left: 0;
  }
  50% {
    animation-timing-function: linear; /* rige el tramo 50% → 100% */
    margin-left: 40%;
  }
  100% {
    margin-left: 100%;
  }
}
```

La curva definida en el último fotograma (`100%`/`to`) nunca llega a usarse, porque no hay ningún tramo posterior al que aplicarla.

### `animation-delay`: retraso antes de empezar

```css
.tarjeta {
  animation-delay: 0.2s;
}
```

Valor inicial `0s`. Acepta valores negativos: un delay negativo hace que la animación arranque como si ya llevara ese tiempo reproduciéndose (útil para sincronizar varias animaciones que empiezan en distintos puntos de su ciclo).

### `animation-iteration-count`: cuántas veces se repite

```css
.spinner {
  animation-iteration-count: infinite;
}
```

Valor inicial `1`. Acepta cualquier número no negativo, incluidos decimales (`1.5` reproduce ciclo y medio) y la palabra clave `infinite` para bucle indefinido.

### `animation-direction`: sentido de reproducción

```css
.spinner {
  animation-direction: alternate;
}
```

| Valor | Efecto |
|---|---|
| `normal` (inicial) | Siempre hacia delante, reiniciando al principio en cada ciclo |
| `reverse` | Siempre hacia atrás, reiniciando al final en cada ciclo |
| `alternate` | Alterna: 1ª iteración hacia delante, 2ª hacia atrás, 3ª hacia delante... |
| `alternate-reverse` | Igual que `alternate` pero empezando hacia atrás |

Con `reverse`, las funciones de aceleración también se invierten (un `ease-in` se comporta como `ease-out`).

### `animation-fill-mode`: estilos antes y después de la animación

Esta es la longhand que más confusión suele generar. Define qué valores aplica el elemento **fuera** del rango en que la animación se está ejecutando: antes de empezar (durante el `animation-delay`) y después de terminar.

```css
.menu {
  animation-name: desplegar;
  animation-duration: 0.3s;
  animation-fill-mode: forwards;
}
```

| Valor | Efecto |
|---|---|
| `none` (inicial) | El elemento no conserva ningún estilo del `@keyframes`: antes y después de la animación se ve con su CSS normal |
| `forwards` | Al terminar, el elemento conserva los valores del **último** fotograma ejecutado |
| `backwards` | Durante el `animation-delay`, el elemento adopta ya los valores del **primer** fotograma |
| `both` | Combina `forwards` y `backwards`: aplica el primer fotograma durante el delay y conserva el último al finalizar |

:::tip[Por qué casi siempre quieres `forwards` en animaciones de una sola pasada]
Sin `animation-fill-mode`, en cuanto termina la animación el elemento **vuelve a su estilo original** definido fuera de `@keyframes`, lo que suele producir un parpadeo brusco si el fotograma final no coincidía con ese estilo base. Si quieres que un elemento "se quede" en el estado final (por ejemplo, un modal que aparece con fade-in y debe permanecer visible), necesitas `animation-fill-mode: forwards` —o directamente definir ese estado final también en el CSS base del elemento, sin depender del relleno de la animación—.
:::

### `animation-play-state`: pausar y reanudar

```css
.spinner {
  animation-play-state: running; /* valor inicial */
}

.spinner:hover {
  animation-play-state: paused;
}
```

Solo admite `running` (inicial) y `paused`. Es la longhand pensada para pausar/reanudar animaciones vía CSS (por ejemplo, en `:hover`) o desde JavaScript (`elemento.style.animationPlayState = 'paused'`). Al reanudarse, la animación continúa desde el punto exacto en que se pausó, no desde el principio.

### El atajo `animation`

Con las ocho longhands anteriores en mente, el atajo `animation` las combina en una sola declaración:

```css
.tarjeta {
  animation: 0.6s ease-out 0.2s 1 normal forwards running aparecer;
}

/* Forma habitual, usando solo lo que hace falta */
.tarjeta {
  animation: aparecer 0.6s ease-out forwards;
}
```

El orden no es estrictamente obligatorio para la mayoría de los valores —el navegador identifica cada palabra clave por su tipo—, pero hay un caso especial: cuando escribes **dos valores de tiempo**, el navegador siempre interpreta el **primero como `animation-duration`** y el **segundo como `animation-delay`**.

```css
.tarjeta {
  animation: deslizar 3s ease-in 1s;
  /* duration: 3s | timing-function: ease-in | delay: 1s | name: deslizar */
}
```

Como buena práctica, coloca `animation-name` al final: si tu `@keyframes` se llamara igual que una palabra clave (por ejemplo `none` o `infinite`), evitas ambigüedades de parseo.

También puedes declarar varias animaciones simultáneas sobre el mismo elemento separándolas por comas, cada una con su propio conjunto de valores:

```css
.notificacion {
  animation:
    aparecer 0.3s ease-out,
    parpadeo 1s ease-in-out 0.3s 3;
}
```

:::caution[El atajo `animation` resetea todo lo que no menciones]
Igual que ocurre con otros shorthands de CSS, escribir `animation: aparecer 0.6s;` resetea implícitamente `animation-timing-function`, `animation-delay`, `animation-iteration-count`, `animation-direction`, `animation-fill-mode` y `animation-play-state` a sus valores iniciales, aunque los hubieras fijado antes con una longhand suelta. Si necesitas mantener un valor concreto de una longhand junto al atajo, declara esa longhand **después** del atajo en la cascada, no antes.
:::

:::note[Un noveno ingrediente: `animation-timeline`]
Las especificaciones más recientes (las que habilitan las animaciones controladas por scroll) añadieron una novena longhand, `animation-timeline`, que también forma parte del atajo `animation` pero de un modo particular: es *reset-only*. Eso significa que declarar el atajo siempre reinicia `animation-timeline` a su valor inicial (`auto`), pero **no** puedes asignarle un valor distinto a través del atajo; si necesitas una línea de tiempo distinta a la del documento, tienes que declarar `animation-timeline` como longhand suelta y, si convive con el atajo `animation`, colocarla después de este en la cascada. El detalle completo está en [Scroll-driven animations](scroll-driven-animations).
:::

## Eventos de JavaScript

Las animaciones CSS disparan eventos que puedes escuchar desde JavaScript sin necesidad de temporizadores manuales: `animationstart`, `animationiteration` (al inicio de cada repetición, salvo la última, ya que esa la cierra `animationend`) y `animationend`. Existe un cuarto evento, `animationcancel`, menos conocido pero también estándar: se dispara cuando la animación se interrumpe **sin** llegar a un `animationend` normal —por ejemplo, si cambias `animation-name`, ocultas el elemento con `display: none` o lo eliminas del DOM mientras seguía animándose—. Todos incluyen `animationName` y `elapsedTime`, útiles para encadenar lógica al terminar (o interrumpir) una animación, como eliminar un elemento del DOM tras su animación de salida.

## `@keyframes`/`animation` frente a `transition`: cuándo usar cada una

Ambas herramientas interpolan valores de CSS a lo largo del tiempo, pero resuelven problemas distintos. La pregunta clave para decidir es: **¿necesito puntos intermedios definidos, o me basta con ir de un estado a otro?**

| | `transition` | `animation` + `@keyframes` |
|---|---|---|
| Disparador | Requiere un cambio de estado (`:hover`, `:focus`, una clase añadida por JS, un cambio de variable) | Puede arrancar sola al aplicarse la regla, sin ningún disparador externo |
| Puntos intermedios | Solo interpola entre el valor inicial y el valor final; no hay fotogramas propios | Tantos fotogramas como definas en `@keyframes`, con control fino de cada uno |
| Repetición | Se ejecuta una vez por cada cambio de estado; no tiene noción de "iteración" | Nativa vía `animation-iteration-count`, incluyendo `infinite` |
| Reversión automática | Si el estado vuelve atrás, la transición se revierte sola de forma simétrica | Requiere `animation-direction: alternate` o reiniciar la animación manualmente |
| Complejidad razonable | Cambios simples de una o pocas propiedades (color, opacidad, transform en hover) | Secuencias coreografiadas: loaders, carruseles, animaciones de entrada/salida complejas |

En la práctica: si la animación depende de que **algo cambie** (el usuario pasa el ratón, un formulario se valida, se añade una clase `.abierto`), `transition` suele ser más simple y con menos código. Si necesitas que **algo se repita solo**, tenga **varios puntos de control** dentro de un mismo ciclo (no solo inicio y fin), o deba reproducirse sin que nada externo lo dispare —un spinner de carga, una animación de introducción al cargar la página—, `@keyframes` con `animation` es la herramienta correcta.

:::tip[Rendimiento: anima `transform` y `opacity` siempre que puedas]
Tanto en `transition` como en `animation`, animar propiedades que afectan al layout (`width`, `height`, `top`, `left`, `margin`) obliga al navegador a recalcular posiciones en cada fotograma. Animar `transform` (`translate`, `scale`, `rotate`) y `opacity` en su lugar permite que el navegador delegue el trabajo a la GPU sin recalcular el layout, lo que se traduce en animaciones más fluidas, especialmente en dispositivos modestos.
:::

:::tip[Respeta `prefers-reduced-motion`]
Algunas personas configuran su sistema operativo para reducir el movimiento en pantalla (mareos, migrañas, trastornos vestibulares). Detecta esa preferencia con la media feature `prefers-reduced-motion` y reduce o elimina animaciones no esenciales:

```css
@media (prefers-reduced-motion: reduce) {
  .spinner {
    animation-duration: 0.001s;
    animation-iteration-count: 1;
  }
}
```
:::

:::tip[Soporte de navegadores]
Las animaciones CSS (`@keyframes` y `animation`) tienen soporte prácticamente universal en navegadores modernos desde hace más de una década. Revisa el detalle y las versiones exactas en [caniuse.com/css-animation](https://caniuse.com/css-animation).
:::

## Ver también

- [Transiciones](transiciones)
- [Transform](transform)
- [Scroll-driven animations](scroll-driven-animations)
- [Unidades y valores](../fundamentos/unidades)

## Fuentes

- [MDN: @keyframes](https://developer.mozilla.org/en-US/docs/Web/CSS/@keyframes)
- [MDN: animation](https://developer.mozilla.org/en-US/docs/Web/CSS/animation)
- [MDN: animation-name](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-name)
- [MDN: animation-duration](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-duration)
- [MDN: animation-timing-function](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timing-function)
- [MDN: animation-delay](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-delay)
- [MDN: animation-iteration-count](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-iteration-count)
- [MDN: animation-direction](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-direction)
- [MDN: animation-fill-mode](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-fill-mode)
- [MDN: animation-play-state](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-play-state)
- [MDN: animation-timeline](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline)
- [MDN: Using CSS animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animations/Using_CSS_animations)
- [MDN: evento animationcancel](https://developer.mozilla.org/en-US/docs/Web/API/Element/animationcancel_event)
- [MDN: transition](https://developer.mozilla.org/en-US/docs/Web/CSS/transition)
- [MDN: transition-property](https://developer.mozilla.org/en-US/docs/Web/CSS/transition-property)
- [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
- [caniuse: CSS Animation](https://caniuse.com/css-animation)
