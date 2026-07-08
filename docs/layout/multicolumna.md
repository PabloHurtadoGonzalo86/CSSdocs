# Layout multi-columna

El layout multi-columna (CSS Multi-column Layout, también conocido como "multicol") permite repartir un bloque de contenido en varias columnas, al estilo de un periódico o una revista, sin tocar el HTML ni recurrir a `float` o divs artificiales. Es la herramienta correcta cuando el problema real es tipográfico: líneas de texto demasiado largas son difíciles de seguir con la vista, y multicol te deja acotar el ancho de línea en pantallas grandes reflowando automáticamente el mismo contenido en dos, tres o más columnas.

## El problema que resuelve

Un párrafo de texto que ocupa todo el ancho de una pantalla de escritorio suele tener líneas demasiado largas: el ojo tarda en volver al principio de la siguiente línea y es fácil perder el sitio de lectura. La solución tradicional en papel impreso —y ahora también en CSS— es dividir el contenido en columnas más estrechas, como hacen los periódicos. La diferencia frente a maquetar "a mano" con varios `<div>` es que multicol reparte automáticamente **el mismo flujo de contenido** entre las columnas que hagan falta: no defines tú qué párrafo va en cada columna, el navegador decide dónde cortar según el espacio disponible.

```css
.articulo {
  column-width: 20em;
}
```

Con esta única línea, el navegador crea tantas columnas de al menos `20em` de ancho como quepan en el contenedor, y las recalcula solas si la ventana cambia de tamaño. Sin media queries.

## `column-count`: número de columnas

`column-count` fija el número de columnas que quieres, dejando que el navegador calcule el ancho de cada una repartiendo el espacio disponible.

```css
column-count: auto | <integer>
```

- Valor inicial: `auto` (el número de columnas lo decide `column-width` u otra propiedad).
- Un `<integer>` debe ser estrictamente positivo (1 o más).
- No es una propiedad heredada.

```css
.articulo {
  column-count: 3;
}
```

Aquí siempre habrá 3 columnas, sea cual sea el ancho del contenedor; lo que varía es el ancho de cada columna. Si el contenedor es muy estrecho, las columnas pueden llegar a ser incómodamente angostas, porque `column-count` por sí solo no impone un ancho mínimo.

## `column-width`: ancho mínimo de columna

`column-width` funciona al revés: en lugar de fijar cuántas columnas quieres, fijas cuál es el **ancho mínimo** que debe tener cada una, y el navegador decide cuántas columnas de ese ancho (o más) caben en el contenedor.

```css
column-width: auto | <length>
```

- Valor inicial: `auto`.
- Acepta cualquier `<length>` estrictamente positiva (`em`, `rem`, `px`, etc.); a diferencia de `column-gap`, el valor `0` no es válido aquí y invalida la declaración.

```css
.articulo {
  column-width: 15em;
}
```

Este es el patrón más habitual para "columnas responsivas sin media queries": a medida que el contenedor se ensancha o se estrecha, el número de columnas sube o baja solo, siempre respetando que ninguna sea más estrecha que `15em` (salvo que el propio contenedor sea más estrecho que ese valor, en cuyo caso queda una sola columna más angosta).

## `columns`: el atajo

`columns` es el shorthand que combina `column-width` y `column-count` en una sola declaración, en cualquier orden. Estas tres líneas son formas alternativas de usarlo (en una regla real declararías solo una; aquí se muestran juntas a modo de referencia, y si aparecieran así en la misma regla, solo la última se aplicaría, porque las tres son la misma propiedad):

```css
/* Opción 1: solo column-count */
.articulo-a { columns: 3; }

/* Opción 2: solo column-width */
.articulo-b { columns: 15em; }

/* Opción 3: ambos, column-count y column-width */
.articulo-c { columns: 3 15em; }
```

### Qué pasa cuando declaras los dos a la vez

Esta es la parte que más confunde: cuando `column-count` y `column-width` tienen ambos un valor distinto de `auto`, **ninguno de los dos "gana" por sí solo**. El número de columnas que se usa realmente es el **menor** de estos dos límites:

1. El valor de `column-count`.
2. Cuántas columnas de al menos `column-width` de ancho caben en el contenedor.

```css
.caja-ancha {
  width: 1000px;
  columns: 3 200px;
  column-gap: 0; /* para que la cuenta sea exacta en el ejemplo */
  /* caben 5 columnas de 200px en 1000px, pero column-count limita a 3.
     Se usan 3 columnas, y cada una crece hasta ~333px para llenar el espacio. */
}

.caja-estrecha {
  width: 500px;
  columns: 3 200px;
  column-gap: 0; /* para que la cuenta sea exacta en el ejemplo */
  /* en 500px solo caben 2 columnas de 200px como mínimo.
     column-width gana aquí: se usan 2 columnas, no 3. */
}
```

(En ambos ejemplos se fija `column-gap: 0` solo para que la aritmética del comentario sea exacta; con el `column-gap` por defecto de `1em`, el hueco entre columnas también cuenta en el cálculo y el número de columnas que "caben" por ancho puede ser ligeramente menor.)

En la práctica, esto hace que `columns: 3 15em` se lea como "hasta 3 columnas, pero nunca más estrechas de 15em": es una forma de poner un tope superior de columnas a un layout que, por lo demás, se comporta como `column-width`.

!!! tip "Soporte de navegadores"

    El soporte base de `column-count`, `column-width` y el atajo `columns` es amplio en todos los navegadores modernos (Chrome, Firefox, Safari, Edge). Aun así, ningún navegador implementa el 100 % de los casos límite de la especificación al pie de la letra (por ejemplo, el equilibrado de alturas de columna varía ligeramente entre motores), así que conviene probar el resultado visual en varios navegadores si el diseño depende de un número exacto de columnas. Consulta el detalle en [caniuse.com/multicolumn](https://caniuse.com/multicolumn).

## `column-gap`: espacio entre columnas

`column-gap` controla la separación entre columnas contiguas. Es la misma propiedad que usas en Flexbox y Grid: su definición vive hoy en el módulo CSS Gaps (que junto con `row-gap` unifica lo que originalmente especificaba CSS Box Alignment), y por eso también puedes escribirla como parte del shorthand `gap`.

```css
column-gap: normal | <length-percentage>
```

- Valor inicial: `normal`, que en un contenedor multi-columna se resuelve como `1em`.
- No admite valores negativos.

```css
.articulo {
  columns: 3 15em;
  column-gap: 2rem; /* separa más las columnas que el 1em por defecto */
}
```

Si prefieres el shorthand unificado, `gap: <row-gap> <column-gap>` también funciona aquí, aunque en un contexto multicol solo tiene sentido el segundo valor (no hay filas que separar).

## `column-rule`: la línea divisoria

`column-rule` dibuja una línea vertical entre columnas, muy parecida visualmente a un `border`, pero con una diferencia clave: **no ocupa espacio en el layout**. Se dibuja centrada dentro del hueco que ya define `column-gap`, así que añadirla o quitarla nunca cambia el ancho de las columnas.

```css
column-rule: <column-rule-width> || <column-rule-style> || <column-rule-color>
```

Es el shorthand de tres propiedades independientes:

| Propiedad | Valor inicial | Qué controla |
| --- | --- | --- |
| `column-rule-width` | `medium` | Grosor de la línea (acepta `thin`, `medium`, `thick` o una longitud) |
| `column-rule-style` | `none` | Estilo: `solid`, `dashed`, `dotted`, `double`, etc. |
| `column-rule-color` | `currentcolor` | Color de la línea |

```css
.articulo {
  columns: 3 15em;
  column-gap: 2rem;
  column-rule: 1px solid #ccc;
}
```

!!! warning "El valor inicial de `column-rule-style` es `none`"

    Si solo declaras `column-rule-color` o `column-rule-width` sin un `column-rule-style` explícito (o dentro del shorthand), no verás ninguna línea: `none` es el valor inicial del estilo, igual que ocurre con `border-style`. Declara siempre un estilo (`solid`, `dashed`...) si quieres que la línea sea visible.

Como la línea no ocupa espacio propio, si el `column-gap` es muy pequeño el resultado puede verse apretado contra el texto de ambas columnas; conviene dejar aire suficiente (por ejemplo `1.5rem` o más) cuando combines `column-rule` con texto denso.

## Controlar los saltos: `break-inside`, `break-before`, `break-after`

Cuando el contenido se reparte entre columnas, el navegador puede cortar un elemento justo por la mitad —una tarjeta, una figura con su pie de foto, un `<blockquote>`— dejando la mitad en una columna y la otra mitad en la siguiente. Las propiedades de fragmentación (`break-inside`, `break-before`, `break-after`) permiten evitar o forzar esos cortes.

```css
break-inside: auto | avoid | avoid-column | avoid-page | avoid-region
break-before: auto | avoid | avoid-column | column | ...
break-after:  auto | avoid | avoid-column | column | ...
```

El uso más común en multicol es evitar que un bloque se parta a la mitad:

```css
.tarjeta,
figure,
blockquote {
  break-inside: avoid;
}
```

`avoid` evita cualquier tipo de corte de fragmentación (columna, página o región); si quieres ser más específico y permitir, por ejemplo, saltos de página al imprimir pero no saltos de columna en pantalla, usa `avoid-column` en su lugar.

También puedes forzar un salto de columna manualmente con el valor `column`, o evitar que un título quede huérfano al final de una columna combinándolo con el párrafo siguiente:

```css
h2 {
  break-after: avoid; /* el título nunca se queda solo al final de una columna */
}

.seccion-nueva {
  break-before: column; /* fuerza que esta sección empiece en una columna nueva */
}
```

!!! tip "Soporte de navegadores"

    `break-inside: avoid` tiene soporte amplio y fiable en navegadores modernos. El valor más específico `avoid-column` está también soportado en los motores actuales, pero al ser más reciente que el genérico `avoid`, conviene revisar su compatibilidad si el proyecto necesita dar soporte a versiones antiguas. Consulta el detalle en [caniuse.com](https://caniuse.com/mdn-css_properties_break-inside_multicol_context_avoid-column).

## `column-span`: elementos que atraviesan todas las columnas

Por defecto, un elemento vive dentro de una sola columna. `column-span: all` hace que ese elemento (por ejemplo, un título o una imagen destacada) se extienda por el ancho completo del contenedor, cruzando todas las columnas.

```css
column-span: none | all
```

```css
.articulo {
  columns: 3 15em;
}

.articulo h2 {
  column-span: all; /* el título ocupa todo el ancho, no una sola columna */
}
```

El contenido que aparece *antes* del elemento con `column-span: all` se balancea automáticamente entre las columnas anteriores, y el contenido que viene *después* retoma el reparto en columnas nuevas debajo. Es el patrón habitual para insertar un titular o una cita destacada en medio de un texto a varias columnas.

## `column-fill`: cómo se reparte el contenido

`column-fill` decide si el contenido se reparte de forma equilibrada entre columnas o si simplemente llena una columna entera antes de pasar a la siguiente.

```css
column-fill: auto | balance | balance-all
```

- **`balance`** (valor inicial): reparte el contenido a partes iguales entre columnas.
- **`auto`**: llena cada columna con todo el contenido que quepa antes de continuar en la siguiente, lo que puede dejar columnas finales vacías.
- **`balance-all`**: pensado para forzar el equilibrado también en contextos paginados; según MDN, a día de hoy no está implementado en ningún navegador.

```css
.articulo {
  columns: 3;
  height: 20em; /* column-fill necesita una altura explícita para tener efecto real */
  column-fill: auto;
}
```

!!! warning "`column-fill` depende de que el contenedor tenga una altura definida"

    Si el contenedor multi-columna no tiene una altura (`height` o `max-height`) explícita, `column-fill` no tiene una columna "llena" de referencia y el comportamiento difiere entre navegadores: Chrome, sin altura fija, ignora en la práctica `column-fill: auto`, mientras que Firefox sí lo respeta y puede volcar todo el contenido en la primera columna. Si necesitas un reparto predecible, fija una altura o confía en el `balance` por defecto sin declarar `column-fill`.

## Cuándo usar multi-columna en lugar de Flexbox o Grid

Multi-columna, Flexbox y Grid resuelven problemas distintos, aunque los tres reparten contenido en un contenedor:

| | Multi-columna | Flexbox | Grid |
| --- | --- | --- | --- |
| ¿Quién decide dónde va cada trozo de contenido? | El navegador, fragmentando el flujo automáticamente | El desarrollador, colocando cada ítem individual | El desarrollador, con control explícito de filas/columnas |
| Dimensión que controla | Reparto de un único flujo en columnas (pensado para texto) | Una dimensión (fila o columna) de ítems independientes | Dos dimensiones simultáneas (filas y columnas) |
| Orden de lectura | Verticalmente por columna, y luego salta a la siguiente columna | El orden que definas con `order`/flujo | El orden que definas en el grid |
| Caso de uso típico | Artículos de texto largo, listados de términos, glosarios | Barras de navegación, tarjetas en una fila, alinear pocos elementos | Layouts de página completos, dashboards, galerías con posiciones explícitas |

En la práctica: elige **multi-columna** cuando tienes un bloque de texto continuo (un artículo, un glosario, una lista larga) y quieres que el propio navegador lo reparta en columnas legibles, sin que te importe exactamente qué párrafo cae en cada una. Elige **Flexbox** o **Grid** cuando tienes un conjunto de componentes discretos (tarjetas, elementos de navegación, secciones de un dashboard) cuya posición sí quieres controlar tú, elemento por elemento.

!!! warning "Cuidado con combinar altura fija y multicol"

    Si fijas una altura al contenedor multi-columna para forzar un número concreto de columnas, ten en cuenta las pautas de accesibilidad (criterio de éxito 1.4.8 "Presentación visual" de WCAG, nivel AAA): el contenido no debería requerir scroll horizontal aunque el usuario duplique (200 %) el tamaño del texto. Una altura demasiado ajustada combinada con texto que crece puede generar justo ese problema.

## Ver también

- [Flexbox](flexbox.md)
- [CSS Grid](grid.md)
- [Overflow y desbordamiento](overflow.md)
- [Fuentes y texto](../tipografia/fuentes-y-texto.md)

## Fuentes

- [CSS multi-column layout - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_multicol_layout)
- [Using multi-column layouts - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Multicol_layout/Using)
- [columns - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/columns)
- [column-count - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/column-count)
- [column-width - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/column-width)
- [column-gap - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/column-gap)
- [column-rule - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/column-rule)
- [break-inside - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/break-inside)
- [column-span - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/column-span)
- [column-fill - MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/column-fill)
- [CSS Multi-column Layout Module Level 1 - W3C](https://www.w3.org/TR/css-multicol-1/)
- [CSS Multiple column layout module - caniuse.com](https://caniuse.com/multicolumn)
- [break-inside: avoid-column (contexto multicol) - caniuse.com](https://caniuse.com/mdn-css_properties_break-inside_multicol_context_avoid-column)
