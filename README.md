# Landing de C.R.O.P.

Página estática de una sola pantalla larga. Sin framework, sin build, sin
dependencias de runtime: `index.html`, `styles.css` y lo que hay en `assets/`.

Para verla, abrí `index.html` en el navegador. No hace falta servidor.

```
index.html      la página entera
styles.css      el único archivo de estilos
assets/
  favicon.svg   provisorio, dibujado acá
  og.png        imagen para compartir, 1200 × 630
  og.html       la fuente de og.png, para poder regenerarla
  README.md     dónde van los PNG de los logos
```

---

## Qué decisiones tomé, y por qué

### La página es clara; el navy aparece una sola vez

Es la regla de superficie del proyecto ("Estación Base"): todo en superficie
clara y el oscuro reservado para el panel donde hay un gráfico con eje. En esta
página eso pasa exactamente una vez, en **"Un número, y lo que lo sostiene"**,
que es el único lugar con una serie sobre un eje temporal. El resto —incluidos
los medidores y las listas de datos— se queda en claro.

### El contorno de doble línea es la firma gráfica

El proyecto ya tenía un recurso propio y medido: para dibujar el borde de un
lote, el *casing* de las cartas topográficas (halo oscuro `#0C1B2C` de 6 px con
un núcleo blanco de 2,6 px encima) le ganó a los rellenos de color, al velo
oscuro y al tinte sobre los cinco fondos satelitales típicos.

Lo usé como gesto repetido y en dos lugares nada más, para que sea una firma y
no un patrón: el contorno del lote en el hero, y el subrayado del título de
**"De dónde salen los números"**, que es la sección que sostiene todo lo demás.

Los trazos llevan `vector-effect="non-scaling-stroke"`, así que el espesor
medido se respeta en píxeles de pantalla a cualquier ancho, en vez de encogerse
cuando el SVG escala. Es la única forma de que "6 px" quiera decir 6 px.

### El hero muestra el lote, no una cifra

Elegí la dirección del lote y su medición en vez del titular grande sobre
gradiente. El polígono es irregular, con lindes rectos de distinto largo, una
esquina en jota y una muesca cóncava: un lote real, nunca un rectángulo. Debajo,
la grilla de 10 m, que es la resolución a la que mide Sentinel-2 de verdad, con
una celda destacada y su cota.

El terreno son parcelas planas, generadas a partir de dos lindes casi verticales
y dos casi horizontales. Es un **dibujo**, y tiene que leerse como dibujo: no hay
ninguna captura de pantalla en toda la página, y el gráfico del panel navy dice
en su epígrafe que es un esquema de la forma de una serie, no una medición.

### Un solo momento animado

El contorno del lote se traza una vez al cargar, y nada más. El estado por
defecto en el CSS es el lote **ya dibujado**; la animación vive adentro de
`@media (prefers-reduced-motion: no-preference)` y sólo se enciende encima. Si
falla, o si alguien pidió menos movimiento, el contorno igual está ahí. No hay
entradas al scrollear ni transiciones en hover repartidas por la página.

### Tipografía: Archivo, una sola familia

**[Archivo](https://fonts.google.com/specimen/Archivo)**, de Omnibus-Type, una
fundidora de Buenos Aires. Es una grotesca dibujada para señalética vial y para
texto de alto rendimiento: aguanta el peso alto sin engordar y se lee chica.
Que sea argentina, para un producto agropecuario argentino, no es decoración:
es la razón por la que la elegí sobre las alternativas obvias.

Una sola familia, con la jerarquía cargada por el peso. Dos grotescas parecidas
leen como un error, no como un sistema, y acá no hacía falta una segunda voz.

**Verifiqué las características sobre el webfont que Google sirve de verdad**
—no sobre la ficha del specimen— abriendo el `.woff2` con `fontTools`:

| | |
|---|---|
| `tnum` (cifras tabulares) | **sí**, y como el default es `pnum` hay que encenderlo a mano |
| Cifras lining | sí; no existe `onum`, no hay cifras de caja baja |
| `ñ á é í ó ú ü Ñ Á É Í Ó Ú ¿ ¡` | completo en el subset `latin` |
| Eje `wght` | variable, 100 → 900 |

Las tabulares están encendidas en `body` con
`font-variant-numeric: tabular-nums lining-nums`, porque la página está llena de
cifras y de columnas. Se carga desde Google Fonts con `font-display: swap`.

**La escala son siete escalones reales** (13 · 15 · 17 · 21 · 27 · 34 px, más uno
de display fluido que llega a 62): entre dos cualesquiera hay más de 3 px. Dos
tamaños que se llevan menos que eso no son dos tamaños.

### Color y contraste: medidos, no estimados

Todos los colores viven como custom properties arriba de `styles.css`. Abajo de
`:root` no hay ni un hex suelto.

Cada par lleva su contraste anotado al lado, calculado con la fórmula de WCAG
2.1. Los pares que no estaban en la ficha los medí yo; el que hacía falta era
**texto atenuado sobre el navy del panel: `#A8C2DC`, 7,56:1**.

Respeté las dos trampas que el proyecto ya tenía medidas, y las volví a
confirmar:

- El ámbar de marca `#F9BC3C` da **1,65:1** como tinta: no se usa como color de
  texto en ningún lado. Para ámbar escrito está `--ambar-tinta: #8A5A00`.
- El azul de marca `#154D7E` sobre el navy da **1,59:1**: invisible. El dato
  sobre oscuro es `#5AB7F0`.

**Auditoría sobre lo renderizado** (no sobre la tabla): recorrí cada nodo con
texto de la página con Playwright, leí el color calculado y el fondo efectivo
del primer ancestro opaco, y comparé contra el umbral que le corresponde por
tamaño y peso. **Cero fallas a 360 px y a 1280 px.**

### Accesibilidad y semántica

Verificado automáticamente: `lang="es-AR"`, un solo `<h1>`, la secuencia de
encabezados sin saltos de nivel, `alt` en toda imagen, nombre accesible en todo
SVG, y `<header> <nav> <main> <footer>` presentes. El foco de teclado es un
contorno sólido de 3 px con 3 px de separación y se ve en todo lo enfocable,
empezando por el enlace de salto al contenido. Sin desborde horizontal en 360,
390, 768, 1024 ni 1280 px.

### Sobre el copy

Castellano rioplatense, voz activa, sin signos de admiración y sin adjetivos de
venta. No hay ninguna cifra de negocio, ni usuarios, ni hectáreas, ni
testimonios, ni logos de clientes: no existen, así que no están. Los únicos
números de la página son los 10 m de resolución de Sentinel-2 y las 43 rutas en
13 grupos de la API.

---

## Lo que quedó pendiente de decisión del equipo

1. **Los tres verdes.** La ficha de marca dice `#1A6C4A`, `logo-full.png` usa
   `#125237` y `logo-icon.png` usa `#198759`. Todo lo que dibujé está pintado
   con el de la ficha y no toqué los PNG. Por eso ninguno de los dos logos queda
   apoyado contra una superficie verde. Igual se va a notar cuando estén los dos
   juntos. Hay que decidir: se rehacen los logos con `#1A6C4A`, o se corrige la
   ficha.

2. **Faltan los PNG de los logos.** La página ya está cableada a
   `assets/logo-icon.png` y `assets/logo-full.png`, y muestra un wordmark
   tipográfico mientras no estén. Los detalles están en
   [`assets/README.md`](assets/README.md), incluido que `logo-full.png` pesa
   388 KB para dibujarse a 112 px y hay que optimizarlo.

3. **No hay masters vectoriales** de ninguno de los dos logos, sólo PNG.

4. **No hay ninguna acción de cierre.** No se decidió si va el repositorio, un
   mail o un video, así que la página termina en el pie, sin botón. No inventé
   un formulario de demo ni una lista de espera. Cuando se decida, va una sola
   acción y va acá.

5. **El dato de la demora del perito no se publicó.** Se decidió no usarlo. El
   hero funciona sin él.

6. **No hay capturas reales de la app**, así que todo lo visual de la página son
   esquemas dibujados, marcados como tales en sus epígrafes.

7. **Los nombres del equipo no están.** La sección dice "cuatro estudiantes de
   secundaria técnica argentina" y nada más.

---

## Regenerar la imagen de compartir

`assets/og.png` sale de `assets/og.html`, que tiene la fuente embebida para no
depender de la red. Después de cambiar el copy:

```bash
chromium --headless --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1200,630 \
  --virtual-time-budget=4000 \
  --screenshot=assets/og.png "file://$PWD/assets/og.html"
```
