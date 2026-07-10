---
title: "@scope: alcance de estilos"
description: Explica la at-rule @scope de CSS para acotar reglas a un subárbol del DOM mediante raíz y límite de scope, el pseudo-elemento :scope, la especificidad dentro de @scope, la proximidad de scope en la cascada y las limitaciones de este aislamiento frente al Shadow DOM.
---

`@scope` es una at-rule que permite limitar un bloque de reglas CSS a un **subárbol concreto del DOM**, definido por un selector de raíz y, opcionalmente, un selector de límite inferior. En la práctica resuelve un problema muy antiguo del CSS en cascada: cómo escribir selectores cortos y poco específicos sin que acaben "escapándose" y afectando a elementos de otras partes de la página que casualmente comparten el mismo nombre de clase o de etiqueta.

## Qué problema resuelve: colisiones sin depender de una convención de nombres

Durante años, la forma habitual de evitar colisiones de estilos ha sido puramente **social**: metodologías como BEM inventan nombres de clase largos y "namespaced" (`.tarjeta__titulo`, `.tarjeta--destacada`) para simular, a mano, un espacio de nombres que el lenguaje CSS no ofrecía. Funciona, pero tiene un coste: nada en el propio CSS impide que alguien reutilice `.titulo` en otro componente sin querer, y cuanto más grande es el proyecto, más largos y menos legibles se vuelven los nombres para intentar compensarlo.

`@scope` ataca el problema desde otro ángulo: en lugar de fabricar nombres únicos, **acota estructuralmente** dónde puede aplicar un selector. Un selector `.titulo` escrito dentro de `@scope (.tarjeta)` solo puede coincidir con un `.titulo` que esté dentro de un elemento `.tarjeta`, sin necesidad de escribir `.tarjeta .titulo` ni de inflar el nombre de la clase para hacerla "única". Esto no sustituye por completo a una convención de nombres (sigues necesitando clases razonables), pero elimina buena parte de la razón por la que esas convenciones se volvían tan verbosas: ya no hace falta fingir un scope con texto, porque ahora el lenguaje lo ofrece de forma nativa.

```css
/* Antes: una convención de nombres hace de "espacio de nombres" manual */
.tarjeta__titulo {
  font-weight: 600;
}

/* Con @scope: el propio selector ya está acotado al subárbol de .tarjeta */
@scope (.tarjeta) {
  .titulo {
    font-weight: 600;
  }
}
```

## Sintaxis: raíz de scope y límite de scope

La forma más completa de `@scope` toma dos listas de selectores entre paréntesis:

```css
@scope (raíz-de-scope) to (límite-de-scope) {
  selector {
    /* declaraciones */
  }
}
```

- **Raíz de scope** (*scope root*, a veces llamado *scope-start*): el selector que marca el límite **superior** del subárbol. Es **inclusivo** por defecto: el propio elemento que coincide con la raíz puede ser seleccionado por las reglas de dentro del bloque.
- **Límite de scope** (*scope limit*, o *scope-end*), tras la palabra clave `to`: opcional. Marca el límite **inferior**. Es **exclusivo** por defecto: ni el elemento que coincide con el límite ni sus descendientes quedan dentro del scope.

Si omites la cláusula `to (...)`, el scope no tiene límite inferior y se extiende a todos los descendientes de la raíz:

```css
@scope (.cuerpo-articulo) {
  img {
    border: 4px solid #333;
    border-radius: 4px;
  }
}
```

Aquí, solo las imágenes que sean descendientes de `.cuerpo-articulo` reciben el borde; una imagen en la cabecera o en el pie de página del sitio, aunque comparta el mismo selector `img`, queda completamente al margen, sin necesidad de escribir `.cuerpo-articulo img` ni de darle una clase especial.

## El "donut scope": excluir una subregión interna

Añadir un límite inferior permite algo que un simple selector descendente no puede hacer con la misma limpieza: dejar un "agujero" dentro del área seleccionada. A este patrón se le suele llamar **donut scope** (scope en forma de rosquilla): un área con borde exterior e interior, donde solo se estiliza lo que queda entre ambos.

```css
@scope (.cuerpo-articulo) to (figure) {
  img {
    border: 4px solid #333;
    background-color: goldenrod;
  }
}
```

Con este bloque, cualquier `img` dentro de `.cuerpo-articulo` recibe el borde dorado, **excepto** las que estén dentro de un `<figure>`. Es el caso típico de una plantilla de artículo: quieres dar un tratamiento genérico a las imágenes del cuerpo del texto, pero las imágenes dentro de un `<figure>` (que ya suelen llevar su propio `figcaption` y su propio estilo) deben quedar fuera de esa regla genérica. Conseguir esto mismo con selectores clásicos obligaría a algo como `.cuerpo-articulo img:not(figure img)`, mucho más frágil y difícil de leer.

### Cambiar qué límite es inclusivo o exclusivo

Como la raíz es inclusiva y el límite es exclusivo por defecto, a veces hace falta invertir ese comportamiento. Se consigue combinando el selector con el combinador de hijo universal `> *`:

| Escritura | Efecto |
|---|---|
| `@scope (raíz) to (límite)` | Raíz inclusiva, límite exclusivo (comportamiento por defecto). |
| `@scope (raíz) to (límite > *)` | Ambos límites inclusivos: el propio elemento del límite también entra en el scope. |
| `@scope (raíz > *) to (límite)` | Ambos límites exclusivos: la propia raíz queda fuera, solo aplica a sus descendientes. |
| `@scope (raíz > *) to (límite > *)` | Raíz exclusiva, límite inclusivo. |

```css
@scope (.cuerpo-articulo) to (figure > *) {
  /* el límite pasa a ser inclusivo: alcanza también a los hijos directos de <figure> */
}
```

## El pseudo-clase `:scope` dentro de `@scope`

Dentro de un bloque `@scope`, el pseudo-clase [`:scope`](https://developer.mozilla.org/en-US/docs/Web/CSS/:scope) apunta directamente a la **raíz del scope**, lo que permite estilizar el contenedor y sus descendientes en el mismo bloque sin repetir el selector de la raíz por fuera:

```css
@scope (.tarjeta) {
  :scope {
    padding: 1rem;
    border-radius: 0.5rem;
    background: white;
  }

  .titulo {
    font-weight: 600;
  }
}
```

`:scope` también puede usarse dentro del propio límite de scope para expresar una relación más precisa con la raíz. Por ejemplo, para que `figure` solo cuente como límite si es un **hijo directo** de la raíz (y no un descendiente más lejano):

```css
@scope (.cuerpo-articulo) to (:scope > figure) {
  /* … */
}
```

Tanto la raíz como el límite pueden ser listas de selectores separadas por coma, en cuyo caso se definen varios scopes independientes a la vez:

```css
@scope (.tarjeta-destacada, .tarjeta-producto) to (figure) {
  img {
    border: 3px solid goldenrod;
  }
}
```

:::note[Las reglas con scope no pueden escapar del subárbol]
Un selector como `:scope + p` no es válido dentro de `@scope`, porque intentaría seleccionar un elemento **fuera** del subárbol acotado (un hermano de la raíz, no un descendiente). El modelo de `@scope` solo permite moverse hacia abajo en el árbol, nunca hacia los lados ni hacia arriba.
:::

## Especificidad dentro de `@scope`

Dentro de un bloque `@scope`, tanto un selector "pelado" (sin `:scope` explícito) como el selector de anidamiento nativo `&` se comportan como si llevaran `:where(:scope)` delante. Como [`:where()`](https://developer.mozilla.org/en-US/docs/Web/CSS/:where) siempre aporta especificidad cero, ni el selector ni `&` suman nada extra por el hecho de estar dentro de `@scope`: el único peso proviene del resto del selector. Usar `:scope` de forma explícita sí suma especificidad, porque cuenta como una pseudo-clase normal (una columna CLASE):

```css
@scope (.tarjeta) {
  .titulo {
    /* especificidad 0-1-0: la de .titulo, @scope no añade nada */
  }

  & .titulo {
    /* misma especificidad, 0-1-0: & tampoco añade nada aquí */
  }

  :scope .titulo {
    /* especificidad 0-2-0: :scope suma una columna CLASE, más la de .titulo */
  }
}
```

:::caution[El peso de `&` dentro de `@scope` puede variar entre navegadores]
Según MDN, el tratamiento de la especificidad de `&` dentro de `@scope` difiere según el motor y la versión del navegador. Si tu selector depende de un cálculo de especificidad muy ajustado (por ejemplo, para que gane o pierda frente a otra regla concreta), revisa la tabla de compatibilidad de la [página de MDN sobre `@scope`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@scope) antes de darlo por sentado.
:::

## Proximidad de scope: cómo se resuelven los conflictos entre scopes

`@scope` añade un criterio nuevo a la cascada: la **proximidad de scope** (*scoping proximity*). Se sitúa justo después de la especificidad y antes del orden de aparición: si dos declaraciones empatan en origen, importancia, capa y especificidad, gana la que provenga del scope cuya raíz está a **menos saltos** en el árbol del DOM respecto al elemento.

Esto soluciona un problema clásico al anidar componentes con temas contrapuestos. Con selectores normales:

```css
.tema-claro p {
  color: #111;
}

.tema-oscuro p {
  color: #f5f5f5;
}
```

```html
<div class="tema-claro">
  <p>Texto en tema claro</p>
  <div class="tema-oscuro">
    <p>Texto en tema oscuro</p>
    <div class="tema-claro">
      <p>¿Qué color gana aquí?</p>
    </div>
  </div>
</div>
```

Las dos reglas tienen exactamente la misma especificidad (0-1-1), así que gana la que se declaró después en el archivo (`.tema-oscuro p`), y el párrafo más interno —que visualmente vive dentro de un `.tema-claro` anidado— acaba en blanco sobre fondo claro, ilegible. Reescribiendo esto con `@scope`:

```css
@scope (.tema-claro) {
  :scope {
    background: #f5f5f5;
  }
  p {
    color: #111;
  }
}

@scope (.tema-oscuro) {
  :scope {
    background: #1a1a1a;
  }
  p {
    color: #f5f5f5;
  }
}
```

Ahora el párrafo más interno queda correctamente en color oscuro sobre fondo claro: está a **un solo salto** de su `.tema-claro` ancestro más cercano, pero a **dos saltos** de `.tema-oscuro`, y la proximidad de scope hace ganar a la regla más cercana, sin importar el orden en que se declararon los bloques.

:::tip[La proximidad de scope no pisa a la especificidad]
Este criterio solo entra en juego cuando todo lo anterior en la cascada ya ha empatado. Si una de las dos reglas en conflicto tiene mayor especificidad, `!important` o está en una capa (`@layer`) posterior, esa diferencia se sigue resolviendo antes y la proximidad de scope ni se llega a evaluar. Puedes ver el resto de criterios de la cascada, en orden, en [Cascada, especificidad y herencia](../fundamentos/cascada-especificidad-herencia).
:::

## Qué NO hace `@scope`: los límites de este aislamiento

Es tentador pensar en `@scope` como una especie de encapsulación total de estilos, similar a la que ofrece el Shadow DOM, pero no lo es. Conviene tener claras sus dos limitaciones principales:

- **La herencia sigue atravesando los límites del scope.** Las propiedades heredables (`color`, `font-family`, `line-height`...) declaradas dentro de un bloque `@scope` se siguen heredando por los descendientes normales de CSS, más allá de cualquier límite (`to`) que hayas puesto. El límite acota **dónde puede coincidir un selector**, no hasta dónde llega un valor heredado.

    ```css
    @scope (.cuerpo-articulo) to (figure) {
      color: crimson; /* se hereda igual dentro de <figure>, aunque el límite lo "excluya" como selector */
    }
    ```

- **`@scope` no bloquea estilos externos.** Una regla declarada fuera de cualquier `@scope` (por ejemplo, en otra hoja de estilos o más abajo en el mismo archivo) puede seguir seleccionando y estilizando elementos que viven dentro de tu subárbol acotado, si su selector coincide y gana la cascada. `@scope` solo restringe el alcance de **tus propios selectores dentro del bloque**; no aísla el subárbol frente al resto del CSS de la página, como sí haría el árbol de un Shadow DOM.

## Uso implícito dentro de un `<style>` embebido

Si omites por completo la raíz de scope y usas `@scope` dentro de un `<style>` que está anidado en el propio HTML, el navegador toma como raíz implícita el **elemento padre de ese `<style>`**:

```html
<section class="cuerpo-articulo">
  <style>
    @scope {
      img {
        border: 4px solid #333;
      }
    }
  </style>
  <!-- … -->
</section>
```

Esto equivale a `@scope (.cuerpo-articulo) { … }`, pero es útil cuando generas fragmentos de HTML con su propio `<style>` incluido (por ejemplo, contenido inyectado dinámicamente) y no quieres depender de que el fragmento conozca de antemano una clase concreta para usarla como selector de raíz.

:::tip[Soporte de navegadores]
`@scope` alcanzó soporte en Chrome/Edge 118 (octubre de 2023) y Safari 17.4 (marzo de 2024); Firefox fue el último de los motores principales en implementarlo, lo que retrasó su condición de *Baseline* hasta finales de 2025 ("*Newly available*" desde diciembre de 2025, según MDN). Si tu proyecto necesita dar soporte a versiones anteriores de Firefox, comprueba el estado actualizado en [caniuse: Scoped Styles (@scope rule)](https://caniuse.com/css-cascade-scope) y [caniuse: CSS at-rule `@scope`](https://caniuse.com/mdn-css_at-rules_scope), y ten en cuenta que un navegador sin soporte simplemente ignora el bloque `@scope` completo (no falla de forma silenciosa a nivel de declaración individual, se descarta la regla entera).
:::

## Ver también

- [Cascada, especificidad y herencia](../fundamentos/cascada-especificidad-herencia)
- [Cascade layers (@layer)](cascade-layers)
- [Selectores modernos (:has, :is, :where)](selectores-modernos)
- [Arquitectura y metodologías CSS](../arquitectura/metodologias-y-organizacion)

## Fuentes

- [MDN: @scope](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@scope)
- [MDN: :scope](https://developer.mozilla.org/en-US/docs/Web/CSS/:scope)
- [MDN: :where()](https://developer.mozilla.org/en-US/docs/Web/CSS/:where)
- [W3C: CSS Cascading and Inheritance Level 6 — scoped styles](https://www.w3.org/TR/css-cascade-6/#scoped-styles)
- [caniuse: Scoped Styles (the @scope rule)](https://caniuse.com/css-cascade-scope)
- [caniuse: CSS at-rule @scope](https://caniuse.com/mdn-css_at-rules_scope)
