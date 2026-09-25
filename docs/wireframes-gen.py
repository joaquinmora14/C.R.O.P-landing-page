# -*- coding: utf-8 -*-
"""Genera los dos wireframes como SVG. La geometría sale de styles.css:
   ancho útil 1280, margen 56 a 1440 y 20 a 390, alto de barra 84 / 67."""
import pathlib

PAPEL="#FFFFFF"; LINEA="#C6CFCB"; BLQ="#DFE5E2"; BLQ2="#CAD3CF"
TINTA="#171D1B"; ROTULO="#67736E"; OSCURO="#2C3A44"
OSC_BLQ="#4B5A65"; OSC_BLQ2="#8494A0"; OSC_IMG="#1D2830"
VERDE="#1A6C4A"; AZUL="#154D7E"; AMBAR="#B07A10"
BANDA_V="#EBF2EE"; BANDA_A="#FAF2E3"

class Lienzo:
    def __init__(s, ancho, margen, esc=True):
        s.W=ancho; s.mg=margen; s.esc=esc
        s.x0=margen; s.x1=ancho-margen; s.cw=s.x1-s.x0
        s.y=0; s.o=[]
    # --- primitivas -------------------------------------------------
    def rect(s,x,y,w,h,fill,rx=0,extra=""):
        s.o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
                   f'rx="{rx}" fill="{fill}"{extra}/>')
    def bar(s,x,y,w,h=7,fill=None):
        s.rect(x,y,w,h,fill or BLQ2,rx=h/2)
    def txt(s,x,y,t,size=11,fill=ROTULO,peso=600,esp=".09em",anc="start"):
        t=(t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))
        s.o.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{fill}" '
                   f'font-weight="{peso}" letter-spacing="{esp}" text-anchor="{anc}">{t}</text>')
    def linea(s,x1,x2,y,col=LINEA,w=1):
        s.o.append(f'<line x1="{x1:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y:.0f}" '
                   f'stroke="{col}" stroke-width="{w}"/>')
    def img(s,x,y,w,h,borde=LINEA,fondo=BLQ):
        s.rect(x,y,w,h,fondo,rx=3)
        s.o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="3" '
                   f'fill="none" stroke="{borde}" stroke-width="1" stroke-dasharray="5 4"/>')
        s.o.append(f'<path d="M{x:.0f} {y:.0f}L{x+w:.0f} {y+h:.0f}M{x+w:.0f} {y:.0f}L{x:.0f} {y+h:.0f}" '
                   f'stroke="{borde}" stroke-width="1" fill="none"/>')
    def circ(s,cx,cy,r,fill):
        s.o.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="{fill}"/>')
    # --- ayudas -----------------------------------------------------
    def rotulo(s,t):
        s.txt(s.x0, s.y+11, t.upper(), size=10 if s.esc else 9)
        s.y += 26 if s.esc else 21
    def parrafo(s,x,w,anchos,y=None,gap=9,h=7,fill=None):
        yy = s.y if y is None else y
        for a in anchos:
            s.bar(x,yy,w*a,h,fill); yy += h+gap
        return yy
    def banda(s,alto,color):
        s.rect(0,s.y,s.W,alto,color)

def cabecera(c, alto):
    """barra superior: emblema + wordmark | nav"""
    c.rect(0,c.y,c.W,alto,PAPEL)
    cy=c.y+alto/2
    lado = 20 if c.esc else 15
    c.rect(c.x0, cy-lado/2, lado, lado, LINEA, rx=4)
    c.bar(c.x0+lado+10, cy-4, 68 if c.esc else 42, 8)
    if c.esc:
        x=c.x1
        for w in (48,50,44,60,56):
            x-=w; c.bar(x, cy-3, w-16, 6); x-=2
    else:
        x=c.x1
        for w in (34,34,16):
            x-=w; c.bar(x, cy-3, w-8, 6); x-=2
    c.linea(0,c.W,c.y+alto)
    c.y += alto

# ═══════════════════════════ ESCRITORIO ═══════════════════════════
def escritorio():
    c=Lienzo(1440,136,True)
    cabecera(c,84)

    # --- hero -------------------------------------------------------
    h0=c.y; alto=520
    izq = c.cw*0.505
    c.y += 40
    yy=c.y
    for a in (.95,.86,.60):
        c.bar(c.x0,yy,izq*a,15,LINEA); yy+=24
    yy+=18
    yy=c.parrafo(c.x0,izq,(.95,.86,.48),y=yy,gap=10)
    yy+=16
    c.rect(c.x0,yy,4,44,VERDE,rx=2)
    c.parrafo(c.x0+18,izq-18,(.82,.40),y=yy+6,gap=10,h=9)
    yy+=64
    px=c.x0
    for w in (150,178,166):
        c.rect(px,yy,w,26,BLQ2,rx=13); px+=w+10
    # el dibujo sangra hasta el borde derecho de la ventana
    c.img(c.x0+izq+44, h0, c.W-(c.x0+izq+44), alto)
    c.y = h0+alto
    c.linea(0,c.W,c.y)

    # --- tres tiempos ----------------------------------------------
    h0=c.y; alto=330
    c.banda(alto,BANDA_V)
    c.y+=28; c.rotulo("Los tres tiempos")
    c.bar(c.x0,c.y,c.cw*.42,15,LINEA); c.bar(c.x0,c.y+24,c.cw*.30,15,LINEA)
    c.parrafo(c.x0+c.cw*.53,c.cw*.47,(.95,.72),y=c.y+6,gap=10)
    c.y+=70
    col=(c.cw-2*36)/3
    for i,col_c in enumerate((AZUL,AMBAR,VERDE)):
        x=c.x0+i*(col+36)
        c.circ(x+11,c.y+11,11,col_c)
        c.rect(x+26,c.y+9,col-26,3,col_c,rx=2)
        c.bar(x,c.y+38,col*.52,10)
        c.parrafo(x,col,(.95,.78,.40),y=c.y+62,gap=9)
    c.y=h0+alto; c.linea(0,c.W,c.y)

    # --- cómo funciona ---------------------------------------------
    h0=c.y; alto=330
    c.y+=28; c.rotulo("Cómo funciona")
    c.bar(c.x0,c.y,c.cw*.30,15,LINEA)
    c.parrafo(c.x0+c.cw*.53,c.cw*.47,(.72,),y=c.y+6)
    c.y+=52
    col=(c.cw-3*30)/4
    for i in range(4):
        x=c.x0+i*(col+30)
        c.rect(x,c.y,col,3,VERDE,rx=2)
        c.img(x,c.y+16,46,46)
        c.bar(x,c.y+76,col*.78,10)
        c.parrafo(x,col,(.95,.86,.55),y=c.y+98,gap=9)
    c.y=h0+alto; c.linea(0,c.W,c.y)

    # --- la medición -----------------------------------------------
    # el alto del panel se deriva de lo que entra adentro, no se estima
    h0=c.y
    c.y+=28; c.rotulo("La medición")
    pad=34; pnl_y=c.y
    px=pnl_y+pad
    pw=c.cw-2*pad; li=pw*0.44
    dw=pw*0.48; ch=dw*300/620
    alto_izq = pad+36+32+14+4*22
    alto_der = pad+ch+14+7+22+32
    pnl_h = max(alto_izq,alto_der)+pad
    alto = (c.y-h0)+pnl_h+34
    c.banda(alto,BANDA_V)
    c.rect(c.x0,pnl_y,c.cw,pnl_h,OSCURO,rx=10)
    bx=c.x0+pad
    yy=pnl_y+pad
    c.bar(bx,yy,li*.82,14,OSC_BLQ2); c.bar(bx,yy+22,li*.58,14,OSC_BLQ2)
    yy=c.parrafo(bx,li,(.95,.74),y=yy+36,gap=9,fill=OSC_BLQ)
    yy+=14
    for _ in range(4):
        c.bar(bx,yy,li*.24,7,AZUL); c.bar(bx+li*.32,yy,li*.62,7,OSC_BLQ); yy+=22
    dx=bx+pw*0.52
    c.img(dx,pnl_y+pad,dw,ch,borde=OSC_BLQ,fondo=OSC_IMG)
    ey=pnl_y+pad+ch+14
    for i in range(3):
        c.bar(dx+i*dw/3+dw/9,ey,dw*.16,7,OSC_BLQ)
    c.parrafo(dx,dw,(.92,.60),y=ey+22,gap=9,fill=OSC_BLQ)
    c.y=h0+alto; c.linea(0,c.W,c.y)

    # --- fuentes ----------------------------------------------------
    h0=c.y
    c.y+=28; c.rotulo("De dónde salen los números")
    c.bar(c.x0,c.y,c.cw*.34,15,LINEA)
    # subrayado de doble línea (casing)
    c.rect(c.x0,c.y+26,150,6,"#0C1B2C",rx=3); c.rect(c.x0,c.y+27.7,150,2.6,PAPEL,rx=1.3)
    c.parrafo(c.x0+c.cw*.53,c.cw*.47,(.92,.58),y=c.y+6,gap=10)
    c.y+=62
    nom=c.cw*0.30
    for i,(nw,pw2,d1,d2) in enumerate([(.72,.80,.95,.70),(.58,.80,.95,.46),
                                       (.82,.42,.80,None),(.48,.94,.95,.60)]):
        c.linea(c.x0,c.x1,c.y)
        c.bar(c.x0,c.y+18,nom*nw,10)
        c.rect(c.x0,c.y+36,nom*pw2,22,BLQ2,rx=11)
        c.bar(c.x0+nom+56,c.y+18,(c.cw-nom-56)*d1)
        if d2: c.bar(c.x0+nom+56,c.y+34,(c.cw-nom-56)*d2)
        c.y+=78
    c.linea(c.x0,c.x1,c.y)
    c.y+=34; c.linea(0,c.W,c.y)

    # --- para qué sirve ---------------------------------------------
    h0=c.y; alto=370
    c.banda(alto,BANDA_A)
    c.y+=28; c.rotulo("Para qué le sirve")
    c.bar(c.x0,c.y,c.cw*.34,15,LINEA); c.bar(c.x0,c.y+24,c.cw*.18,15,LINEA)
    c.y+=62
    col=(c.cw-46)/2
    for i,col_c in enumerate((VERDE,AMBAR,AZUL,VERDE)):
        x=c.x0+(i%2)*(col+46); y=c.y+(i//2)*104
        c.rect(x,y,4,74,col_c,rx=2)
        c.bar(x+18,y,col*.70,10)
        c.parrafo(x+18,col-18,(.92,.60),y=y+22,gap=9)
    c.y+=228
    c.rect(c.x0,c.y,c.cw,2,VERDE)
    c.parrafo(c.x0,c.cw,(.44,.34),y=c.y+20,gap=10,h=11)
    c.y=h0+alto; c.linea(0,c.W,c.y)

    # --- quiénes somos ----------------------------------------------
    h0=c.y; alto=250
    c.y+=28; c.rotulo("Quiénes somos")
    izq=c.cw*0.52
    c.bar(c.x0,c.y,izq*.60,15,LINEA)
    c.parrafo(c.x0,izq,(.95,.95,.72),y=c.y+32,gap=10)
    dx=c.x0+c.cw*0.56; dw=c.cw-(dx-c.x0)
    yy=c.y
    for lw,nw in ((.60,42),(.74,22),(.48,None)):
        c.linea(dx,c.x1,yy)
        c.bar(dx,yy+18,dw*lw)
        if nw: c.rect(c.x1-nw,yy+12,nw,15,VERDE,rx=3)
        else:  c.bar(c.x1-78,yy+15,78,10)
        yy+=48
    c.linea(dx,c.x1,yy)
    c.y=h0+alto; c.linea(0,c.W,c.y)

    # --- pie --------------------------------------------------------
    h0=c.y; alto=280
    c.y+=36; c.rotulo("Pie")
    cx=c.W/2
    c.img(cx-32,c.y,64,64)
    c.bar(cx-190,c.y+84,380,11); c.bar(cx-130,c.y+106,260,11)
    c.bar(cx-80,c.y+132,160,7)
    # horizonte: tierra verde y órbita azul, abajo de todo
    c.o.append(f'<ellipse cx="{cx:.0f}" cy="{h0+alto+300:.0f}" rx="{c.W*0.92:.0f}" ry="360" fill="{BANDA_V}"/>')
    c.o.append(f'<ellipse cx="{cx:.0f}" cy="{h0+alto+300:.0f}" rx="{c.W*0.86:.0f}" ry="382" '
               f'fill="none" stroke="{AZUL}" stroke-width="2.5" opacity=".38"/>')
    c.y=h0+alto
    return c

# ═══════════════════════════ TELÉFONO ═══════════════════════════
def telefono():
    c=Lienzo(390,20,False)
    cabecera(c,67)

    # --- hero -------------------------------------------------------
    h0=c.y
    c.y+=22; c.rotulo("Hero")
    yy=c.y
    for a in (.95,.72):
        c.bar(c.x0,yy,c.cw*a,13,LINEA); yy+=20
    yy+=10
    yy=c.parrafo(c.x0,c.cw,(.95,.84),y=yy,gap=8)
    yy+=10
    c.rect(c.x0,yy,3,26,VERDE,rx=2)
    c.bar(c.x0+12,yy+8,c.cw*.72,9)
    yy+=40
    for w in (.76,.90,.82):
        c.rect(c.x0,yy,c.cw*w,20,BLQ2,rx=10); yy+=26
    yy+=8
    c.img(c.x0,yy,c.cw,c.cw)   # 1:1
    c.y=yy+c.cw+24; c.linea(0,c.W,c.y)

    # --- tres tiempos ----------------------------------------------
    h0=c.y
    alto=22+21+34+3*74+20
    c.banda(alto,BANDA_V)
    c.y+=22; c.rotulo("Los tres tiempos")
    c.bar(c.x0,c.y,c.cw*.82,13,LINEA); c.bar(c.x0,c.y+20,c.cw*.95,7)
    c.y+=40
    for col_c,a in ((AZUL,.95),(AMBAR,.84),(VERDE,.95)):
        c.circ(c.x0+8,c.y+8,8,col_c)
        c.rect(c.x0+20,c.y+6.5,c.cw-20,3,col_c,rx=2)
        c.bar(c.x0,c.y+26,c.cw*.50,9)
        c.bar(c.x0,c.y+46,c.cw*a)
        c.y+=74
    c.y=h0+alto; c.linea(0,c.W,c.y)

    # --- cómo funciona ---------------------------------------------
    h0=c.y
    c.y+=22; c.rotulo("Cómo funciona")
    c.bar(c.x0,c.y,c.cw*.56,13,LINEA); c.bar(c.x0,c.y+20,c.cw*.84,7)
    c.y+=40
    for a in (.95,.78,.95,.84):
        c.rect(c.x0,c.y,c.cw,3,VERDE,rx=2)
        c.img(c.x0,c.y+14,34,34)
        c.bar(c.x0,c.y+58,c.cw*.72,9)
        c.bar(c.x0,c.y+76,c.cw*a)
        c.y+=100
    c.y+=6; c.linea(0,c.W,c.y)

    # --- la medición -----------------------------------------------
    # igual que en escritorio: el alto sale de sumar lo que entra
    h0=c.y
    c.y+=22; c.rotulo("La medición")
    pnl_y=c.y; pad=18
    pw=c.cw; iw=pw-2*pad; ch=iw*300/620
    ph = pad+24+30+6+4*28+ch+pad
    c.banda((c.y-h0)+ph+24,BANDA_V)
    c.rect(c.x0,pnl_y,pw,ph,OSCURO,rx=8)
    px=c.x0+pad
    yy=pnl_y+pad
    c.bar(px,yy,iw*.82,12,OSC_BLQ2); yy+=24
    yy=c.parrafo(px,iw,(.95,.72),y=yy,gap=8,fill=OSC_BLQ)
    yy+=6
    for _ in range(4):
        c.bar(px,yy,iw*.34,7,AZUL); c.bar(px,yy+12,iw*.88,7,OSC_BLQ); yy+=28
    c.img(px,yy,iw,ch,borde=OSC_BLQ,fondo=OSC_IMG)
    c.y=pnl_y+ph+24; c.linea(0,c.W,c.y)

    # --- fuentes ----------------------------------------------------
    c.y+=22; c.rotulo("De dónde salen los números")
    c.bar(c.x0,c.y,c.cw*.84,13,LINEA)
    c.rect(c.x0,c.y+22,86,6,"#0C1B2C",rx=3); c.rect(c.x0,c.y+23.7,86,2.6,PAPEL,rx=1.3)
    c.bar(c.x0,c.y+40,c.cw*.84,7)
    c.y+=60
    for nw,pw2,dw in ((.60,.64,.95),(.48,.64,.84),(.74,.42,.95)):
        c.linea(c.x0,c.x1,c.y)
        c.bar(c.x0,c.y+14,c.cw*nw,9)
        c.rect(c.x0,c.y+30,c.cw*pw2,18,BLQ2,rx=9)
        c.bar(c.x0,c.y+56,c.cw*dw)
        c.y+=76
    c.linea(c.x0,c.x1,c.y)
    c.y+=24; c.linea(0,c.W,c.y)

    # --- para qué sirve ---------------------------------------------
    h0=c.y
    alto=22+21+26+4*70+20+34+24
    c.banda(alto,BANDA_A)
    c.y+=22; c.rotulo("Para qué le sirve")
    c.bar(c.x0,c.y,c.cw*.56,13,LINEA)
    c.y+=26
    for col_c,a in ((VERDE,.95),(AMBAR,.95),(AZUL,.84),(VERDE,.95)):
        c.rect(c.x0,c.y,3,48,col_c,rx=2)
        c.bar(c.x0+14,c.y,c.cw*.78,9)
        c.bar(c.x0+14,c.y+20,(c.cw-14)*a)
        c.y+=70
    c.rect(c.x0,c.y,c.cw,2,VERDE)
    c.bar(c.x0,c.y+16,c.cw*.84,10); c.bar(c.x0,c.y+34,c.cw*.60,10)
    c.y=h0+alto; c.linea(0,c.W,c.y)

    # --- quiénes somos ----------------------------------------------
    c.y+=22; c.rotulo("Quiénes somos")
    c.bar(c.x0,c.y,c.cw*.56,13,LINEA)
    c.parrafo(c.x0,c.cw,(.95,.84),y=c.y+24,gap=8)
    c.y+=62
    for lw,nw in ((.60,30),(.74,16),(.48,None)):
        c.linea(c.x0,c.x1,c.y)
        c.bar(c.x0,c.y+14,c.cw*lw)
        if nw: c.rect(c.x1-nw,c.y+9,nw,13,VERDE,rx=3)
        else:  c.bar(c.x1-52,c.y+11,52,9)
        c.y+=38
    c.linea(c.x0,c.x1,c.y)
    c.y+=26; c.linea(0,c.W,c.y)

    # --- pie --------------------------------------------------------
    h0=c.y; alto=230
    c.y+=28; c.rotulo("Pie")
    cx=c.W/2
    c.img(cx-22,c.y,44,44)
    c.bar(cx-98,c.y+60,196,10); c.bar(cx-70,c.y+80,140,10)
    c.bar(cx-56,c.y+102,112,7)
    c.o.append(f'<ellipse cx="{cx:.0f}" cy="{h0+alto+180:.0f}" rx="{c.W*0.95:.0f}" ry="212" fill="{BANDA_V}"/>')
    c.o.append(f'<ellipse cx="{cx:.0f}" cy="{h0+alto+180:.0f}" rx="{c.W*0.90:.0f}" ry="228" '
               f'fill="none" stroke="{AZUL}" stroke-width="2" opacity=".38"/>')
    c.y=h0+alto
    return c

def armar(c, titulo, desc, salida):
    H=int(c.y)
    cab=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {c.W} {H}" '
         f'width="{c.W}" height="{H}" role="img" aria-labelledby="ttl dsc" '
         f'font-family="Archivo, Helvetica Neue, Arial, sans-serif">\n'
         f'<title id="ttl">{titulo}</title>\n<desc id="dsc">{desc}</desc>\n'
         f'<rect width="{c.W}" height="{H}" fill="{PAPEL}"/>\n')
    pathlib.Path(salida).write_text(cab+"\n".join(c.o)+"\n</svg>\n", encoding="utf-8")
    import os
    print(f"{salida}  {c.W} × {H}  ·  {os.path.getsize(salida)//1024} KB  ·  {len(c.o)} formas")

d=pathlib.Path("/home/user/C.R.O.P-landing-page/docs"); d.mkdir(exist_ok=True)
armar(escritorio(), "Wireframe de C.R.O.P. — escritorio",
      "La landing completa a 1440 px: barra, hero a dos columnas con el dibujo sangrando al borde, "
      "los tres tiempos sobre banda verde, cuatro pasos, el panel oscuro de medición, el registro de "
      "fuentes, los cuatro usos sobre banda ámbar, el equipo y el pie con el horizonte.",
      str(d/"wireframe-escritorio.svg"))
armar(telefono(), "Wireframe de C.R.O.P. — teléfono",
      "La misma landing a 390 px, con las nueve secciones apiladas en una sola columna.",
      str(d/"wireframe-telefono.svg"))
