# assets

## Logos — faltan los PNG

La landing ya está cableada a estos dos archivos. Copialos acá con **exactamente
estos nombres** y aparecen solos, sin tocar una línea de código:

| Archivo | Dónde se usa | Tamaño al que se dibuja |
|---|---|---|
| `logo-icon.png` | barra superior | 34 × 34 px |
| `logo-full.png` | pie de página | 112 px de ancho |

Salen de `crop-front/crop-rn/assets/images/` en el repo del proyecto grande.

Mientras no estén, la página **no muestra imagen rota**: cada `<img>` lleva un
`onerror` que se saca a sí mismo del DOM, y queda el wordmark tipográfico
"C.R.O.P." compuesto en Archivo con el azul de marca. Es un fallback, no la
solución: el logo real tiene que estar.

### Antes de commitearlos, dos cosas

1. **Optimizalos.** `logo-full.png` pesa 388 KB para dibujarse a ~112 px. Pasalo
   por `oxipng -o4` o `pngquant`, y si podés generá también un `.webp` al lado.
   Hoy no hay masters vectoriales de ninguno de los dos: eso sigue pendiente.
2. **El verde no coincide.** La ficha de marca dice `#1A6C4A`, `logo-full.png`
   usa `#125237` y `logo-icon.png` usa `#198759`. Son tres verdes distintos,
   medidos contando píxeles. La página está pintada con el de la ficha. Por eso
   ninguno de los dos logos queda pegado a una superficie verde: en la barra
   superior el ícono va contra fondo claro y en el pie el logo completo también.
   Igual se va a notar si mirás los dos verdes juntos. **Es una decisión del
   equipo**: o se rehacen los logos con `#1A6C4A`, o se corrige la ficha.

## favicon.svg

Provisorio, dibujado para esta landing: el contorno de doble línea reducido a
cinco vértices sobre el navy de panel, para que siga leyéndose a 16 px. Cuando
tengan `logo-icon.png` optimizado pueden reemplazarlo y cambiar el `<link
rel="icon">` de `index.html`.

## og.png

Imagen para compartir, 1200 × 630. Generada desde `og.html` (en este mismo
directorio) con Chromium. Para regenerarla después de un cambio de copy:

```
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1200,'height':630}, device_scale_factor=2)
    pg.goto('file:///ruta/absoluta/a/assets/og.html'); pg.wait_for_timeout(1200)
    pg.screenshot(path='assets/og.png'); b.close()"
```
