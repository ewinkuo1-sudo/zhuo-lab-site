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
