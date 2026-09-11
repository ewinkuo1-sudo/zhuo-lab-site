"""Review square corners, page gutters, colour contrast and interactive states.
Uses the same local build/prefix as check_home_redesign.py. Saves review evidence.
"""
import argparse
import json
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright
from check_home_redesign import Quiet


def ready(page):
    page.locator('img').evaluate_all('(images)=>images.forEach(i=>i.loading="eager")')
    page.evaluate("async () => { await Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))); await new Promise(requestAnimationFrame); }")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--before', type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(('127.0.0.1', 18766), partial(Quiet, directory=str(args.root)))
    Thread(target=server.serve_forever, daemon=True).start()
    base = 'http://127.0.0.1:18766/zhuo-lab-site/'
    failures, results, interactions = [], [], []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel='msedge', headless=True)
            page = browser.new_page(reduced_motion='reduce')
            paths = ['', 'people/', 'research/', 'gallery/', 'news/', 'publication/',
                     'author/guan-yu-zhuo/', 'author/jackson-rodrigues/', 'join/', 'contact/', 'facilities/']
            for width in [1920, 1440, 1024, 768, 390, 320]:
                page.set_viewport_size({'width': width, 'height': 960})
                for lang in ['', 'zh/']:
                    for path in (paths if width in [1440, 320] else ['']):
                        print('Visual review', width, lang+path or '/', flush=True)
                        response = page.goto(base+lang+path, wait_until='networkidle')
                        ready(page)
                        info = page.evaluate("""() => {
                            const visible = e => { const r=e.getBoundingClientRect(); const s=getComputedStyle(e); return r.width>0 && r.height>0 && s.visibility!=='hidden' && s.display!=='none'; };
                            const els=[...document.querySelectorAll('body *')].filter(visible);
                            const rounded=els.filter(e=>['borderTopLeftRadius','borderTopRightRadius','borderBottomLeftRadius','borderBottomRightRadius'].some(k=>parseFloat(getComputedStyle(e)[k])>0)).map(e=>e.tagName+'.'+e.className).slice(0,8);
                            const frame=document.querySelector('.home-section .container, .universal-wrapper, .article-container');
                            const r=frame?.getBoundingClientRect();
                            const badImages=[...document.images].filter(i=>!i.closest('#map') && (!i.naturalWidth || (visible(i) && (i.width<2 || i.height<2)))).map(i=>i.src);
                            return {overflow:document.documentElement.scrollWidth>innerWidth,rounded,badImages,
                                frame:r?{left:r.left,right:innerWidth-r.right,width:r.width}:null};
                        }""")
                        info.update(width=width, path=lang+path, status=response.status)
                        results.append(info)
                        if response.status != 200 or info['overflow'] or info['rounded'] or info['badImages']:
                            failures.append(info)
                        if info['frame'] and (info['frame']['left']<23 or info['frame']['right']<23 or info['frame']['width']>1041):
                            failures.append({'gutters': info})
                        if not path and width in [1440,390]:
                            # Scroll once to reveal elements driven by IntersectionObserver before full-page capture.
                            page.evaluate('async () => { for(let y=0;y<document.body.scrollHeight;y+=700){scrollTo(0,y);await new Promise(requestAnimationFrame);}scrollTo(0,0);await new Promise(requestAnimationFrame); }')
                            prefix = 'zh' if lang else 'en'
                            page.screenshot(path=str(args.output/f'{prefix}-after-{width}.png'), full_page=True)
                            hidden_header=page.add_style_tag(content='header { visibility: hidden !important; }')
                            for section in ['home','research','publications','people','activities','join']:
                                page.locator('#'+section).screenshot(path=str(args.output/f'{prefix}-{section}-{width}.png'))
                            hidden_header.evaluate('(el)=>el.remove()')
                        if not path and width in [1440,320]:
                            page.evaluate('scrollTo(0,0)')
                            page.locator('.i18n-dropdown > a').click()
                            menu=page.locator('.i18n-dropdown .dropdown-menu')
                            menu.wait_for(state='visible')
                            menu.locator('a.dropdown-item').click()
                            page.wait_for_load_state('networkidle')
                            expected=base if lang else base+'zh/'
                            assert page.url==expected, page.url
                            page.goto(base+lang,wait_until='networkidle')
                            if width<992:
                                page.locator('.navbar-toggler').click()
                                page.locator('#navbar-content').wait_for(state='visible')
                                page.locator('#navbar-content a.nav-link').filter(has_text='成員' if lang else 'People').click()
                                page.wait_for_function("document.querySelector('#people').getBoundingClientRect().top >= 0 && document.querySelector('#people').getBoundingClientRect().top < 150")
                                page.evaluate('scrollTo(0,0)')
                            page.locator('.navbar .js-search').click()
                            query=page.locator('#search-query')
                            query.wait_for(state='visible')
                            query.fill('collagen')
                            query.press('Enter')
                            page.wait_for_selector('.search-hit', timeout=15000)
                            assert page.locator('.search-hit').count()>0
                            page.keyboard.press('Escape')
                            query.wait_for(state='hidden')
                            page.locator('.zl-hero-actions a').first.focus()
                            page.keyboard.press('Tab')
                            focus=page.evaluate("() => {let e=document.activeElement,s=getComputedStyle(e);return {tag:e.tagName,outline:s.outlineStyle,width:parseFloat(s.outlineWidth)};}")
                            assert focus['tag']=='A' and focus['outline']!='none' and focus['width']>=2, focus
                            interactions.append({'width':width,'language':lang or 'en','language_switch':True,'menu':True,'search':True,'keyboard_focus':focus})
            # Measure real rendered foreground/background pairs, including button hover and focus.
            page.set_viewport_size({'width':1440,'height':1000})
            page.goto(base,wait_until='networkidle')
            contrasts=[]
            selectors=['.zl-hero-copy h1','.zl-hero-statement','.zl-hero-description',
                       '.zl-hero-figure figcaption','.zl-hero-actions .btn-primary',
                       '.zl-news-category','.zl-news-award','.zl-milestones time',
                       '.zl-highlight-copy .zl-image-credit','.zl-event-category',
                       '#join .section-heading h1','#join .section-heading > p',
                       '#join .zl-apply p','#join .zl-apply .btn-primary',
                       '.zl-member-copy p','.navbar .nav-link']
            for selector in selectors:
                node=page.locator(selector).first
                for state in (['normal','hover','focus'] if '.btn' in selector else ['normal']):
                    page.mouse.move(0,0)
                    if state=='hover': node.hover()
                    if state=='focus': node.focus()
                    pair=node.evaluate(r"""e=>{
                      const rgb=s=>(s.match(/[\d.]+/g)||[]).map(Number);
                      const style=getComputedStyle(e); let bg=null,gradient=false;
                      for(let n=e;n;n=n.parentElement){let s=getComputedStyle(n),c=rgb(s.backgroundColor);if(s.backgroundImage.includes('gradient'))gradient=true;if(c.length===3||c[3]===1){bg=c;break;}}
                      if(!bg)bg=[255,255,255];
                      // Hero uses a navy gradient; use its lighter endpoint for conservative contrast.
                      if(gradient)bg=[32,62,88];
                      const lum=c=>c.slice(0,3).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4}).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0);
                      let a=lum(rgb(style.color)),b=lum(bg);
                      return {foreground:style.color,background:bg,ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05)};
                    }""")
                    pair.update(selector=selector,state=state)
                    contrasts.append(pair)
                    if pair['ratio']<4.5: failures.append({'contrast':pair})
            if args.before:
                old=ThreadingHTTPServer(('127.0.0.1',18768),partial(Quiet,directory=str(args.before)))
                Thread(target=old.serve_forever,daemon=True).start()
                try:
                    for width in [1440,390]:
                        page.set_viewport_size({'width':width,'height':960})
                        for lang in ['', 'zh/']:
                            page.goto('http://127.0.0.1:18768/zhuo-lab-site/'+lang,wait_until='networkidle')
                            ready(page)
                            page.evaluate('async () => { for(let y=0;y<document.body.scrollHeight;y+=700){scrollTo(0,y);await new Promise(requestAnimationFrame);}scrollTo(0,0);await new Promise(requestAnimationFrame); }')
                            prefix='zh' if lang else 'en'
                            page.screenshot(path=str(args.output/f'{prefix}-before-{width}.png'),full_page=True)
                finally:
                    old.shutdown()
            browser.close()
    finally:
        server.shutdown()
    report={'views':len(results),'results':results,'interactions':interactions,'contrasts':contrasts,'failures':failures}
    (args.output/'visual-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'views':len(results),'interactions':len(interactions),'contrast_pairs':len(contrasts),'failures':failures},ensure_ascii=False,indent=2))
    assert not failures

if __name__=='__main__':
    main()
