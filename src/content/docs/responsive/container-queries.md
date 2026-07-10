---
title: Container queries
description: Guía sobre las container queries en CSS - container-type, container-name, la at-rule @container y las unidades cqw/cqh/cqi/cqb/cqmin/cqmax para adaptar componentes al tamaño de su contenedor.
---

Las *container queries* (consultas de contenedor) permiten aplicar estilos a un elemento según el tamaño de **su contenedor**, no según el tamaño del viewport. Esto cambia por completo cómo se construyen componentes reutilizables: en lugar de diseñar pensando en "¿qué tamaño tiene la pantalla?", diseñas pensando en "¿cuánto espacio tiene disponible este componente ahora mismo?", que es la pregunta que de verdad importa cuando un mismo bloque de UI puede vivir en una barra lateral estrecha, en el cuerpo principal o dentro de un modal.

## El problema que resuelven frente a media queries

Una `@media` query solo sabe responder preguntas sobre el **viewport** (o, con `@media` de tipo `print`, sobre el dispositivo de salida): ancho de la ventana, orientación, resolución... Nunca sabe nada sobre el elemento en el que se aplica ni sobre el espacio real que ese elemento tiene disponible dentro de su layout.

Esto es un problema real en cuanto construyes componentes pensados para reutilizarse en distintos contextos. Imagina una tarjeta de producto:

```css
.tarjeta {
  display: flex;
  flex-direction: column;
}

@media (min-width: 600px) {
  .tarjeta {
    flex-direction: row; /* imagen a la izquierda, texto a la derecha */
  }
}
```

Esto funciona si la tarjeta ocupa casi todo el ancho de la pantalla. Pero si esa misma tarjeta se coloca dentro de una barra lateral de 280px en un layout de tres columnas, la media query seguirá disparándose en cuanto el **viewport** supere los 600px, aunque la tarjeta en sí nunca tenga más de 280px reales para trabajar. El resultado: contenido en horizontal apretujado en un contenedor demasiado estrecho.

Las *container queries* resuelven esto invirtiendo la pregunta: en lugar de "¿qué ancho tiene la ventana?", preguntan "¿qué ancho tiene el contenedor de este elemento?". El mismo componente puede así decidir su propio layout según el espacio real que le rodea, sea cual sea el tamaño de la pantalla o dónde lo hayas colocado en la página.

## Declarar un contenedor de consulta: `container-type`

Para que un elemento pueda consultarse por tamaño, primero hay que convertirlo explícitamente en un **contenedor de consulta** (*query container*) con la propiedad `container-type`. No es un paso opcional ni automático: por defecto, ningún elemento es consultable.

```css
.post {
  container-type: inline-size;
}
```

| Valor | Efecto |
|---|---|
| `normal` (inicial) | El elemento **no** es un contenedor de tamaño. Puede seguir usándose en *container queries* de estilo o en queries "solo por nombre" (ver más abajo), pero no en condiciones de ancho/alto. |
| `inline-size` | Establece contención de tamaño en el **eje inline** (el ancho, en escritura horizontal): permite `@container` queries basadas en el ancho del contenedor. |
| `size` | Establece contención de tamaño en **ambos ejes** (inline y block): permite `@container` queries basadas en ancho **y** alto. |

`inline-size` es, en la práctica, el valor que más se usa: la mayoría de layouts responsivos solo necesitan reaccionar al ancho disponible, no al alto.

:::caution[`container-type: size` puede colapsar el alto del contenedor]
Tanto `inline-size` como `size` aplican **contención** (*containment*) sobre el elemento: básicamente, le dicen al navegador "el tamaño de esta caja se puede calcular en aislamiento, sin mirar el contenido de sus hijos". Es necesario por rendimiento —si el navegador tuviera que recalcular constantemente el tamaño de cada contenedor mirando a sus descendientes, se arriesgaría a bucles infinitos cuando un hijo cambia de tamaño según el propio contenedor—, pero tiene una consecuencia práctica: con `container-type: size`, si no le das al contenedor una altura por otra vía (un valor explícito, `min-height`, el contexto de un grid/flex que le asigne alto...), **puede terminar colapsando a 0 de alto**, porque el navegador ignora el alto que "pediría" su contenido. Por eso `inline-size` (que solo contiene el eje horizontal, dejando el alto en su comportamiento normal según el contenido) es la opción más segura por defecto.
:::

## Nombrar el contenedor: `container-name`

Cuando solo tienes un contenedor de consulta en la ruta de ancestros de un elemento, `@container` lo encuentra automáticamente (busca hacia arriba el contenedor más cercano). Pero en layouts anidados —un contenedor dentro de otro contenedor— puede ser ambiguo a cuál te refieres. `container-name` asigna uno o varios nombres a un contenedor para poder apuntar a él explícitamente:

```css
.post {
  container-type: inline-size;
  container-name: sidebar;
}
```

`container-name` acepta un identificador (`sidebar`), varios separados por espacio (`container-name: tarjeta destacado;`, útil si quieres que el mismo contenedor responda a varias `@container` con nombres distintos) o el valor inicial `none` (sin nombre). Los nombres no pueden coincidir con las palabras reservadas `and`, `or`, `not` ni `default`, y son sensibles a mayúsculas/minúsculas.

### El atajo `container`

Igual que `flex` combina `flex-grow`/`flex-shrink`/`flex-basis`, la propiedad shorthand `container` combina nombre y tipo en una sola declaración, con el nombre primero y el tipo después de una barra `/`:

```css
.post {
  container: sidebar / inline-size;
  /* equivale a:
     container-name: sidebar;
     container-type: inline-size; */
}
```

## La at-rule `@container`: escribir las reglas condicionales

Con el contenedor ya declarado, `@container` funciona de forma parecida a `@media`, pero evaluando el tamaño del contenedor en vez del viewport. Todo selector dentro del bloque sigue aplicando a los **descendientes** de ese contenedor (nunca al propio contenedor, que es una limitación intencionada del modelo).

```css
.post {
  container-type: inline-size;
}

.card h2 {
  font-size: 1em;
}

@container (width > 700px) {
  .card h2 {
    font-size: 2em;
  }
}
```

Aquí `.card h2` cambia de tamaño cuando el `.post` que lo contiene supera los 700px de ancho, sin que importe el tamaño del viewport: si `.post` mide 700px porque está en una columna estrecha de una pantalla de 4K, la regla no se aplica; si mide más de 700px dentro de un móvil en horizontal con una ventana grande, sí.

### Sintaxis de las condiciones

`@container` admite tanto la sintaxis clásica de rango con `min-width`/`max-width` como la sintaxis de comparación abreviada (rediseñada para *media queries* de nivel 4 y compartida con `@container`):

```css
@container (min-width: 700px) { /* … */ }
@container (width >= 700px) { /* misma condición, sintaxis de rango */ }
@container (400px <= width <= 700px) { /* entre 400 y 700px */ }
```

Los descriptores disponibles para consultas de tamaño incluyen `width`, `height`, `inline-size`, `block-size`, `aspect-ratio` y `orientation` (con los valores `portrait`/`landscape`, igual que en `@media`). Ojo con un detalle importante: `height`, `block-size`, `aspect-ratio` y `orientation` solo se pueden evaluar en un contenedor con `container-type: size`, porque necesitan contención también en el eje *block*. Si el contenedor solo tiene `container-type: inline-size` (el caso más habitual, como en los ejemplos de esta guía), esas condiciones se consideran de resultado "desconocido" y la regla **nunca llega a aplicarse** —la sintaxis no da ningún error, simplemente el bloque `@container` se comporta como si la condición fuera falsa—. Si necesitas consultar el alto o el *aspect ratio*, recuerda cambiar el contenedor a `container-type: size` (y ten presente la advertencia sobre el colapso de alto que se explica más arriba).

### Apuntar a un contenedor por nombre

Si has puesto `container-name`, puedes anteponer ese nombre a la condición para asegurarte de que la consulta ignora contenedores intermedios sin ese nombre:

```css
@container sidebar (width > 700px) {
  .card {
    font-size: 2em;
  }
}
```

También existen las **queries "solo por nombre"**, sin ninguna condición de tamaño: aplican el estilo a los descendientes de cualquier contenedor con ese nombre, tenga o no `container-type` distinto de `normal`.

```css
@container sidebar {
  p {
    color: rebeccapurple;
  }
}
```

### Combinar condiciones

`@container` admite los mismos operadores lógicos que `@media`: `and`, `or` y `not`.

```css
@container (width > 400px) and (height > 300px) { /* … */ }
@container not (width < 400px) { /* … */ }
```

:::tip[Más allá del tamaño: *style queries*]
Además de consultar dimensiones, `@container` también admite **queries de estilo** con la función `style()`, que evalúan el valor computado de una *custom property* del contenedor (por ejemplo `@container style(--tema: oscuro) { … }`). Es una capacidad más reciente y, durante más tiempo, con menos soporte que las *size queries*; si la necesitas, revisa su estado actual en [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/@container#container_style_queries) antes de depender de ella en producción.
:::

## Unidades de container query: `cqw`, `cqh`, `cqi`, `cqb`, `cqmin`, `cqmax`

Cuando un elemento tiene `container-type: size` o `inline-size`, puedes usar unidades relativas al **tamaño del contenedor** (no del viewport) para definir tipografía, espaciados o cualquier otra longitud que deba escalar junto con el contenedor.

Cada unidad se resuelve buscando, eje por eje, el contenedor de tamaño más cercano que tenga contención en ese eje concreto. Esto importa porque `inline-size` solo contiene el eje inline: en un contenedor con `container-type: inline-size`, las unidades `cqi`/`cqw` sí reflejan el ancho de ese contenedor, pero `cqb`/`cqh` siguen subiendo por el árbol de ancestros en busca de un contenedor con `container-type: size` (el único que también contiene el eje block); si no encuentran ninguno, caen igualmente al valor de *small viewport* equivalente, tal y como se explica más abajo.

| Unidad | Equivale a |
|---|---|
| `cqw` | 1% del **ancho** del contenedor de consulta |
| `cqh` | 1% del **alto** del contenedor de consulta |
| `cqi` | 1% del tamaño en el **eje inline** del contenedor (el ancho, en escritura horizontal) |
| `cqb` | 1% del tamaño en el **eje block** del contenedor (el alto, en escritura horizontal) |
| `cqmin` | El menor valor entre `cqi` y `cqb` |
| `cqmax` | El mayor valor entre `cqi` y `cqb` |

```css
.card h2 {
  /* crece junto con el ancho del contenedor, con un mínimo legible */
  font-size: max(1.25rem, 1rem + 2cqi);
}
```

`cqi`/`cqb` son las variantes recomendadas para la mayoría de casos porque respetan el modo de escritura (en un documento vertical, `cqi` seguiría representando el eje "principal" de lectura); `cqw`/`cqh` son más directas cuando ya piensas en términos físicos de ancho/alto.

:::note[Qué pasa si no hay contenedor válido]
Si un elemento usa unidades `cq*` pero no tiene ningún contenedor de tamaño válido en su cadena de ancestros (por ejemplo, porque olvidaste poner `container-type` en el padre), esas unidades recurren a las unidades de *small viewport* equivalentes (`svw`, `svh`, `svi`, `svb`, `svmin`, `svmax`) en lugar de romper el cálculo o no aplicar nada.
:::

## Ejemplo práctico: una tarjeta que se adapta a su contenedor

Uniendo todo lo anterior, así se ve un componente de tarjeta que cambia de layout y tipografía según el espacio real que tenga, sin ninguna media query de por medio:

```css
.post {
  container: tarjetas / inline-size;
}

.card {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card h2 {
  font-size: 1.1rem;
}

@container tarjetas (width > 480px) {
  .card {
    flex-direction: row; /* imagen y texto en horizontal si hay sitio */
    align-items: center;
    gap: 1rem;
  }

  .card h2 {
    font-size: max(1.1rem, 1rem + 1.5cqi);
  }
}
```

La misma `.card` se apila en columna cuando vive en un espacio estrecho (una barra lateral, una columna de un grid de tres) y pasa a fila horizontal en cuanto su contenedor `.post` supera 480px de ancho, sea cual sea el tamaño real de la ventana del navegador.

:::tip[Soporte de navegadores]
Las *container queries* de tamaño (`container-type`, `container-name`, `@container` con condiciones de ancho/alto) alcanzaron soporte en Chrome/Edge 106, Firefox 110 y Safari 16, y hoy se consideran ampliamente disponibles (*Baseline: Widely available*). Las unidades `cqw`/`cqh`/`cqi`/`cqb`/`cqmin`/`cqmax` llegaron en Chrome/Edge 105, Firefox 110 y Safari 16. Si tu proyecto necesita dar soporte a navegadores anteriores a esas versiones, verifica el detalle actualizado en [caniuse: CSS Container Queries](https://caniuse.com/css-container-queries) y [caniuse: CSS Container Query Units](https://caniuse.com/css-container-query-units), y prepara un fallback razonable (por ejemplo, un layout en columna simple que funcione sin `@container`).
:::

## Ver también

- [Media queries](media-queries)
- [Unidades y funciones responsivas](unidades-y-funciones)
- [Flexbox](../layout/flexbox)
- [CSS Grid](../layout/grid)

## Fuentes

- [MDN: CSS container queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries)
- [MDN: container-type](https://developer.mozilla.org/en-US/docs/Web/CSS/container-type)
- [MDN: container-name](https://developer.mozilla.org/en-US/docs/Web/CSS/container-name)
- [MDN: container (shorthand)](https://developer.mozilla.org/en-US/docs/Web/CSS/container)
- [MDN: @container](https://developer.mozilla.org/en-US/docs/Web/CSS/@container)
- [MDN: contain](https://developer.mozilla.org/en-US/docs/Web/CSS/contain)
- [MDN: CSS container size and style queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_size_and_style_queries)
- [W3C: CSS Containment Module Level 3](https://www.w3.org/TR/css-contain-3/)
- [caniuse: CSS Container Queries (Size)](https://caniuse.com/css-container-queries)
- [caniuse: CSS Container Query Units](https://caniuse.com/css-container-query-units)
- [caniuse: CSS Container Style Queries](https://caniuse.com/css-container-queries-style)
