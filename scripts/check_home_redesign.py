"""Browser smoke checks for a bilingual Hugo site served under a project prefix.
Build with baseURL http://127.0.0.1:18766/zhuo-lab-site/ before running.
Usage: python scripts/check_home_redesign.py --root BUILD_PARENT --output SCREENSHOT_DIR
"""
import argparse,json
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
from urllib.parse import urlsplit,unquote
from html.parser import HTMLParser
from playwright.sync_api import sync_playwright
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args): pass
class IDs(HTMLParser):
 def __init__(self): super().__init__(); self.ids=set()
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k=='id': self.ids.add(v)
def main():
 parser=argparse.ArgumentParser(); parser.add_argument('--root',type=Path,required=True); parser.add_argument('--output',type=Path,required=True); args=parser.parse_args(); args.output.mkdir(parents=True,exist_ok=True)
 server=ThreadingHTTPServer(('127.0.0.1',18766),partial(Quiet,directory=str(args.root)))
 Thread(target=server.serve_forever,daemon=True).start()
 base='http://127.0.0.1:18766/zhuo-lab-site/'; results=[]; failures=[]; fetched={}
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch(channel='msedge',headless=True)
   for width in [1440,1024,768,390]:
    page=browser.new_page(viewport={'width':width,'height':1000},device_scale_factor=1,reduced_motion='reduce')
    for suffix in ['','zh/']:
     print('Checking', width, suffix or '/', flush=True)
     response=page.goto(base+suffix,wait_until='networkidle')
     page.locator('img').evaluate_all('(images)=>images.forEach(i=>i.loading="eager")')
     page.wait_for_function('Array.from(document.images).every(i=>i.complete)')
     info=page.evaluate('''() => ({overflow:document.documentElement.scrollWidth>innerWidth,broken:[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src),duplicateIds:[...document.querySelectorAll('[id]')].map(e=>e.id).filter((v,i,a)=>a.indexOf(v)!==i),members:document.querySelectorAll('.zl-member-card').length,highlights:document.querySelectorAll('.zl-highlight').length,piPhotos:document.querySelectorAll('.zl-pi img').length,sections:[...document.querySelectorAll('section[id]')].map(e=>e.id)})''')
     info.update(width=width,path=suffix,status=response.status); results.append(info)
     if info['overflow'] or info['broken'] or info['duplicateIds'] or info['status']!=200 or info['members']!=12 or info['highlights']!=3 or info['piPhotos']!=1: failures.append(info)
     # Check the actual generated URLs, including fragment targets and the deployment prefix.
     for href in page.locator('a[href]').evaluate_all('(a)=>a.map(x=>x.href)'):
      u=urlsplit(href)
      if u.netloc!='127.0.0.1:18766': continue
      key=u.scheme+'://'+u.netloc+u.path
      if key not in fetched:
       r=page.request.get(key); ids=IDs()
       if 'text/html' in r.headers.get('content-type',''): ids.feed(r.text())
       fetched[key]=(r.status,ids.ids)
      status,ids=fetched[key]
      if status!=200 or (u.fragment and unquote(u.fragment) not in ids): failures.append({'path':suffix,'href':href,'status':status,'missing_fragment':u.fragment if unquote(u.fragment) not in ids else ''})
     if width in [1440,390]:
      page.evaluate('async () => { await Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))); await new Promise(requestAnimationFrame); }')
      prefix='zh' if suffix else 'en'
      page.screenshot(path=str(args.output/f'{prefix}-home-{width}.png'),full_page=True)
      capture_style=page.add_style_tag(content='header { visibility: hidden !important; }')
      page.locator('#home').screenshot(path=str(args.output/f'{prefix}-hero-{width}.png'))
      for section in ['research','publications','people']:
       page.locator('#'+section).screenshot(path=str(args.output/f'{prefix}-{section}-{width}.png'))
     if width in [1440,390]: capture_style.evaluate('(el)=>el.remove()')
     page.evaluate('window.scrollTo(0,0)')
     if width<992:
      button=page.locator('.navbar-toggler'); button.click(); page.wait_for_function('document.querySelector("#navbar-content").classList.contains("show")')
     page.locator('#navbar-content a.nav-link').filter(has_text='成員' if suffix else 'People').click()
     page.wait_for_function('document.querySelector("#people").getBoundingClientRect().top >= 0 && document.querySelector("#people").getBoundingClientRect().top < 150')
     if urlsplit(page.url).path!=urlsplit(base+suffix).path: failures.append({'navigation':page.url})
    page.close()
   page=browser.new_page(viewport={'width':390,'height':900})
   for suffix in ['people/','zh/people/','research/','zh/research/','gallery/','zh/gallery/','news/','zh/news/','publication/']:
    response=page.goto(base+suffix,wait_until='networkidle')
    page.locator('img').evaluate_all('(images)=>images.forEach(i=>i.loading="eager")')
    page.wait_for_function('Array.from(document.images).every(i=>i.complete)')
    info=page.evaluate('''() => ({overflow:document.documentElement.scrollWidth>innerWidth,broken:[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src),people:document.querySelectorAll('.zl-person').length,nav:[...document.querySelectorAll('#navbar-content a.nav-link')].map(a=>a.href)})''')
    info.update(path=suffix,status=response.status); results.append(info)
    if info['overflow'] or info['broken'] or response.status!=200: failures.append(info)
    if suffix.endswith('people/') and info['people']!=13: failures.append({'lost_profiles':info})
    expected=base+('zh/' if suffix.startswith('zh/') else '')
    if any(not h.startswith(expected+'#') for h in info['nav']): failures.append({'subpage_nav':info})
   browser.close()
 finally: server.shutdown()
 output={'views':len(results),'unique_internal_urls':len(fetched),'failures':failures,'results':results}
 (args.output/'checks.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'views':len(results),'unique_internal_urls':len(fetched),'failures':failures},ensure_ascii=False,indent=2))
 assert not failures
if __name__=='__main__': main()
