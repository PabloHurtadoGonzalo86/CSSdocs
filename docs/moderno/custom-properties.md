# Custom properties (variables CSS)

Las custom properties son el mecanismo nativo de CSS para declarar un valor una sola vez y reutilizarlo en cualquier parte de tu hoja de estilos, sin depender de un preprocesador. A diferencia de las variables de Sass o Less, que se resuelven en tiempo de compilación y desaparecen antes de llegar al navegador, las custom properties viven **dentro del navegador**: participan en la cascada, se heredan, se pueden leer y escribir desde JavaScript, y su valor puede cambiar en tiempo real según el estado del documento (una clase, un `:hover`, una media query). Esto las convierte en la base de casi cualquier sistema de theming moderno, incluido el clásico modo claro/oscuro.

## Declaración con `--nombre` y uso con `var()`

Una custom property se declara como cualquier otra declaración CSS, pero su nombre debe empezar por dos guiones (`--`). Según la especificación [CSS Custom Properties for Cascading Variables Module Level 1](https://www.w3.org/TR/css-variables-1/) del W3C, una custom property es, literalmente, "cualquier propiedad cuyo nombre empiece por dos guiones, como `--foo`": el propio lenguaje nunca le da un significado propio a ese valor, es un contenedor que tú defines:

```css
:root {
  --color-marca: #6d28d9;
  --espaciado-base: 1rem;
  --sombra-tarjeta: 0 2px 8px rgb(0 0 0 / 0.15);
}
```

Para usar ese valor en cualquier propiedad "de verdad" (una que sí tiene significado para el navegador, como `color` o `padding`), se emplea la función [`var()`](https://developer.mozilla.org/en-US/docs/Web/CSS/var):

```css
.boton {
  background-color: var(--color-marca);
  padding: var(--espaciado-base);
  box-shadow: var(--sombra-tarjeta);
}
```

`var()` acepta un segundo argumento opcional que actúa como **valor por defecto** (*fallback*): se usa si la custom property referenciada no está declarada, o si su valor no es válido en el punto donde se usa (lo que la especificación llama *invalid at computed-value time*, IACVT):

```css
.tarjeta {
  /* Si --radio-tarjeta no existe en ningún selector aplicable, usa 8px */
  border-radius: var(--radio-tarjeta, 8px);
}
```

El fallback puede ser cualquier valor CSS válido, incluida otra `var()` anidada, lo que permite encadenar varios niveles de "por si acaso":

```css
.aviso {
  /* Si --color-aviso no existe, prueba --color-marca; si tampoco existe, usa gray */
  color: var(--color-aviso, var(--color-marca, gray));
}
```

Un detalle importante de la sintaxis: si el fallback contiene comas, **todo lo que hay después de la primera coma se considera parte del fallback**, no argumentos adicionales de `var()`. Por eso esto es válido y produce el fallback `"Arial, sans-serif"` completo:

```css
.texto {
  font-family: var(--fuente-principal, Arial, sans-serif);
}
```

Mientras que escribir `var(--a, --b, pink)` **no** define dos fallbacks alternativos: `"--b, pink"` se trata como un único valor de fallback (y como `--b` no es un nombre de propiedad "de verdad" en ese contexto sino texto literal, probablemente sea inválido). Para encadenar alternativas reales, la forma correcta es anidar `var()` como en el ejemplo anterior.

!!! warning "Qué pasa sin fallback y sin valor válido"
    Si usas `var(--algo)` sin segundo argumento y `--algo` no está definida en ningún selector que aplique al elemento (ni se hereda de un antecesor), el navegador trata la propiedad como si se le hubiera aplicado la palabra clave [`unset`](https://developer.mozilla.org/en-US/docs/Web/CSS/unset): vuelve al valor heredado si la propiedad es heredable, o a su valor inicial si no lo es. No se produce ningún error visible en consola: el fallo es silencioso, así que conviene revisar bien los nombres al depurar.

Dos reglas de nomenclatura a tener en cuenta:

- Los nombres de custom properties son **sensibles a mayúsculas y minúsculas**: `--color-marca` y `--Color-Marca` son dos propiedades distintas, a diferencia de los nombres de propiedades estándar de CSS (`color`, `background`...), que no distinguen mayúsculas.
- `--` a secas (dos guiones sin nada detrás) no es un nombre válido: debe haber al menos un carácter después del prefijo.

## Cascada y herencia: la gran diferencia con Sass o Less

Aquí está la diferencia conceptual más importante frente a las variables de un preprocesador. Una variable de Sass (`$color-marca`) es una sustitución de texto que ocurre **antes** de que el archivo se convierta en CSS: cuando el navegador recibe el CSS ya compilado, la variable ya no existe, solo queda el valor final tal cual quedó en ese punto del código. No hay forma de que su valor cambie después, ni de que dependa de qué elemento del DOM la está usando.

Una custom property, en cambio, es una declaración CSS más, y como tal **participa en la cascada**: distintos selectores pueden asignarle valores distintos, y gana el que corresponda según el propio algoritmo de la cascada (origen, especificidad, orden de aparición), exactamente igual que con `color` o `margin`. Además, las custom properties **se heredan por defecto**, sea cual sea su nombre, algo que no ocurre automáticamente con la mayoría de propiedades estándar (ver [Cascada, herencia y especificidad](../fundamentos/cascada-especificidad-herencia.md)):

```css
:root {
  --color-texto: #1f2937;
}

.tarjeta-destacada {
  --color-texto: #7c3aed; /* Sobrescribe el valor solo para este elemento y sus descendientes */
}

p {
  color: var(--color-texto);
}
```

```html
<p>Texto normal.</p>
<div class="tarjeta-destacada">
  <p>Este párrafo hereda --color-texto: #7c3aed de su antecesor.</p>
</div>
```

El resultado práctico: el mismo `var(--color-texto)`, escrito una sola vez en el selector `p`, resuelve a un color distinto según en qué parte del árbol del documento se encuentre el párrafo. Esto es exactamente lo que hace posible el theming dinámico (cambiar de tema sin recompilar nada) y es imposible de replicar con una variable de Sass, cuyo valor queda fijado en el momento de la compilación, no en el del renderizado.

Como consecuencia de la herencia, si una custom property no está definida en el elemento donde se usa con `var()`, el navegador sigue buscando su valor hacia arriba en el árbol, en los antecesores, antes de recurrir al fallback o al `unset`.

!!! tip "Registrar el tipo y la herencia con `@property`"
    Por defecto, **toda** custom property se hereda y no tiene validación de tipo (admite cualquier valor, incluso uno inválido para el uso que le des). Si necesitas lo contrario —una custom property no heredable, con un tipo concreto y un valor inicial garantizado—, puedes registrarla explícitamente con la at-rule [`@property`](https://developer.mozilla.org/en-US/docs/Web/CSS/@property):

    ```css
    @property --progreso {
      syntax: "<percentage>";
      inherits: false;
      initial-value: 0%;
    }
    ```

    Esto es un tema aparte (y una API de CSS Houdini con soporte más reciente: Chrome/Edge desde la versión 85, Firefox desde la 128 y Safari desde la 16.4, según [caniuse.com/mdn-css_at-rules_property](https://caniuse.com/mdn-css_at-rules_property)), pero merece mencionarse aquí porque es la excepción que confirma que la herencia "por defecto" de las custom properties normales es, precisamente, una decisión de diseño y no una casualidad.

## Alcance: `:root` vs alcance local

Dónde declares una custom property determina su **alcance** (*scope*): la propiedad existe únicamente en el elemento donde se declara y en sus descendientes (por herencia), nunca fuera de ese subárbol.

`:root` es la pseudoclase que selecciona el elemento raíz del documento (`<html>` en HTML), y es el lugar habitual para declarar las variables "globales" de un proyecto, precisamente porque, al estar en la raíz, se heredan en todo el documento:

```css
:root {
  --color-primario: #2563eb;
  --color-fondo: #ffffff;
  --radio-borde: 0.5rem;
}
```

Pero nada obliga a declarar las custom properties en `:root`: cualquier selector puede definir (o redefinir) una, y su alcance queda limitado a ese selector y a lo que herede de él. Esto es útil para crear variantes locales sin tocar el valor global:

```css
:root {
  --color-boton: #2563eb;
}

.boton {
  background-color: var(--color-boton);
}

.boton--peligro {
  --color-boton: #dc2626; /* Redefine la variable solo dentro de .boton--peligro */
}
```

```html
<button class="boton">Guardar</button>
<button class="boton boton--peligro">Eliminar</button>
```

El segundo botón usa `#dc2626` porque `--color-boton` se redefine en `.boton--peligro`, un selector que aplica directamente a ese `<button>`; el primero, al no tener esa clase, no tiene ninguna declaración de `--color-boton` en el elemento mismo, así que hereda el valor definido en `:root`. Ojo con la explicación: no es que `.boton--peligro` tenga "más especificidad" que `:root` (de hecho, una clase y una pseudoclase tienen exactamente la misma especificidad, 0-1-0 cada una); lo que ocurre es que compiten en **elementos distintos**. `:root` solo selecciona el `<html>`, así que su valor le llega al `<button>` por herencia; `.boton--peligro`, en cambio, selecciona directamente al propio `<button>`. En la cascada, una declaración que aplica directamente a un elemento siempre prevalece sobre un valor meramente heredado de un antecesor, sea cual sea la especificidad de la regla que originó ese valor heredado.

Un patrón muy común es declarar variables "de componente" directamente en la clase del componente, para que solo existan dentro de él y de sus hijos:

```css
.tarjeta {
  --tarjeta-padding: 1.5rem;
  --tarjeta-radio: 12px;

  padding: var(--tarjeta-padding);
  border-radius: var(--tarjeta-radio);
}

.tarjeta__titulo {
  /* Puede reutilizar las variables de .tarjeta porque las hereda */
  margin-bottom: calc(var(--tarjeta-padding) / 2);
}
```

Fuera de `.tarjeta` (por ejemplo, en un `<p>` hermano en el mismo nivel del DOM), `var(--tarjeta-padding)` no encontraría ningún valor, porque ese `<p>` no es descendiente de ningún elemento con la clase `.tarjeta` y por tanto no hereda la variable.

## Caso práctico: theming claro/oscuro con `prefers-color-scheme`

La combinación de custom properties con la media feature [`prefers-color-scheme`](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme) es, hoy, la forma más habitual de implementar un modo claro/oscuro que respete la preferencia del sistema operativo del usuario. `prefers-color-scheme` detecta si el usuario ha configurado su sistema (o navegador) para preferir un tema claro o uno oscuro, y admite los valores `light` y `dark`.

La idea central es: declaras un conjunto de custom properties "semánticas" (no `--azul`, sino `--color-fondo`, `--color-texto`...) en `:root`, y luego **redefines esas mismas variables** dentro de un bloque `@media (prefers-color-scheme: dark)`. El resto del CSS no cambia nunca: solo consume las variables con `var()`, sin saber ni preocuparse por si el tema activo es claro u oscuro.

```css
:root {
  /* Valores por defecto: tema claro */
  --color-fondo: #ffffff;
  --color-texto: #1a1a1a;
  --color-borde: #e2e2e2;
  --color-marca: #6d28d9;
}

@media (prefers-color-scheme: dark) {
  :root {
    /* Se redefinen las mismas variables para el tema oscuro */
    --color-fondo: #121212;
    --color-texto: #f0f0f0;
    --color-borde: #3a3a3a;
    --color-marca: #a78bfa;
  }
}

body {
  background-color: var(--color-fondo);
  color: var(--color-texto);
}

.tarjeta {
  border: 1px solid var(--color-borde);
  background-color: var(--color-fondo);
}

.enlace {
  color: var(--color-marca);
}
```

Por qué funciona: `@media (prefers-color-scheme: dark)` no crea una capa nueva de especificidad ni cambia la cascada de forma especial; simplemente hace que ese bloque de reglas **solo se evalúe** cuando la condición de la media query es verdadera. Cuando el sistema está en modo oscuro, el segundo bloque `:root { ... }` también aplica, y como es una declaración posterior con la misma especificidad que el primer `:root`, gana por orden de aparición (el último criterio de la cascada, ver [Cascada, herencia y especificidad](../fundamentos/cascada-especificidad-herencia.md)). El resto de tu CSS —`body`, `.tarjeta`, `.enlace`— no necesita ningún bloque `@media` propio, porque no hace más que leer, con `var()`, el valor vigente de cada variable en cada momento.

Esto es justo lo que **no** se puede hacer con variables de Sass: como se resuelven en tiempo de compilación, no existe forma de que una `$variable` de Sass "escuche" una media query y cambie de valor en el navegador sin generar dos bloques de CSS completamente separados y duplicar cada regla que las use. Con custom properties, escribes las reglas de layout y color una sola vez, y el tema cambia por debajo sin tocarlas.

Si además quieres que los controles nativos del navegador (scrollbars, campos de formulario) se adapten al tema, se puede combinar con la propiedad [`color-scheme`](https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme):

```css
:root {
  color-scheme: light;
}

@media (prefers-color-scheme: dark) {
  :root {
    color-scheme: dark;
  }
}
```

Y para permitir que la persona usuaria elija manualmente un tema que anule la preferencia del sistema (un botón de "modo oscuro" en la propia interfaz), basta con añadir un selector adicional, por ejemplo un atributo en el `<html>`, con **mayor especificidad** que el simple `:root` del bloque de la media query:

```css
:root[data-tema="oscuro"] {
  --color-fondo: #121212;
  --color-texto: #f0f0f0;
}
```

`:root[data-tema="oscuro"]` combina una pseudoclase y un selector de atributo, así que su especificidad (0-2-0) es mayor que la de un `:root` a secas (0-1-0), tanto la del `:root` inicial como la del `:root` dentro del `@media`. Por eso este bloque gana sobre ambos en cuanto el atributo `data-tema="oscuro"` está presente en el `<html>` —la especificidad decide antes que el orden de aparición, así que da igual en qué parte del archivo lo coloques—. Si además defines un `:root[data-tema="claro"]` equivalente con los valores del tema claro, tendrá esa misma especificidad y solo se aplicará cuando el atributo valga `"claro"`; así, JavaScript puede forzar cualquiera de los dos temas simplemente cambiando el valor del atributo, sin necesidad de `!important`.

!!! tip "Soporte de navegadores"
    Las custom properties (`--*` y `var()`) tienen **soporte universal en navegadores modernos** desde hace años (Chrome 49+, Firefox 31+, Safari 10+, Edge 16+); el único hueco relevante es Internet Explorer 11, que no las soporta. Consulta el detalle en [caniuse.com/css-variables](https://caniuse.com/css-variables). La media feature `prefers-color-scheme` también goza de soporte amplio (Baseline: ampliamente disponible desde 2020), con el mismo hueco en Internet Explorer; el detalle está en [caniuse.com/mdn-css_at-rules_media_prefers-color-scheme](https://caniuse.com/mdn-css_at-rules_media_prefers-color-scheme).

## Ver también

- [Cascada, herencia y especificidad](../fundamentos/cascada-especificidad-herencia.md)
- [Media queries](../responsive/media-queries.md)
- [Color moderno (oklch, color-mix)](color-moderno.md)
- [Cascade layers (@layer)](cascade-layers.md)

## Fuentes

- [MDN: Using CSS custom properties (variables)](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascading_variables/Using_CSS_custom_properties)
- [MDN: var()](https://developer.mozilla.org/en-US/docs/Web/CSS/var)
- [MDN: --* (custom property)](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
- [MDN: @property](https://developer.mozilla.org/en-US/docs/Web/CSS/@property)
- [MDN: prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme)
- [MDN: color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme)
- [W3C: CSS Custom Properties for Cascading Variables Module Level 1](https://www.w3.org/TR/css-variables-1/)
- [caniuse: CSS variables (Custom Properties)](https://caniuse.com/css-variables)
- [caniuse: prefers-color-scheme media query](https://caniuse.com/mdn-css_at-rules_media_prefers-color-scheme)
- [caniuse: @property CSS at-rule](https://caniuse.com/mdn-css_at-rules_property)
