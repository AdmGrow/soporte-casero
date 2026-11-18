(function(){
var R=document.documentElement;
var tb=document.querySelector('.tema');if(tb)tb.onclick=function(){var t=R.dataset.theme==='oscuro'?'claro':'oscuro';R.dataset.theme=t;try{localStorage.setItem('tema',t)}catch(e){}};
function left(f){var s=(new Date(f)-Date.now())/1000;if(s<=0)return null;var d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60);return(d?d+' d ':'')+h+' h '+m+' min'}
function tick(){
 document.querySelectorAll('.estreno[data-fecha]').forEach(function(el){var l=left(el.dataset.fecha),c=el.querySelector('.falta');
  if(l){if(c)c.textContent='Faltan '+l}else if(!el.dataset.done){el.dataset.done=1;el.outerHTML='<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/'+el.dataset.yt+'" title="Short de YouTube" loading="lazy" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div><p><a class="btn sm" href="https://youtube.com/shorts/'+el.dataset.yt+'" rel="noopener">Ver el Short en YouTube</a></p>'}});
 // estado programado -> publicado cuando pasa la fecha
 document.querySelectorAll('.badge.programado[data-fecha]').forEach(function(b){if(!left(b.dataset.fecha)){b.className='badge publicado';b.textContent='Publicado'}});
}
tick();setInterval(tick,30000);
})();
