"""Offline check of internal links in a built Hugo site.

Usage: python scripts/check_links.py PUBLIC_DIR BASE_URL
Every href/src that points inside BASE_URL (absolute, root-relative or relative) must resolve to a file in
PUBLIC_DIR, and a #fragment on an HTML target must match an id on that page. External links are not fetched.
Exit code 1 if anything is broken.
"""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if not v:
                continue
            if k == 'id' or (k == 'name' and tag == 'a'):
                self.ids.add(v)
            elif k in ('href', 'src'):
                self.links.append(v)
            elif k == 'srcset':
                self.links += [part.strip().split(' ')[0] for part in v.split(',') if part.strip()]


def main():
    public = Path(sys.argv[1]).resolve()
    base = sys.argv[2].rstrip('/') + '/'
    prefix = urlsplit(base).path
    host = urlsplit(base).netloc
    pages = {}

    def parse(f):
        if f not in pages:
            p = Page()
            p.feed(f.read_text(encoding='utf-8', errors='replace'))
            pages[f] = p
        return pages[f]

    def target(path):
        if not path.startswith(prefix):
            return None
        f = public / unquote(path[len(prefix):])
        if f.is_dir():
            f = f / 'index.html'
        return f

    broken = []
    files = sorted(public.rglob('*.html'))
    for f in files:
        rel = f.relative_to(public).as_posix()
        page_url = base + (rel[:-len('index.html')] if rel.endswith('index.html') else rel)
        for link in parse(f).links:
            if link.startswith(('mailto:', 'tel:', 'javascript:', 'data:', '#')) and not link.startswith('#'):
                continue
            u = urlsplit(urljoin(page_url, link))
            if u.scheme not in ('http', 'https') or u.netloc != host:
                continue
            t = target(u.path)
            if t is None:
                continue  # same host but outside this site
            if not t.is_file():
                broken.append((rel, link, 'missing file'))
            elif u.fragment and t.suffix == '.html' and unquote(u.fragment) not in parse(t).ids \
                    and unquote(u.fragment) != 'top' and t.parent.name != 'publication':
                # the publication list reads its #fragment in JavaScript as a type filter, not as an anchor
                broken.append((rel, link, 'missing anchor'))
    for rel, link, why in broken:
        print('::warning file=%s::%s -> %s (%s)' % (rel, rel, link, why))
    print('%d pages checked, %d broken internal links' % (len(files), len(broken)))
    return 1 if broken else 0


if __name__ == '__main__':
    sys.exit(main())
