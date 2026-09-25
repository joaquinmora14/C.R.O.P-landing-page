# Versión previa de la landing

Esta es la **primera landing**, tal como quedó antes del rediseño. No es una
reconstrucción: son los archivos del commit `ff59288`, sacados del historial sin
tocarles una línea.

Abrí `index.html` en el navegador. Anda sola, con sus propios `assets/`.

## Por qué los logos no aparecen

Porque en ese momento **todavía no estaban**. Cada `<img>` lleva un `onerror`
que se saca a sí mismo del DOM, así que la página cae en el wordmark
tipográfico. Se ve exactamente como se veía entonces, que es el punto de
guardarla.

## Qué cambió del previo al final

| | Previa (`ff59288`) | Final |
|---|---|---|
| Ancho útil | 1140 px | 1280 px |
| Tipografía | Archivo, sólo eje de peso | Archivo con peso **y ancho**: títulos en Expanded |
| Título más grande | hasta 62 px | hasta 58 px, pero expandido |
| Bandas de color | ninguna | verde y ámbar |
| Isotipo en la página | no está | la órbita cruza el hero y vuelve en el pie |
| Logos | no existían | emblema en la barra, logo completo en el pie |
| Navegación | 4 etiquetas largas | 5 cortas, con la sección actual marcada |
| JavaScript | nada | 40 líneas propias |
| Cifras del cierre | rutas de API, grupos, React Native | lado del píxel, índices, fuentes públicas |

### Las tres correcciones que más se notan

1. **El hero.** Antes el dibujo del campo era un recuadro al lado del texto.
   Ahora sangra hasta el borde de la ventana, con la órbita del isotipo
   cruzándolo y el borde de arriba disolviéndose en el fondo.

2. **El color.** La previa es casi toda azul y gris. Siendo un producto del
   agro, eso estaba al revés: el verde pasó a llevar las bandas, los filetes de
   las secuencias y el horizonte del pie.

3. **El detalle técnico.** La previa cerraba contando cuántas rutas tiene la API
   y en qué está hecha la app. A quien entra a decidir si le sirve para su lote
   eso no le mueve la aguja, y ocupaba el lugar de lo que sí: el lado del píxel,
   cuántos índices devuelve y de dónde salen los datos.

## Lo que ya estaba bien y no se tocó

La estructura de nueve secciones, el orden, el copy en castellano rioplatense y
la regla de no afirmar nada sin respaldo. Tampoco cambió la regla de superficie:
el panel oscuro aparece una sola vez, donde hay un dato sobre un eje.
