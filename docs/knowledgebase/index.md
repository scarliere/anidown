# Anidown Knowledgebase

This knowledgebase documents the current intent and function-level behavior of the Anidown application.

## App Intent

Anidown is a small Python desktop utility for finding anime episode torrents on Nyaa.si and saving matching `.torrent` files locally. It keeps a JSON record of anime titles, preferred release group/subber, and the latest tracked episode so future downloads can continue from the next episode.

The current code supports two usage styles:

- A Tkinter GUI launched by `python main.py`.
- A background polling loop in `anidown.app.run()` that can repeatedly check saved anime entries.

## Knowledgebase Pages

- [Architecture](architecture.md): module responsibilities and runtime flow.
- [Function Catalog](functions.md): every public function/class in the current code and what it is intended to do.
- [Data Model](data-model.md): JSON files, fields, paths, and expected value shapes.
- [Operations](operations.md): setup assumptions, run commands, and operational caveats.

## Source Map

- `main.py`: repository-root GUI launcher.
- `src/anidown/gui.py`: Tkinter interface and one-shot download workflow.
- `src/anidown/processor.py`: Nyaa RSS search, title matching, and torrent download logic.
- `src/anidown/mal_scraper.py`: MyAnimeList search and episode-count scraping.
- `src/anidown/app.py`: polling loop that combines saved anime, MAL counts, and Nyaa downloads.
- `src/anidown/paths.py`: central project, data, and download paths.
