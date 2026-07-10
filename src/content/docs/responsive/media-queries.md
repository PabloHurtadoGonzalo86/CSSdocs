---
title: Media queries
description: Explicación de las media queries en CSS - sintaxis de @media, operadores lógicos, tipos de media, media features comunes como width, orientation y prefers-color-scheme, las estrategias mobile-first y desktop-first, y la sintaxis moderna de rango.
---

Las **media queries** son el mecanismo que tiene CSS para aplicar unos estilos u otros según las características del dispositivo o del entorno en el que se muestra la página: el ancho de la ventana, la orientación de la pantalla, si el usuario prefiere temas oscuros o si el medio de salida es una impresora. Son la pieza central de cualquier diseño responsivo: sin ellas, una hoja de estilos produce siempre el mismo layout, sin importar si se ve en un móvil de 360&nbsp;px o en un monitor de 2560&nbsp;px.

## Sintaxis de `@media`

Una media query se declara con la regla `@media`, seguida de una condición (la *media query* en sí) y un bloque de llaves con las reglas CSS normales que se aplicarán solo cuando esa condición se cumpla:

```css
@media screen and (width >= 900px) {
  article {
    padding: 1rem 3rem;
  }
}
```

Según [MDN](https://developer.mozilla.org/es/docs/Web/CSS/CSS_media_queries/Using_media_queries), una media query se compone de:

- Un **tipo de media** opcional (`screen`, `print`...). Si se omite, se asume `all`.
- Una o varias **expresiones de media feature**, cada una entre paréntesis, como `(width >= 900px)` o `(orientation: landscape)`.
- **Operadores lógicos** opcionales para combinar varias condiciones.

La media query completa se evalúa como verdadera cuando el tipo de media (si se especifica) coincide con el dispositivo actual **y** todas las expresiones de features se cumplen. Si alguna condición no se cumple, el bloque entero de reglas se ignora, como si no existiera.

### Operadores lógicos

| Operador | Qué hace | Ejemplo |
|---|---|---|
| `and` | Combina un tipo de media con features, o varias features entre sí; todas deben cumplirse | `@media screen and (width >= 900px) and (orientation: landscape) { }` |
| `,` (coma) | Actúa como un **or**: si cualquiera de las queries separadas por comas se cumple, se aplican los estilos | `@media (height >= 680px), screen and (orientation: portrait) { }` |
| `or` | Alternativa a la coma, añadida en Media Queries Level 4, con el mismo significado | `@media screen or print { }` |
| `not` | Niega toda la media query a la que se aplica (no una feature suelta, salvo que la envuelvas entre paréntesis) | `@media not print { }` |
| `only` | Solo tiene efecto en navegadores muy antiguos sin soporte de media queries; en navegadores modernos no cambia nada. Si lo usas, es obligatorio especificar también un tipo de media | `@media only screen and (color) { }` |

```css
/* Aplica en pantalla, cuando el ancho sea de 30em o más Y la orientación sea horizontal */
@media screen and (width >= 30em) and (orientation: landscape) {
  .layout {
    grid-template-columns: 1fr 1fr;
  }
}

/* Aplica en pantalla O en impresión (basta con que una de las dos se cumpla) */
@media screen, print {
  body {
    line-height: 1.4;
  }
}

/* Aplica en cualquier medio EXCEPTO impresión */
@media not print {
  .solo-pantalla {
    display: block;
  }
}
```

:::tip[Soporte de navegadores]
El operador `or` y la posibilidad de que `not` niegue una feature individual entre paréntesis (`not (width > 1000px)`) forman parte de **Media Queries Level 4**, más reciente que la coma o el `and` clásicos. El soporte de navegadores para estas novedades va de la mano del resto de features de este nivel de la especificación (incluida la sintaxis de rango que veremos más abajo); consulta [caniuse: CSS Media Queries Range Syntax](https://caniuse.com/css-media-range-syntax) para una referencia orientativa.
:::

## Tipos de media: `screen`, `print` y `all`

La especificación original definía muchos tipos de media (`tv`, `handheld`, `projection`, `braille`, `aural`...), pero **Media Queries Level 4 los declaró obsoletos** y hoy solo quedan tres con sentido real, tal como confirma [MDN](https://developer.mozilla.org/es/docs/Web/CSS/@media):

- **`all`**: adecuado para cualquier dispositivo. Es el valor por defecto cuando no se indica ningún tipo.
- **`screen`**: pensado para pantallas (monitores, móviles, tablets...).
- **`print`**: pensado para material paginado y para la vista previa de impresión del navegador.

```css
/* Estilos para impresión: oculta la navegación y fuerza texto negro sobre blanco */
@media print {
  nav,
  .no-imprimir {
    display: none;
  }

  body {
    color: #000;
    background: #fff;
  }
}
```

En la práctica, la inmensa mayoría de media queries de un proyecto no necesitan ningún tipo de media explícito: como `all` es el valor por defecto, basta con escribir directamente las features entre paréntesis (`@media (width >= 900px) { }`), y solo se añade `screen` o `print` cuando de verdad importa distinguir el medio de salida.

## Media features comunes

Las *media features* son las condiciones concretas que se evalúan dentro de los paréntesis. Estas son las que más vas a usar en un proyecto real.

### `width` y `height`

Miden el ancho o alto del **viewport** (no del documento completo ni de la pantalla física). Son las features más usadas para construir layouts responsivos.

```css
@media (width <= 600px) {
  .barra-lateral {
    display: none;
  }
}
```

### `orientation`

Indica si el viewport es más alto que ancho (`portrait`) o más ancho que alto (`landscape`), según [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/orientation).

```css
@media (orientation: landscape) {
  .galeria {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### `prefers-color-scheme`

Detecta si el usuario ha activado un tema claro u oscuro a nivel de sistema operativo o de user agent. Admite dos valores: `light` (el usuario prefiere un tema claro, o no ha expresado ninguna preferencia) y `dark` (prefiere un tema oscuro), según confirma [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme).

```css
:root {
  --fondo: #ffffff;
  --texto: #111111;
}

@media (prefers-color-scheme: dark) {
  :root {
    --fondo: #111111;
    --texto: #eeeeee;
  }
}

body {
  background: var(--fondo);
  color: var(--texto);
}
```

Este patrón —definir custom properties por defecto y sobreescribirlas dentro de la media query— evita duplicar reglas enteras solo para cambiar unos pocos colores.

### `prefers-reduced-motion`

Detecta si el usuario ha pedido al sistema que reduzca el movimiento no esencial (animaciones, parpadeos, desplazamientos grandes), algo pensado sobre todo para personas con trastornos vestibulares. Admite `reduce` y `no-preference`, y usar la feature sin valor (`(prefers-reduced-motion)`) equivale a comprobar que **no** vale `no-preference`, según [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion).

```css
.tarjeta {
  transition: transform 0.3s ease;
}

.tarjeta:hover {
  transform: scale(1.05);
}

@media (prefers-reduced-motion: reduce) {
  .tarjeta {
    transition: none;
  }

  .tarjeta:hover {
    transform: none;
  }
}
```

:::tip[Soporte de navegadores]
Tanto `prefers-color-scheme` como `prefers-reduced-motion` tienen soporte amplio en todos los navegadores modernos desde 2020. Consulta el detalle actualizado en [caniuse: prefers-color-scheme](https://caniuse.com/prefers-color-scheme) y [caniuse: prefers-reduced-motion](https://caniuse.com/prefers-reduced-motion).
:::

:::caution[Respeta siempre `prefers-reduced-motion`]
Si tu sitio usa animaciones decorativas (parallax, elementos que crecen, paneles que se deslizan), añadir el bloque `prefers-reduced-motion: reduce` no es un detalle opcional de accesibilidad: para algunas personas, ese movimiento puede provocar mareo o náuseas reales.
:::

## Mobile-first vs. desktop-first: `min-width` vs. `max-width`

`width` y `height` son *range features*: además de la sintaxis `min-width`/`max-width` clásica, aceptan comparaciones matemáticas modernas (lo vemos en la siguiente sección). Pero antes de la sintaxis, lo importante es la **estrategia**: en qué orden escribes tus media queries y qué asumes por defecto.

### Enfoque mobile-first (`min-width`)

Se parte de los estilos para pantallas pequeñas **sin ninguna media query**, y se van añadiendo ajustes a medida que el ancho disponible crece, con `min-width`:

```css
/* Estilos base: pensados para móvil, se aplican siempre */
.tarjetas {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

/* A partir de 600px, dos columnas */
@media (min-width: 600px) {
  .tarjetas {
    grid-template-columns: 1fr 1fr;
  }
}

/* A partir de 900px, tres columnas */
@media (min-width: 900px) {
  .tarjetas {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

Es el enfoque recomendado hoy en día por dos razones prácticas: la mayoría del tráfico web es móvil, y escribir primero los estilos más simples (una columna, sin florituras) y luego ir *añadiendo* complejidad conforme hay más espacio suele producir hojas de estilos más cortas y fáciles de razonar que partir de un layout complejo e ir desmontándolo.

### Enfoque desktop-first (`max-width`)

Es el enfoque inverso: se parte de los estilos para pantallas grandes sin media query, y se van sobreescribiendo con `max-width` a medida que el ancho se reduce:

```css
/* Estilos base: pensados para escritorio */
.tarjetas {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

/* Por debajo de 900px, dos columnas */
@media (max-width: 899px) {
  .tarjetas {
    grid-template-columns: 1fr 1fr;
  }
}

/* Por debajo de 600px, una columna */
@media (max-width: 599px) {
  .tarjetas {
    grid-template-columns: 1fr;
  }
}
```

Tiene sentido cuando el proyecto es genuinamente una aplicación de escritorio a la que se añade soporte móvil después, pero en la mayoría de sitios web actuales suele acabar generando más CSS de "anulación" (sobreescribir reglas complejas para simplificarlas) que el enfoque mobile-first.

:::note[No mezcles los breakpoints a ciegas]
Da igual el enfoque que elijas: lo importante es ser consistente dentro de un mismo proyecto. Mezclar `min-width` y `max-width` sin criterio en los mismos breakpoints suele acabar en solapamientos (un rango de anchos donde se aplican dos reglas contradictorias) o en huecos (un rango donde no se aplica ninguna).
:::

## Sintaxis moderna de rango (`width < 600px`)

Media Queries Level 4 introdujo una **sintaxis de rango** que usa los operadores de comparación matemática (`<`, `>`, `<=`, `>=`) directamente sobre la feature, en lugar de los prefijos `min-`/`max-`. Es más legible, especialmente cuando se comprueba un rango con dos límites a la vez, según documenta [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/width):

```css
/* Sintaxis clásica (min-/max-) */
@media (min-width: 480px) and (max-width: 900px) {
  .contenido {
    padding: 1.5rem;
  }
}

/* Sintaxis de rango equivalente, en una sola expresión */
@media (480px <= width <= 900px) {
  .contenido {
    padding: 1.5rem;
  }
}

/* Comparaciones simples */
@media (width < 600px) {
  .menu {
    display: none;
  }
}

@media (width >= 600px) {
  .menu {
    display: flex;
  }
}
```

Fíjate en el matiz entre `<`/`>` (exclusivos, el valor límite queda fuera) y `<=`/`>=` (inclusivos, el valor límite queda dentro): `(width < 600px)` no incluye exactamente `600px`, mientras que `(width <= 600px)` sí. Es la misma diferencia que hay entre `max-width: 599px` y `max-width: 600px` con la sintaxis clásica, pero expresada de forma mucho más directa.

:::tip[Soporte de navegadores]
La sintaxis de rango es más reciente que `min-width`/`max-width`: tiene buen soporte en navegadores modernos (Chrome y Edge desde la versión 104, Firefox desde la 63, Safari desde la 16.4), pero **no funciona en absoluto** en navegadores más antiguos como Internet Explorer. Si tu proyecto necesita dar soporte a navegadores muy antiguos, la sintaxis clásica con `min-width`/`max-width` sigue siendo la opción segura. Consulta el detalle actualizado en [caniuse: CSS Media Queries Range Syntax](https://caniuse.com/css-media-range-syntax).
:::

## Ver también

- [Container queries](container-queries)
- [Unidades y funciones responsivas](unidades-y-funciones)
- [Flexbox](../layout/flexbox)
- [Unidades y valores](../fundamentos/unidades)

## Fuentes

- [MDN: Uso de media queries](https://developer.mozilla.org/es/docs/Web/CSS/CSS_media_queries/Using_media_queries)
- [MDN: @media](https://developer.mozilla.org/es/docs/Web/CSS/@media)
- [MDN: orientation](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/orientation)
- [MDN: prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme)
- [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
- [MDN: width](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/width)
- [caniuse: prefers-color-scheme](https://caniuse.com/prefers-color-scheme)
- [caniuse: prefers-reduced-motion](https://caniuse.com/prefers-reduced-motion)
- [caniuse: CSS Media Queries Range Syntax](https://caniuse.com/css-media-range-syntax)
