# Cheatsheet: Selectores CSS

Chuleta de referencia rápida con los selectores más usados en CSS: qué sintaxis tienen y qué eligen del DOM, en una línea por selector. Está pensada para consultarla mientras escribes CSS —sin explicaciones largas—, no para aprender el modelo desde cero: si necesitas entender el *por qué* detrás de cada uno (especificidad, combinadores, listas "perdonadoras"...), la [guía completa de selectores](../fundamentos/selectores.md) y la de [selectores modernos](../moderno/selectores-modernos.md) cubren eso en profundidad.

## Selectores básicos

| Selector | Ejemplo | Selecciona |
|---|---|---|
| Universal | `*` | Todos los elementos del documento (especificidad nula) |
| Tipo (etiqueta) | `p` | Todos los elementos `<p>` |
| Clase | `.card` | Todos los elementos cuyo atributo `class` incluye `card` |
| ID | `#main-nav` | El único elemento con `id="main-nav"` |
| Compuesto (sin espacio) | `.card.destacada` | Elementos que tienen **ambas** clases a la vez |
| Agrupación (coma) | `h1, h2, h3` | Cualquier elemento que coincida con alguno de los selectores de la lista |

## Selectores de atributo

| Selector | Ejemplo | Selecciona |
|---|---|---|
| `[attr]` | `a[title]` | Elementos que tienen ese atributo, sea cual sea su valor |
| `[attr=valor]` | `input[type="email"]` | El valor del atributo es exactamente ese |
| `[attr~=valor]` | `[class~="destacado"]` | El atributo contiene esa palabra dentro de una lista separada por espacios |
| `[attr\|=valor]` | `[lang\|="es"]` | El valor es exactamente ese, o empieza por ese valor seguido de un guion (`es`, `es-MX`) |
| `[attr^=valor]` | `a[href^="https://"]` | El valor del atributo **empieza por** ese texto |
| `[attr$=valor]` | `a[href$=".pdf"]` | El valor del atributo **termina en** ese texto |
| `[attr*=valor]` | `a[href*="ejemplo.com"]` | El valor del atributo **contiene** ese texto en cualquier posición |
| `[attr=valor i]` | `a[href*="pdf" i]` | Igual que la variante sin `i`, pero comparando sin distinguir mayúsculas/minúsculas |

```css
/* Enlaces externos que apuntan a un PDF, sin distinguir mayúsculas en la extensión */
a[href^="http"][href$=".pdf" i] {
  padding-left: 1.5em;
  background: url("icon-pdf.svg") left center no-repeat;
}
```

Encadenar varios selectores de atributo (sin espacio entre ellos) exige que el elemento cumpla **todas** las condiciones a la vez, igual que ocurre al encadenar clases.

!!! tip "Soporte de navegadores"

    Los selectores de atributo básicos tienen soporte universal desde hace años. El modificador de sensibilidad **`i`** (comparar sin distinguir mayúsculas/minúsculas) también tiene soporte amplio: [css-case-insensitive en caniuse.com](https://caniuse.com/css-case-insensitive). Su opuesto, **`s`** (forzar comparación sensible a mayúsculas/minúsculas incluso si el atributo es case-insensitive por HTML), tiene soporte mucho más limitado: hoy en día solo lo implementa Firefox, así que no lo uses en producción a menos que confirmes soporte para tu caso: [entrada en caniuse.com](https://caniuse.com/mdn-css_selectors_attribute_case_sensitive_modifier). Recuerda además que, si un navegador no reconoce el modificador que escribas, toda la regla del selector se invalida y no se aplica.

## Combinadores

| Combinador | Ejemplo | Selecciona |
|---|---|---|
| Descendiente (espacio) | `article p` | Cualquier `<p>` dentro de `<article>`, a cualquier profundidad |
| Hijo directo (`>`) | `.menu > li` | Solo los `<li>` que son hijos **inmediatos** de `.menu` |
| Hermano adyacente (`+`) | `h2 + p` | El `<p>` que viene justo después de un `<h2>` (mismo padre) |
| Hermano general (`~`) | `h2 ~ p` | Todos los `<p>` posteriores a un `<h2>` dentro del mismo padre |

## Pseudo-clases estructurales

| Pseudo-clase | Ejemplo | Selecciona |
|---|---|---|
| `:first-child` | `li:first-child` | El elemento que es el primer hijo de su padre |
| `:last-child` | `li:last-child` | El elemento que es el último hijo de su padre |
| `:only-child` | `p:only-child` | Un elemento que es hijo único de su padre |
| `:nth-child(An+B)` | `tr:nth-child(odd)` | Elementos en las posiciones impares, contando entre **todos** los hermanos |
| `:nth-last-child(An+B)` | `li:nth-last-child(2)` | Igual que `:nth-child()`, pero contando desde el último hijo hacia atrás |
| `:nth-child(An+B of S)` | `li:nth-child(1 of .destacado)` | El primer hermano que además cumple el selector `S`, contando la posición solo entre los que lo cumplen |
| `:first-of-type` | `p:first-of-type` | El primer hermano de su mismo tipo de etiqueta |
| `:last-of-type` | `p:last-of-type` | El último hermano de su mismo tipo de etiqueta |
| `:nth-of-type(An+B)` | `p:nth-of-type(2)` | Cuenta la posición solo entre hermanos del **mismo tipo** de etiqueta |
| `:only-of-type` | `img:only-of-type` | Único hermano de su tipo dentro de su padre |
| `:empty` | `p:empty` | Elemento sin hijos ni contenido de texto (ni siquiera espacios en blanco) |
| `:root` | `:root` | El elemento raíz del documento (`<html>` en HTML) |

!!! tip "Soporte de navegadores"

    La cláusula `of <selector>` en `:nth-child()`/`:nth-last-child()` es la incorporación más reciente de este grupo: tiene ya soporte amplio (Chrome/Edge 111+, Firefox 113+, Safari), pero conviene comprobarlo si tu proyecto da soporte a versiones antiguas en [css-nth-child-of en caniuse.com](https://caniuse.com/css-nth-child-of).

## Pseudo-clases de estado, interacción y formulario

| Pseudo-clase | Ejemplo | Selecciona |
|---|---|---|
| `:hover` | `a:hover` | Mientras el puntero está sobre el elemento |
| `:focus` | `input:focus` | Mientras el elemento tiene el foco, sin importar cómo lo obtuvo |
| `:focus-visible` | `button:focus-visible` | El elemento enfocado, solo cuando el navegador estima que ese foco debe mostrarse visualmente |
| `:focus-within` | `form:focus-within` | Un elemento cuando él mismo o alguno de sus descendientes tiene el foco |
| `:active` | `button:active` | Mientras el elemento está siendo activado (p. ej. clic sostenido) |
| `:link` | `a:link` | Enlaces (con `href`) todavía no visitados |
| `:visited` | `a:visited` | Enlaces ya visitados |
| `:target` | `#seccion:target` | El elemento cuyo `id` coincide con el fragmento (`#...`) de la URL actual |
| `:checked` | `input:checked` | Checkbox, radio o `<option>` marcado/seleccionado |
| `:indeterminate` | `input:indeterminate` | Checkbox con la propiedad `indeterminate` puesta a `true` por JavaScript, grupo de radios donde ninguno está marcado, o `<progress>` sin valor definido |
| `:disabled` | `button:disabled` | Elemento de formulario deshabilitado |
| `:enabled` | `button:enabled` | Elemento de formulario habilitado (opuesto a `:disabled`) |
| `:required` | `input:required` | Campo de formulario marcado como obligatorio |
| `:optional` | `input:optional` | Campo de formulario sin el atributo `required` |
| `:valid` | `input:valid` | Campo cuyo valor cumple sus reglas de validación |
| `:invalid` | `input:invalid` | Campo cuyo valor no cumple sus reglas de validación |
| `:placeholder-shown` | `input:placeholder-shown` | Input que está mostrando su texto de `placeholder` (campo vacío) |
| `:read-only` | `input:read-only` | Elemento que el usuario no puede editar |
| `:read-write` | `[contenteditable]:read-write` | Elemento editable por el usuario |
| `:default` | `input:default` | Control marcado por defecto en su grupo (checkbox/radio con `checked` en el HTML, opción por defecto de un `<select>`, o el botón que actúa como envío por defecto de un formulario) |
| `:in-range` | `input:in-range` | Input con límites `min`/`max` (`number`, `range`, `date`, `month`, `week`, `time`...) cuyo valor está dentro de ellos |
| `:out-of-range` | `input:out-of-range` | Igual que `:in-range`, pero cuyo valor está fuera de `min`/`max` |

!!! tip "Soporte de navegadores"

    `:focus-visible` es *Baseline: Widely available* desde marzo de 2022; consulta [css-focus-visible en caniuse.com](https://caniuse.com/css-focus-visible) si necesitas dar soporte a navegadores más antiguos. El resto de pseudo-clases de esta tabla llevan más tiempo estabilizadas y tienen soporte prácticamente universal en navegadores actuales.

## Negación y selectores lógicos/relacionales modernos

| Selector | Ejemplo | Selecciona |
|---|---|---|
| `:not(S)` | `button:not(:disabled)` | Elementos que **no** coinciden con el selector (o lista de selectores) `S` |
| `:is(S1, S2, ...)` | `:is(h1, h2, h3)` | Cualquier elemento que coincida con alguno de los selectores de la lista; toma la especificidad del **más específico** de ellos |
| `:where(S1, S2, ...)` | `:where(h1, h2, h3)` | Igual que `:is()`, pero con especificidad **siempre igual a cero** |
| `:has(S)` | `section:has(img)` | El elemento si contiene (o va seguido de, según el selector relativo dentro del paréntesis) algo que coincide con `S` |

```css
/* :is() como atajo: aplica el mismo margen a varios encabezados sin repetir la regla */
:is(h1, h2, h3) {
  margin-block: 0.5em;
}

/* :where() para estilos "base" de baja prioridad, fáciles de sobrescribir después */
:where(section, article, aside) a {
  color: teal; /* especificidad 0 + tipo: cualquier "a { color }" posterior gana */
}

/* :has() como "selector de padre": resalta una tarjeta que contiene una imagen sin alt */
.card:has(img[alt=""]) {
  outline: 2px dashed crimson;
}
```

`:is()`, `:where()` y `:not()` con lista de selectores crean **listas perdonadoras** (*forgiving selector list*): si uno de los selectores dentro del paréntesis no es válido o no tiene soporte, el navegador lo ignora y sigue aplicando el resto, en vez de descartar toda la regla como ocurre con una lista agrupada por comas normal.

!!! tip "Soporte de navegadores"

    `:is()` y `:where()` son *Baseline: Widely available* desde enero de 2021 — consulta [css-matches-pseudo en caniuse.com](https://caniuse.com/css-matches-pseudo) (la entrada conserva el nombre histórico `:matches()`) y [css-where en caniuse.com](https://caniuse.com/css-where). `:has()` es *Baseline: Widely available* desde diciembre de 2023: revisa [css-has en caniuse.com](https://caniuse.com/css-has) si tu proyecto necesita soporte más amplio, y ten en cuenta que anclar `:has()` a selectores muy generales (`body:has(...)`, `:root:has(...)`) puede ser costoso en rendimiento porque obliga a re-evaluar el árbol entero.

## Pseudo-elementos

| Pseudo-elemento | Ejemplo | Selecciona |
|---|---|---|
| `::before` | `.tooltip::before` | Contenido generado justo antes del contenido real del elemento (requiere la propiedad `content`) |
| `::after` | `a[href^="http"]::after` | Contenido generado justo después del contenido real del elemento (requiere `content`) |
| `::first-line` | `p::first-line` | La primera línea *renderizada* del texto de un bloque (depende del ancho del contenedor) |
| `::first-letter` | `p::first-letter` | La primera letra del texto de un bloque (útil para el efecto de letra capital) |
| `::marker` | `li::marker` | La caja del marcador de un elemento de lista (la viñeta o el número) |
| `::placeholder` | `input::placeholder` | El texto de marcador de posición de un `<input>`/`<textarea>` |
| `::selection` | `::selection` | La porción de texto que el usuario tiene actualmente seleccionada |

!!! tip "Soporte de navegadores"

    `::placeholder` es *Baseline: Widely available* desde enero de 2020. `::marker` tiene soporte completo en Chrome, Edge y Firefox, pero solo **parcial** en Safari (algunas propiedades, como `content` para reemplazar el marcador, no se aplican igual): revisa [css-marker-pseudo en caniuse.com](https://caniuse.com/css-marker-pseudo) antes de depender de él para algo más que color o tamaño. `::selection` no es *Baseline* según MDN por diferencias de soporte entre navegadores para algunas propiedades: comprueba el detalle en [css-selection en caniuse.com](https://caniuse.com/css-selection).

## Ver también

- [Selectores: guía completa](../fundamentos/selectores.md)
- [Selectores modernos (:has, :is, :where)](../moderno/selectores-modernos.md)
- [Cascada, especificidad y herencia](../fundamentos/cascada-especificidad-herencia.md)
- [Cheatsheet: Flexbox](flexbox-cheatsheet.md)

## Fuentes

- [MDN: CSS selectors](https://developer.mozilla.org/es/docs/Web/CSS/CSS_selectors)
- [MDN: Selectores de atributo](https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors)
- [MDN: Pseudo-elementos](https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-elements)
- [MDN: :nth-child()](https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-child)
- [MDN: :nth-of-type()](https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-of-type)
- [MDN: :not()](https://developer.mozilla.org/en-US/docs/Web/CSS/:not)
- [MDN: :is()](https://developer.mozilla.org/en-US/docs/Web/CSS/:is)
- [MDN: :where()](https://developer.mozilla.org/en-US/docs/Web/CSS/:where)
- [MDN: :has()](https://developer.mozilla.org/en-US/docs/Web/CSS/:has)
- [MDN: :focus-visible](https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible)
- [MDN: ::marker](https://developer.mozilla.org/en-US/docs/Web/CSS/::marker)
- [MDN: ::placeholder](https://developer.mozilla.org/en-US/docs/Web/CSS/::placeholder)
- [MDN: ::selection](https://developer.mozilla.org/en-US/docs/Web/CSS/::selection)
- [W3C: Selectors Level 4](https://drafts.csswg.org/selectors/)
- [caniuse: Case-insensitive CSS attribute selectors](https://caniuse.com/css-case-insensitive)
- [caniuse: Case-sensitive attribute selector modifier](https://caniuse.com/mdn-css_selectors_attribute_case_sensitive_modifier)
- [caniuse: selector list argument of :nth-child and :nth-last-child](https://caniuse.com/css-nth-child-of)
- [caniuse: :focus-visible](https://caniuse.com/css-focus-visible)
- [caniuse: :is() / :matches()](https://caniuse.com/css-matches-pseudo)
- [caniuse: :where()](https://caniuse.com/css-where)
- [caniuse: :has()](https://caniuse.com/css-has)
- [caniuse: ::marker](https://caniuse.com/css-marker-pseudo)
- [caniuse: ::selection](https://caniuse.com/css-selection)
