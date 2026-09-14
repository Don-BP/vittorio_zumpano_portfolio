# Vittorio Zumpano — portfolio

The live page is served from `docs/` by GitHub Pages.

- `docs/index.html` — the finished portfolio, a single self-contained file
- `docs/TalentDesk_Presentation.html` — the TalentDesk product walkthrough the page links to
- `_portfolio_source/` — the editable source

## Rebuilding

All wording lives in `_portfolio_source/src/03_copy.js`. After editing:

```
cd _portfolio_source
python build_portfolio.py
```

That writes the finished file, which is then copied over `docs/index.html`.

The page carries a `noindex` instruction and `docs/robots.txt` disallows crawlers,
so it is reachable by link but stays out of search results.
