# Zhuo Lab website

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
| `static/media/gen/` | `hero-collagen.webp` (CSS background of the hero) and the logo mark |

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
| `hero_collagen.py` | `hero-collagen.webp` (2400x1500 simulated SHG collagen) | Home hero background (`template.scss`) |
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
