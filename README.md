# Landing de C.R.O.P.

Página estática de una sola pantalla larga. Sin framework, sin build y sin
dependencias: `index.html`, `styles.css` y lo que hay en `assets/`. El único
JavaScript son cuarenta líneas propias, al final del HTML.

Para verla, abrí `index.html` en el navegador. No hace falta servidor.

```
index.html      la página entera
styles.css      el único archivo de estilos
assets/
  logo-full.png  emblema + wordmark, para el pie
  logo-mark.png  sólo el emblema, para la barra superior
  logo-icon.png  el tile navy original del equipo
  favicon.png    el tile, como favicon y apple-touch-icon
  og.png         imagen para compartir, 1200 × 630
  og.html        la fuente de og.png, para poder regenerarla
  README.md      qué se le hizo a cada logo, y por qué
```

---

## Qué decisiones tomé, y por qué

### Está diseñada para escritorio y se pliega al teléfono

La composición principal es la de pantalla ancha: el hero a dos columnas con el
campo sangrando hasta el borde de la ventana, los tres tiempos sobre un eje
horizontal, los cuatro pasos en fila, el panel de medición a dos columnas y las
fuentes en dos columnas. Las consultas de ancho mínimo van juntando todo eso en
una sola columna hacia abajo. Verificado sin desborde horizontal a 360, 390,
768, 1024 y 1280 px.

### Dos gestos gráficos, los dos del proyecto

**El contorno de doble línea.** Para dibujar el borde de un lote, el *casing* de
las cartas topográficas (halo oscuro `#0C1B2C` de 6 px con un núcleo blanco de
2,6 px encima) le ganó a los rellenos de color, al velo oscuro y al tinte sobre
los cinco fondos satelitales típicos. Aparece en el lote del hero, en el ícono
del primer paso y como subrayado del título de **"De dónde salen los números"**.
Los trazos llevan `vector-effect="non-scaling-stroke"`, así el espesor medido se
respeta en píxeles de pantalla a cualquier ancho en vez de encogerse cuando el
SVG escala. Es la única forma de que "6 px" quiera decir 6 px.

**La órbita del isotipo.** El logo tiene una elipse azul que rodea a la plántula,
con un satélite y un destello. La misma órbita cruza el hero de borde a borde y
pasa por detrás del lote, con el mismo satélite y el mismo destello, y vuelve
como un arco tenue en el pie. Es lo que hace que la página se reconozca como de
C.R.O.P. y no como de cualquier otra cosa.

### El hero muestra el lote, no una cifra

El polígono es irregular, con lindes rectos de distinto largo, esquinas marcadas
y una muesca cóncava: un lote real, nunca un rectángulo. Debajo, la grilla de
10 m, que es la resolución a la que mide Sentinel-2 de verdad, con una celda
destacada y su cota.

El terreno son parcelas planas, generadas a partir de dos lindes casi verticales
y dos casi horizontales, que es como se divide el campo. Es un **dibujo** y tiene
que leerse como dibujo: no hay ninguna captura de pantalla en toda la página, y
el gráfico del panel oscuro dice en su epígrafe que es un esquema de la forma de
una serie, no una medición.

El lienzo del dibujo tiene proporción 0,93 a propósito: queda entre la columna de
escritorio (0,86) y el cuadrado del teléfono (1,0), así el recorte del `slice`
nunca pasa del 4 % por lado y la cota, el satélite y el lote quedan siempre
adentro del cuadro.

### El color de marca hace trabajo, no decora

Los tres tiempos llevan cada uno un color con sentido: **azul** para *Antes*
(Órbita & Datos, mirar adelante), **ámbar** para *Durante* (Predicción & Alerta,
pasó algo) y **verde** para *Después* (Cosecha). Las fuentes llevan etiquetas de
color por dominio. Los cuatro usos llevan un filete del color que les toca.

### La barra superior

Al tope de la página la barra se deja lisa —sin filete ni desenfoque— para que
nada corte el dibujo del hero, y el borde de arriba del dibujo se **disuelve**
en el fondo con un degradado en vez de cortarse a 90° contra la barra. Apenas se
scrollea, la barra toma un velo translúcido, su filete y una sombra mínima, que
es lo que la despega del contenido que le pasa por abajo.

El estado por defecto en el CSS es el segundo, el seguro: **sin JavaScript la
barra igual se ve bien**, sólo que no se alisa al llegar al tope.

Las etiquetas de la nav son cortas a propósito. Con las largas de antes, en
teléfono se partían en dos filas y la barra se comía **181 px, el 21 % de la
pantalla** —bastante arriba del 15 % donde una barra fija empieza a sentirse
opresiva—. Ahora mide **67 px**, porque la nav corre en horizontal en vez de
envolverse, con un difuminado en los bordes que avisa que hay más. En escritorio
mide 84 px.

El link de la sección que estás mirando queda marcado, con
`IntersectionObserver`. Y las secciones llevan `scroll-margin-top`, así un
anclaje frena abajo de la barra y no atrás: antes funcionaba de casualidad,
porque el padding de las secciones era generoso.

### El JavaScript: cuarenta líneas, propias

Es todo el que hay, y hace exactamente dos cosas: alisar la barra cuando estás
al tope, y marcar la sección visible. Sin dependencias, sin build, sin bundle.
El scroll va con `requestAnimationFrame` y listener pasivo.

### Los encabezados de sección van a dos columnas

En pantalla ancha, el título a la izquierda y la bajada a la derecha, apoyados
sobre la misma línea de base. Con el título solo, ocupaba el 40 % izquierdo y
dejaba media pantalla vacía.

### Un solo momento animado

El contorno del lote y la órbita se trazan una vez al cargar, juntos, y nada más.
El estado por defecto en el CSS es el lote **ya dibujado**; la animación vive
adentro de `@media (prefers-reduced-motion: no-preference)` y sólo se enciende
encima. Si falla, o si alguien pidió menos movimiento, el dibujo igual está ahí.
No hay entradas al scrollear ni transiciones en hover repartidas por la página.

### Tipografía: Archivo, una familia con dos ejes

**[Archivo](https://fonts.google.com/specimen/Archivo)**, de Omnibus-Type, una
fundidora de Buenos Aires. Es una grotesca dibujada para señalética vial y para
texto de alto rendimiento: aguanta el peso alto sin engordar y se lee chica. Que
sea argentina, para un producto agropecuario argentino, no es decoración: es la
razón por la que la elegí sobre las alternativas obvias.

Archivo es variable en **dos** ejes, y ahí está el sistema: el **peso** carga la
jerarquía y el **ancho** separa las dos voces. Los títulos van en Archivo
Expanded (`font-stretch: 114%`) y el texto en el ancho normal. Es una sola
familia con dos voces claramente distintas, en vez de dos grotescas parecidas
que leerían como un error y no como un sistema — y es un solo archivo de fuente,
sin un pedido más.

**Verifiqué las características sobre el webfont que Google sirve de verdad**
—no sobre la ficha del specimen— abriendo el `.woff2` con `fontTools`:

| | |
|---|---|
| Ejes servidos | `wght` 100 → 900 **y** `wdth` 62 → 125, en un solo archivo |
| `tnum` (cifras tabulares) | **sí**, y como el default es `pnum` hay que encenderlo a mano |
| Cifras lining | sí; no existe `onum`, no hay cifras de caja baja |
| `ñ á é í ó ú ü Ñ Á É Í Ó Ú ¿ ¡` | completo en el subset `latin` |

Las tabulares están encendidas en `body` con
`font-variant-numeric: tabular-nums lining-nums`, porque la página está llena de
cifras y de columnas. Se carga desde Google Fonts con `font-display: swap`.

**La escala es la del proyecto** (13 · 15 · 17 · 21 · 26 px) más dos escalones de
display fluidos, hasta 44 y 58 px.

### Los logos entraron medidos

Cuando el equipo subió los PNG los medí pixel a pixel antes de cablearlos. El
azul de `logo-full` es `#154D7E` y el fondo de `logo-icon` es `#112D4E`: los dos
**coinciden exacto** con `--azul` y `--navy` de la página, lo que confirma que la
familia oscura salió del fondo del ícono. El verde es el único que no coincide, y
son tres distintos.

También había trabajo de optimización: `logo-full.png` venía en 379 KB con el
77 % de sus píxeles transparentes para dibujarse a 164 px. Recortado y cuantizado
quedó en 22 KB. Y la barra superior usa un recorte con **sólo el emblema**,
porque el tile del ícono trae el wordmark horneado y a 44 px es ilegible. Todo el
detalle, y qué se le hizo a cada archivo, en
[`assets/README.md`](assets/README.md).

### Color y contraste: medidos, no estimados

Todos los colores viven como custom properties arriba de `styles.css`. Abajo de
`:root` no hay ni un hex suelto. Cada par lleva su contraste anotado al lado,
calculado con la fórmula de WCAG 2.1.

Dos cosas que salieron de medir y que cambiaron el diseño:

- **El ámbar de marca sobre el navy del panel da 8,14:1.** El color que es
  ilegible como tinta sobre claro (1,65:1) sí funciona como tinta sobre oscuro.
  Por eso la caída abrupta del gráfico está marcada en ámbar: es el único lugar
  de la página donde "Predicción & Alerta" puede ser color de dato, y es
  justamente donde corresponde.
- **Sobre las bandas teñidas, `--tinta-3` se acerca al límite** (4,52:1 sobre la
  banda verde, y 4,43:1 sobre un tinte azul que por eso descarté). Regla que
  quedó en el CSS: el texto atenuado vive sólo sobre fondo claro puro; sobre una
  banda va `--tinta-2`.

Se mantienen las dos trampas que el proyecto ya tenía medidas, las dos
reconfirmadas: el ámbar de marca como tinta sobre claro da **1,65:1**, y el azul
de marca sobre el navy da **1,59:1** (por eso el dato sobre oscuro es `#5AB7F0`
y no el azul de marca).

**Auditoría sobre lo renderizado**, no sobre la tabla: recorrí cada nodo con
texto de la página con Playwright, leí el color calculado y el fondo efectivo del
primer ancestro opaco, y comparé contra el umbral que le corresponde por tamaño y
peso. **Cero fallas a 360 px y a 1280 px.**

### Accesibilidad y semántica

Verificado automáticamente: `lang="es-AR"`, un solo `<h1>`, la secuencia de
encabezados sin saltos de nivel, `alt` en toda imagen, nombre accesible en todo
SVG, y un solo `<header>`, `<nav>`, `<main>` y `<footer>`. El foco de teclado es
un contorno sólido de 3 px con 3 px de separación y se ve en todo lo enfocable,
empezando por el enlace de salto al contenido.

### Sobre el copy

Castellano rioplatense, voz activa, sin signos de admiración y sin adjetivos de
venta. No hay ninguna cifra de negocio, ni usuarios, ni hectáreas, ni
testimonios, ni logos de clientes: no existen, así que no están. Los únicos
números de la página son los 10 m de resolución de Sentinel-2 y las 43 rutas en
13 grupos de la API.

---

## Lo que quedó pendiente de decisión del equipo

1. **Los tres verdes.** Medidos contando píxeles sobre los PNG: `logo-full` usa
   `#125237`, `logo-icon` usa `#198759` y la ficha dice `#1A6C4A`. La página está
   pintada con el de la ficha y los PNG quedaron intactos, y por eso ningún logo
   queda apoyado contra una superficie verde. Es una decisión del equipo: o se
   rehacen los logos con `#1A6C4A`, o se corrige la ficha.

   La buena noticia es que **el azul y el navy sí coinciden exacto**
   (`#154D7E` y `#112D4E`, distancia 0 contra la paleta de la página), así que el
   verde es el único desacuerdo que queda. Detalle en
   [`assets/README.md`](assets/README.md).

2. **No hay masters vectoriales** de los logos, sólo PNG. La órbita, el satélite
   y el destello de la página están redibujados a mano a partir del isotipo, no
   extraídos de él. Si aparece un SVG conviene rehacerlos desde ahí.

3. **No hay ninguna acción de cierre.** No se decidió si va el repositorio, un
   mail o un video, así que la página termina en el pie, sin botón. No inventé un
   formulario de demo ni una lista de espera. Cuando se decida, va una sola
   acción y va acá.

4. **El pie y el hero son claros, no oscuros.** Un pie en navy quedaría muy bien,
   pero contradice la regla de superficie "Estación Base" (todo claro, el oscuro
   sólo para el panel con gráfico). Respeté la regla. Si el equipo quiere
   revisarla, es una decisión de diseño del producto, no de esta página.

5. **El dato de la demora del perito no se publicó**, por decisión del equipo. El
   hero funciona sin él.

6. **No hay capturas reales de la app**, así que todo lo visual de la página son
   esquemas dibujados, marcados como tales en sus epígrafes.

7. **Los nombres del equipo no están.** La sección dice "cuatro estudiantes de
   secundaria técnica argentina" y nada más.

---

## Publicar

Es HTML y CSS estáticos, así que se publica sin build. En Vercel: importar el
repo y dejar el framework en **Other**, sin comando de build y con el directorio
raíz como salida. También anda en GitHub Pages o en cualquier hosting estático.

Para verla en local alcanza con abrir `index.html` en el navegador. Si algo se
comporta raro con `file://`, `python3 -m http.server 8000` desde la raíz.

---

## Regenerar la imagen de compartir

`assets/og.png` sale de `assets/og.html`, que tiene la fuente embebida para no
depender de la red y reusa la misma geometría del hero.

Usá un viewport real: el `--screenshot` del headless viejo de Chromium
**rinde mal el alto** y deja una franja en blanco abajo.

```bash
python3 - <<'PY'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.goto("file:///RUTA/ABSOLUTA/assets/og.html")
    pg.wait_for_timeout(1500)
    pg.screenshot(path="assets/og.png")
    b.close()
PY
```
