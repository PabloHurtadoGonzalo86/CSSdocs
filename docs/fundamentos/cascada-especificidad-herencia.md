# Cascada, especificidad y herencia

Cuando dos reglas CSS distintas intentan poner un color diferente al mismo párrafo, algo tiene que decidir cuál gana. Ese "algo" es la **cascada**: el algoritmo que ordena todas las declaraciones que aplican a un elemento y elige la definitiva. La **especificidad** es uno de los criterios que usa esa cascada para desempatar, y la **herencia** es el mecanismo que rellena los huecos cuando ninguna regla dice nada sobre una propiedad. Entender estos tres conceptos es lo que separa a quien "prueba cosas hasta que funciona" de quien sabe exactamente por qué un estilo se aplica o no, sin recurrir a `!important` como parche.

## Qué es la cascada

La cascada ("Cascading" en *Cascading Style Sheets*) es el proceso mediante el cual el navegador combina declaraciones CSS de distintos orígenes (tu hoja de estilos, la del usuario, la del propio navegador) y decide, para **cada propiedad de cada elemento**, qué valor final se aplica. Según la especificación y la [documentación de MDN sobre la cascada](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascade/Cascade), cuando varias declaraciones compiten por la misma propiedad en el mismo elemento, el navegador las ordena siguiendo, en este orden, estos criterios:

1. **Origen e importancia**: de dónde viene la regla (navegador, usuario, autor) y si lleva `!important`.
2. **Especificidad**: qué tan concreto es el selector.
3. **Proximidad de scope**: si se usa [`@scope`](../moderno/scope.md), gana la regla cuyo *scope* está más cerca del elemento en el árbol del documento.
4. **Orden de aparición**: si todo lo anterior empata, gana la última declaración leída.

Fíjate en el orden: la especificidad **solo entra en juego si el origen y la importancia ya son iguales**. Esto explica por qué un selector con más clases no siempre gana: si compite contra una regla de otro origen o con distinta importancia, la especificidad ni se llega a mirar.

### Origen e importancia: la primera criba

El origen determina de dónde sale la regla. De menor a mayor prioridad:

| Prioridad | Origen | Importancia |
|---|---|---|
| 1 (más baja) | Navegador (*user-agent*) | normal |
| 2 | Usuario | normal |
| 3 | Autor (tu CSS) | normal |
| 4 | Animaciones CSS (`@keyframes`) en curso | — |
| 5 | Autor (tu CSS) | `!important` |
| 6 | Usuario | `!important` |
| 7 | Navegador (*user-agent*) | `!important` |
| 8 (más alta) | Transiciones CSS en curso | — |

Como desarrolladores trabajamos casi siempre en la franja 3 y 5 (autor, normal y `!important`). Lo interesante es lo que pasa en los extremos: un `!important` del **usuario** (por ejemplo, estilos que la persona define en su navegador para accesibilidad, como un tamaño de letra mínimo) vence a cualquier `!important` que pongas en tu propia hoja de estilos. Es una decisión de diseño intencionada: la accesibilidad del usuario debe poder imponerse sobre las preferencias del sitio.

!!! tip "Soporte de navegadores"
    El núcleo de este orden (user-agent, usuario, autor, y sus variantes `!important`) ya estaba en CSS 2.1, aunque con solo cinco niveles: esa especificación no contemplaba la posición de las animaciones y transiciones en curso, que se incorporó después con **CSS Cascading and Inheritance Level 4**, ni las capas de cascada, que llegaron todavía más tarde con **CSS Cascading and Inheritance Level 5**. Hoy toda la tabla de ocho niveles está soportada universalmente en navegadores modernos. Lo que sí es relativamente reciente es el nivel de **capas de cascada** (`@layer`) que se describe a continuación: consulta [caniuse.com/css-cascade-layers](https://caniuse.com/css-cascade-layers) para el detalle de versiones.

### Las capas de cascada (`@layer`)

Dentro del origen "autor", `@layer` añade un nivel extra de prioridad **antes** de que se compare la especificidad. Las capas se ordenan por el momento en que se declaran: la primera capa declarada tiene la prioridad más baja y la última la más alta. Los estilos que **no** están dentro de ninguna capa (*unlayered*) superan siempre a cualquier estilo en capa, sin importar su especificidad:

```css
@layer base, utilidades;

@layer base {
  h1 {
    color: darkslategray;
  }
}

@layer utilidades {
  .text-brand {
    color: rebeccapurple;
  }
}

h1 {
  color: crimson; /* Sin capa: gana siempre frente a cualquier regla en capa */
}
```

Aquí `h1` se pinta `crimson`, no `darkslategray`, aunque la capa `base` esté declarada y el selector `h1` sea igual de específico en ambos casos: al estar fuera de capa, gana por definición. Esto convierte a `@layer` en una herramienta mucho más predecible que `!important` para gestionar prioridades entre, por ejemplo, un framework de terceros y tus propios estilos. El tema se trata en profundidad en [Cascade layers (@layer)](../moderno/cascade-layers.md).

## Cómo se calcula la especificidad

Una vez que dos (o más) declaraciones compiten dentro del **mismo origen, la misma importancia y la misma capa**, la cascada mira la especificidad del selector. Según [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascade/Specificity), la especificidad se representa como un valor de **tres columnas** —ID, CLASE y TIPO— que se comparan de izquierda a derecha, **sin convertirlas nunca en un único número**:

| Columna | Cuenta... | Ejemplos |
|---|---|---|
| **ID** | Selectores de ID | `#header` |
| **CLASE** | Clases, selectores de atributo y pseudoclases | `.card`, `[type="radio"]`, `:hover`, `:nth-child(2)` |
| **TIPO** | Selectores de tipo (elemento) y pseudoelementos | `div`, `p`, `::before` |

El selector universal (`*`) y los combinadores (` `, `>`, `+`, `~`) **no suman nada**. El selector de anidamiento nativo `&`, en cambio, **sí puede sumar especificidad**: no aporta peso por sí mismo, pero toma el peso del selector al que representa (el selector del bloque padre), con una lógica equivalente a envolver ese selector en `:is()`. Volvemos sobre esto un poco más abajo.

```css
li {
  /* 0-0-1 → una columna TIPO */
}

ul li.nav-item {
  /* 0-1-2 → una CLASE, dos TIPO (ul y li) */
}

#sidebar .widget[data-open] {
  /* 1-2-0 → un ID, más una clase y un atributo (ambos van a la columna CLASE, así que suman 2) */
}
```

### Por qué no se suman en un solo número

Como cada columna se compara por separado (primero ID, luego CLASE, luego TIPO), un solo ID siempre gana a cualquier cantidad de clases, y una sola clase siempre gana a cualquier cantidad de selectores de tipo:

```css
.card .card .card .card .card {
  color: blue; /* 0-5-0 */
}

#app {
  color: red; /* 1-0-0 → gana, aunque tenga muchísimas menos "unidades" en total */
}
```

`#app` gana porque su columna ID (1) es mayor que la de la otra regla (0), y ahí termina la comparación: da igual lo que haya en las columnas siguientes.

### Estilos inline

Un estilo puesto directamente en el atributo `style` de un elemento HTML tiene una especificidad tan alta que MDN la describe con una cuarta columna por delante de las otras tres: `1-0-0-0`. En la práctica, un estilo inline gana a cualquier regla de una hoja de estilos, sea cual sea su especificidad:

```html
<p style="color: purple;">Texto</p>
```

```css
#texto-especial p {
  color: green; /* No sirve: el inline (1-0-0-0) siempre gana a esto (1-0-1) */
}
```

Como cada elemento solo tiene un atributo `style`, no hay "otro" estilo inline con el que compita por especificidad: si escribes la misma propiedad dos veces dentro del mismo atributo (`style="color: purple; color: green;"`), simplemente gana la última por orden de escritura dentro de ese bloque de declaraciones, sin que intervenga la cascada. La única forma real de ganarle a un estilo inline **desde una hoja de estilos** es una regla con `!important`, porque `!important` actúa en el paso de **importancia**, que se evalúa antes que la especificidad.

### `:is()`, `:where()`, `:not()` y `:has()`

Estas pseudoclases tienen un tratamiento especial en el cálculo de especificidad:

- `:is()`, `:not()` y `:has()` **no añaden peso por sí mismas**: su especificidad es la del argumento **más específico** que contengan.
- `:where()` es la excepción: su especificidad se sustituye **siempre por cero** (`0-0-0`), sea cual sea su contenido. Es justo lo que la hace tan útil para escribir estilos base fáciles de sobrescribir.

```css
:is(#nav, .menu) a {
  /* La especificidad de :is() es la de su argumento más específico: #nav (1-0-0) */
  /* Total: 1-0-1 */
  color: teal;
}

:where(#nav, .menu) a {
  /* :where() siempre aporta 0-0-0, pase lo que pase dentro */
  /* Total: 0-0-1 */
  color: navy;
}

div:not(.oculto) p {
  /* :not() toma el peso de su argumento (.oculto → 0-1-0), más los dos elementos */
  /* Total: 0-1-2 */
  color: gray;
}
```

El caso de `&` (el selector de anidamiento nativo) sigue una lógica parecida a `:is()` y se explica con más detalle en [Nesting nativo](../moderno/nesting.md).

## El peso de `!important` y por qué evitarlo

`!important` se escribe al final de una declaración, justo antes del punto y coma:

```css
p {
  color: red !important;
}
```

Lo que hace `!important` es **invertir el paso de importancia** en la cascada: una declaración `!important` de origen "autor" pasa a competir en el nivel 5 de la tabla de arriba, muy por encima de cualquier declaración normal del mismo origen (nivel 3), sin importar cuán específico sea su selector. Entre dos declaraciones `!important` del mismo origen y capa, se vuelve a mirar la especificidad y, si hace falta, el orden de aparición. Ojo con un detalle poco intuitivo: `!important` también **invierte el orden de las capas de `@layer`**. En declaraciones normales gana la última capa declarada, pero entre dos `!important` en capas distintas gana la **primera** capa declarada, justo al revés.

Por qué se recomienda evitarlo en la práctica:

- **Rompe la cascada de forma poco visible.** Una regla con `!important` en un archivo CSS puede anular silenciosamente estilos que se escriban después, en otro archivo, sin que nada en ese segundo archivo indique el conflicto.
- **Solo se puede sobrescribir con más `!important`.** Esto genera una escalada: cada `!important` nuevo obliga a otro más específico o posterior para ganarle, y el código se vuelve cada vez más frágil.
- **Dificulta el mantenimiento en equipo.** Cuando `!important` se usa como atajo para "ganar" a una especificidad alta en vez de arreglar la causa (selectores demasiado anidados, orden de carga incorrecto), el problema de fondo sigue ahí.

La alternativa moderna para los casos típicos en los que se recurría a `!important` (por ejemplo, para que tus estilos venzan siempre a los de una librería de terceros) son las [capas de cascada](../moderno/cascade-layers.md): cargas el CSS de terceros en una capa temprana y el tuyo fuera de capa o en una capa posterior, y ganas por reglas de la cascada, no por fuerza bruta.

```css
/* En vez de esto: */
.mi-boton {
  background: teal !important;
}

/* Mejor: controla la precedencia con capas */
@layer libreria, mis-estilos;

@layer libreria {
  .mi-boton {
    background: gray;
  }
}

@layer mis-estilos {
  .mi-boton {
    background: teal; /* Gana sin necesidad de !important */
  }
}
```

Quedan usos razonables de `!important` fuera del control del autor: por ejemplo, estilos de utilidad de un usuario final para accesibilidad, o para sobrescribir estilos inline que genera un script de terceros que no controlas. Pero dentro de tu propio código, trátalo como una señal de alarma, no como una herramienta habitual.

## Herencia: qué pasa cuando no declaras una propiedad

La **herencia** ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/inheritance)) resuelve una pregunta distinta a la de la cascada: no "qué regla gana", sino "qué valor toma una propiedad que **ninguna regla ha fijado** para este elemento". Aquí hay dos comportamientos posibles, y dependen de la propiedad en concreto:

- **Propiedades heredables**: si nadie fija un valor, el elemento toma el **valor computado de su elemento padre**. Son, sobre todo, propiedades relacionadas con el texto: `color`, `font-family`, `font-size`, `line-height`, `text-align`.
- **Propiedades no heredables**: si nadie fija un valor, el elemento usa el **valor inicial** de esa propiedad (el definido por la especificación), ignorando a su padre. Son la mayoría de propiedades de caja: `border`, `margin`, `padding`, `width`, `height`, `background`, `display`.

```css
p {
  color: green;      /* Se hereda */
  border: 1px solid; /* No se hereda */
}
```

```html
<p>Este párrafo tiene <em>texto enfatizado</em>.</p>
```

El `<em>` hereda el `color: green` de su `<p>` padre (por eso el texto enfatizado también se ve verde), pero **no** hereda el borde: como `border` no es una propiedad heredable, el `<em>` usa su valor inicial (`none`), y no muestra ningún borde propio.

Que una propiedad se herede o no lo decide la especificación de esa propiedad, no una regla general que puedas memorizar de un vistazo: cada página de propiedad en MDN indica explícitamente "Inherited: yes" o "Inherited: no" en su ficha técnica. Ante la duda, consúltalo ahí en vez de asumirlo. Un caso particular interesante son las [custom properties](../moderno/custom-properties.md), que se heredan por defecto salvo que se registren explícitamente con un tipo distinto.

## Controlando la herencia a mano: `inherit`, `initial`, `unset`, `revert` y `revert-layer`

CSS ofrece cinco valores especiales ("CSS-wide keywords") que puedes asignar a **cualquier** propiedad para forzar un comportamiento concreto, independientemente de si esa propiedad se hereda o no por defecto:

| Valor | Qué hace |
|---|---|
| [`inherit`](https://developer.mozilla.org/en-US/docs/Web/CSS/inherit) | Fuerza el valor computado del elemento padre, aunque la propiedad no sea heredable por defecto. |
| [`initial`](https://developer.mozilla.org/en-US/docs/Web/CSS/initial) | Aplica el valor inicial que define la especificación CSS para esa propiedad (no el aspecto por defecto del navegador). |
| [`unset`](https://developer.mozilla.org/en-US/docs/Web/CSS/unset) | Actúa como `inherit` si la propiedad se hereda por defecto, o como `initial` si no. |
| [`revert`](https://developer.mozilla.org/en-US/docs/Web/CSS/revert) | Retrocede al valor que tendría la propiedad en el origen anterior de la cascada: la hoja de estilos del usuario si existe, o si no, la hoja del navegador (*user-agent*). |
| [`revert-layer`](https://developer.mozilla.org/en-US/docs/Web/CSS/revert-layer) | Retrocede al valor definido en la **capa de cascada anterior**, dentro del mismo origen. No sale del origen "autor". |

La diferencia entre `initial` y `revert` se entiende mejor con un ejemplo clásico: el peso de la fuente en un `<h1>`. Los navegadores traen, en su hoja de estilos por defecto, una regla aproximada a `h1 { font-weight: bold; }`. Pero el **valor inicial** que define la especificación para `font-weight` es `normal`, no `bold`:

```css
.prueba-initial {
  font-weight: initial; /* → "normal": el valor inicial de la especificación */
}

.prueba-revert {
  font-weight: revert; /* → "bold": el valor que ya traía del user-agent stylesheet para <h1> */
}
```

Es decir: `initial` te lleva al valor por defecto **de la propiedad según la especificación**, mientras que `revert` te lleva al valor que **el navegador** ya había decidido para ese elemento antes de que tu CSS entrara en juego. Por eso, para "deshacer" un estilo y recuperar el aspecto nativo de un elemento, `revert` suele dar resultados más intuitivos que `initial`.

`revert-layer` sigue la misma idea que `revert`, pero limitada a las capas de `@layer`:

```css
@layer base, tema;

@layer base {
  .btn {
    background-color: slateblue;
  }
}

@layer tema {
  .btn {
    background-color: revert-layer; /* Ignora esta capa y usa el valor de "base": slateblue */
  }
}
```

Por último, existe la propiedad abreviada `all`, que aplica cualquiera de estos cinco valores a **todas** las propiedades CSS de un elemento a la vez (excepto `direction`, `unicode-bidi` y las custom properties):

```css
.widget-reseteado {
  all: revert; /* Recupera el aspecto nativo del navegador en todas sus propiedades */
}
```

!!! tip "Soporte de navegadores"
    `inherit`, `initial` y `unset` funcionan en todos los navegadores modernos desde hace años. `revert` y, especialmente, `revert-layer` son más recientes: según MDN, `revert-layer` está ampliamente disponible desde marzo de 2022. Antes de usarlo en un proyecto con soporte a navegadores antiguos, revisa [caniuse.com/mdn-css_types_global_keywords_revert-layer](https://caniuse.com/mdn-css_types_global_keywords_revert-layer) y [caniuse.com/css-cascade-layers](https://caniuse.com/css-cascade-layers).

## Ver también

- [Selectores](selectores.md)
- [Cascade layers (@layer)](../moderno/cascade-layers.md)
- [Selectores modernos (:has, :is, :where)](../moderno/selectores-modernos.md)
- [Custom properties](../moderno/custom-properties.md)

## Fuentes

- [MDN: Introduction to the CSS cascade](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascade/Cascade)
- [MDN: Specificity](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascade/Specificity)
- [MDN: @layer](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@layer)
- [MDN: Inheritance](https://developer.mozilla.org/en-US/docs/Web/CSS/inheritance)
- [MDN: !important](https://developer.mozilla.org/en-US/docs/Web/CSS/important)
- [MDN: inherit](https://developer.mozilla.org/en-US/docs/Web/CSS/inherit)
- [MDN: initial](https://developer.mozilla.org/en-US/docs/Web/CSS/initial)
- [MDN: unset](https://developer.mozilla.org/en-US/docs/Web/CSS/unset)
- [MDN: revert](https://developer.mozilla.org/en-US/docs/Web/CSS/revert)
- [MDN: revert-layer](https://developer.mozilla.org/en-US/docs/Web/CSS/revert-layer)
- [MDN: all](https://developer.mozilla.org/en-US/docs/Web/CSS/all)
- [caniuse: CSS Cascade Layers](https://caniuse.com/css-cascade-layers)
- [caniuse: revert-layer keyword](https://caniuse.com/mdn-css_types_global_keywords_revert-layer)
- [caniuse: CSS unset value](https://caniuse.com/css-unset-value)
