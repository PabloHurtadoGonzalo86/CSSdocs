import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://pablohurtadogonzalo86.github.io',
  base: '/CSSdocs',
  integrations: [
    starlight({
      title: 'CSSdocs',
      description: 'Documentación viva de CSS para dominio profesional en Frontend',
      locales: {
        root: {
          label: 'Español',
          lang: 'es',
        },
      },
      lastUpdated: true,
      editLink: {
        baseUrl: 'https://github.com/PabloHurtadoGonzalo86/CSSdocs/edit/main/',
      },
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/PabloHurtadoGonzalo86/CSSdocs',
        },
        {
          icon: 'youtube',
          label: 'Curso de referencia (midulive)',
          href: 'https://www.youtube.com/@midulive',
        },
      ],
      sidebar: [
        { label: 'Inicio', link: '/' },
        {
          label: 'Fundamentos',
          items: [
            'fundamentos/que-es-css',
            'fundamentos/cascada-especificidad-herencia',
            'fundamentos/selectores',
            'fundamentos/unidades',
            'fundamentos/colores',
            'fundamentos/modelo-de-caja',
          ],
        },
        {
          label: 'Layout',
          items: [
            'layout/display-y-flujo-normal',
            'layout/overflow',
            'layout/positioning',
            'layout/flexbox',
            'layout/grid',
            'layout/multicolumna',
          ],
        },
        {
          label: 'Diseño responsivo',
          items: [
            'responsive/media-queries',
            'responsive/container-queries',
            'responsive/unidades-y-funciones',
          ],
        },
        { label: 'Tipografía', items: ['tipografia/fuentes-y-texto'] },
        {
          label: 'Animaciones',
          items: [
            'animaciones/transiciones',
            'animaciones/keyframes',
            'animaciones/transform',
            'animaciones/scroll-driven-animations',
          ],
        },
        {
          label: 'CSS moderno',
          items: [
            'moderno/custom-properties',
            'moderno/selectores-modernos',
            'moderno/nesting',
            'moderno/cascade-layers',
            'moderno/scope',
            'moderno/color-moderno',
          ],
        },
        { label: 'Arquitectura CSS', items: ['arquitectura/metodologias-y-organizacion'] },
        {
          label: 'Cheatsheets',
          items: [
            'cheatsheets/flexbox-cheatsheet',
            'cheatsheets/grid-cheatsheet',
            'cheatsheets/selectores-cheatsheet',
          ],
        },
        { label: 'Curso de midulive', items: ['curso-midulive'] },
        { label: 'Novedades', items: ['novedades/changelog'] },
      ],
    }),
  ],
});
