# Arquitectura CSS: metodologías y organización a escala

Escribir una regla CSS que funcione es fácil; que siga funcionando dentro de seis meses, con quince personas más tocando el mismo código base, es otro problema completamente distinto. La **arquitectura CSS** es el conjunto de decisiones —cómo nombras clases, cómo divides archivos, qué mecanismo usas para evitar colisiones y en qué orden se aplican tus capas de estilos— que determina si un proyecto crece de forma predecible o se convierte en una hoja de estilos donde nadie se atreve a borrar nada por miedo a romper algo en otra parte. No hay una única "arquitectura correcta": hay un puñado de metodologías con compromisos distintos, y elegir bien depende del proyecto, del equipo y de las herramientas que ya tengas en marcha.

## Por qué esto se convierte en un problema real al escalar

CSS tiene una característica que lo hace único frente a JavaScript o los tipos de un lenguaje tipado: **todo selector es, por defecto, global**. Una clase `.title` definida en un archivo puede verse afectada —o afectar— a cualquier otro `.title` en cualquier otra parte del proyecto, sin que exista un mecanismo nativo de módulos que aísle ese alcance. A esto se suma que la cascada resuelve conflictos por [especificidad y orden de aparición](../fundamentos/cascada-especificidad-herencia.md), dos criterios que dependen de *cómo* escribiste el selector y *dónde* colocaste la regla, no de tu intención.

En un proyecto pequeño esto apenas se nota. En un proyecto con decenas de componentes, varias personas escribiendo CSS en paralelo y meses de historial, dos síntomas aparecen casi siempre:

- **Colisiones de nombres**: dos personas usan `.card` con expectativas distintas y una sobrescribe a la otra sin darse cuenta.
- **Especificidad creciente**: para "ganarle" a una regla anterior, alguien añade un selector más específico o un `!important`, lo que obliga a la siguiente persona a ser aún más específica para vencer a esa. El CSS se vuelve cada vez más frágil y nadie se atreve a borrar una regla porque no sabe qué depende de ella.

Las metodologías de nomenclatura (BEM, utility-first, CSS Modules, CSS-in-JS) y las herramientas de organización (custom properties, cascade layers, particionado de archivos) existen precisamente para devolver algo de previsibilidad a estos dos problemas.

## Panorama de metodologías de nomenclatura y organización

### BEM: Block, Element, Modifier

[BEM](https://getbem.com/) es una convención de nomenclatura de clases (no requiere ninguna herramienta de compilación) pensada para que cada selector sea plano, autoexplicativo y con una especificidad constante. El nombre resume su estructura: **Block** (un componente independiente, con sentido por sí mismo), **Element** (una parte de ese bloque que no tiene sentido fuera de él) y **Modifier** (una variante de un bloque o de un elemento).

Según la convención documentada en getbem.com, la sintaxis es:

```css
/* Block: el componente en sí */
.card { }

/* Element: partes internas del block, unidas con doble guion bajo */
.card__image { }
.card__title { }
.card__cta { }

/* Modifier: variantes del block o de un element, unidas con doble guion */
.card--featured { }
.card__cta--disabled { }
```

```html
<article class="card card--featured">
  <img class="card__image" src="foto.jpg" alt="">
  <h3 class="card__title">Auriculares inalámbricos</h3>
  <button class="card__cta card__cta--disabled">Agotado</button>
</article>
```

Lo importante no es la sintaxis en sí, sino lo que garantiza: **todos los selectores son una sola clase** (`0-1-0` en términos de especificidad), así que nunca compites por especificidad entre bloques y nunca necesitas anidar selectores para expresar una relación (`.card .title` desaparece a favor de `.card__title`). Esto hace que cada clase sea, en la práctica, un espacio de nombres manual: `.card__title` no puede colisionar con el `.title` de otro componente porque ya lleva el prefijo del bloque.

Existen pequeñas variaciones de esta notación entre equipos (por ejemplo, un solo guion bajo para el modificador), pero el patrón `bloque`, `bloque__elemento`, `bloque--modificador` es el que se ha estandarizado ampliamente en la comunidad frontend.

!!! note "El coste de BEM"

    BEM no elimina el problema de las colisiones automáticamente: lo delega en la **disciplina del equipo**. Si dos personas nombran un bloque `.card` sin coordinarse, BEM no lo impide por sí solo; ayuda a que sea menos probable y a que el conflicto sea más fácil de detectar en una revisión de código, pero sigue siendo una convención humana, no una garantía técnica como el scoping automático de CSS Modules.

### Utility-first (estilo Tailwind)

El enfoque *utility-first* (popularizado por frameworks como Tailwind CSS) invierte la pregunta: en vez de inventar un nombre semántico para cada componente y escribir una regla CSS a medida, compones el aspecto de un elemento directamente en el marcado combinando clases muy pequeñas y reutilizables, cada una asociada casi siempre a una única declaración CSS:

```html
<button class="px-4 py-2 rounded-md bg-indigo-600 text-white font-semibold hover:bg-indigo-700">
  Guardar cambios
</button>
```

Cada una de esas clases (`px-4`, `rounded-md`, `bg-indigo-600`…) ya existe en la hoja de utilidades del framework; tú no escribes CSS nuevo, solo lo compones en el HTML. Por debajo, una utilidad no es más que una regla mínima como esta:

```css
.px-4 { padding-inline: 1rem; }
.rounded-md { border-radius: 0.375rem; }
```

La ventaja principal es que **elimina la decisión de nombrar cosas** (una de las fuentes más habituales de fricción y de deuda técnica en CSS) y fuerza a que todos los espaciados, colores y tamaños salgan de una escala consistente en vez de valores sueltos inventados sobre la marcha. Las herramientas de este tipo generan en tiempo de compilación solo las clases utilitarias que detectan realmente usadas en tus archivos de marcado, así que el CSS final no crece de forma descontrolada aunque la librería de utilidades disponible sea enorme.

La contrapartida es un HTML más verboso y una curva de aprendizaje distinta (memorizar o consultar constantemente el catálogo de utilidades) y, si no se combina con componentes reutilizables a nivel de framework (React, Vue, etc.) o con una función de extracción de patrones repetidos, la misma combinación larga de clases puede terminar duplicada en muchos sitios.

### CSS Modules: scoping automático vía build tool

[CSS Modules](https://github.com/css-modules/css-modules) no es una especificación del navegador ni del W3C: es una convención que aplica una herramienta de compilación (un *loader* de webpack, un plugin de Vite, PostCSS…) sobre archivos `.css` normales. La herramienta reescribe cada nombre de clase por un identificador único (a menudo con un hash) y expone, desde JavaScript, un objeto que mapea el nombre original al generado:

```css
/* Card.module.css */
.card {
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgb(0 0 0 / 0.1);
}

.title {
  font-size: 1.125rem;
  font-weight: 600;
}
```

```js
import styles from './Card.module.css';

function Card({ title }) {
  return (
    <article className={styles.card}>
      <h3 className={styles.title}>{title}</h3>
    </article>
  );
}
```

En tiempo de compilación, `.card` puede convertirse en algo como `Card_card__1a2b3`, único en todo el proyecto. Esto significa que puedes escribir `.title` en veinte archivos `.module.css` distintos sin que ninguno colisione con otro: el aislamiento no depende de que tú prefijes nada a mano (como en BEM), sino de que la herramienta lo garantiza mecánicamente. Escribes CSS normal, sin sintaxis especial, y el coste de ejecución en el navegador es el mismo que el de cualquier hoja de estilos estática, porque todo el trabajo ocurre en el build, no en tiempo de ejecución.

### CSS-in-JS: estilos co-ubicados con el componente

CSS-in-JS agrupa un conjunto de librerías (styled-components, Emotion, vanilla-extract, entre otras) que permiten escribir los estilos de un componente **dentro del mismo archivo JavaScript/TypeScript** que su lógica, en vez de en un archivo `.css` aparte:

```js
import styled from 'styled-components';

const Card = styled.article`
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgb(0 0 0 / 0.1);
  background: ${(props) => (props.$featured ? 'var(--color-brand-100)' : 'white')};
`;
```

La ventaja evidente es la **co-ubicación**: el estilo vive junto al componente que lo usa, se importa y se elimina con él (menos CSS huérfano), y puedes usar directamente valores de JavaScript —props, estado, resultado de un cálculo— dentro de la propia declaración de estilos, algo que en CSS puro solo se consigue indirectamente (por ejemplo, escribiendo esos valores en custom properties desde JS).

Aquí conviene distinguir dos familias, porque su coste no es el mismo:

- **CSS-in-JS con runtime** (styled-components, Emotion en su modo clásico): la librería calcula y genera clases, e inyecta las reglas CSS en el documento durante la ejecución en el navegador. Esto añade algo de JavaScript al bundle y trabajo en tiempo de ejecución para producir el CSS final.
- **CSS-in-JS de compilación estática o "zero-runtime"** (por ejemplo, vanilla-extract): el CSS se extrae y se genera como archivos `.css` estáticos durante el build, igual que con CSS Modules, y en el navegador no queda ningún coste adicional de JavaScript dedicado a producir estilos.

Ambas variantes resuelven el aislamiento de nombres de forma automática (como CSS Modules), pero difieren en si ese trabajo ocurre en el build o en el navegador del usuario final.

## Cómo elegir una metodología según el proyecto y el equipo

No existe una metodología objetivamente "mejor": cada una asume un contexto distinto. Algunas preguntas ayudan a decidir:

| Criterio | BEM | Utility-first | CSS Modules | CSS-in-JS |
|---|---|---|---|---|
| ¿Dónde se resuelve el aislamiento de nombres? | Convención humana (disciplina de nomenclatura) | Convención + catálogo compartido de utilidades | Automático, en el build | Automático, en runtime o en build según la librería |
| ¿Requiere una herramienta de compilación específica? | No, funciona con CSS plano | Sí (generador de utilidades) | Sí (loader/plugin del bundler) | Sí (la librería elegida) |
| Acoplamiento entre marcado y estilos | Bajo: clases semánticas, el HTML no cambia si cambia el diseño interno | Alto: el aspecto vive en el propio marcado | Medio: import explícito por componente | Alto: estilo y lógica en el mismo archivo |
| Encaja especialmente bien cuando... | No hay framework de componentes, o el equipo quiere CSS legible sin build adicional | Ya existe un sistema de diseño con una escala de tokens y un bundler configurado | El proyecto ya está organizado en componentes (React, Vue, Svelte) y se quiere CSS "de verdad", sin sintaxis especial | Los estilos dependen mucho de props/estado en tiempo real y se prioriza la co-ubicación sobre el coste de runtime |

En la práctica, muchos proyectos no usan una sola metodología de forma pura: es habitual, por ejemplo, apoyarse en utility-first para el grueso de la maquetación y usar BEM o CSS Modules para un puñado de componentes complejos con muchos estados. Lo que realmente importa no es la pureza metodológica, sino que **todo el equipo entienda y siga la misma convención**, porque el coste real de no tener una arquitectura no es filosófico: es el tiempo perdido averiguando si es seguro borrar o modificar una regla.

## Organización de archivos CSS a escala

Elegida (o combinada) una metodología de nomenclatura, queda resolver un segundo problema: cómo estructurar los archivos y en qué orden se cargan, para que crecer el proyecto no signifique perder el control sobre qué gana a qué.

### Particionado por componente

El principio básico es evitar una única hoja de estilos monolítica y, en su lugar, dividir el CSS en archivos pequeños con una responsabilidad clara —normalmente, un archivo (o una carpeta) por componente— que se ensamblan mediante `@import`, el sistema de módulos del bundler, o los propios imports de CSS Modules/CSS-in-JS. Una estructura habitual:

```
styles/
├── tokens/
│   ├── color.css
│   ├── spacing.css
│   └── typography.css
├── base/
│   ├── reset.css
│   └── elements.css
├── components/
│   ├── button.css
│   ├── card.css
│   └── modal.css
└── main.css
```

Este patrón no es una invención propia de este documento: es la misma idea detrás de guías de arquitectura Sass muy extendidas como el **patrón 7-1** (siete carpetas temáticas —`abstracts`, `base`, `components`, `layout`, `pages`, `themes`, `vendors`— más un único archivo que las importa todas) o de **ITCSS** (*Inverted Triangle CSS*, de Harry Roberts), que ordena las capas de genérico a específico —`settings` → `tools` → `generic` → `elements` → `objects` → `components` → `trumps`— para que la especificidad crezca en el mismo sentido en que crece el CSS, evitando así la necesidad de `!important`. No hace falta adoptar ninguno de los dos al pie de la letra: lo que vale la pena tomar de ambos es el principio de fondo, dividir por responsabilidad y mantener un orden de carga explícito, no accidental.

La ventaja práctica de particionar por componente es que borrar un componente (o refactorizarlo) se convierte en una operación local: eliminas su archivo, quitas su import, y no queda CSS huérfano flotando en un archivo compartido de 3000 líneas.

### Custom properties como design tokens

Los *design tokens* (los valores atómicos de un sistema de diseño: colores, espaciados, tamaños de tipografía, radios de borde) necesitan vivir en un único lugar y propagarse desde ahí a todos los componentes. Las [custom properties](../moderno/custom-properties.md) nativas de CSS son el mecanismo natural para esto, porque —a diferencia de las variables de un preprocesador, que se resuelven en tiempo de compilación y desaparecen— siguen vivas en el navegador, participan en la cascada y pueden redefinirse por contexto (un tema oscuro, un componente dentro de otro):

```css
:root {
  --color-brand-500: #6d28d9;
  --color-brand-100: #ede9fe;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --radius-card: 0.5rem;
}

.card {
  border-radius: var(--radius-card);
  padding: var(--space-md);
  background: var(--color-brand-100);
}
```

Para tokens que además necesitan animarse o transicionarse con suavidad —por ejemplo, una "elevación" numérica que controla la intensidad de una sombra—, conviene registrarlos con [`@property`](https://developer.mozilla.org/en-US/docs/Web/CSS/@property): una custom property declarada con `--` a secas se trata como texto sin tipo (su tipo de animación es *discreto*, es decir, salta de un valor a otro sin interpolar), mientras que `@property` le asigna un tipo (`<number>`, `<color>`, `<length>`…) que sí permite una transición o animación continua:

```css
@property --card-elevation {
  syntax: "<number>";
  inherits: false;
  initial-value: 0;
}

.card {
  --card-elevation: 1;
  box-shadow: 0 calc(var(--card-elevation) * 2px) calc(var(--card-elevation) * 6px) rgb(0 0 0 / 0.15);
  transition: --card-elevation 0.2s ease;
}

.card:hover {
  --card-elevation: 3;
}
```

!!! tip "Soporte de navegadores"

    Las custom properties básicas (`--nombre` y `var()`) tienen soporte prácticamente universal en navegadores modernos (en torno al 96% de uso global según caniuse, con Chrome desde la versión 49, Firefox desde la 31, Safari desde la 10 y Edge desde la 16); no funcionan en Internet Explorer. `@property` es una incorporación más reciente —clasificada como *Baseline: Newly available* desde julio de 2024 (es decir, ya soportada por los tres motores principales, pero sin los cerca de 30 meses de historial que exige la clasificación *Widely available*, así que todavía conviene tratarla con algo más de cautela que a las custom properties básicas), con soporte desde Chrome 85, Firefox 128 y Safari 16.4, en torno al 93% de uso global— así que conviene comprobar el detalle actualizado en [caniuse: CSS Variables](https://caniuse.com/css-variables) y [caniuse: @property](https://caniuse.com/mdn-css_at-rules_property) antes de depender de ella si el proyecto necesita soporte a versiones antiguas.

### Cascade layers para ordenar las capas de un design system

Cuando un proyecto combina varias fuentes de CSS —un *reset*, tokens, estilos base, componentes propios, utilidades y quizá un framework de terceros— el orden en que "gana" cada una no debería depender de qué tan específico sea cada selector ni de en qué archivo se cargó por casualidad más tarde. Las [cascade layers](../moderno/cascade-layers.md) (`@layer`) resuelven justo esto: dejan declarar explícitamente, con un identificador legible, en qué orden compiten bloques enteros de estilos, **antes** de que la especificidad entre en juego.

Combinado con el particionado por componente del apartado anterior, el patrón habitual en un `main.css` (o su equivalente en el entrypoint del bundler) es declarar primero el orden de capas y luego importar cada partición dentro de la capa que le corresponde:

```css
@layer reset, tokens, base, components, utilities;

@import url("base/reset.css") layer(reset);
@import url("tokens/color.css") layer(tokens);
@import url("tokens/spacing.css") layer(tokens);
@import url("base/elements.css") layer(base);
@import url("components/button.css") layer(components);
@import url("components/card.css") layer(components);
```

Con esto, un selector muy específico dentro de `components` (por ejemplo, `.card .title.destacado`) nunca podrá vencer accidentalmente a una regla mínima de `utilities` si esta se declara en una capa posterior, y viceversa: el orden lo decide la lista de capas, no quién tiene el selector más largo. Esto es especialmente valioso al integrar un framework de terceros: puedes cargar su CSS en una capa temprana (por ejemplo, `@import url("framework.css") layer(vendor);` como primera capa de la lista) y garantizar que tus propios estilos, en una capa posterior, siempre lo sobrescriban sin recurrir a `!important` ni a selectores artificialmente específicos.

!!! tip "Soporte de navegadores"

    Las cascade layers (`@layer`, incluida la sintaxis `@import ... layer(...)`) están clasificadas como *Baseline: Widely available* desde marzo de 2022, con soporte desde Chrome/Edge 99, Firefox 97 y Safari 15.4, y un uso global en torno al 94% según caniuse. No hay soporte en Internet Explorer. Revisa el detalle actualizado en [caniuse: CSS Cascade Layers](https://caniuse.com/css-cascade-layers) si el proyecto debe convivir con navegadores más antiguos, y ten preparado un plan de repliegue (por ejemplo, ordenar manualmente los archivos de import) para ese caso.

## Ver también

- [Cascada, herencia y especificidad](../fundamentos/cascada-especificidad-herencia.md)
- [Custom properties](../moderno/custom-properties.md)
- [Cascade layers (@layer)](../moderno/cascade-layers.md)
- [Selectores](../fundamentos/selectores.md)

## Fuentes

- [MDN: Using CSS custom properties (variables)](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties)
- [MDN: --* (custom property)](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
- [MDN: var()](https://developer.mozilla.org/en-US/docs/Web/CSS/var)
- [MDN: @property](https://developer.mozilla.org/en-US/docs/Web/CSS/@property)
- [MDN: @layer](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@layer)
- [MDN: @import](https://developer.mozilla.org/en-US/docs/Web/CSS/@import)
- [W3C: CSS Custom Properties for Cascading Variables Module Level 1](https://www.w3.org/TR/css-variables-1/)
- [W3C: CSS Cascading and Inheritance Level 5](https://www.w3.org/TR/css-cascade-5/)
- [getbem.com: BEM — Block Element Modifier](https://getbem.com/)
- [GitHub: css-modules/css-modules](https://github.com/css-modules/css-modules)
- [caniuse: CSS Variables (Custom Properties)](https://caniuse.com/css-variables)
- [caniuse: @property](https://caniuse.com/mdn-css_at-rules_property)
- [caniuse: CSS Cascade Layers](https://caniuse.com/css-cascade-layers)
