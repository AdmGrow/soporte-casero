#!/usr/bin/env python3
"""Genera el sitio estático de Soporte casero. Fuente: data/curso.json, data/videos.json y posts/*.html.
Uso: python3 tools/build.py"""
import json,re,os,glob,html,datetime
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
B='https://admgrow.github.io/soporte-casero/'
CH='https://www.youtube.com/@soporteCasero'
REPO='https://github.com/AdmGrow/soporte-casero'
SITE='Soporte casero'
ORG={"@type":"Organization","name":"Soporte Casero","url":B,"sameAs":[CH,REPO],"logo":B+"img/logo.svg"}
C=json.load(open('data/curso.json'));V=json.load(open('data/videos.json'))
def e(x):return html.escape(str(x or ''),quote=True)
MES=['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
def fmt(f,hora=True):
    if not f:return ''
    y,m,d=f[:10].split('-');s=f'{d}/{m}/{y}'
    return s+(f' · {f[11:16]} (hora Argentina)' if hora and len(f)>10 else '')
NAV=[('curso/index.html','Curso Google Docs'),('blog/index.html','Lecciones'),('calendario/index.html','Calendario'),('gestion/index.html','Gestión')]
def page(path,title,desc,body,ld=None,img=None,typ='website'):
    d='../'*path.count('/');url=B+re.sub(r'index\.html$','',path)
    lds=''.join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>' for x in (ld or []))
    ogi=B+(img or 'img/og.png')
    nav=''.join(f'<a href="{d}{h}"{" aria-current=page" if path.startswith(h.split("/")[0]+"/") else ""}>{t}</a>' for h,t in NAV)
    full=title if title.endswith(SITE) else f'{title} · {SITE}'
    return f'''<!doctype html><html lang="es-AR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="google-site-verification" content="DZyE-QFIWeNXQ9TOPrV2uCMqNhyqMSfGzKceuzIN4ek">
<title>{e(full)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}"><meta name="robots" content="index,follow">
<meta property="og:type" content="{typ}"><meta property="og:site_name" content="{SITE}"><meta property="og:locale" content="es_AR"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{ogi}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{d}img/logo.svg" type="image/svg+xml"><meta name="theme-color" content="#0b6bcb">
<link rel="stylesheet" href="{d}style.css"><script>try{{document.documentElement.dataset.theme=localStorage.getItem('tema')||(matchMedia('(prefers-color-scheme: dark)').matches?'oscuro':'claro')}}catch(e){{}}</script>{lds}</head>
<body><a class="skip" href="#main">Saltar al contenido</a>
<header class="top"><a class="logo" href="{d}index.html"><i aria-hidden="true">🛠</i> Soporte <b>casero</b></a>
<nav aria-label="Principal">{nav}<a href="{CH}" rel="noopener">YouTube</a>
<button class="tema" type="button" aria-label="Cambiar modo claro/oscuro">◐</button></nav></header>
<main id="main">{body}</main>
<footer><b>Soporte Casero</b> · tutoriales de tecnología para resolver en casa · <a href="{CH}" rel="noopener">Canal de YouTube @soporteCasero</a> · <a href="{REPO}" rel="noopener">Proyecto en GitHub</a><br>Capturas propias en documentos de ejemplo. Google Docs es una marca de Google LLC; este sitio no está afiliado a Google.</footer>
<script src="{d}app.js" defer></script></body></html>'''
def W(path,s):
    os.makedirs(os.path.dirname(path) or '.',exist_ok=True);open(path,'w').write(s)
def badge(est,fecha=None):
    da=f' data-fecha="{fecha}"' if est=='programado' and fecha else ''
    return f'<span class="badge {est}"{da}>{C["estados"][est]}</span>'
L=C['lecciones'];N=len(L)
hechas=[x for x in L if x['estado'] in('publicado','programado')]
quedan=N-len(hechas);co=C['conteo_real'];qop=co['total']-co['cubiertas']
def countdown(d):
    pct=round(100*len(hechas)/N)
    return f'''<div class="cd" role="status"><div><p class="kicker">Cuenta regresiva</p><div class="big">Quedan {quedan} de {N}</div><p class="date">tutoriales por publicar · opciones de menú: quedan {qop} de {co["total"]}</p></div><div class="bar" aria-label="{pct}% del curso listo"><span style="width:{max(pct,2)}%"></span></div></div>'''
# ---------- posts ----------
posts=[]
for f in sorted(glob.glob('posts/[0-9]*.html')):
    raw=open(f).read();meta,body=raw.split('\n',1);p=json.loads(meta);p['body']=body;posts.append(p)
posts.sort(key=lambda p:p['fecha'])
def img(m):
    src,alt=m[1],m[2]
    return f'<figure><img src="../img/lecciones/{src}" alt="{e(alt)}" loading="lazy" width="1225" height="800"><figcaption>{e(alt)} (captura propia).</figcaption></figure>'
for i,p in enumerate(posts):
    les=next(x for x in L if x['n']==p['leccion']);path=f'blog/{p["slug"]}.html'
    body=re.sub(r'\{IMG:([^:}]+):([^}]+)\}',img,p['body'])
    yt=p['youtube_id'];short=f'https://youtube.com/shorts/{yt}'
    vid=f'''<div class="estreno" data-fecha="{p["fecha"]}" data-yt="{yt}"><p><b>Estreno del Short:</b> {fmt(p["fecha"])}</p><p class="falta" aria-live="polite"></p><noscript><p><a href="{short}">Ver el Short en YouTube</a></p></noscript></div>'''
    prev=f'<a href="{posts[i-1]["slug"]}.html">← {e(posts[i-1]["titulo"])}</a>' if i else '<span></span>'
    nxt=f'<a href="{posts[i+1]["slug"]}.html">{e(posts[i+1]["titulo"])} →</a>' if i<len(posts)-1 else '<span></span>'
    art=f'''<article class="post"><p class="crumbs"><a href="../curso/index.html">Curso de Google Documentos</a> › {e(les["menu"])} › Lección {les["n"]}</p>
<p class="kicker">Lección {les["n"]} de {N} · menú {e(les["menu"])}</p><h1>{e(p["titulo"])}</h1>
<p class="date">Fecha del video: <time datetime="{p["fecha"]}">{fmt(p["fecha"])}</time> · {badge(les["estado"],p["fecha"])}</p>
{body}
<h2 id="video">Mirá el Short</h2>{vid}
<p class="src"><b>Fuente oficial:</b> <a href="{p["fuente"]}" rel="noopener">Ayuda de Editores de Documentos de Google</a>. Capturas propias en un documento de ejemplo («Lista de compras»). El video usa voz generada con IA.</p>
<p class="actions"><a class="btn" href="../curso/index.html">Ver el curso completo</a><a class="btn ghost" href="{CH}" rel="noopener">Suscribite al canal</a></p>
<nav class="pager" aria-label="Lecciones">{prev}{nxt}</nav></article>'''
    ld=[{"@context":"https://schema.org","@type":["Article","HowTo"],"headline":p['titulo'],"name":p['titulo'],"description":p['resumen'],"image":B+p['imagen'],"datePublished":p['fecha'],"dateModified":p['fecha'],"inLanguage":"es-AR","mainEntityOfPage":B+path,"author":ORG,"publisher":ORG,"keywords":', '.join(p['etiquetas']),"isPartOf":{"@type":"Course","name":C['curso'],"url":B+'curso/'},
        "step":[{"@type":"HowToStep","position":k+1,"name":re.sub('<[^>]+>','',h),"url":f'{B}{path}#paso-{k+1}'} for k,h in enumerate(re.findall(r'<h2 id="paso-\d">(.*?)</h2>',p['body']))],
        "video":{"@type":"VideoObject","name":p['titulo'],"description":p['resumen'],"thumbnailUrl":f'https://i.ytimg.com/vi/{yt}/hqdefault.jpg',"uploadDate":p['fecha'],"contentUrl":short,"embedUrl":f'https://www.youtube.com/embed/{yt}'}},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inicio","item":B},{"@type":"ListItem","position":2,"name":C['curso'],"item":B+'curso/'},{"@type":"ListItem","position":3,"name":p['titulo'],"item":B+path}]}]
    W(path,page(path,p['titulo'],p['resumen'],art,ld,p['imagen'],'article'))
def cards(d):
    return '<div class="grid">'+''.join(f'''<article class="card"><a href="{d}blog/{p["slug"]}.html"><img src="{d}{p["imagen"]}" alt="" loading="lazy" width="1225" height="800"></a><div class="cb"><p class="kicker">Lección {p["leccion"]} · {fmt(p["fecha"],False)}</p><h3><a href="{d}blog/{p["slug"]}.html">{e(p["titulo"])}</a></h3><p class="date">{e(p["resumen"][:150])}…</p></div></article>''' for p in reversed(posts))+'</div>'
W('blog/index.html',page('blog/index.html','Lecciones del curso de Google Docs','Lecciones paso a paso de Google Documentos del canal Soporte casero, con capturas reales, el Short de cada tema y la fuente oficial.',
  f'<p class="kicker">Lecciones</p><h1>Lecciones paso a paso</h1><p class="lead">Cada lección explica en texto y con capturas reales lo que muestra el Short. Las que todavía no salieron aparecen como «próximamente» en el <a href="../curso/index.html">curso</a>.</p>{cards("../")}',
  [{"@context":"https://schema.org","@type":"Blog","name":"Lecciones de Soporte casero","url":B+'blog/',"publisher":ORG,"inLanguage":"es-AR"}]))
# ---------- curso ----------
pmap={p['leccion']:p for p in posts}
def row(x,d='../'):
    p=pmap.get(x['n']);t=e(x['titulo'])
    if p and x['estado'] in('publicado','programado'): t=f'<a href="{d}blog/{p["slug"]}.html">{e(x.get("titulo_video") or x["titulo"])}</a><br><span class="soon">{fmt(x["fecha"])}</span>'
    else: t+=' <span class="soon">· próximamente</span>'
    if x.get('issue'): t+=f' <a class="soon" href="{REPO}/issues/{x["issue"]}" rel="noopener">issue #{x["issue"]}</a>'
    return f'<li><span class="n">{x["n"]:02d}</span><span>{t}</span>{badge(x["estado"],x.get("fecha"))}</li>'
b1=C['bloque1'];bl=[next(x for x in L if x['n']==n) for n in b1['lecciones']]
sec=f'''<section class="menu" id="bloque-1"><h2>{e(b1["nombre"])} <small>{len(bl)} Shorts + 1 video largo</small></h2><p class="date">Primer recorrido: lo mínimo para usar Docs. Cada Short se enlaza después al video largo del bloque.</p><ul class="les">{"".join(row(x) for x in bl)}<li><span class="n">▶</span><span>{e(b1["largo"]["titulo"])} <span class="soon">· video largo · próximamente</span> <a class="soon" href="{REPO}/issues/{b1["largo"]["issue"]}" rel="noopener">issue #{b1["largo"]["issue"]}</a></span>{badge(b1["largo"]["estado"])}</li></ul></section>'''
for m in C['menus']:
    ls=[x for x in L if x['menu']==m['menu']]
    sec+=f'''<section class="menu" id="{m["menu"].lower()}"><h2>Menú {e(m["menu"])} <small>{len(ls)} tutoriales · {m["opciones"]} opciones reales</small></h2><ul class="les">{"".join(row(x) for x in ls)}</ul></section>'''
idx=' · '.join(f'<a href="#{m["menu"].lower()}">{m["menu"]}</a>' for m in C['menus'])
cur=f'''<p class="kicker">Curso gratis · {N} tutoriales · 9 menús</p><h1>{e(C["curso"])}, menú por menú</h1>
<p class="lead">Un curso ordenado de Google Docs (Documentos de Google) en español: primero un Short de cada función, en 3 pasos, y después un video largo que ordena cada bloque.</p>
{countdown('../')}
<p>El curso sale del conteo real de la barra de menús de Docs en la web, en español ({fmt(co["fecha"],False)}): <b>{co["menus"]} menús, {co["opciones_nivel1"]} opciones y {co["subopciones"]} subopciones, {co["total"]} en total</b>, agrupadas en {N} tutoriales.</p>
<p><b>Estados:</b> {badge("publicado")} {badge("programado")} {badge("en-produccion")} {badge("pendiente")}</p>
<p>Ir a: <a href="#bloque-1">Bloque 1</a> · {idx}</p>{sec}'''
W('curso/index.html',page('curso/index.html','Curso de Google Documentos gratis, menú por menú','Curso gratis de Google Docs en español: 53 tutoriales ordenados por los 9 menús reales (Archivo, Editar, Ver, Insertar, Formato, Herramientas, Gemini, Extensiones y Ayuda).',cur,
  [{"@context":"https://schema.org","@type":"Course","name":C['curso'],"description":"Curso gratis de Google Docs en español, menú por menú, con Shorts y videos largos.","provider":ORG,"inLanguage":"es-AR","isAccessibleForFree":True,"url":B+'curso/',"hasCourseInstance":{"@type":"CourseInstance","courseMode":"online","courseWorkload":"PT1M"},"offers":{"@type":"Offer","price":0,"priceCurrency":"ARS","category":"Free"}}]))
# ---------- calendario ----------
vs=sorted(V['videos'],key=lambda v:v['fecha'])
def iss(n):return f'<a href="{REPO}/issues/{n}" rel="noopener">#{n}</a>' if n else '—'
def ytl(v):
    if not v.get('youtube_id') or v['estado']=='planificado': return '<span class="soon">—</span>'
    return f'<a href="https://youtube.com/{"shorts/" if v["tipo"]=="short" else "watch?v="}{v["youtube_id"]}" rel="noopener">{v["youtube_id"]}</a>'
DIAS=['lun','mar','mié','jue','vie','sáb','dom']
def dia(f):return DIAS[datetime.date(int(f[:4]),int(f[5:7]),int(f[8:10])).weekday()]
rows=''.join(f'''<tr class="r-{v["estado"]}{" r-largo" if v["tipo"]=="largo" else ""}"><td>{k+1}</td><td><time datetime="{v["fecha"]}">{dia(v["fecha"])} {fmt(v["fecha"],False)[:5]} · {v["fecha"][11:16]}</time></td><td>{e(v["titulo"])}<br><span class="soon">{"Short" if v["tipo"]=="short" else "Video largo"}{f" · lección {v['leccion']}" if v.get("leccion") else ""}{(f" · {v['menu']}" if v['menu']=='Bloque 1' else f" · menú {v['menu']}") if v.get("menu") else ""}</span></td><td>{ytl(v)}</td><td>{e(v["playlist"])}</td><td>{badge(v["estado"],v["fecha"])}</td><td>{f'<a href="../{v["post"]}">Post</a>' if v.get("post") else "—"}</td><td>{iss(v.get("issue"))}</td></tr>''' for k,v in enumerate(vs))
cnt={s:sum(v['estado']==s for v in vs) for s in ('publicado','programado','planificado')}
nl=sum(v['tipo']=='largo' for v in vs)
cal=f'''<p class="kicker">Proyecto de publicación · serie Google Docs</p><h1>Calendario de YouTube</h1><p class="lead">Todos los videos de la serie en orden de publicación: 2 por día, a las 09:00 y a las 17:00 (hora Argentina).</p>
<div class="box"><p><b>Importante:</b> las fechas «planificado» son tentativas. Cada video se publica solo después de que el dueño del canal lo aprueba; si se mueve uno, se corren los siguientes.</p></div>
<p><b>{len(vs)} videos</b> ({len(vs)-nl} Shorts y {nl} videos largos), del {fmt(vs[0]["fecha"],False)} al {fmt(vs[-1]["fecha"],False)}: {badge("publicado")} {cnt["publicado"]} · {badge("programado")} {cnt["programado"]} · {badge("planificado")} {cnt["planificado"]}</p>
<div class="tbl-wrap"><table><thead><tr><th>#</th><th>Fecha y hora (ART)</th><th>Título</th><th>YouTube</th><th>Playlist</th><th>Estado</th><th>Post</th><th>Issue</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="src">Fuente: <a href="{REPO}/blob/main/data/videos.json" rel="noopener">data/videos.json</a> · seguimiento en <a href="{REPO}/milestones" rel="noopener">milestones de GitHub</a>.</p>'''
W('calendario/index.html',page('calendario/index.html','Calendario de publicación en YouTube','Calendario de publicación de la serie de Google Docs de Soporte casero en YouTube: 2 videos por día, Shorts y videos largos, con estado y lección del sitio.',cal))
# ---------- gestión ----------
ges=f'''<p class="kicker">Cómo trabajamos</p><h1>Gestión del proyecto</h1>
<p class="lead">El proyecto se gestiona en GitHub: cada tutorial es un issue con su checklist y cada bloque o menú es un milestone.</p>
<h2>Dónde está cada cosa</h2><ul>
<li><a href="{REPO}/issues" rel="noopener">Issues</a>: un issue por tutorial (53) y uno por video largo.</li>
<li><a href="{REPO}/milestones" rel="noopener">Milestones</a>: Bloque 1 – Lo básico y uno por menú.</li>
<li><a href="{REPO}/labels" rel="noopener">Etiquetas</a>: una por menú y una por estado (short, largo, post, esperando-ok, programado, publicado).</li>
<li><a href="../calendario/index.html">Calendario</a>: orden de publicación en YouTube.</li></ul>
<h2>Flujo de cada tutorial</h2><ol>
<li>Capturas reales en un documento de ejemplo (nunca datos personales).</li><li>Diapositivas en Google Slides.</li><li>Video en Google Vids con voz IA.</li>
<li>OK del dueño del canal antes de subir.</li><li>Programado en YouTube, en su playlist.</li><li>Post de la lección en este sitio, enlazado desde la descripción del video.</li><li>Cuando existe el video largo del bloque, cada Short lo enlaza como «Video relacionado».</li></ol>
<h2>Estados</h2><p>{badge("publicado")} salió en YouTube · {badge("programado")} con fecha en YouTube · {badge("en-produccion")} hecho, esperando OK · {badge("pendiente")} sin empezar.</p>
<p>Las instrucciones para agregar una lección están en el <a href="{REPO}#readme" rel="noopener">README del repositorio</a>.</p>'''
W('gestion/index.html',page('gestion/index.html','Gestión del proyecto','Cómo se organiza el proyecto Soporte casero en GitHub: issues por tutorial, milestones por menú, etiquetas de estado y calendario.',ges))
# ---------- inicio ----------
home=f'''<section class="hero"><p class="kicker">Canal de YouTube · @soporteCasero</p><h1>Soporte casero</h1>
<p class="lead">Tutoriales cortos de tecnología para resolver en casa, paso a paso y en español. Ahora: el curso completo de Google Documentos, menú por menú.</p>
<p class="actions"><a class="btn" href="curso/index.html">Ir al curso de Google Docs</a><a class="btn ghost" href="{CH}" rel="noopener">Ver el canal en YouTube</a></p></section>
{countdown('')}
<h2>Últimas lecciones</h2>{cards("")}
<h2>Cómo es el curso</h2><ul><li>Un Short por función, en 3 pasos, con capturas reales.</li><li>Un video largo por bloque que ordena esas funciones.</li><li>Una lección escrita en este sitio por cada video, con la fuente oficial de Google.</li></ul>'''
W('index.html',page('index.html','Soporte casero: tutoriales de Google Docs y tecnología en casa','Soporte casero: tutoriales cortos de tecnología en español. Curso gratis de Google Documentos menú por menú, con Shorts, lecciones escritas y capturas reales.',home,
  [{"@context":"https://schema.org","@type":"WebSite","name":SITE,"url":B,"inLanguage":"es-AR","publisher":ORG},dict({"@context":"https://schema.org"},**ORG)]))
W('404.html',page('404.html','Página no encontrada','La página que buscás no existe.',f'<h1>Página no encontrada</h1><p><a href="{B}">Volver al inicio</a> · <a href="{B}curso/">Curso de Google Docs</a></p>').replace('href="style.css"',f'href="{B}style.css"').replace('src="app.js"',f'src="{B}app.js"').replace('<meta name="robots" content="index,follow">','<meta name="robots" content="noindex">'))
# ---------- sitemap / robots ----------
hoy=datetime.date.today().isoformat()
urls=[('',hoy),('curso/',hoy),('blog/',hoy),('calendario/',hoy),('gestion/',hoy)]+[(f'blog/{p["slug"]}.html',p['fecha'][:10]) for p in posts]
W('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{B}{u}</loc><lastmod>{m}</lastmod></url>\n' for u,m in urls)+'</urlset>\n')
W('robots.txt',f'User-agent: *\nAllow: /\n\nSitemap: {B}sitemap.xml\n')
print('ok:',len(posts),'posts,',N,'lecciones, quedan',quedan)
