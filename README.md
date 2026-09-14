# Vittorio Zumpano — portfolio

Live: **https://don-bp.github.io/vittorio_zumpano_portfolio/**

- `docs/index.html` — the finished portfolio, one self-contained file
- `docs/TalentDesk_Presentation.html` — the product walkthrough the page links to
- `_portfolio_source/` — a mirror of the editable source, kept as a backup

The page carries a `noindex` instruction and `docs/robots.txt` disallows crawlers,
so it is reachable by link but stays out of search results.

## Updating it

The source of truth is `D:\Don_Portfolio\_portfolio_source`, not the mirror in
this repo. All wording lives in `src/03_copy.js`. To rebuild and publish:

```
cd D:\Don_Portfolio\_portfolio_source
python publish.py
```

That builds the file, refreshes `docs/` and this mirror, commits and pushes.
GitHub Pages picks it up a minute or two later.
