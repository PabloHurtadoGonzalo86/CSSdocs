---
title: "Selectores modernos: `:has()`, `:is()`, `:where()`"
description: Explica cómo :is(), :where() y :has() de Selectors Level 4 agrupan selectores repetitivos y permiten estilar un elemento en función de su contenido o de lo que le sigue.
---

Durante años, CSS solo pudo "mirar hacia abajo": un selector podía describir un elemento y sus descendientes, pero nunca condicionar un estilo al contenido que ese elemento tuviera dentro, ni evitar repetir la misma combinación de selectores una y otra vez. Las pseudo-clases `:is()`, `:where()` y `:has()`, definidas en la especificación [Selectors Level 4](https://drafts.csswg.org/selectors/), cierran ambas carencias: las dos primeras comprimen listas de selectores repetitivas, y `:has()` permite por fin estilar un elemento en función de lo que contiene, algo que hasta hace poco solo se podía resolver con JavaScript.

## `:is()` y `:where()`: agrupar selectores sin repetir combinaciones

Ambas pseudo-clases reciben una **lista de selectores** como argumento y seleccionan cualquier elemento que coincida con alguno de ellos. Son, en esencia, una forma de factorizar selectores que comparten una misma estructura.

Compara este selector repetitivo:

```css
header a:hover,
nav a:hover,
footer a:hover {
  color: var(--color-accent);
}
```

con su versión usando `:is()`:

```css
:is(header, nav, footer) a:hover {
  color: var(--color-accent);
}
```

Ambas reglas seleccionan exactamente lo mismo, pero la segunda escala mejor: si mañana añades un `<aside>` a la lista, solo tocas un sitio. El ahorro es aún más claro cuando el selector tiene varios niveles, porque el número de combinaciones crece de forma multiplicativa:

```css
/* Antes: hay que enumerar cada combinación de contenedor y encabezado */
section h2,
article h2,
aside h2,
nav h2 {
  font-size: 1.5rem;
}

/* Después: una sola regla cubre las mismas combinaciones */
:is(section, article, aside, nav) h2 {
  font-size: 1.5rem;
}
```

### Listas "perdonadoras" (forgiving selector list)

Una lista de selectores separada por comas normal es "no perdonadora": si uno solo de sus selectores es inválido o no está soportado por el navegador, **toda la regla se descarta**, incluidos los selectores que sí eran correctos. `:is()` y `:where()`, en cambio, usan una *forgiving selector list*: si alguno de los selectores del argumento no es válido, simplemente se ignora, y el resto sigue funcionando.

```css
/* Si el navegador no soporta ":unsupported", esta línea completa se ignora */
:valid,
:unsupported {
  outline: 2px solid green;
}

/* Con :is(), ":valid" se sigue aplicando aunque ":unsupported" no exista */
:is(:valid, :unsupported) {
  outline: 2px solid green;
}
```

Esto es especialmente útil para adoptar pseudo-clases nuevas sin arriesgarte a que un navegador antiguo tire por la borda toda una regla por una sola pseudo-clase que no reconoce.

:::caution[Restricción: no aceptan pseudo-elementos]
El argumento de `:is()` y `:where()` admite selectores simples, compuestos y complejos, pero **no pseudo-elementos** (`::before`, `::after`, etc.). Es decir, `some-element:is(::before, ::after)` no es válido; para eso sigue haciendo falta la agrupación clásica con coma: `some-element::before, some-element::after`.
:::

### La diferencia clave: la especificidad

Aquí es donde `:is()` y `:where()` dejan de ser intercambiables:

- **`:is()` toma la especificidad del selector *más específico* de su lista de argumentos.**
- **`:where()` siempre tiene especificidad cero**, sea cual sea su contenido.

Esto no es un detalle menor: determina si tus reglas son fáciles o difíciles de sobrescribir después. Compara los dos ejemplos siguientes, donde ambos seleccionan lo mismo pero se comportan de forma opuesta frente a un selector simple posterior:

```css
/* Con :is(): la especificidad es la de ".card" (una clase) + "h2" (un tipo) = 0-1-1 */
:is(.card, .panel, .widget) h2 {
  margin-top: 0;
}

/* Esta regla NUNCA puede ganar aquí: su especificidad (0-0-1) es menor que 0-1-1 */
h2 {
  margin-top: 1rem;
}
```

```css
/* Con :where(): la lista de clases aporta 0, así que la especificidad total es solo la de "h2" = 0-0-1 */
:where(.card, .panel, .widget) h2 {
  margin-top: 0;
}

/* Esta regla tiene la MISMA especificidad (0-0-1): gana por orden en la cascada, no por fuerza bruta */
h2 {
  margin-top: 1rem;
}
```

En el segundo caso, `h2 { margin-top: 1rem; }` gana si aparece después en la cascada, sin necesidad de añadir una clase extra o recurrir a `!important`. Por eso `:where()` es la elección natural cuando escribes estilos "base" pensados para que otra persona (o tu propio CSS de componente, cargado después) los pueda sobrescribir sin fricción: resets, temas por defecto de un sistema de diseño, o cualquier capa de estilos que quieras que ceda fácilmente ante reglas más concretas. `:is()`, en cambio, conviene cuando sí quieres que ese peso de especificidad se mantenga, por ejemplo al simplificar un selector ya de por sí específico sin rebajar su prioridad en la cascada.

:::tip[Soporte de navegadores]
`:is()` y `:where()` son *Baseline: Widely available* (ampliamente soportados) desde enero de 2021. Puedes consultar el detalle por versión en [caniuse.com: :is()](https://caniuse.com/css-matches-pseudo) y [caniuse.com: :where()](https://caniuse.com/mdn-css_selectors_where).
:::

## `:has()`: el selector relacional (el "selector de padre")

`:has()` resuelve algo que llevaba pidiéndose desde los primeros borradores de Selectors Level 4: seleccionar un elemento **en función de lo que hay dentro de él, o de lo que le sigue**, en lugar de solo poder descender por el árbol. Por eso se le suele llamar informalmente "el selector de padre": permite subir en la jerarquía en vez de bajar.

Formalmente, `:has()` representa a un elemento si, al anclar en él uno o varios **selectores relativos**, alguno de ellos encuentra coincidencia. Un selector relativo es un selector que empieza (de forma implícita) por un combinador respecto al elemento ancla: descendiente, hijo directo (`>`), hermano adyacente (`+`) o hermano general (`~`).

### Ejemplo práctico: un formulario con un campo inválido

Uno de los casos de uso más citados de `:has()` es dar feedback visual a un formulario completo cuando alguno de sus campos falla la validación nativa del navegador, sin necesidad de JavaScript ni de que el propio campo lleve la marca:

```css
form:has(:invalid) {
  border: 2px solid crimson;
  outline-offset: 4px;
}

form:has(:invalid):hover {
  cursor: not-allowed;
}
```

`form:has(:invalid)` selecciona el `<form>` cuando **al menos uno** de sus campos descendientes está en estado `:invalid` (por ejemplo, un `<input type="email">` con un valor mal formado, o un campo `required` vacío). Antes de `:has()`, expresar "el padre reacciona al estado de un hijo" era terreno exclusivo de JavaScript o de trucos con `:focus-within`, que solo cubre el foco, no la validez.

### Ejemplo práctico: una tarjeta que contiene una imagen

Otro uso muy habitual es adaptar el layout de un componente según si contiene cierto tipo de contenido, sin tener que añadir una clase modificadora manualmente cada vez que cambia el contenido:

```css
/* Layout de dos columnas solo cuando la tarjeta trae imagen */
.card:has(img) {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 1rem;
}

/* El resto de tarjetas conserva un layout de una sola columna (el valor por defecto) */
.card {
  display: block;
  padding: 1rem;
}
```

Aquí `.card:has(img)` da un estilo distinto a las tarjetas que incluyen una `<img>` en cualquier nivel de profundidad, mientras que las tarjetas sin imagen siguen usando el layout de bloque simple. El CSS reacciona al contenido real del HTML, no a una clase que alguien tiene que recordar añadir.

### Combinadores dentro de `:has()`: también hermanos

El argumento de `:has()` no se limita a descendientes; también acepta combinadores de hermano, lo que permite condicionar un elemento a lo que viene *después* de él (algo que ningún otro selector de CSS permitía hasta ahora):

```css
/* Reduce el margen de un h1 si justo después viene un h2 (subtítulo pegado) */
h1:has(+ h2) {
  margin-block-end: 0.25rem;
}
```

Y se puede combinar con `:is()` para cubrir varios niveles de encabezado a la vez:

```css
:is(h1, h2, h3):has(+ :is(h2, h3, h4)) {
  margin-block-end: 0.25rem;
}
```

También sirve para expresar lógica "Y"/"O" encadenando varios `:has()`, cada uno actuando como una condición independiente:

```css
/* O: el body contiene un <video> O un <audio> (basta con que aparezca uno de los dos en la lista) */
body:has(video, audio) {
  --has-media: true;
}

/* Y: el body contiene un <video> Y, además, un <audio> */
body:has(video):has(audio) {
  --has-media: true;
}
```

### Restricciones que conviene conocer

- **No se puede anidar `:has()` dentro de otro `:has()`.** Esta limitación existe para evitar selectores circulares y consultas de coste imprevisible.
- **No admite pseudo-elementos**: ni como argumento (`:has(::before)` no es válido) ni como elemento ancla (`::before:has(...)` tampoco).
- **No es una lista perdonadora por sí sola**: si el propio `:has()` no está soportado, toda la regla se descarta, igual que con cualquier selector no reconocido. Para que falle de forma "perdonadora" hay que envolverlo en `:is()` o `:where()`, como en `:is(:has(...)) { … }`.

:::caution[Cuidado con el rendimiento en anclas muy amplias]
Anclar `:has()` en elementos muy altos del árbol (`body:has(.modal-abierto)`, `:root:has(...)`) obliga al navegador a comprobar el estado de subárboles enteros del DOM en cada repintado relevante. Siempre que puedas, ancla `:has()` en el contenedor más concreto posible (`.modal-container:has(...)` en vez de `body:has(...)`) y usa combinadores directos (`:has(> .foo)`) cuando la relación lo permita, para acotar cuánto tiene que recorrer el navegador.
:::

:::tip[Soporte de navegadores]
`:has()` es *Baseline: Widely available* (ampliamente soportado) desde diciembre de 2023, más reciente que `:is()`/`:where()`. Si tu proyecto necesita dar soporte a navegadores anteriores a esa fecha, revisa el detalle exacto por versión en [caniuse.com: :has()](https://caniuse.com/css-has) y considera usarlo como mejora progresiva (con un fallback vía clase de JavaScript) en vez de como único mecanismo.
:::

## Ver también

- [Selectores en CSS](../fundamentos/selectores)
- [Cascada, especificidad y herencia](../fundamentos/cascada-especificidad-herencia)
- [Nesting nativo](nesting)
- [Cheatsheet de selectores](../cheatsheets/selectores-cheatsheet)

## Fuentes

- [MDN: :is()](https://developer.mozilla.org/en-US/docs/Web/CSS/:is)
- [MDN: :where()](https://developer.mozilla.org/en-US/docs/Web/CSS/:where)
- [MDN: :has()](https://developer.mozilla.org/en-US/docs/Web/CSS/:has)
- [W3C CSSWG: Selectors Level 4 — The Relational Pseudo-class: :has()](https://drafts.csswg.org/selectors/#relational)
- [W3C CSSWG: Selectors Level 4 — Forgiving selector list](https://drafts.csswg.org/selectors-4/#typedef-forgiving-selector-list)
- [caniuse: :is() (css-matches-pseudo)](https://caniuse.com/css-matches-pseudo)
- [caniuse: :where()](https://caniuse.com/mdn-css_selectors_where)
- [caniuse: :has()](https://caniuse.com/css-has)
