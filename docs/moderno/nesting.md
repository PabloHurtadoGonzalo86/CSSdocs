# CSS Nesting nativo

El *CSS Nesting* (anidamiento nativo de CSS) permite escribir una regla de estilo dentro de otra, de forma que el selector de la regla anidada se resuelve en relación con el selector de la regla que la contiene. Es exactamente el tipo de comodidad que durante más de una década solo ofrecían preprocesadores como Sass o Less, pero ahora la interpreta el propio navegador, sin paso de compilación. Esto importa en un proyecto real porque elimina una dependencia de build solo para agrupar estilos relacionados, y porque lo que ves en el archivo `.css` es exactamente lo que el navegador ejecuta, sin la capa de indirección de un preprocesador.

## Qué es y cómo se procesa

El anidamiento nativo está definido en la especificación [CSS Nesting Module Level 1](https://www.w3.org/TR/css-nesting-1/) del W3C/CSSWG. La idea central: dentro del bloque de una regla de estilo puedes escribir otras reglas de estilo completas (selector + declaraciones), y esas reglas anidadas se combinan con el selector "padre" en el momento en que el navegador parsea el CSS.

```css
.card {
  background-color: white;
  padding: 1rem;
  border-radius: 0.5rem;

  .card__title {
    font-size: 1.25rem;
    font-weight: 600;
  }
}
```

El navegador interpreta este bloque exactamente igual que si hubieras escrito:

```css
.card {
  background-color: white;
  padding: 1rem;
  border-radius: 0.5rem;
}

.card .card__title {
  font-size: 1.25rem;
  font-weight: 600;
}
```

No hay ninguna transformación de cadenas de texto ni generación de clases nuevas: `.card__title` sigue siendo el selector literal `.card__title`, simplemente el navegador le antepone un combinador descendiente (`.card .card__title`) porque no encontró nada que le indicara otra relación. Esta es la clave para entender todo lo demás en esta página: **el anidamiento define selectores relativos al padre, no genera texto nuevo**.

!!! tip "Soporte de navegadores"
    El anidamiento nativo de CSS es, según [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/Nesting_selector), *Baseline: Widely available*, disponible en todos los navegadores principales desde diciembre de 2023 (Chrome/Edge 120, Firefox 117, Safari 17.2). Para el detalle completo de versiones consulta [caniuse.com/css-nesting](https://caniuse.com/css-nesting). Más abajo hay una precisión importante sobre cómo cambió la sintaxis entre las primeras versiones (Chrome 112–119, Safari 16.5–17.1) y la versión final.

## El selector `&` (nesting selector)

El símbolo `&` es el **selector de anidamiento**: representa explícitamente los elementos que coinciden con el selector (o la lista de selectores) de la regla padre. Es la pieza que te permite construir selectores compuestos —sin espacio— entre el padre y el hijo, algo que la anidación implícita por sí sola no puede hacer.

```css
.button {
  background-color: royalblue;
  color: white;

  &:hover,
  &:focus-visible {
    background-color: darkblue;
  }

  &.is-disabled {
    background-color: gainsboro;
    color: gray;
  }

  &::before {
    content: "→ ";
  }
}
```

Esto equivale a:

```css
.button { background-color: royalblue; color: white; }
.button:hover,
.button:focus-visible { background-color: darkblue; }
.button.is-disabled { background-color: gainsboro; color: gray; }
.button::before { content: "→ "; }
```

Fíjate en que en los tres primeros casos `&` se pega directamente al resto del selector, sin espacio: eso es justo lo que forma un selector compuesto (mismo elemento), en contraste con el espacio que el navegador inserta automáticamente cuando no hay `&` (ver la siguiente sección).

### `&` también sirve para "invertir" el contexto

Como `&` es un selector real (no una simple marca de posición), puedes usarlo en cualquier parte de un selector complejo, incluido el principio, para expresar "cuando este componente está dentro de un ancestro concreto":

```css
.card {
  border: 1px solid gainsboro;

  .featured & {
    /* equivalente a: .featured .card */
    border-color: goldenrod;
  }
}
```

Aquí `.card` no cambia su propio color de borde salvo cuando aparece dentro de un elemento con la clase `.featured`. Esto sería mucho más incómodo de expresar sin nesting, porque tendrías que salir del bloque de `.card` y escribir una regla completamente aparte.

### Especificidad de `&`: como `:is()`, no como cero

Según la propia especificación, *"la especificidad del selector de anidamiento es igual a la especificidad más alta entre los selectores complejos de la lista de selectores de la regla padre (idéntico al comportamiento de [`:is()`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:is))"*. Esto significa que `&` **no aporta una especificidad fija ni nula**: adquiere el peso del selector (o selectores) al que representa.

```css
#sidebar, .widget {
  color: black;

  & a {
    /* la especificidad de "&" aquí es la más alta entre #sidebar (1-0-0) y .widget (0-1-0) */
    /* así que "& a" pesa como "#sidebar a": 1-0-1 */
    color: teal;
  }
}
```

Esto es coherente con cómo se explica la especificidad de `:is()` en [Cascada, herencia y especificidad](../fundamentos/cascada-especificidad-herencia.md): `&`, al igual que `:is()`, toma el peso del argumento más específico, no lo ignora y no lo suma aparte.

Cuando la regla padre tiene varios selectores separados por coma (como en el ejemplo anterior), `&` los representa a todos a la vez, de forma parecida a como lo haría `:is(#sidebar, .widget) a`. Es una forma cómoda de evitar repetir un bloque completo de declaraciones para cada selector de una lista.

## Cuándo hace falta `&` explícito (y cuándo no)

Esta es la parte que más confunde a quien viene de Sass, así que conviene una regla precisa. Según [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/Nesting_selector):

> Si un selector anidado **no** empieza con un combinador explícito (` `, `>`, `+`, `~`) y **no** usa `&`, el navegador inserta automáticamente un espacio (combinador descendiente) entre el contexto del padre y ese selector.

Esta regla se aplica igual sin importar con qué tipo de selector empiece la regla anidada (clase, id, atributo, tipo de elemento o pseudo-clase):

```css
.notice {
  padding: 1rem;

  .notice-icon {
    /* sin & → se interpreta como: .notice .notice-icon (descendiente) */
    margin-inline-end: 0.5rem;
  }

  strong {
    /* sin & → se interpreta como: .notice strong (descendiente) */
    font-weight: 700;
  }
}
```

Así que, en la práctica, **no necesitas `&` para el caso más habitual**: un elemento descendiente normal se escribe igual que lo escribirías fuera del nesting, solo que sin repetir `.notice`.

### El caso que sí te puede sorprender: pseudo-clases y pseudo-elementos sueltos

El problema aparece cuando quieres que el selector anidado se aplique **al propio elemento padre**, no a un descendiente. Ahí, omitir `&` no da un error de sintaxis: da un selector válido, pero con un significado distinto (y casi siempre no deseado). El propio [borrador de la especificación](https://drafts.csswg.org/css-nesting-1/) lo ilustra con este ejemplo clásico:

```css
a {
  color: blue;

  &:hover {
    color: lightblue; /* equivale a: a:hover */
  }
}
```

Si quitas el `&`:

```css
a {
  color: blue;

  :hover {
    color: lightblue; /* equivale a: a :hover  (¡con espacio!) */
  }
}
```

`a :hover` no selecciona el enlace en hover: selecciona **cualquier descendiente del enlace** que esté en estado `:hover`. Es sintácticamente válido, se aplica sin avisos, y produce un resultado que casi nunca es el que querías. Por eso, aunque la regla general diga que `&` es "opcional", en la práctica **es obligatorio siempre que quieras combinar algo con el propio elemento padre**: otra clase, un atributo, una pseudo-clase o un pseudo-elemento.

```css
.notice {
  &.is-warning {
    /* equivale a: .notice.is-warning (mismo elemento) */
    border-color: darkorange;
  }

  &::before {
    /* equivale a: .notice::before */
    content: "ⓘ";
  }
}
```

### Selectores de tipo combinados con `&`: el orden importa

En cualquier selector compuesto de CSS, si hay un selector de tipo (nombre de elemento), este **debe ir en primer lugar**. Esto no es una regla especial de nesting, es una regla general de los selectores CSS que el nesting hereda: por eso `&Element` es inválido y hay que escribir `Element&`.

```css
.card {
  /* ✗ inválido: el selector de tipo no puede ir después de & */
  /* &article { } */

  /* ✓ válido: el tipo va primero, formando el compuesto article.card */
  article& {
    display: block;
  }
}
```

### Resumen en una tabla

| Situación | ¿Hace falta `&`? | Resultado |
|---|---|---|
| Selector anidado empieza con `>`, `+`, `~` | No | Combinador explícito respetado, relativo al padre |
| Selector anidado empieza con clase, id, atributo, tipo o pseudo-clase, sin combinador | No es obligatorio, pero cambia el significado si tu intención era el mismo elemento | Se inserta un descendiente implícito (`.padre .hijo`) |
| Quieres combinar con el padre en el **mismo elemento** (otra clase, pseudo-clase, pseudo-elemento, atributo) | Sí, obligatorio | Selector compuesto (`.padre.hijo`, `.padre:hover`, `.padre::before`) |
| Quieres combinar `&` con un selector de tipo | Sí, y debe ir **después** del tipo | `Element&`, nunca `&Element` |
| Quieres invertir el contexto (ancestro en vez de descendiente) | Sí, obligatorio | `.ancestro &` |

!!! warning "Historia: no siempre fue tan permisivo"
    Las primeras implementaciones (Chrome 112–119 y Safari 16.5–17.1) exigían `&` incluso para anidar un simple selector de tipo, por ejemplo `& h2` en vez de `h2` a secas, porque el motor de parseo no sabía distinguir de antemano un selector de tipo de una declaración. Chrome resolvió esto con una estrategia de "reintento": si el parser no logra interpretar el contenido como una propiedad, reinicia asumiendo que es un selector. Esta sintaxis "relajada" (*relaxed syntax*) llegó a Chrome/Edge 120, y Firefox 117 y Safari 17.2 la soportaron desde su primera versión con nesting. Si ves tutoriales o código de 2023 con `& h2` donde hoy bastaría `h2`, es un resto de esa etapa inicial. Detalle completo en el [blog de Chrome for Developers](https://developer.chrome.com/blog/css-nesting-relaxed-syntax-update).

## Anidar at-rules (`@media`, `@supports`, `@layer`...)

El nesting no se limita a selectores: también puedes anidar *at-rules* completas —`@media`, `@supports`, `@container`, `@layer`, `@scope`, `@starting-style`— dentro de una regla de estilo. Las declaraciones dentro de la at-rule anidada se comportan como si estuvieran envueltas en un bloque `& { }` implícito:

```css
.sidebar {
  display: block;

  @media (width >= 768px) {
    display: grid;
    grid-template-columns: 240px 1fr;
  }
}
```

Esto equivale, sin anidamiento, a:

```css
.sidebar {
  display: block;
}

@media (width >= 768px) {
  .sidebar {
    display: grid;
    grid-template-columns: 240px 1fr;
  }
}
```

Puedes seguir anidando selectores (con o sin `&`) dentro de la at-rule anidada, y anidar at-rules dentro de otras at-rules:

```css
.sidebar {
  @media (width >= 768px) {
    &:hover {
      background-color: whitesmoke;
    }
  }
}
```

!!! warning "El orden de las declaraciones ahora puede importar"
    Antes de que existiera el nesting, dentro de una misma regla el orden entre declaraciones normales nunca importaba para la cascada salvo en caso de empate de especificidad, porque todas competían igual. Con nesting, si intercalas declaraciones sueltas **antes y después** de una regla o at-rule anidada, el navegador respeta el **orden de aparición en el código fuente** para decidir cuál gana en caso de empate:

    ```css
    .foo {
      background-color: silver;
      @media screen {
        color: tomato;
      }
      color: black; /* esta gana sobre "tomato", por ir después en el código */
    }
    ```

    MDN documenta que, para preservar este orden, el CSSOM envuelve las declaraciones sueltas que aparecen **después** de una regla anidada en una interfaz especial llamada [`CSSNestedDeclarations`](https://developer.mozilla.org/en-US/docs/Web/API/CSSNestedDeclarations). MDN advierte además que los navegadores que no implementan esta interfaz "pueden parsear las reglas anidadas en el orden equivocado". En la práctica: evita intercalar declaraciones sueltas antes y después de un bloque anidado si quieres que el resultado sea inequívoco a simple vista.

Hay un límite adicional que merece la pena conocer: `&` no puede representar un pseudo-elemento (la misma limitación que tiene `:is()`). Por tanto, si el selector del padre incluye un pseudo-elemento, una at-rule anidada dentro de esa regla **no llega a aplicarse**, porque el `&` implícito que la envuelve no puede "ser" ese pseudo-elemento:

```css
.foo::before {
  content: "Hola";

  @media (width < 600px) {
    color: red; /* No se aplica: & no puede representar a ::before */
  }
}
```

## Diferencias con el anidamiento de Sass o Less

El anidamiento de Sass (y el muy similar de Less) inspiró directamente esta característica de CSS, pero no son equivalentes. Estas son las diferencias que de verdad importan al migrar código:

| Aspecto | CSS Nesting nativo | Sass / Less |
|---|---|---|
| Cuándo se procesa | En el navegador, al parsear el CSS | En el build, antes de que el navegador vea el CSS |
| Qué ves en DevTools | El CSS real que escribiste, tal cual | CSS ya "aplanado"; el original con `&` no existe en tiempo de ejecución |
| Espacio automático sin `&` | Sí, con reglas idénticas para clases, ids, tipos y pseudo-clases | Sí, comportamiento equivalente (por eso `&:hover` también es necesario en Sass/Less para evitar `a :hover`) |
| Concatenar texto con `&` (BEM: `&__elemento`, `&--modificador`) | **No es posible**: `&` es un selector, no una cadena de texto | Sí: `&` se sustituye textualmente, así que puede pegarse a cualquier cadena |
| Anidar propiedades relacionadas (`font: { size: ...; weight: ...; }`) | No existe en CSS nativo | Sí, es una característica propia de Sass |
| Especificidad de `&` | Calculada como `:is()`: toma el peso del selector más específico del padre | No aplica: es sustitución de texto, la especificidad resultante es la del selector final ya "aplanado" |

La diferencia que más suele doler en una migración es la de la concatenación de texto. En Sass, este patrón (típico de la metodología BEM) es habitual:

```scss
// Sass — esto SÍ funciona
.component {
  &__title {
    font-weight: 600;
  }
  &--active {
    border-color: seagreen;
  }
}
// Compila a: .component__title { ... }  y  .component--active { ... }
```

En CSS nativo esto no tiene equivalente directo, porque el nesting **no es una transformación de sintaxis: hace coincidir elementos reales que ya cumplen el selector del padre**, no genera identificadores nuevos concatenando cadenas. Escribir `&__title` tampoco produce un error silencioso "que no hace nada": es directamente un selector inválido (un selector de tipo no puede ir después de `&`, como se explicó más arriba), así que toda la regla se descarta.

```css
/* CSS nativo — esto NO funciona: &__title es un selector inválido */
.component {
  &__title {
    font-weight: 600;
  }
}
```

Si vienes de BEM y quieres nesting nativo, la alternativa es escribir el nombre completo de la clase, o apoyarte en una clase modificadora que sí sea un selector compuesto real (`&.is-active`, que sí es válido porque `.is-active` es una clase independiente, no un fragmento de cadena):

```css
.component {
  &.is-active {
    /* equivale a: .component.is-active */
    border-color: seagreen;
  }
}
```

## Ver también

- [Selectores modernos (:has, :is, :where)](selectores-modernos.md)
- [Cascade layers (@layer)](cascade-layers.md)
- [Cascada, especificidad y herencia](../fundamentos/cascada-especificidad-herencia.md)
- [Selectores en CSS](../fundamentos/selectores.md)

## Fuentes

- [MDN: CSS nesting (guía general)](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Nesting)
- [MDN: Using CSS nesting](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Nesting/Using)
- [MDN: & nesting selector](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/Nesting_selector)
- [MDN: CSS nesting at-rules](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_nesting/Nesting_at-rules)
- [MDN: CSSNestedDeclarations](https://developer.mozilla.org/en-US/docs/Web/API/CSSNestedDeclarations)
- [MDN: :is()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:is)
- [W3C: CSS Nesting Module Level 1](https://www.w3.org/TR/css-nesting-1/)
- [CSSWG Editor's Draft: CSS Nesting Module Level 1](https://drafts.csswg.org/css-nesting-1/)
- [Chrome for Developers: CSS nesting relaxed syntax update](https://developer.chrome.com/blog/css-nesting-relaxed-syntax-update)
- [Sass: Parent selector (&), incluida la concatenación para BEM](https://sass-lang.com/documentation/style-rules/parent-selector/)
- [Less: Parent selectors (&)](https://lesscss.org/features/#parent-selectors-feature)
- [caniuse: CSS Nesting](https://caniuse.com/css-nesting)
