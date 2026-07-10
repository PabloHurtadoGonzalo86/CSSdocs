---
title: "Cascade layers (@layer)"
description: Cómo usar la regla @layer para agrupar CSS en capas de cascada y controlar explícitamente el orden de prioridad entre bloques de estilos, evitando la guerra de especificidad y el abuso de !important.
---

Las **capas de cascada** (*cascade layers*), definidas con la regla `@layer`, permiten agrupar bloques enteros de CSS y decidir explícitamente en qué orden compiten entre sí, **antes** de que la especificidad o el orden de aparición entren en juego. Son la respuesta moderna a un problema muy real en cualquier proyecto que combina varias fuentes de estilos —un reset, un framework de terceros, componentes de una librería de UI y tu propio CSS—: evitar la guerra de especificidad y el abuso de `!important` para que "tus" estilos ganen a los de fuera.

## Qué problema resuelven

Sin capas, cuando dos reglas de orígenes distintos compiten por la misma propiedad en el mismo elemento, gana la que tenga **más especificidad** y, en caso de empate, la que aparezca **más tarde** en el CSS. Esto genera un problema conocido por cualquiera que haya integrado un framework CSS de terceros: si ese framework usa selectores muy específicos (por ejemplo, varias clases encadenadas), sobrescribir uno de sus estilos con un simple `.mi-clase { color: teal; }` puede no funcionar, aunque tu regla se cargue después. La solución habitual —añadir más clases al selector, o directamente `!important`— funciona, pero es frágil: cada parche exige otro parche más específico para deshacerlo.

Las capas cortan ese nudo desde la raíz. Según [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@layer), el orden entre capas se decide **por el momento en que se declaran**, no por la especificidad de sus selectores: una regla `h1 { color: red; }` dentro de una capa declarada más tarde vence a `#header h1.titulo { color: blue; }` en una capa declarada antes, aunque esta última tenga muchísima más especificidad. Esto convierte la prioridad entre bloques de CSS en algo que se decide **una vez, de forma explícita**, en vez de negociarse selector por selector.

## Sintaxis: crear una capa y asignarle estilos

La forma más directa de usar `@layer` es como bloque con nombre: agrupa un conjunto de reglas dentro de una capa.

```css
@layer reset {
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
}
```

Todo lo que va dentro de `@layer reset { ... }` pertenece a la capa `reset`. Puedes declarar la misma capa varias veces en distintos puntos de tu CSS (o incluso en archivos distintos): las reglas se van **acumulando** en la capa, y su posición en el orden de prioridad queda fijada por la primera vez que esa capa se mencionó, no por dónde se "reabre":

```css
@layer utilidades {
  .flex { display: flex; }
}

/* Más adelante en el mismo archivo, o en otro archivo */
@layer utilidades {
  .grid { display: grid; }
}
```

Ambas reglas terminan en la misma capa `utilidades`, sin que esto altere su posición relativa frente a otras capas.

## Sintaxis: declarar el orden sin escribir estilos todavía

La segunda forma de `@layer` es una declaración (*statement*), sin llaves, que sirve solo para fijar el orden de una o varias capas por adelantado:

```css
@layer reset, base, componentes, utilidades;
```

Esta línea no aplica ningún estilo: únicamente establece que, de menor a mayor prioridad, el orden será `reset` → `base` → `componentes` → `utilidades`. Es una práctica muy recomendable al principio de tu hoja de estilos principal, porque documenta de un vistazo la jerarquía completa del proyecto, y porque te permite declarar capas concretas más adelante (o en archivos que se cargan en cualquier orden) sin preocuparte de en qué secuencia física llegan al navegador: el orden ya quedó fijado por esta declaración inicial.

```css
/* 1. Fijamos el orden de todo el proyecto */
@layer reset, terceros, propios;

/* 2. Cada bloque puede llegar en cualquier orden físico después de esto */
@layer propios {
  .btn-primario { background: rebeccapurple; }
}

@layer reset {
  * { margin: 0; }
}

@layer terceros {
  .btn { background: gray; padding: 0.5em 1em; }
}
```

Aunque en el código `propios` aparece declarado primero (en el paso 2), su prioridad real es la más alta de las tres, porque así se fijó en la declaración de orden del paso 1. Esta es precisamente la ventaja frente a depender del orden de aparición: el orden de **prioridad** y el orden **físico** en el archivo dejan de ser la misma cosa.

Si nunca declaras el orden por adelantado, cada capa nueva que aparece por primera vez se añade al final de la lista de prioridad, en el orden en que el navegador la encuentra al parsear el CSS.

## Capas anónimas y capas anidadas

Un `@layer` sin nombre crea una **capa anónima**: ocupa su posición en el orden igual que una con nombre, pero no se puede reabrir ni referenciar después, porque no hay forma de nombrarla:

```css
@layer {
  body {
    line-height: 1.5;
  }
}
```

También puedes anidar capas dentro de otras, para organizar sub-bloques dentro de un framework o módulo, usando notación con punto para referenciar la subcapa desde fuera:

```css
@layer framework {
  @layer botones {
    .btn { border-radius: 0.25rem; }
  }
}

/* Añadir más reglas a la subcapa desde otro punto del CSS */
@layer framework.botones {
  .btn { font-weight: 600; }
}
```

## Los estilos sin capa (unlayered) siempre ganan

Una regla que no está dentro de ningún `@layer` se considera **sin capa** (*unlayered*), y en la comparación normal (sin `!important`) tiene **más prioridad que cualquier estilo dentro de una capa**, sin importar cuántas capas hayas declarado ni su especificidad:

```css
@layer base {
  p {
    color: green;
  }
}

p {
  color: crimson; /* Sin capa: gana siempre frente a "base" */
}
```

Aquí el párrafo se pinta `crimson`. Esto tiene una implicación práctica muy útil: si quieres que tu CSS de autor tenga garantizado el máximo control sobre un reset o un framework de terceros, basta con meter ese reset y ese framework **dentro** de capas, y dejar tus estilos propios **fuera** de cualquier capa. Ganan por definición, sin necesidad de aumentar especificidad ni recurrir a `!important`.

:::caution[El orden se invierte con `!important`]
Dentro de declaraciones marcadas con `!important`, la cascada **invierte** el orden de prioridad entre capas: la **primera** capa declarada pasa a tener la prioridad más alta, y los estilos sin capa con `!important` pasan a tener la prioridad más **baja** de todas las combinaciones normales. Es un detalle poco intuitivo pero coherente con la idea de que `!important` representa una "corrección de emergencia": conviene que la corrección más temprana (por ejemplo, la de un reset) sea difícil de tapar por accidente desde capas posteriores.
:::

## Importar CSS de terceros directamente en una capa

`@import` admite la palabra clave `layer()` para asignar un archivo completo a una capa en el momento de importarlo, lo cual es ideal para meter un framework o librería externa en su propia capa sin tocar su código fuente:

```css
@layer reset, terceros, propios;

@import url("normalize.css") layer(reset);
@import url("framework-ui.css") layer(terceros);
```

Recuerda que, como cualquier `@import`, estas líneas deben ir al principio de la hoja de estilos: solo pueden precederlas `@charset` y declaraciones `@layer` sin bloque (la forma de orden que vimos antes). En cuanto aparece una regla de estilo normal, ya no se admite ningún `@import` después.

## Caso práctico: reset, framework de terceros y estilos propios

Este es el escenario donde `@layer` demuestra su valor con más claridad: tres fuentes de CSS con distinta especificidad y distinto grado de control sobre su código, que necesitan convivir con una jerarquía de prioridad predecible.

```css
/* 1. Declaramos el orden de todo el proyecto en un solo lugar */
@layer reset, terceros, propios;

/* 2. Un reset básico, con selectores de baja especificidad mezclados con otros altos */
@layer reset {
  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    font-family: system-ui, sans-serif;
  }
}

/* 3. El CSS de un framework de terceros (aquí, simulado; en la práctica llegaría
      con @import url("framework.css") layer(terceros);) */
@layer terceros {
  .btn.btn-primary.btn-lg {
    /* Selector muy específico, típico de un framework */
    background-color: #0d6efd;
    padding: 0.75rem 1.5rem;
    border-radius: 0.375rem;
  }
}

/* 4. Tus propios estilos, con un selector deliberadamente simple */
@layer propios {
  .btn {
    background-color: var(--color-marca, teal);
    font-weight: 600;
  }
}
```

```html
<button class="btn btn-primary btn-lg">Comprar</button>
```

El botón termina con `background-color` de la capa `propios` (`teal` o el color de marca) y no con el azul del framework, **a pesar de que** `.btn.btn-primary.btn-lg` tiene mucha más especificidad que `.btn`. Sin capas, este mismo resultado habría exigido igualar o superar esa especificidad (por ejemplo, repitiendo `.btn-primary.btn-lg` en tu selector) o recurrir a `!important`. Con capas, la prioridad quedó decidida una sola vez en el paso 1, y cualquier estilo nuevo que añadas dentro de `propios` seguirá ganando automáticamente a `terceros`, sin que tengas que volver a pensar en especificidad cada vez que el framework cambie sus clases internas.

Fíjate también en que `padding` y `border-radius`, definidos solo en `terceros`, sí se aplican con normalidad: `@layer` no bloquea propiedades, solo resuelve **conflictos** cuando dos capas fijan un valor distinto para la misma propiedad del mismo elemento.

:::tip[Soporte de navegadores]
Las capas de cascada (`@layer`) tienen un soporte muy amplio: según [caniuse](https://caniuse.com/css-cascade-layers), están disponibles desde Chrome y Edge 99, Firefox 97 y Safari 15.4 (todos de principios de 2022). Si necesitas dar soporte a versiones anteriores, ten en cuenta que en esos navegadores el bloque `@layer` se ignora por completo (no se aplica ningún estilo de dentro), así que conviene comprobar el comportamiento con `@supports at-rule(@layer)` antes de depender de esta técnica como único mecanismo de prioridad.
:::

## Ver también

- [Cascada, especificidad y herencia](../fundamentos/cascada-especificidad-herencia)
- [Selectores modernos (:has, :is, :where)](selectores-modernos)
- [Nesting nativo](nesting)
- [Arquitectura y organización de CSS](../arquitectura/metodologias-y-organizacion)

## Fuentes

- [MDN: @layer](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@layer)
- [MDN: Cascade layers (Learn web development)](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Cascade_layers)
- [MDN: Introduction to the CSS cascade](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Introduction)
- [MDN: @import](https://developer.mozilla.org/en-US/docs/Web/CSS/@import)
- [caniuse: CSS Cascade Layers](https://caniuse.com/css-cascade-layers)
