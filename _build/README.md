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
