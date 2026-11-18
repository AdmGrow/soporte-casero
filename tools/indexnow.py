#!/usr/bin/env python3
"""Envía URLs a IndexNow (Bing, Yandex, Seznam, Naver, etc.). Correr DESPUÉS de que GitHub Pages termine el deploy.
Uso: python3 tools/indexnow.py            -> todas las URLs de sitemap.xml
     python3 tools/indexnow.py URL [URL]  -> solo esas URLs"""
import sys,os,re,glob,json,urllib.request
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
B='https://admgrow.github.io/soporte-casero/'
key=[os.path.basename(f)[:-4] for f in glob.glob('*.txt') if re.fullmatch(r'[0-9a-f]{32}\.txt',os.path.basename(f))][0]
urls=sys.argv[1:] or re.findall(r'<loc>([^<]+)</loc>',open('sitemap.xml').read())
assert urllib.request.urlopen(B+key+'.txt').read().decode().strip()==key,'archivo de clave no publicado todavía'
data=json.dumps({"host":"admgrow.github.io","key":key,"keyLocation":B+key+'.txt',"urlList":urls}).encode()
req=urllib.request.Request('https://api.indexnow.org/indexnow',data=data,headers={'Content-Type':'application/json; charset=utf-8'})
try: r=urllib.request.urlopen(req,timeout=30);print('HTTP',r.status,r.reason,'-',len(urls),'URLs');print(r.read().decode()[:300])
except urllib.error.HTTPError as ex: print('HTTP',ex.code,ex.reason);print(ex.read().decode()[:500]);sys.exit(1)
