# CSSdocs

Documentación viva y personal sobre CSS, pensada para dominarlo a nivel profesional en desarrollo Frontend.

- 📖 **Sitio publicado:** https://pablohurtadogonzalo86.github.io/CSSdocs/
- 🎓 **Basada en:** fuentes oficiales (MDN Web Docs, especificaciones W3C/CSSWG, web.dev) + el curso ["Curso de CSS desde cero completo y GRATIS"](https://www.youtube.com/playlist?list=PLUofhDIg_38q7l8gV4IVCz_pjUeyD99_j) de [midulive](https://www.youtube.com/@midulive).
- 🤖 **Vigilante semanal automático:** cada semana, un workflow de GitHub Actions revisa fuentes oficiales (repo de contenido de MDN, `caniuse-lite`, estado de especificaciones CSSWG) y abre un Issue con los cambios detectados desde la última revisión, para mantener la documentación al día sin depender de la memoria de nadie.

## Estructura

```
docs/
├── fundamentos/       Sintaxis, cascada, especificidad, herencia, selectores, unidades, colores, modelo de caja
├── layout/             Display, flujo normal, overflow, positioning, flexbox, grid, multi-columna
├── responsive/         Media queries, container queries, unidades y funciones responsivas
├── tipografia/         Fuentes web y propiedades de texto
├── animaciones/        Transiciones, @keyframes, transform, scroll-driven animations
├── moderno/            Custom properties, :has()/:is()/:where(), nesting, @layer, @scope, color moderno
├── arquitectura/       Metodologías y organización de CSS a escala
├── cheatsheets/        Chuletas rápidas de Flexbox, Grid y selectores
├── curso-midulive/     Notas y enlaces a los resúmenes del curso en Google Docs
└── novedades/          Changelog donde aterrizan los hallazgos del vigilante semanal
```

## Desarrollo local

```bash
pip install -r requirements.txt
mkdocs serve
```

## Licencia

MIT — ver [LICENSE](LICENSE).
