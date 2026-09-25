# -*- coding: utf-8 -*-
"""Genera los dos mockups de media fidelidad como SVG.

Media fidelidad = la estructura de los wireframes, con texto real, jerarquía
tipográfica y color de marca, pero SIN los rasgos que definen al diseño final
(la órbita del isotipo, el hero sangrando al borde, Archivo Expanded).
La dirección es la de una ficha de campo: bloques con borde y barra numerada.
"""
import pathlib, textwrap

# paleta de marca, con los contrastes ya medidos
VERDE="#1A6C4A"; AZUL="#154D7E"; AMBAR="#F9BC3C"; AMBAR_T="#8A5A00"
NAVY="#112D4E"; DATO="#5AB7F0"; NAVY_SUAVE="#A8C2DC"; NAVY_LIN="#24476F"
PAPEL="#F9FBFC"; HOJA="#FFFFFF"; TINTA="#10202E"; TINTA2="#51697A"; TINTA3="#5F7280"
BORDE="#C7D2D9"; FINO="#E3E9ED"; EST_V="#E7F3ED"; EST_A="#FEF3DC"
TERR=["#CFDCC9","#B7CCB0","#A2BD9B","#CCC0A7"]; CAMINO="#B9A483"; CASING="#0C1B2C"
FAM="Archivo, Helvetica Neue, Arial, sans-serif"
MONO="JetBrains Mono, SFMono-Regular, Menlo, monospace"

def esc(t):
    return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

class Lienzo:
    def __init__(s, ancho, margen, esc_=True):
        s.W=ancho; s.mg=margen; s.esc=esc_
        s.x0=margen; s.x1=ancho-margen; s.cw=s.x1-s.x0
        s.y=0; s.o=[]; s.buf=None
    def _add(s,t): (s.buf if s.buf is not None else s.o).append(t)

    # ── primitivas ───────────────────────────────────────────────
    def rect(s,x,y,w,h,fill,rx=0,stroke=None,sw=1,dash=None):
        a=f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{rx}" fill="{fill}"'
        if stroke: a+=f' stroke="{stroke}" stroke-width="{sw}"'
        if dash: a+=f' stroke-dasharray="{dash}"'
        s._add(a+'/>')
    def linea(s,x1,x2,y,col=FINO,w=1):
        s._add(f'<line x1="{x1:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y:.0f}" stroke="{col}" stroke-width="{w}"/>')
    def txt(s,x,y,t,size=14,fill=TINTA,peso=400,fam=None,anc="start",esp="0"):
        s._add(f'<text x="{x:.0f}" y="{y:.0f}" font-family="{fam or FAM}" font-size="{size}" '
               f'fill="{fill}" font-weight="{peso}" text-anchor="{anc}" letter-spacing="{esp}">{esc(t)}</text>')
    def parr(s,x,y,ancho,t,size=13,fill=TINTA2,peso=400,inter=1.5):
        """texto envuelto: ancho de caracter estimado para una grotesca"""
        f = 0.505 if peso<600 else 0.545
        n = max(8, int(ancho/(size*f)))
        yy=y
        for ln in textwrap.wrap(t, n):
            s.txt(x,yy,ln,size,fill,peso); yy += size*inter
        return yy
    def circ(s,cx,cy,r,fill,stroke=None,sw=0):
        a=f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="{fill}"'
        if stroke: a+=f' stroke="{stroke}" stroke-width="{sw}"'
        s._add(a+'/>')
    def path(s,d,fill="none",stroke=None,sw=1,extra=""):
        a=f'<path d="{d}" fill="{fill}"'
        if stroke: a+=f' stroke="{stroke}" stroke-width="{sw}"'
        s._add(a+extra+'/>')

    # ── bloque de sección, con el alto derivado del contenido ────
    def abrir(s):
        s.buf=[]; s._bloque_y=s.y; return s
    def cerrar(s, num, titulo, color, nota=None, texto_claro=True, pad=None):
        pad = pad if pad is not None else (20 if s.esc else 14)
        cuerpo=s.buf; s.buf=None
        alto_cab = 34 if s.esc else 28
        alto = (s.y - s._bloque_y) + pad
        y0 = s._bloque_y
        s.rect(s.x0, y0, s.cw, alto_cab+alto, HOJA, stroke=TINTA, sw=2)
        s.rect(s.x0+1, y0+1, s.cw-2, alto_cab-1, color)
        col = HOJA if texto_claro else TINTA
        fs = 15 if s.esc else 12.5
        s.txt(s.x0+16, y0+alto_cab*0.68, num, fs-3, col, 600, MONO)
        s.txt(s.x0+(48 if s.esc else 40), y0+alto_cab*0.68, titulo, fs, col, 700)
        if nota and s.esc:
            s.txt(s.x1-16, y0+alto_cab*0.66, nota, 10.5, col, 600, MONO, anc="end", esp=".05em")
        s.o.extend(cuerpo)
        s.y = y0+alto_cab+alto + (20 if s.esc else 14)
    def contenido_y(s, pad=None):
        pad = pad if pad is not None else (20 if s.esc else 14)
        s.y = s._bloque_y + (34 if s.esc else 28) + pad
        return s.y

# ── dibujos ─────────────────────────────────────────────────────
def lote(c,x,y,w,h):
    """la plancha del lote: parcelas, grilla de 10 m y el contorno de doble línea"""
    cid=f"cl{int(x)}{int(y)}"
    c._add(f'<clipPath id="{cid}"><rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}"/></clipPath>')
    c._add(f'<g clip-path="url(#{cid})">')
    c.rect(x,y,w,h,TERR[0])
    P=lambda pts,f: c.path("M"+" L".join(f"{x+a*w:.1f} {y+b*h:.1f}" for a,b in pts)+" Z",fill=f)
    P([(0,0),(.55,0),(.50,.35),(0,.39)],TERR[1])
    P([(.55,0),(1,0),(1,.31),(.50,.35)],TERR[3])
    P([(0,.39),(.50,.35),(.55,.74),(0,.78)],TERR[2])
    P([(.50,.35),(1,.31),(1,.71),(.55,.74)],TERR[1])
    P([(0,.78),(.55,.74),(.58,1),(0,1)],TERR[3])
    P([(.55,.74),(1,.71),(1,1),(.58,1)],TERR[2])
    c.path(f"M{x-6:.0f} {y+h*.70:.0f} C {x+w*.3:.0f} {y+h*.67:.0f} {x+w*.7:.0f} {y+h*.62:.0f} {x+w+6:.0f} {y+h*.60:.0f}",
           stroke=CAMINO, sw=max(6,w*0.028))
    paso=w/17
    g=[]
    k=paso
    while k<w: g.append(f"M{x+k:.1f} {y:.0f}V{y+h:.0f}"); k+=paso
    k=paso
    while k<h: g.append(f"M{x:.0f} {y+k:.1f}H{x+w:.0f}"); k+=paso
    c.path("".join(g), stroke=HOJA, sw=1, extra=' opacity=".34"')
    c._add('</g>')
    # cota de 10 m. El ancla es el alto disponible menos lo que ocupan la celda,
    # la línea de cota y su etiqueta: si no, en pantalla angosta se sale de la
    # plancha y pisa el epígrafe de abajo.
    cx0=x+paso*0.6; cy0=y+h-(paso+44)
    c._add(f'<rect x="{cx0:.1f}" y="{cy0:.1f}" width="{paso:.1f}" height="{paso:.1f}" '
           f'fill="{HOJA}" fill-opacity=".42" stroke="{HOJA}" stroke-width="1.5"/>')
    c.path(f"M{cx0:.1f} {cy0+paso+13:.1f}H{cx0+paso:.1f}M{cx0:.1f} {cy0+paso+8:.1f}v10M{cx0+paso:.1f} {cy0+paso+8:.1f}v10",
           stroke=CASING, sw=1.6)
    c.txt(cx0+paso/2, cy0+paso+34, "10 m", 11 if not c.esc else 12, CASING, 700, MONO, anc="middle")
    # el polígono, con casing
    pts=[(.19,.42),(.30,.19),(.53,.13),(.72,.19),(.85,.33),(.88,.50),
         (.76,.57),(.83,.70),(.68,.79),(.46,.84),(.33,.80),(.26,.66),(.22,.56)]
    d="M"+" L".join(f"{x+a*w:.1f} {y+b*h:.1f}" for a,b in pts)+" Z"
    c.path(d, stroke=CASING, sw=6, extra=' stroke-linejoin="round"')
    c.path(d, stroke=HOJA, sw=2.6, extra=' stroke-linejoin="round"')

def grafico(c,x,y,w,h):
    """la serie con su banda de desvío y la caída marcada en ámbar"""
    c.rect(x,y,w,h,NAVY,rx=4)
    px,py,pw,ph = x+14,y+14,w-28,h-52
    sx=lambda t: px+pw*t; sy=lambda v: py+ph*v
    c.path("".join(f"M{px:.0f} {sy(v):.1f}H{px+pw:.0f}" for v in (.2,.4,.6,.8)), stroke=NAVY_LIN, sw=1)
    c.path(f"M{sx(.33):.0f} {py:.0f}V{py+ph:.0f}M{sx(.67):.0f} {py:.0f}V{py+ph:.0f}", stroke=NAVY_LIN, sw=1)
    cur=[(0,.86),(.14,.66),(.28,.34),(.45,.16),(.50,.17),(.545,.58),(.62,.66),(.76,.72),(1,.82)]
    def poli(off):
        return " L".join(f"{sx(t):.1f} {sy(min(max(v+off,0),1)):.1f}" for t,v in cur)
    c.path("M"+poli(-.07)+" L"+" L".join(f"{sx(t):.1f} {sy(min(max(v+.07,0),1)):.1f}" for t,v in reversed(cur))+" Z",
           fill=DATO, extra=' fill-opacity=".26"')
    c.path("M"+poli(0), stroke=DATO, sw=3, extra=' stroke-linecap="round"')
    c.path(f"M{sx(.50):.0f} {py:.0f}V{py+ph:.0f}", stroke=AMBAR, sw=2, extra=' stroke-dasharray="6 6"')
    c.circ(sx(.50), sy(.17), 7, AMBAR, stroke=NAVY, sw=3)
    c.linea(px,px+pw,py+ph+8,NAVY_SUAVE,1.5)
    for i,t in enumerate(("siembra","desarrollo","cosecha")):
        c.txt(px+pw*(i/3+1/6), py+ph+26, t, 10.5, NAVY_SUAVE, 600, MONO, anc="middle")

FUENTES=[("Sentinel-2","Agencia Espacial Europea","Imagen óptica cada pocos días, a 10 m por píxel. De ahí salen el verdor del canopeo, el agua en la hoja y el suelo descubierto."),
         ("Sentinel-1","Agencia Espacial Europea","Radar. Mide a través de las nubes, así que sigue viendo el lote cuando la imagen óptica no sirve."),
         ("NASA POWER","NASA","Clima diario sobre el lote: lluvia, temperatura, radiación."),
         ("MAGyP","Agricultura, Ganadería y Pesca","Rendimientos por departamento, campaña por campaña."),
         ("SoilGrids y SISINTA","ISRIC e INTA","Suelo: textura, materia orgánica, profundidad del perfil."),
         ("SAOCOM","CONAE","Humedad del perfil de suelo, medida por radar argentino."),
         ("IGN y georef","Instituto Geográfico Nacional","Geografía: límites, departamentos, localidades."),
         ("NOAA y CPC","NOAA","Fase de El Niño y La Niña, que cambia lo que se puede esperar de la campaña.")]
TIEMPOS=[("01","Antes",AZUL,True,"Qué eventos climáticos pueden pegarle a esta campaña y cuánta plata tenés expuesta en el lote.","antes de sembrar, y mientras decidís"),
         ("02","Durante",AMBAR,False,"Pasó algo: en qué parte del lote, qué día, y con qué intensidad.","mientras el cultivo crece"),
         ("03","Después",VERDE,True,"Cuánto perdiste, y cuánto habrías ganado si ese evento no hubiera pasado.","cerrada la campaña")]
PASOS=[("Dibujás tu lote sobre el mapa","Con la forma que tiene de verdad, alambrado por alambrado. Todo lo que sigue se calcula adentro de ese polígono."),
       ("El satélite lo mide","Sentinel-2 pasa cada pocos días y devuelve índices sobre la grilla de 10 m: NDVI para el verdor, LSWI para el agua en la hoja y BSI para el suelo descubierto. Cuando hay nubes, Sentinel-1 mide igual, porque es radar."),
       ("El sistema cruza el resto","El suelo del lote, el clima diario de la zona, los rendimientos históricos del departamento y la fase de El Niño. Todo de fuentes públicas."),
       ("Recibís el número y su margen","Con la fecha de la imagen de la que salió y cuántos píxeles válidos entraron en la cuenta. Un informe en castellano explica qué significa.")]
ANAT=[("índice","NDVI, LSWI o BSI, promediado adentro del polígono."),
      ("desvío","Cuánto varía el índice de un sector del lote a otro."),
      ("píxeles válidos","Cuántos quedaron después de descartar nube y sombra."),
      ("fecha","El día exacto en que el satélite pasó por encima.")]
USOS=[("Saber cuánta plata tiene en juego","La economía del lote, con los costos y el precio del cultivo, convertida en cuánto representa la campaña en pesos.",VERDE),
      ("Ubicar un evento en el lote","Cuando el índice cae de golpe, el sistema dice en qué sector del polígono cayó y entre qué fechas.",AMBAR),
      ("Cotizar una cobertura por índice","Cuánto costaría un seguro que pague por un disparador medido, y con qué supuestos se calculó.",AZUL),
      ("Leerlo en castellano","Un informe narrado explica los números medidos. El modelo sólo puede usar los valores que recibió.",VERDE)]
CIFRAS=[("El lado de cada píxel que mide","10 m"),("Índices que devuelve sobre tu lote","3"),
        ("Las fuentes de los datos","Todas públicas")]

def cabecera(c):
    alto = 60 if c.esc else 50
    c.rect(c.x0,c.y,c.cw,alto,HOJA,stroke=TINTA,sw=2)
    cy=c.y+alto*0.60
    c.txt(c.x0+18,cy,"C.R.O.P.",22 if c.esc else 17,AZUL,800,esp=".01em")
    if c.esc:
        c.linea(c.x0+128,c.x0+128,c.y+14,BORDE,2)
        c.path(f"M{c.x0+128} {c.y+16}V{c.y+alto-16}",stroke=BORDE,sw=2)
        c.txt(c.x0+144,cy-2,"Riesgo de lote medido por satélite",13,TINTA2,400)
        x=c.x1-16
        for t in ("06 Equipo","05 Usos","04 Fuentes","03 Medición","02 Cómo","01 Tiempos"):
            an=len(t)*6.6+22; x-=an
            c.rect(x,c.y+alto/2-13,an,26,HOJA,stroke=FINO,sw=1)
            c.txt(x+an/2,c.y+alto/2+4.5,t,10.5,TINTA2,600,MONO,anc="middle")
    else:
        c.txt(c.x1-16,cy-1,"6 secciones",10.5,TINTA3,600,MONO,anc="end")
    c.y+=alto+(20 if c.esc else 14)

# ══════════════════════════ ARMADO ══════════════════════════
def pantalla(ancho, margen, es_esc):
    c=Lienzo(ancho,margen,es_esc); c.y=margen
    G=20 if es_esc else 14
    cabecera(c)

    # ── 00 qué es ────────────────────────────────────────────
    c.abrir(); y=c.contenido_y()
    if es_esc:
        iw=c.cw*0.52
        c.txt(c.x0+G,y+30,"El riesgo de tu lote,",38,TINTA,800,esp="-.02em")
        c.txt(c.x0+G,y+74,"medido por satélite",38,TINTA,800,esp="-.02em")
        yy=c.parr(c.x0+G,y+112,iw-G,
            "C.R.O.P. mide tu lote desde el espacio y te contesta tres preguntas: qué te puede pasar esta campaña, qué te pasó, y cuánto perdiste.",16,TINTA2)
        yy+=10
        c.rect(c.x0+G,yy,iw-G,44,EST_V); c.rect(c.x0+G,yy,4,44,VERDE)
        c.txt(c.x0+G+18,yy+28,"Cada número viene con su fuente y su margen.",15,TINTA,600)
        yy+=64
        for k,v in (("Lado de cada píxel medido","10 m"),("Índices sobre el lote","NDVI · LSWI · BSI"),("Cuando hay nubes","radar")):
            c.linea(c.x0+G,c.x0+iw-G,yy,FINO)
            c.txt(c.x0+G,yy+20,k,13,TINTA2); c.txt(c.x0+iw-G,yy+20,v,14,AZUL,600,MONO,anc="end")
            yy+=32
        c.linea(c.x0+G,c.x0+iw-G,yy,FINO)
        pw=c.cw-iw-G; px=c.x0+iw
        lote(c,px,y,pw-G,300)
        c.parr(px,y+322,pw-G,"Esquema. El lote es el polígono que es, nunca un rectángulo. Cada celda mide 10 × 10 m: la resolución real a la que Sentinel-2 mide el terreno.",12,TINTA3)
        c.y=max(yy+8,y+370)
    else:
        c.txt(c.x0+G,y+24,"El riesgo de tu lote,",23,TINTA,800,esp="-.02em")
        c.txt(c.x0+G,y+52,"medido por satélite",23,TINTA,800,esp="-.02em")
        yy=c.parr(c.x0+G,y+82,c.cw-2*G,
            "C.R.O.P. mide tu lote desde el espacio y te contesta tres preguntas: qué te puede pasar esta campaña, qué te pasó, y cuánto perdiste.",13,TINTA2)
        yy+=8
        c.rect(c.x0+G,yy,c.cw-2*G,38,EST_V); c.rect(c.x0+G,yy,3,38,VERDE)
        c.txt(c.x0+G+13,yy+16,"Cada número viene con su",12.5,TINTA,600)
        c.txt(c.x0+G+13,yy+31,"fuente y su margen.",12.5,TINTA,600)
        yy+=52
        for k,v in (("Lado de cada píxel","10 m"),("Índices sobre el lote","3"),("Cuando hay nubes","radar")):
            c.linea(c.x0+G,c.x1-G,yy,FINO)
            c.txt(c.x0+G,yy+17,k,11.5,TINTA2); c.txt(c.x1-G,yy+17,v,12,AZUL,600,MONO,anc="end")
            yy+=27
        c.linea(c.x0+G,c.x1-G,yy,FINO); yy+=14
        lote(c,c.x0+G,yy,c.cw-2*G,190)
        c.y=c.parr(c.x0+G,yy+208,c.cw-2*G,"Esquema. Cada celda mide 10 × 10 m: la resolución real a la que mide Sentinel-2.",11,TINTA3)
    c.cerrar("00","Qué es",NAVY,"Sentinel-2 · 10 m/píxel")

    # ── 01 tres tiempos ──────────────────────────────────────
    c.abrir(); y=c.contenido_y()
    for n,t,col,claro,d,cuando in TIEMPOS:
        c.rect(c.x0+G,y,44 if es_esc else 34,28 if es_esc else 22,col)
        c.txt(c.x0+G+(22 if es_esc else 17),y+(19 if es_esc else 15),n,12 if es_esc else 10,
              HOJA if claro else TINTA,600,MONO,anc="middle")
        tx=c.x0+G+(62 if es_esc else 46)
        c.txt(tx,y+(20 if es_esc else 16),t,18 if es_esc else 15,TINTA,700)
        if es_esc:
            yy=c.parr(tx+140,y+16,c.cw-(tx-c.x0)-140-G,d,14,TINTA2)
            c.txt(tx+140,yy+4,cuando,11,TINTA3,600,MONO)
            y+=max(62,yy-y+22)
        else:
            yy=c.parr(c.x0+G,y+40,c.cw-2*G,d,12,TINTA2)
            c.txt(c.x0+G,yy+4,cuando,10,TINTA3,600,MONO)
            y=yy+22
        c.linea(c.x0+G,c.x1-G,y-10,FINO)
    c.y=y-10
    c.cerrar("01","Los tres tiempos de una campaña",VERDE,"antes · durante · después")

    # ── 02 cómo funciona ─────────────────────────────────────
    c.abrir(); y=c.contenido_y()
    for i,(t,d) in enumerate(PASOS):
        c.txt(c.x0+G,y+(14 if es_esc else 12),f"0{i+1}",12 if es_esc else 10.5,VERDE,600,MONO)
        tx=c.x0+G+(38 if es_esc else 30)
        c.txt(tx,y+(15 if es_esc else 13),t,16 if es_esc else 13.5,TINTA,700)
        yy=c.parr(tx,y+(36 if es_esc else 31),c.x1-G-tx,d,13.5 if es_esc else 12,TINTA2)
        y=yy+(14 if es_esc else 12)
        if i<3: c.linea(c.x0+G,c.x1-G,y-7,FINO)
    c.y=y-7
    c.cerrar("02","Cómo funciona",AZUL,"cuatro pasos, ninguno escondido")

    # ── 03 medición ──────────────────────────────────────────
    c.abrir(); y=c.contenido_y()
    if es_esc:
        iw=c.cw*0.46
        yy=c.parr(c.x0+G,y+14,iw-G,
            "Una medición no es un valor suelto. Es el índice, cuánto varía dentro del lote, cuántos píxeles quedaron limpios y de qué día es la imagen.",14,TINTA2)
        yy+=12
        for k,v in ANAT:
            c.linea(c.x0+G,c.x0+iw-G,yy,FINO)
            c.txt(c.x0+G,yy+19,k,11.5,AZUL,600,MONO)
            c.parr(c.x0+G+118,yy+19,iw-G-118,v,13,TINTA2)
            yy+=38
        c.linea(c.x0+G,c.x0+iw-G,yy,FINO)
        gx=c.x0+iw; gw=c.cw-iw-G
        grafico(c,gx,y,gw,250)
        c.parr(gx,y+276,gw,"Esquema de la forma de una serie, no una medición. La banda alrededor de la curva es el desvío: es parte del dato, no un adorno.",12,TINTA3)
        c.y=max(yy+8,y+320)
    else:
        yy=c.parr(c.x0+G,y+12,c.cw-2*G,
            "Una medición no es un valor suelto. Es el índice, cuánto varía dentro del lote, cuántos píxeles quedaron limpios y de qué día es la imagen.",12,TINTA2)
        yy+=10
        for k,v in ANAT:
            c.linea(c.x0+G,c.x1-G,yy,FINO)
            c.txt(c.x0+G,yy+16,k,10.5,AZUL,600,MONO)
            yy=c.parr(c.x0+G,yy+32,c.cw-2*G,v,11.5,TINTA2)+8
        c.linea(c.x0+G,c.x1-G,yy,FINO); yy+=14
        grafico(c,c.x0+G,yy,c.cw-2*G,170)
        c.y=c.parr(c.x0+G,yy+188,c.cw-2*G,"Esquema de la forma de una serie, no una medición.",11,TINTA3)
    c.cerrar("03","Un número, y lo que lo sostiene",NAVY,"esquema, no medición")

    # ── 04 fuentes ───────────────────────────────────────────
    c.abrir(); y=c.contenido_y()
    y=c.parr(c.x0+G,y+12,c.cw-2*G if not es_esc else c.cw*.72,
        "Todas las fuentes son públicas y están nombradas. Cualquiera puede ir a buscarlas y verificar de dónde salió cada cosa.",
        13 if es_esc else 12,TINTA2)+10
    if es_esc:
        c1=c.x0+G; c2=c1+230; c3=c2+220
        for h,xx in (("fuente",c1),("organismo",c2),("qué aporta",c3)):
            c.txt(xx,y,h,10.5,TINTA3,600,MONO,esp=".08em")
        y+=8; c.linea(c.x0+G,c.x1-G,y,TINTA,2); y+=6
        for n,org,d in FUENTES:
            c.txt(c1,y+16,n,14,TINTA,700)
            c.parr(c2,y+16,210,org,11.5,TINTA3)
            yy=c.parr(c3,y+16,c.x1-G-c3,d,13,TINTA2)
            y=max(y+34,yy+4); c.linea(c.x0+G,c.x1-G,y,FINO); y+=2
        c.y=y
    else:
        for n,org,d in FUENTES[:4]:
            c.linea(c.x0+G,c.x1-G,y,FINO)
            c.txt(c.x0+G,y+17,n,12.5,TINTA,700)
            c.txt(c.x1-G,y+17,org,9.5,TINTA3,600,MONO,anc="end")
            y=c.parr(c.x0+G,y+33,c.cw-2*G,d,11.5,TINTA2)+8
        c.linea(c.x0+G,c.x1-G,y,FINO)
        c.txt(c.x0+G,y+18,"+ SAOCOM, IGN y georef, NOAA y CPC",10.5,TINTA3,600,MONO)
        c.y=y+26
    c.cerrar("04","De dónde salen los números",VERDE,"8 fuentes, todas públicas")

    # ── 05 usos ──────────────────────────────────────────────
    c.abrir(); y=c.contenido_y()
    if es_esc:
        cw2=(c.cw-2*G-18)/2
        for i,(t,d,col) in enumerate(USOS):
            xx=c.x0+G+(i%2)*(cw2+18); yy=y+(i//2)*116
            c.rect(xx,yy,cw2,100,HOJA,stroke=BORDE,sw=1)
            c.rect(xx,yy,cw2,4,col)
            c.txt(xx+14,yy+30,t,15,TINTA,700)
            c.parr(xx+14,yy+50,cw2-28,d,12.5,TINTA2)
        y+=232
        c.rect(c.x0+G,y,c.cw-2*G,44,EST_A); c.rect(c.x0+G,y,4,44,AMBAR_T)
        c.txt(c.x0+G+18,y+28,"El cliente es el productor, y quien le presta plata: el banco, la cooperativa, el acopio.",14,TINTA,600)
        c.y=y+44
    else:
        for t,d,col in USOS:
            c.rect(c.x0+G,y,c.cw-2*G,4,col)
            c.txt(c.x0+G,y+24,t,13,TINTA,700)
            y=c.parr(c.x0+G,y+42,c.cw-2*G,d,11.5,TINTA2)+12
        c.rect(c.x0+G,y,c.cw-2*G,52,EST_A); c.rect(c.x0+G,y,3,52,AMBAR_T)
        c.parr(c.x0+G+13,y+20,c.cw-2*G-26,"El cliente es el productor, y quien le presta plata: el banco, la cooperativa, el acopio.",11.5,TINTA,600)
        c.y=y+52
    c.cerrar("05","Para qué le sirve al productor",AMBAR,"cuatro usos",texto_claro=False)

    # ── 06 equipo ────────────────────────────────────────────
    c.abrir(); y=c.contenido_y()
    if es_esc:
        iw=c.cw*0.55
        c.parr(c.x0+G,y+16,iw-G,
            "Cuatro estudiantes de secundaria técnica argentina. C.R.O.P. es un proyecto académico, construido con estándar profesional y con fuentes de datos reales.",14,TINTA2)
        dx=c.x0+iw; yy=y
        c.linea(dx,c.x1-G,yy,TINTA,2)
        for k,v in CIFRAS:
            yy+=10; c.txt(dx,yy+16,k,12.5,TINTA2)
            c.txt(c.x1-G,yy+20,v,24 if v!="Todas públicas" else 14,VERDE if v!="Todas públicas" else TINTA,
                  800 if v!="Todas públicas" else 700,anc="end")
            yy+=26; c.linea(dx,c.x1-G,yy,FINO)
        c.y=max(y+92,yy)
    else:
        y=c.parr(c.x0+G,y+14,c.cw-2*G,
            "Cuatro estudiantes de secundaria técnica argentina. C.R.O.P. es un proyecto académico, construido con estándar profesional y con fuentes de datos reales.",12,TINTA2)+12
        c.linea(c.x0+G,c.x1-G,y,TINTA,2)
        for k,v in CIFRAS:
            y+=8; c.txt(c.x0+G,y+15,k,11,TINTA2)
            c.txt(c.x1-G,y+18,v,18 if v!="Todas públicas" else 12,VERDE if v!="Todas públicas" else TINTA,
                  800 if v!="Todas públicas" else 700,anc="end")
            y+=24; c.linea(c.x0+G,c.x1-G,y,FINO)
        c.y=y
    c.cerrar("06","Quiénes somos",AZUL,"proyecto académico")

    # ── pie ──────────────────────────────────────────────────
    alto = 110 if es_esc else 96
    c.rect(c.x0,c.y,c.cw,alto,NAVY,stroke=TINTA,sw=2)
    cx=c.W/2
    if es_esc:
        c.txt(cx,c.y+48,"Cada número sale de una fuente verificable",17,HOJA,600,anc="middle")
        c.txt(cx,c.y+72,"y viene con su margen de error.",17,HOJA,600,anc="middle")
        c.txt(cx,c.y+95,"C.R.O.P. · proyecto académico · Argentina, 2026",11,NAVY_SUAVE,600,MONO,anc="middle")
    else:
        c.txt(cx,c.y+30,"Cada número sale de una fuente",13,HOJA,600,anc="middle")
        c.txt(cx,c.y+48,"verificable y viene con su margen.",13,HOJA,600,anc="middle")
        c.txt(cx,c.y+74,"C.R.O.P. · Argentina, 2026",9.5,NAVY_SUAVE,600,MONO,anc="middle")
    c.y+=alto+margen
    return c

def armar(c,titulo,desc,salida):
    H=int(c.y)
    cab=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {c.W} {H}" width="{c.W}" height="{H}" '
         f'role="img" aria-labelledby="ttl dsc">\n<title id="ttl">{esc(titulo)}</title>\n'
         f'<desc id="dsc">{esc(desc)}</desc>\n<rect width="{c.W}" height="{H}" fill="{PAPEL}"/>\n')
    pathlib.Path(salida).write_text(cab+"\n".join(c.o)+"\n</svg>\n",encoding="utf-8")
    import os
    print(f"{salida}  {c.W} × {H}  ·  {os.path.getsize(salida)//1024} KB")

d=pathlib.Path(__file__).resolve().parent
armar(pantalla(1440,40,True),"C.R.O.P. — mockup de escritorio",
  "Mockup de media fidelidad de la landing de C.R.O.P. a 1440 px: la estructura del wireframe con texto real, "
  "jerarquía tipográfica y color de marca, en bloques con borde y barra numerada.",
  str(d/"mockup-escritorio.svg"))
armar(pantalla(390,14,False),"C.R.O.P. — mockup de teléfono",
  "El mismo mockup de media fidelidad a 390 px, con las secciones apiladas en una columna.",
  str(d/"mockup-telefono.svg"))
