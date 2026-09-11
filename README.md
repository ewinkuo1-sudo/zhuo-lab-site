# Zhuo Lab website

[網站配色、直角與留白改版計畫](NEXT_SESSION_PLAN.md)（2026-09-11；已完成）。驗證與比較圖見 [改版紀錄](docs/visual-refresh-review.md)。

Lab website for Prof. Guan-Yu Zhuo, Institute of Biophotonics, National Yang Ming Chiao Tung University.
Built with [Hugo Blox](https://hugoblox.com) (research-group template, blox-bootstrap v5) and deployed to GitHub Pages.

## Layout

| Path | What |
|---|---|
| `content/en/` | English pages: home, research, people, publication, facilities, join, contact |
| `content/zh/` | Traditional Chinese pages (publications are not translated; the zh menu links to the English list) |
| `content/en/authors/<slug>/` | One folder per person. `user_groups` decides which section of People they appear in |
| `publications.bib` | Source of truth for the Publications page. Edit or export from Zotero, push, and a GitHub Action opens a PR that regenerates `content/en/publication/` |
| `config/_default/` | Site config. `languages.yaml` holds the Chinese menu |
| `.github/workflows/publish.yaml` | Builds with Hugo **0.135.0** (pinned) and deploys to GitHub Pages on push to `main` |
| `layouts/partials/blocks/features.html` | Override of the Hugo Blox features block: adds `image`, `image_alt` and `url` per item (research cards) |
| `scripts/imagegen/` | Deterministic Python/SVG generators for every illustration on the site (see below) |
| `assets/media/gen/` | Illustrations used by content (research thumbs, beam-path schematic); Hugo resizes them to WebP |
| `static/media/gen/` | Legacy concept artwork and the logo mark; the current hero uses `assets/media/gallery/lab-04.png` |

## Local preview (Windows)

Hugo 0.135.0 extended and Go are kept as portable binaries under `..\tools\` so the local build matches CI exactly.

```powershell
$env:PATH = "C:\Users\ewink\rc-desktop\tools\go-1.27.0\bin;$env:PATH"
C:\Users\ewink\rc-desktop\tools\hugo-0.135.0\hugo.exe server -D
```

Then open http://localhost:1313/ (Chinese at /zh/).

## Regenerate publications locally

```powershell
pip install academic==0.10.0
academic import publications.bib content/en/publication/ --compact
```

## Adding a person

Copy `content/en/authors/guan-yu-zhuo/` to a new slug (e.g. `wang-xiao-ming`), replace `avatar.jpg`,
edit `_index.md`, and set `user_groups` to one of: Principal Investigator, Graduate Students,
Undergraduate Students, Alumni. Set `superuser: false`.

## Upgrading Hugo Blox

Hugo Blox has shipped breaking changes several times. Bump `WC_HUGO_VERSION` in `publish.yaml`, the module
versions in `go.mod`, and the local `tools\hugo-*` binary together, once a year at most, and check the
Hugo Blox release notes first.

## Illustrations (simulated, not data)

The placeholder research illustrations are generated procedurally by the scripts in `scripts/imagegen/` (numpy, scipy, Pillow,
matplotlib; SVG rendered with headless Chromium). They are *simulations* of what the lab's modalities look like,
labelled as illustrations on the pages, and should be replaced by real micrographs as soon as the PI supplies them.

| Script | Output | Used by |
|---|---|---|
| `hero_collagen.py` | `hero-collagen.webp` (2400x1500 simulated SHG collagen) | Legacy hero artwork (the current hero uses a supplied research image) |
| `thumb_multimodal.py` | `thumb-multimodal.webp` (SHG + TPEF + CARS composite) | Home card 1, Research |
| `thumb_pshg.py` | `thumb-pshg.webp` (P-SHG orientation map) | Home card 2, Research |
| `thumb-endoscope.py` | `thumb-endoscope.webp` (probe schematic) | Home card 3, Research |
| `thumb-ai.py` | `thumb-ai.webp` (tile classifier overlay) | Home card 4, Research |
| `facilities-beampath.py` | `facilities-beampath.svg` (multiphoton beam path) | Facilities |
| `logo-mark.py` | `logo-mark.svg`, `wordmark.svg` | `assets/media/logo.svg` (navbar), OG image |
| `sharing.html` | `sharing.png` / `sharing-zh.png` (1200x630 Open Graph) | `assets/media/sharing.png` |

Scripts write to `static/media/gen/`; copy the WebP/SVG files you want into `assets/media/gen/` (or `assets/media/logo.svg`,
`assets/media/sharing.png`) after regenerating. Run e.g. `python3 scripts/imagegen/thumb_pshg.py`.
To replace an illustration with a real image, drop the real file in `assets/media/gen/` under the same name and delete the script.

## Imported Google Sites content (2026-09-11)

The supplied Google Sites snapshot adds five microscopy images in `assets/media/gallery/`, a bilingual Gallery, and the lab's full English name in the home-page introduction. `data/gallery.yaml` holds bilingual display text; `docs/gallery-sources.json` records hashes and original dimensions. Original files are preserved; Hugo creates responsive WebP previews without cropping. Image descriptions only describe visible appearance; sample types, imaging modalities and publication matches still need source captions.

`data/lab_news.yaml` is the shared news content for the home pages and new bilingual News pages. Supplied, explicitly named portraits were added for Guan-Yu Zhuo and Jackson Rodrigues in both languages. The remaining unlabelled portraits were not assigned.

## Full source-folder follow-up

See `docs/website-source-audit.md` for the complete source review and unresolved gaps. Six additional member portraits, source-backed bilingual biographies, three member profiles, a group photo and a sixth gallery image were added. The first two gallery originals now use the higher-resolution supplied source files. Existing profile URLs remain stable.

## People layout and events

The lab_people block displays full bilingual author biographies alongside rectangular, uncropped portraits. data/people_order.json follows the reference screenshot order; new author profiles are appended automatically. Edit biographies in the existing author files.

The lab_events block uses data/lab_events.json for bilingual event captions and image paths on Home, News and Gallery. Unspecified dates are omitted. Image provenance is in docs/event-photo-sources.json.


## Homepage redesign (2026-09-11)

Home now leads with a real lab image and research mission, followed by news, four research directions, three selected papers, PI, milestones, compact member cards, image and activity previews, recruitment and contact. Full People and author pages remain available.

- `data/highlights.json`: bilingual selected-paper summaries and attributed figures; titles, journals, years and DOIs come from existing publication pages.
- `data/gallery.yaml`: eight images, including two newly sourced paper figures and five originals awaiting scientific captions.
- `layouts/partials/lab_url.html`: language-aware page links using actual page permalinks. The navbar override fixes homepage anchors when deployed under a GitHub Pages project path.
- `lab_people` with `compact: true`: profile summaries on Home; full biographies on People.
- `docs/homepage-figure-sources.json`: figure provenance, hashes and open licences where applicable. Original figures remain uncropped; Hugo generates WebP previews.
- Homepage metrics count website records; they do not claim lab-only lifetime output or unverified clinical partnerships.

Browser verification requires Python with Playwright and Microsoft Edge. Build with the deployment prefix so the Chinese URL regression is exercised:

```powershell
$env:PATH = "C:\Users\ewink\.cache\zhuo-site-tools\go\go\bin;" + $env:PATH
& 'C:\Users\ewink\.cache\zhuo-site-tools\hugo\hugo.exe' --minify --baseURL 'http://127.0.0.1:18766/zhuo-lab-site/' --destination 'C:\Users\ewink\.cache\zhuo-site-review\redesign-public\zhuo-lab-site'
& 'C:\Users\ewink\AppData\Local\Programs\Python\Python312\python.exe' scripts/check_home_redesign.py --root 'C:\Users\ewink\.cache\zhuo-site-review\redesign-public' --output 'C:\Users\ewink\.cache\zhuo-site-review\redesign'
```

## Colour and spacing refresh (2026-09-11)

The bilingual site now uses square corners, a centered 1040 px content width, wider gutters, a two-column research grid and compact horizontal member cards on narrow phones. Navy and teal distinguish research content; warm accents distinguish lab life and milestones. See `docs/visual-refresh-review.md` for browser checks and before/after screenshots.

## Hero background and research alignment (2026-09-11)

The bilingual homepage now uses the supplied microscopy image as an uncropped background with a separate readability gradient and a direct original-image link. Research detail pages reuse the home research names, order, images, credits and stable anchors. `data/research.json` holds bilingual evidence summaries and publication slugs; `lab_research.html` reads publication metadata from the English records.

See [validation and previews](docs/research-hero-review.md), [source audit](docs/research-content-audit.md), and [future sessions](FUTURE_ROADMAP.md). Current project progress and equipment capabilities still require confirmation; the audit distinguishes published evidence from unverified drafts.
