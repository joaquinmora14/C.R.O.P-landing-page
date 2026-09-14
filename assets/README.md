# assets

## Los logos

Los subió el equipo en el commit `bfbb758`. Acá están, optimizados y con los
recortes que hacía falta hacer. **No se les tocó ningún color.**

| Archivo | Qué es | Dónde se usa | Peso |
|---|---|---|---|
| `logo-full.png` | emblema + wordmark, fondo transparente | pie de página, a 164 px | 22 KB |
| `logo-mark.png` | **sólo el emblema**, recortado de `logo-full` | barra superior, a 44 px | 15 KB |
| `logo-icon.png` | tile navy con esquinas redondeadas | — | 3 KB |
| `favicon.png` | el tile, a 180 px | `<link rel="icon">` y apple-touch-icon | 4 KB |

### Qué se les hizo, y por qué

**Optimización.** `logo-full.png` venía en 1003 × 972 y **379 KB**, con el 77 %
de sus píxeles totalmente transparentes, para dibujarse a 164 px. Se le recortó
el margen vacío, se bajó a 433 × 460 y se cuantizó a paleta indexada de 96
colores: **quedó en 22 KB, un 94 % menos.** Son logos de colores planos, así que
la paleta indexada no les hace daño: los colores dominantes se mueven una o dos
unidades (`#154D7E` → `#154C7D`), que es imperceptible. Mismo tratamiento al
ícono: 27 KB → 3 KB.

**`logo-mark.png`: por qué existe.** `logo-icon.png` es un tile navy que trae el
wordmark "C.R.O.P." horneado adentro. A 44 px en la barra superior ese texto es
una mancha ilegible, y además duplica al wordmark tipográfico que va al lado.
Encima es el único elemento oscuro en una página que por regla de superficie es
clara. Así que la barra usa el **emblema solo**, recortado de `logo-full.png`
por la franja de píxeles transparentes que separa el emblema del wordmark. Es un
recorte, no un retoque: ni un color cambiado.

El tile navy queda para el favicon y el apple-touch-icon, que es exactamente
para lo que sirve un ícono de app con fondo y esquinas redondeadas.

### Los colores, medidos

Contando píxeles sobre los PNG que subió el equipo:

| | Medido | Paleta de la página | |
|---|---|---|---|
| Azul de `logo-full` | `#154D7E` | `--azul` `#154D7E` | **coincide exacto** |
| Fondo de `logo-icon` | `#112D4E` | `--navy` `#112D4E` | **coincide exacto** |
| Verde de `logo-full` | `#125237` | `--verde` `#1A6C4A` | no coincide |
| Verde de `logo-icon` | `#198759` | `--verde` `#1A6C4A` | no coincide, y distinto del anterior |

O sea: **el azul y el navy son canon y no hay nada que discutir ahí.** Confirma
de paso que la familia oscura del proyecto salió del fondo del ícono, como decía
la ficha.

**El verde sigue siendo el único desacuerdo real**, y son tres distintos. La
página está pintada con el de la ficha (`#1A6C4A`) y los PNG quedaron intactos.
Por eso ningún logo queda apoyado contra una superficie verde: en la barra el
emblema va sobre fondo claro y en el pie también. Es una decisión del equipo: o
se rehacen los logos con `#1A6C4A`, o se corrige la ficha.

### Lo que sigue faltando

**No hay masters vectoriales**, sólo PNG. La órbita, el satélite y el destello
que dibuja la landing en el hero y en el pie están **redibujados a mano** a
partir del isotipo: son formas propias de esta página, no recortes del PNG. Si
aparece un SVG del logo, conviene rehacerlas desde ahí.

## og.png

Imagen para compartir, 1200 × 630, generada desde `og.html` (mismo directorio),
que reusa la geometría del hero, lleva el logo real y tiene la tipografía
embebida. El comando para regenerarla está en el
[README de la raíz](../README.md).
