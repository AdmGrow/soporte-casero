# Soporte casero

Sitio y gestión del canal de YouTube [Soporte casero (@soporteCasero)](https://www.youtube.com/@soporteCasero).

- Sitio: https://admgrow.github.io/soporte-casero/
- Curso de Google Documentos: https://admgrow.github.io/soporte-casero/curso/
- Calendario de YouTube: https://admgrow.github.io/soporte-casero/calendario/

## Cómo se gestiona
- **Issues**: uno por tutorial (53) y uno por video largo, con checklist: capturas reales → Slides → Vids → OK del dueño → programado en YouTube → post en el sitio → enlace Short → largo.
- **Milestones**: Bloque 1 – Lo básico y uno por menú (Archivo, Editar, Ver, Insertar, Formato, Herramientas, Gemini, Extensiones, Ayuda).
- **Etiquetas**: una por menú y una por estado: `short`, `largo`, `post`, `esperando-ok`, `programado`, `publicado`.
- Nada se sube a YouTube sin el OK del dueño del canal. Sin datos personales en capturas ni commits.

## Estructura
```
data/curso.json      53 lecciones (estado, fecha, Short, post, issue) + conteo real de menús
data/videos.json     calendario de YouTube, una fila por video, en orden de salida
posts/AAAA-MM-DD-slug.html   fuente de cada lección (1.ª línea = JSON de metadatos)
img/lecciones/<tema>/        capturas reales en WebP
tools/build.py       genera index, curso/, blog/, calendario/, gestion/, 404, sitemap.xml y robots.txt
```

## Agregar una lección
1. Capturas → `img/lecciones/<tema>/*.webp` (recortadas, sin barra del navegador, cuenta ni mail).
2. Copiá un post de `posts/` a `posts/AAAA-MM-DD-<slug>.html`. Primera línea JSON: `titulo`, `slug` (corto y definitivo: la URL queda `blog/<slug>.html` y se pone en la descripción del video), `fecha` (ISO con `-03:00`), `leccion`, `youtube_id`, `fuente`, `resumen`, `imagen`, `etiquetas`. Pasos como `<h2 id="paso-1">`…; imágenes con `{IMG:<tema>/archivo.webp:texto alternativo}`.
3. En `data/curso.json`, en la lección: `estado` (`programado`/`publicado`/`en-produccion`/`pendiente`), `fecha`, `youtube_id`, `post`, `titulo_video`. Si suma opciones de menú, subí `conteo_real.cubiertas`.
4. En `data/videos.json` agregá la fila del video.
5. `python3 tools/build.py`, commit y push. Cerrá o actualizá el issue.
