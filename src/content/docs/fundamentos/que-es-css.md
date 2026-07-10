---
title: Qué es CSS y cómo se aplica
description: Explica qué es CSS, su sintaxis básica de selector y declaración, los comentarios, y las tres formas de aplicarlo a un documento HTML (hoja externa, interna y en línea).
---

CSS (*Cascading Style Sheets*, "hojas de estilo en cascada") es el lenguaje que describe **cómo se presenta** un documento HTML: colores, tipografías, espaciados, tamaños, posición de los elementos en pantalla, en papel o incluso en voz. Entenderlo bien —qué es exactamente, cómo se relaciona con HTML y JavaScript, y las distintas formas de "engancharlo" a una página— es el cimiento sobre el que se apoya todo lo demás: cascada, especificidad, selectores, layout... Si esta base no queda clara, cualquier bug de estilos se vuelve mucho más difícil de razonar.

## Qué es CSS exactamente

Según la propia definición de [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS), CSS es un **lenguaje de hojas de estilo** que se usa para describir la presentación de un documento escrito en HTML o XML (incluyendo dialectos como SVG o MathML). Es decir, CSS no crea contenido ni estructura: **decora y organiza visualmente** un contenido que ya existe.

CSS es, junto con HTML y JavaScript, una de las tres tecnologías centrales de la web, y cada una tiene una responsabilidad distinta:

| Tecnología | Responsabilidad | Pregunta que responde |
| --- | --- | --- |
| **HTML** | Estructura y contenido | ¿Qué hay en la página? |
| **CSS** | Presentación visual | ¿Cómo se ve? |
| **JavaScript** | Comportamiento e interactividad | ¿Qué hace y cómo reacciona? |

Esta separación de responsabilidades no es un capricho estético: permite que un mismo HTML se pueda re-estilizar por completo cambiando solo el CSS (sin tocar el contenido), y que la lógica de interacción viva en JS sin mezclarse con las reglas de estilo. Cuando esa separación se rompe —por ejemplo, abusando de estilos en línea, como veremos más abajo— el código se vuelve más difícil de mantener y de razonar.

Técnicamente, CSS no es un lenguaje de programación: no tiene variables (en el sentido clásico), bucles ni condicionales como JS. Es un lenguaje **declarativo basado en reglas**: describes *qué* quieres conseguir (este párrafo en azul, esta caja con este ancho) y es el navegador quien decide *cómo* aplicarlo, resolviendo conflictos mediante el algoritmo de la cascada.

## Sintaxis básica: selector, propiedad y valor

La unidad fundamental de CSS es la **regla** (*ruleset*), que combina un **selector** con un **bloque de declaraciones**:

```css
selector {
  propiedad: valor;
}
```

Un ejemplo concreto:

```css
h1 {
  color: red;
  font-size: 2rem;
}
```

Aquí:

- **`h1`** es el *selector*: indica a qué elementos del HTML se aplica la regla (en este caso, todos los `<h1>` del documento).
- **`color: red;`** y **`font-size: 2rem;`** son *declaraciones*: cada una es un par **propiedad: valor** que termina en punto y coma.
- **`color`** y **`font-size`** son *propiedades*: la característica que se está modificando.
- **`red`** y **`2rem`** son los *valores*: cómo se ajusta esa propiedad.
- Todo el conjunto de declaraciones entre `{` y `}` es el *bloque de declaración*.

Un mismo bloque puede aplicarse a varios selectores a la vez separándolos por comas:

```css
h1,
p,
li {
  color: green;
}
```

Algunos detalles de sintaxis que conviene interiorizar desde el principio:

- Las propiedades y los valores predefinidos por CSS **no distinguen mayúsculas de minúsculas** (`color: red;` es equivalente a `COLOR: RED;`), pero en la práctica siempre se escriben en minúsculas por convención y legibilidad.
- El espacio en blanco (saltos de línea, tabulaciones, espacios) alrededor de selectores, propiedades y valores se ignora, lo cual es lo que permite formatear el código de forma legible.
- Si un selector de la lista no es válido, **toda la regla se descarta**, incluso si el resto de selectores son correctos.
- La última declaración de un bloque no requiere el punto y coma final, pero es buena práctica incluirlo siempre para evitar errores al añadir una nueva declaración después.

## Comentarios en CSS

CSS usa un único estilo de comentario, delimitado por `/*` y `*/`. Puede ocupar una línea o varias:

```css
/* Esto es un comentario de una sola línea */

/*
  Esto es un comentario
  que ocupa varias líneas
*/

p {
  color: red; /* también se puede comentar al final de una línea */
}
```

:::caution[No existen los comentarios `//` en CSS estándar]
A diferencia de JavaScript, CSS **no** admite comentarios de línea con `//`. Si escribes `// esto es un comentario` en un archivo `.css`, el navegador no lo reconocerá como comentario y probablemente ignorará la declaración siguiente por sintaxis inválida. Los comentarios `//` sí existen en preprocesadores como Sass/SCSS, pero se compilan a CSS plano antes de llegar al navegador, así que no son intercambiables.
:::

## Las tres formas de aplicar CSS a un documento

Existen tres maneras de conectar CSS con un HTML, y las tres son válidas sintácticamente, pero no son equivalentes en cuanto a mantenibilidad.

### 1. Hoja de estilos externa (`<link>`)

Consiste en escribir el CSS en un archivo `.css` independiente y enlazarlo desde el `<head>` del HTML mediante el elemento [`<link>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/link):

```html
<!-- index.html -->
<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>Mi página</title>
    <link rel="stylesheet" href="estilos.css" />
  </head>
  <body>
    <h1>Hola mundo</h1>
  </body>
</html>
```

```css
/* estilos.css */
h1 {
  color: red;
  font-size: 2rem;
}
```

El atributo `rel="stylesheet"` le dice al navegador que ese recurso enlazado es una hoja de estilos, y `href` apunta a su ubicación (ruta relativa o absoluta). No hace falta añadir `type="text/css"`: dado que CSS es hoy el único lenguaje de hojas de estilo usado en la web, MDN señala explícitamente que omitir el atributo `type` es la práctica recomendada actualmente.

### 2. Hoja de estilos interna (`<style>`)

El CSS se escribe directamente dentro de un elemento [`<style>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/style), que debe ir dentro del `<head>` del documento:

```html
<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>Mi página</title>
    <style>
      h1 {
        color: red;
        font-size: 2rem;
      }
    </style>
  </head>
  <body>
    <h1>Hola mundo</h1>
  </body>
</html>
```

Este CSS solo afecta al documento HTML donde está escrito. Si hay varios `<style>` en la misma página, se aplican en cascada según el orden en que aparecen: ante igual especificidad, gana la declaración que aparece más abajo en el documento.

### 3. Estilos en línea (atributo `style`)

Las declaraciones se escriben directamente en el atributo `style` del elemento HTML, sin selector (porque el "selector" ya es el propio elemento):

```html
<h1 style="color: red; font-size: 2rem;">Hola mundo</h1>
```

Aquí no hay selector ni llaves: solo el bloque de declaraciones, separadas por punto y coma, dentro de las comillas del atributo.

## Por qué se recomienda la hoja externa

MDN es explícito al respecto: la hoja de estilos externa es "el método más común y útil" para aplicar CSS, mientras que sobre los estilos en línea afirma literalmente "evita usar CSS de esta forma si es posible: es una mala práctica" y recomienda evitarlos siempre que se pueda. Las razones, en la práctica diaria, son de mantenibilidad:

| Método | Reutilizable entre páginas | Cacheable por el navegador | Mezcla CSS con el HTML |
| --- | --- | --- | --- |
| Externa (`<link>`) | Sí, un mismo archivo sirve a todo el sitio | Sí | No |
| Interna (`<style>`) | No, hay que copiarla en cada página | No | Sí (mismo documento) |
| En línea (`style=""`) | No, es por elemento | No | Sí, directamente en la etiqueta |

En concreto:

- **Una sola hoja externa puede enlazarse desde muchas páginas HTML**, así que un cambio de diseño (por ejemplo, el color corporativo) se hace en un único archivo y se propaga a todo el sitio, en lugar de tener que editar el `<style>` o el atributo `style` de cada página o cada elemento.
- El archivo `.css` externo puede beneficiarse del **caché del navegador**: se descarga una vez y se reutiliza en la navegación posterior, algo que no ocurre con el CSS incrustado en cada HTML.
- Mantiene **separadas la estructura (HTML) y la presentación (CSS)**, lo que hace el código de ambos más legible y fácil de depurar; MDN señala literalmente que el CSS en línea "mezcla código de presentación con el HTML y el contenido, haciendo todo más difícil de leer y entender".
- Los estilos en línea tienen además una **especificidad muy alta** en la cascada (superior a cualquier selector normal), lo que suele obligar a usar `!important` más adelante para poder sobrescribirlos: un problema que se evita simplemente no usándolos.

En la práctica, verás `<style>` sobre todo en prototipos rápidos, demos aisladas o emails HTML (donde el soporte de `<link>` externo es limitado en muchos clientes de correo), y estilos en línea generados dinámicamente desde JavaScript (por ejemplo, `elemento.style.transform = ...` para animaciones calculadas en tiempo de ejecución). Para el CSS de un proyecto real, la hoja externa es la opción por defecto.

:::tip[Soporte de navegadores]
Las tres formas de aplicar CSS —`<link rel="stylesheet">`, `<style>` y el atributo `style`— llevan soportadas de forma universal desde los primeros navegadores con CSS y no presentan problemas de compatibilidad hoy en día. Puedes consultar la tabla de soporte del atributo `rel` del elemento `<link>` en [caniuse.com](https://caniuse.com/mdn-html_elements_link_rel).
:::

## Ver también

- [Cascada, herencia y especificidad](cascada-especificidad-herencia)
- [Selectores](selectores)
- [El modelo de caja](modelo-de-caja)
- [Display y flujo normal](../layout/display-y-flujo-normal)

## Fuentes

- [CSS - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [Getting started with CSS - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Getting_started)
- [CSS syntax - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/Syntax)
- [<link>: The External Resource Link element - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/link)
- [<style>: The Style Information element - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/style)
- [HTML element: link, rel — Can I use](https://caniuse.com/mdn-html_elements_link_rel)
