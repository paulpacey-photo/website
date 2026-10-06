# How this site is built

The live site (the files in the folder above this one) is generated from the design boards in `project/`.

- `project/*.dc.html` – the page designs (desktop and mobile boards) exported from the Claude Design canvas:
  https://claude.ai/artifact/2WfPZ5bcrJWDGbETHF5nRG
- `assets/` – original images and logos used by the boards
- `build.py` – turns the boards into the responsive site (needs Python 3 and Pillow)
- `site.js`, `site.css`, `fit.js` – menu, slider, form behaviour and layout scaling
- `wix.js` – sends form entries to Wix Forms (site "Paul Pacey – Forms")

## To change the site

1. Update the board(s) in `project/` (or re-export them from the canvas).
2. Run `python3 _build/build.py` from the repository root.
3. Copy everything in `_build/dist/` to the repository root, replacing the old files. Keep `CNAME`, `.nojekyll`, `README.md` and `_build/`.
4. Commit and push. GitHub Pages republishes within a minute or two.

## Articles

Each article is a set of boards in `project/` named `Article-<Slug>*.dc.html` (desktop split into 2 boards, mobile into 3, because canvas boards max out at 8000px tall). `tools/make_article.py` generates them from the article text; copy it, replace the content blocks, run it, then add the page to `PAGES` and `AUTO_HEIGHT` in `build.py`. Scroll effects (reveal, highlighted words, parallax bands, reading-progress bar) come from `site.js`/`site.css` and are driven by `data-reveal`, `data-hl`, `data-parallax` and `data-article` attributes.
