# Positioning: static, relative, absolute, fixed, sticky

La propiedad `position` decide **cómo se coloca un elemento**: si sigue el flujo normal del documento o si se saca de él para colocarlo en un punto concreto. Entenderla bien —junto con `top`/`right`/`bottom`/`left`, el concepto de *containing block* y el *stacking context*— es lo que separa a quien "prueba cosas hasta que funciona" de quien sabe exactamente por qué un elemento aparece donde aparece, o por qué un `z-index: 9999` a veces no hace absolutamente nada.

## Los cinco valores de `position`

El valor inicial (por defecto) de `position` es `static`. Los otros cuatro valores —`relative`, `absolute`, `fixed` y `sticky`— se agrupan bajo el término **elementos posicionados** (*positioned elements*), y son los únicos en los que `top`, `right`, `bottom`, `left` e `inset` tienen algún efecto. `z-index` sigue casi la misma regla, con una excepción que veremos más adelante: también funciona en los ítems flex o grid aunque conserven `position: static`.

### `static`: el flujo normal

Es el comportamiento por defecto de cualquier elemento. Ocupa su lugar en el flujo del documento tal cual dicta el modelo de caja, y las propiedades de desplazamiento (`top`, `right`, `bottom`, `left`) **no tienen ningún efecto** sobre él.

```css
.tarjeta {
  position: static; /* casi nunca hace falta escribirlo explícitamente */
}
```

Rara vez se declara a propósito, salvo para **anular** un `position` aplicado antes en la cascada (por ejemplo, para "desactivar" el posicionamiento de un componente reutilizable). Ten en cuenta que `position` **no es una propiedad heredable** (al igual que `border`, `margin` o `display`): un elemento nunca recibe el `position` de su padre de forma automática, solo el que le llegue por la cascada (una regla que lo seleccione) o, explícitamente, mediante la palabra clave `position: inherit`.

### `relative`: se mueve a sí mismo, sin afectar a los demás

El elemento sigue en el flujo normal —reserva su espacio como si no se hubiera movido— pero `top`/`right`/`bottom`/`left` lo desplazan visualmente **respecto a su propia posición original**. Ese desplazamiento no empuja ni reordena a los elementos vecinos.

```css
.aviso {
  position: relative;
  top: 4px;   /* se desplaza 4px hacia abajo desde su posición normal */
  left: 8px;  /* se desplaza 8px hacia la derecha */
}
```

El uso más habitual de `relative` en proyectos reales **no es mover el elemento**, sino convertirlo en el punto de referencia (containing block) para un descendiente `absolute`:

```css
.tarjeta {
  position: relative; /* no se desplaza, pero ahora es el "ancla" del badge */
}

.tarjeta__badge {
  position: absolute;
  top: 0;
  right: 0;
  transform: translate(50%, -50%);
}
```

### `absolute`: fuera del flujo, anclado a un ancestro posicionado

El elemento se **extrae por completo del flujo normal** (no reserva espacio, otros elementos se comportan como si no existiera) y se posiciona respecto a su *containing block* — en la práctica, el ancestro posicionado más cercano (más abajo se explica esto en detalle).

```css
.dropdown {
  position: relative;
}

.dropdown__menu {
  position: absolute;
  top: 100%;   /* justo debajo del botón */
  left: 0;
  min-width: 100%;
}
```

Este patrón —contenedor `relative` + hijo `absolute`— es la base de menús desplegables, tooltips, badges, overlays de imágenes, etc.

### `fixed`: fuera del flujo, anclado al viewport

Igual que `absolute` en que se extrae del flujo, pero su *containing block* es siempre el **viewport** (la ventana visible), no un ancestro. Por eso un elemento `fixed` permanece en el mismo punto de la pantalla aunque el usuario haga scroll.

```css
.volver-arriba {
  position: fixed;
  right: 1.5rem;
  bottom: 1.5rem;
  z-index: 1000;
}
```

!!! warning "Un ancestro con transform, filter o will-change puede 'romper' el fixed"
    Si algún ancestro tiene `transform`, `translate`, `scale`, `rotate`, `filter`, `backdrop-filter`, `perspective`, `will-change` (con una propiedad que genere containing block), `contain: layout|paint|strict|content` o `content-visibility: auto` con un valor distinto de su inicial, ese ancestro pasa a ser el *containing block* del descendiente `fixed`, y el elemento dejará de anclarse al viewport para anclarse a ese ancestro. Es una causa muy común —y muy confusa— de "mi `position: fixed` no se queda fijo".

### `sticky`: híbrido entre `relative` y `fixed`

`sticky` es probablemente el valor más malentendido. El elemento se comporta como `relative` (ocupa su lugar en el flujo) **hasta que**, durante el scroll, alcanza el umbral definido por `top`, `right`, `bottom` o `left` dentro de su contenedor de scroll; a partir de ahí se comporta como `fixed` (se "pega") **pero solo mientras su contenedor padre siga visible en pantalla**. Cuando el padre sale del viewport, el elemento sticky se va con él.

```css
.tabla thead th {
  position: sticky;
  top: 0;         /* se pega al llegar al borde superior del scroll */
  background: white;
  z-index: 1;     /* para que quede por encima de las filas al superponerse */
}
```

Dos requisitos imprescindibles que suelen olvidarse:

1. **Necesita al menos una propiedad de desplazamiento** (`top`, `right`, `bottom`, `left` o sus equivalentes lógicos) con un valor distinto de `auto`. Sin eso, `sticky` se comporta igual que `relative`.
2. **Ningún ancestro entre el elemento y su contenedor de scroll puede tener `overflow` distinto de `visible`** (es decir, `hidden`, `auto` o `scroll`) a menos que sea precisamente el contenedor de scroll que quieres usar como referencia. Un `overflow: hidden` puesto "por accidente" en un contenedor intermedio es la causa número uno de que un `sticky` no funcione: ese ancestro pasa a ser el nuevo contenedor de scroll de referencia, y el elemento deja de "pegarse" donde lo esperas. Si necesitas recortar el contenido de ese contenedor sin sacrificar el `sticky`, usa `overflow: clip` en su lugar: recorta igual que `hidden`, pero no crea un contexto de scroll propio, así que no interfiere.

```css
.barra-lateral {
  position: sticky;
  top: 1rem; /* se detiene a 1rem del borde superior del viewport de scroll */
}
```

## `top`, `right`, `bottom`, `left` e `inset`

Estas cuatro propiedades ("propiedades de desplazamiento" o *inset properties*) solo tienen efecto sobre elementos posicionados (cualquier valor de `position` distinto de `static`). Su significado cambia según el valor de `position`:

- Con `absolute` o `fixed`: fijan la distancia entre el borde del elemento y el borde correspondiente de su *containing block*.
- Con `relative`: fijan cuánto se desplaza el elemento respecto a su propia posición normal (`top` lo mueve hacia abajo, `left` hacia la derecha; no hacia arriba/izquierda como podría parecer intuitivamente).
- Con `sticky`: definen el umbral de distancia al contenedor de scroll a partir del cual el elemento se "pega".
- Con `static`: no tienen ningún efecto.

El valor inicial de las cuatro es `auto`, y aceptan longitudes (`px`, `rem`...) o porcentajes, calculados sobre el tamaño del *containing block*.

`inset` es la propiedad abreviada (shorthand) que agrupa las cuatro, con la misma sintaxis multivalor que `margin`:

```css
/* Estas dos declaraciones son equivalentes */
.modal {
  inset: 10px 20px 30px 40px; /* top | right | bottom | left */
}

.modal-equivalente {
  top: 10px;
  right: 20px;
  bottom: 30px;
  left: 40px;
}

/* Un solo valor: los cuatro lados */
.overlay {
  position: absolute;
  inset: 0; /* equivalente a top:0; right:0; bottom:0; left:0; */
}
```

`inset: 0` es un atajo muy usado para hacer que un elemento `absolute` (o `fixed`) cubra exactamente a su *containing block*, típico en overlays, capas de carga o fondos de tarjetas.

!!! tip "Soporte de navegadores"
    `inset` es *Baseline: ampliamente disponible* desde abril de 2021. Si necesitas dar soporte a navegadores más antiguos (Safari < 14.1, por ejemplo), usa las cuatro propiedades individuales `top`/`right`/`bottom`/`left` en lugar del shorthand. Consulta el detalle en [caniuse: CSS property inset](https://caniuse.com/mdn-css_properties_inset).

## El *containing block* (contenedor de posicionamiento)

El *containing block* es el rectángulo respecto al cual se calculan la posición y los porcentajes (`width`, `height`, `top`, etc.) de un elemento. Cuál es exactamente depende del valor de `position` del elemento:

| `position` del elemento | Containing block |
|---|---|
| `static`, `relative` o `sticky` | El *content box* del ancestro en bloque más cercano (o el que establece un formatting context: flex, grid, tabla...) |
| `absolute` | El *padding box* del ancestro posicionado (`position` distinto de `static`) más cercano; si no existe ninguno, el *initial containing block* (el bloque raíz del documento) |
| `fixed` | El viewport (en pantalla) o el área de página (al imprimir) |

Además, para `absolute` y `fixed` hay una regla adicional muy relevante en la práctica: si un ancestro tiene cualquiera de estas propiedades con un valor distinto del inicial, ese ancestro **también** se convierte en el *containing block*, aunque su `position` sea `static`:

- `transform`, `translate`, `scale` o `rotate`
- `filter` o `backdrop-filter`
- `perspective`
- `will-change` (cuando incluye alguna de las propiedades anteriores)
- `contain: layout`, `paint`, `strict` o `content`
- `content-visibility: auto`

```css
.galeria {
  /* sin position, pero con transform: se convierte en containing block */
  transform: rotate(0deg);
}

.galeria__etiqueta {
  position: absolute; /* se ancla a .galeria, no al body */
  top: 8px;
  left: 8px;
}
```

Este es el motivo técnico exacto por el que técnicas como "aplicar `transform: translateZ(0)` a un contenedor" pueden desplazar de sitio a hijos `absolute` o `fixed`: sin darse cuenta, ese `transform` acaba de convertir al contenedor en su nuevo *containing block*.

Una precisión importante sobre `absolute` sin ancestro posicionado: se ancla al *initial containing block*, que tiene el tamaño del viewport pero **forma parte del flujo del documento y se desplaza con el scroll**, a diferencia de `fixed`, que se ancla al viewport de forma literal y permanece fijo en pantalla durante el scroll.

## El contexto de apilamiento (*stacking context*) y `z-index`

Cuando varios elementos se superponen, el navegador necesita decidir cuál se dibuja encima de cuál en el eje Z (perpendicular a la pantalla). Ese orden se resuelve dentro de **contextos de apilamiento**: agrupaciones jerárquicas e independientes entre sí, donde los `z-index` de los elementos de un contexto nunca se comparan con los de otro contexto distinto.

`z-index` solo tiene efecto en elementos posicionados (cualquier `position` distinto de `static`) y en ítems flex o grid. Su valor inicial es `auto` (el elemento no crea un contexto de apilamiento propio y su nivel de apilamiento es `0`); con un valor entero, el elemento **crea un nuevo contexto de apilamiento** para sí mismo y sus descendientes.

```css
.wrapper {
  position: relative;
}

.caja-oro {
  position: absolute;
  z-index: 3; /* se dibuja por encima de las siguientes */
}

.caja-verde {
  position: absolute;
  z-index: 2;
}

.caja-gris {
  position: absolute;
  z-index: 1; /* se dibuja debajo de las otras dos */
}
```

Lo que sorprende a mucha gente: no hace falta usar `position` + `z-index` para generar un contexto de apilamiento. Estas condiciones, entre otras, también lo crean:

- El elemento raíz del documento (`<html>`).
- `position: fixed` o `position: sticky` (siempre, sin necesitar `z-index`).
- `position: absolute` o `position: relative` con `z-index` distinto de `auto`.
- Ser un ítem flex o grid con `z-index` distinto de `auto`.
- `opacity` con un valor menor que `1`.
- `mix-blend-mode` distinto de `normal`.
- `transform`, `scale`, `rotate` o `translate` con un valor distinto de `none`.
- `filter`, `backdrop-filter` o `perspective` con un valor distinto de `none`.
- `clip-path` o `mask`/`mask-image`/`mask-border` con un valor distinto de `none`.
- `isolation: isolate`.
- `will-change` especificando alguna propiedad que por sí sola generaría un contexto de apilamiento.
- `contain: layout`, `paint`, `strict` o `content`.
- `container-type: size` o `inline-size`.
- Elementos en el *top layer* (fullscreen, `popover`) y su `::backdrop`.
- Un elemento cuya animación por `@keyframes` cambia alguna de las propiedades anteriores (por ejemplo `opacity`) y usa `animation-fill-mode: forwards`.

```css
/* opacity < 1 crea un contexto de apilamiento nuevo, */
/* aunque el elemento sea position: static */
.superpuesto {
  opacity: 0.99;
}
```

La consecuencia práctica más importante: **un `z-index` alto no sirve de nada si tu elemento está "encerrado" dentro de un contexto de apilamiento distinto** al del elemento con el que compite. Por ejemplo, si el padre de tu componente tiene `opacity: 0.98` o un `transform` cualquiera, ese padre ya creó su propio contexto de apilamiento, y ningún `z-index: 99999` en un hijo hará que ese hijo se dibuje por encima de un elemento que vive fuera de ese contexto. La solución casi siempre pasa por subir el `z-index` (o el contexto que lo genera) en un nivel más alto del árbol, no por seguir aumentando el número.

!!! tip "Soporte de navegadores"
    `position: sticky` es *Baseline: ampliamente disponible* (todos los navegadores principales desde 2017 aproximadamente) y cubre más del 95% de uso global. Si tu proyecto necesita soportar Internet Explorer o versiones muy antiguas de Safari/Chrome, revisa el detalle exacto en [caniuse: CSS position:sticky](https://caniuse.com/css-sticky) antes de depender de él sin *fallback*.

## Ver también

- [Display y flujo normal](display-y-flujo-normal.md)
- [Overflow y desbordamiento](overflow.md)
- [Flexbox](flexbox.md)
- [Transform](../animaciones/transform.md)

## Fuentes

- [MDN: position](https://developer.mozilla.org/en-US/docs/Web/CSS/position)
- [MDN: Layout and the containing block](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Display/Containing_block)
- [MDN: Stacking context](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Positioned_layout/Stacking_context)
- [MDN: z-index](https://developer.mozilla.org/en-US/docs/Web/CSS/z-index)
- [MDN: inset](https://developer.mozilla.org/en-US/docs/Web/CSS/inset)
- [MDN: top](https://developer.mozilla.org/en-US/docs/Web/CSS/top)
- [caniuse: CSS position:sticky](https://caniuse.com/css-sticky)
- [caniuse: CSS property inset](https://caniuse.com/mdn-css_properties_inset)
