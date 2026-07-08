# Transform: mover, rotar, escalar

La propiedad `transform` te permite mover, girar, escalar o inclinar visualmente un elemento sin tocar ni una sola propiedad del modelo de caja (`width`, `top`, `margin`...). Es, junto a `opacity`, la base de casi cualquier animación fluida en la web moderna: un botón que crece al pasar el ratón, una tarjeta que gira sobre sí misma, un menú que se desliza hacia dentro. Entender cómo funciona —y sobre todo *por qué* es tan barata para el navegador comparada con animar propiedades de layout— es imprescindible para construir interfaces que se sientan ágiles incluso en móviles de gama baja.

## Por qué `transform` no toca el flujo del documento

Cuando cambias `width`, `top` o `margin`, el navegador tiene que recalcular la posición y el tamaño de ese elemento **y de todos los que dependen de él**: eso es *reflow* (o *layout*), un proceso caro. `transform`, en cambio, actúa sobre una etapa posterior del pipeline de renderizado: modifica el espacio de coordenadas en el que se pinta el elemento, cambiando su forma y posición visual **sin alterar el flujo normal del documento**. El resto de la página no se entera de que ese elemento se movió, giró o escaló: para el layout, sigue ocupando exactamente el mismo hueco que ocupaba antes.

Esto tiene una consecuencia práctica enorme: como no afecta al layout ni al pintado del resto de la página, el navegador puede promocionar el elemento a su propia capa de composición y animar el `transform` casi por completo en la GPU, fuera del hilo principal. Es la misma razón por la que `opacity` es igual de barata de animar. Cambiar `top` o `width` en cada fotograma, en cambio, obliga a recalcular layout y a repintar en el hilo principal en cada paso, lo que arruina la fluidez en dispositivos modestos.

!!! warning "Un `transform` distinto de `none` crea un nuevo contexto de apilamiento"

    Aplicar cualquier `transform` (aunque sea uno casi imperceptible como `scale(0.999)`) convierte al elemento en un **contexto de apilamiento** y, además, lo transforma en el **bloque contenedor** de cualquier descendiente con `position: absolute` o `position: fixed`. Es un efecto secundario poco intuitivo: si envuelves contenido con `position: fixed` dentro de un ancestro con `transform`, ese elemento fijo dejará de posicionarse respecto al viewport y pasará a posicionarse respecto al ancestro transformado. Tenlo en cuenta antes de añadir un `transform` "inocente" a un contenedor de layout.

## Funciones de transformación en 2D

Todas estas funciones se usan como valor de la propiedad `transform` y pueden combinarse en una misma declaración.

### `translate()`: mover

```css
.caja {
  transform: translate(50px, 20px); /* eje X, eje Y */
}

.caja-horizontal {
  transform: translateX(50px); /* solo en X */
}

.caja-vertical {
  transform: translateY(-20%); /* solo en Y, admite porcentajes */
}
```

Con un único argumento, `translate(x)` mueve solo en el eje horizontal. Un detalle importante: cuando usas porcentajes, se calculan **respecto al propio tamaño de la caja del elemento**, no respecto a su contenedor (a diferencia de `top`/`left`, que sí son relativos al bloque contenedor). Esto es justo lo que hace posible el truco clásico de centrado perfecto sin conocer las dimensiones del elemento:

```css
.modal {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* retrocede la mitad de su propio ancho/alto */
}
```

### `rotate()`: girar

```css
.caja {
  transform: rotate(45deg);
}
```

Gira el elemento sobre un punto fijo (por defecto, su centro, definido por `transform-origin`). Acepta cualquier valor del tipo `<angle>`: `deg`, `grad`, `rad` o `turn` (por ejemplo, `rotate(0.25turn)` equivale a `rotate(90deg)`). En un contexto de escritura de izquierda a derecha (el habitual), los valores positivos giran en el sentido de las agujas del reloj y los negativos en sentido contrario; en un contexto de escritura de derecha a izquierda (`direction: rtl`) el sentido se invierte.

### `scale()`: escalar

```css
.caja {
  transform: scale(1.2); /* 20% más grande en ambos ejes */
}

.caja-ancha {
  transform: scale(2, 0.5); /* el doble de ancho, la mitad de alto */
}
```

Un único valor numérico escala ambos ejes por igual; con dos valores controlas `scaleX` y `scaleY` por separado. Los valores entre `0` y `1` encogen el elemento, los mayores que `1` lo agrandan, y un valor negativo lo invierte (efecto espejo) además de escalarlo.

### `skew()`: inclinar

```css
.caja {
  transform: skew(10deg, 5deg); /* inclina el eje X 10°, el eje Y 5° */
}

.caja-solo-x {
  transform: skewX(15deg);
}
```

Inclina los lados del elemento el ángulo indicado. A diferencia de `translate` y `scale`, `skew` **no tiene equivalente en 3D**: no existen funciones `skewZ()` ni `skew3d()` en la especificación.

## Combinar funciones: el orden importa

Puedes encadenar varias funciones en una misma declaración, separadas por espacios:

```css
.caja {
  transform: translateX(10px) rotate(10deg) translateY(5px);
}
```

Las funciones se aplican de **izquierda a derecha**, y cada una establece un nuevo sistema de coordenadas para la siguiente. Esto significa que el orden cambia el resultado visual, aunque uses exactamente las mismas funciones:

```css
/* Se traslada 200px y LUEGO gira sobre su nuevo centro */
.a {
  transform: translateX(200px) rotate(45deg);
}

/* Se gira sobre su centro original y LUEGO se traslada 200px
   en el eje ya rotado */
.b {
  transform: rotate(45deg) translateX(200px);
}
```

`.a` termina en una posición distinta a `.b` porque, tras `rotate(45deg)`, el eje X ya no apunta en horizontal: la `translateX` posterior se mueve sobre ese eje rotado, no sobre el eje original de la pantalla.

!!! tip "Todo se reduce a una matriz"

    Internamente, cada combinación de funciones se puede expresar como una única `matrix()` (en 2D) o `matrix3d()` (en 3D). Rara vez escribirás una matriz a mano, pero es útil saber que existe: herramientas de animación y el propio DevTools a veces muestran el `transform` calculado en esta forma.

## `transform-origin`: el punto fijo de la transformación

Todas las funciones anteriores giran, escalan o inclinan **alrededor de un punto de referencia**, y ese punto lo define `transform-origin`. Su valor inicial es `50% 50% 0`: el centro exacto del elemento.

```css
.caja {
  transform-origin: top left; /* gira/escala desde la esquina superior izquierda */
  transform: rotate(45deg);
}
```

Acepta palabras clave (`left`, `center`, `right`, `top`, `bottom`), porcentajes o longitudes para los ejes X e Y, y opcionalmente un tercer valor en longitud (nunca porcentaje) para el eje Z en transformaciones 3D:

```css
.caja {
  transform-origin: 20px 10px;      /* x y, ambos como longitud */
  transform-origin: right bottom;   /* esquina inferior derecha */
  transform-origin: center center 30px; /* con desplazamiento en Z */
}
```

Cambiar el origen es lo que diferencia, por ejemplo, una animación de "bisagra" (una imagen que se despliega desde uno de sus bordes) de una simple rotación centrada.

## Transformaciones 3D: añadiendo profundidad

Las funciones 2D tienen equivalentes en 3D que suman un eje Z (hacia dentro y fuera de la pantalla):

| Función 2D | Equivalente 3D |
|---|---|
| `translate(x, y)` | `translate3d(x, y, z)` / `translateZ(z)` |
| `rotate(angle)` (siempre sobre el eje Z) | `rotate3d(x, y, z, angle)` / `rotateX()` / `rotateY()` / `rotateZ()` |
| `scale(x, y)` | `scale3d(x, y, z)` / `scaleZ(z)` |
| `matrix(a, b, c, d, e, f)` | `matrix3d(...)` (16 valores) |

```css
.caja {
  transform: translate3d(20px, 10px, 50px); /* desplaza también en profundidad */
}

.caja {
  transform: rotateX(45deg); /* gira alrededor del eje X (efecto "bisagra" horizontal) */
}

.caja {
  transform: rotate3d(1, 1, 0, 45deg); /* gira sobre un eje diagonal */
}
```

!!! note "`rotate3d()` no son tres ángulos, es un eje más un ángulo"

    Es un error común pensar que `rotate3d(x, y, z, angle)` recibe tres ángulos distintos, uno por eje. En realidad, `x`, `y` y `z` describen un **vector** que define el eje de rotación, y `angle` es el único ángulo que se gira alrededor de ese eje. Por ejemplo, `rotate3d(1, 1, 0, 45deg)` gira 45° alrededor de la diagonal que forman los ejes X e Y, no 45° en X y 45° en Y por separado.

### `perspective`: sin ella, el 3D no se ve

Un `rotateY()` o `translateZ()` por sí solo no produce ninguna sensación de profundidad si el navegador no sabe desde qué distancia estás "mirando" la escena. Para eso existe `perspective`, que puede aplicarse de dos formas distintas:

**Como propiedad, en el elemento padre** — establece un punto de fuga compartido para todos los hijos transformados en 3D, ideal cuando varias piezas deben parecer parte de la misma escena:

```css
.escena {
  perspective: 800px; /* cuanto más bajo, más dramática la distorsión 3D */
}

.tarjeta {
  transform: rotateY(30deg);
}
```

**Como función, dentro del propio `transform`** — aplica la perspectiva solo a ese elemento, de forma aislada:

```css
.tarjeta {
  transform: perspective(800px) rotateY(30deg);
}
```

En ambos casos el valor es una longitud (nunca un porcentaje): valores bajos (por ejemplo `200px`) generan una distorsión muy pronunciada, como mirar de muy cerca; valores altos (`1500px` o más) generan un efecto sutil, como mirar desde lejos. El punto de fuga se puede reposicionar con `perspective-origin` (por defecto, el centro del elemento).

## `transform-style: preserve-3d`: que los hijos vivan en el mismo espacio 3D

Por defecto (`transform-style: flat`), cuando un elemento transformado en 3D tiene hijos que también aplican su propio `transform`, esos hijos se **aplanan** sobre el plano del padre antes de renderizarse: cualquier `translateZ` o `rotate` que apliques al hijo pierde su efecto de profundidad relativo a la escena.

```css
.grupo {
  transform: rotateX(45deg);
  transform-style: preserve-3d; /* sin esto, .grupo__hijo se aplana */
}

.grupo__hijo {
  transform: translateZ(60px); /* con preserve-3d, se ve realmente "más cerca" */
}
```

Con `transform-style: preserve-3d` en `.grupo`, sus hijos dejan de aplanarse: cada uno conserva su propia posición en el espacio 3D compartido con el padre, y por eso `.grupo__hijo` aparece realmente desplazado en profundidad respecto al resto de la escena, no solo respecto a su propio plano. Es la propiedad que hace posibles efectos como cubos 3D o tarjetas que giran mostrando dos caras distintas: sin ella, todo el conjunto quedaría aplastado en un único plano. Ten en cuenta que `transform-style` **no se hereda**, así que si tienes varios niveles de anidamiento 3D, hay que declararla en cada nivel intermedio que la necesite.

!!! tip "Soporte de navegadores"

    El soporte de transformaciones 2D (`transform`, `transform-origin`) es prácticamente universal desde hace más de una década en todos los navegadores modernos. Las transformaciones 3D (`translate3d`, `rotate3d`, `perspective`, `transform-style: preserve-3d`) también tienen soporte muy amplio (más del 96% de uso global), con la salvedad de que Internet Explorer 10-11 solo las implementa de forma parcial. Consulta el detalle actualizado en [caniuse.com/transforms2d](https://caniuse.com/transforms2d) y [caniuse.com/transforms3d](https://caniuse.com/transforms3d).

!!! tip "Alternativa moderna: propiedades individuales `translate`, `rotate` y `scale`"

    Además de la función `transform`, CSS define las propiedades independientes `translate`, `rotate` y `scale` (sin equivalente para `skew`), que permiten animar cada transformación por separado sin tener que reescribir todo el valor de `transform` cada vez. Cuando se combinan con `transform`, el orden de aplicación es siempre fijo: primero `translate`, luego `rotate`, después `scale` y por último `transform`. Tienen buen soporte en navegadores modernos desde 2022 (Chrome 104; Firefox y Safari ya lo soportaban antes), pero no están pensadas para proyectos que deban dar soporte a navegadores antiguos. Revisa el estado en [caniuse.com/wf-individual-transforms](https://caniuse.com/wf-individual-transforms).

## Ver también

- [Transiciones](transiciones.md)
- [Keyframes y animation](keyframes.md)
- [Scroll-driven animations](scroll-driven-animations.md)
- [Positioning](../layout/positioning.md)

## Fuentes

- [MDN: transform](https://developer.mozilla.org/en-US/docs/Web/CSS/transform)
- [MDN: transform-origin](https://developer.mozilla.org/en-US/docs/Web/CSS/transform-origin)
- [MDN: transform-style](https://developer.mozilla.org/en-US/docs/Web/CSS/transform-style)
- [MDN: perspective](https://developer.mozilla.org/en-US/docs/Web/CSS/perspective)
- [MDN: Using CSS transforms](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_transforms/Using_CSS_transforms)
- [MDN: CSS and JavaScript animation performance](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/CSS_JavaScript_animation_performance)
- [web.dev: Finer grained control over CSS transforms with individual transform properties](https://web.dev/articles/css-individual-transform-properties)
- [W3C: CSS Transforms Module Level 1](https://www.w3.org/TR/css-transforms-1/)
- [W3C: CSS Transforms Module Level 2 (funciones 3D y propiedades individuales)](https://www.w3.org/TR/css-transforms-2/)
- [caniuse: CSS3 2D Transforms](https://caniuse.com/transforms2d)
- [caniuse: CSS3 3D Transforms](https://caniuse.com/transforms3d)
- [caniuse: Individual transform properties](https://caniuse.com/wf-individual-transforms)
