# Architecture

## High-Level Purpose

Anidown automates a narrow workflow:

1. Track anime titles and their last downloaded episode in JSON.
2. Search Nyaa RSS for a release group, title, episode number, and resolution.
3. Download the first matching `.torrent` file.
4. Update the local episode record after a successful download.

## Runtime Entry Points

### GUI Entry Point

`main.py` is the default entry point. It disables bytecode generation, adds `src` to `sys.path`, imports `anidown.gui.run_gui`, and starts the Tkinter app.

The GUI lets the user enter:

- Anime title.
- Subber/release group.
- Next episode number.
- Destination folder for the `.torrent` file.

When the user clicks **Add and Download**, the GUI starts a background thread that calls `processor.processpage_with_resolution_fallback()`. On success, the GUI stores the anime in `data/latest_episodetest.json`.

### Polling Entry Point

`anidown.app.run(interval_seconds=60)` is a non-GUI loop. It reads the saved anime list, checks MyAnimeList for the total episode count, attempts to download the next episode, updates the saved list on success, and sleeps before repeating.

This loop is not currently called from `main.py`, but it is available as application logic.

## Module Responsibilities

### `gui.py`

Owns the desktop interface and user interaction. It handles form validation, status messages, saved-anime list rendering, and running downloads in a background thread so the UI does not freeze.

### `processor.py`

Owns Nyaa-facing torrent lookup and download behavior. It builds RSS URLs, parses RSS XML, checks titles against expected subber/episode/resolution patterns, downloads torrent files, and falls back from 1080p to lower resolutions.

### `mal_scraper.py`

Owns MyAnimeList scraping. It searches MAL by title, opens the first search result, and extracts the total episode count from the anime detail page.

### `app.py`

Coordinates unattended checking. It combines the episode JSON, MAL total episode counts, and Nyaa downloads into a repeated polling process.

### `paths.py`

Centralizes filesystem paths so data and download locations are not duplicated across modules.

## External Services

- Nyaa.si RSS feed: searched for torrent releases.
- Nyaa.si torrent links: downloaded after a matching RSS item is found.
- MyAnimeList: scraped by the polling loop to decide whether another episode should be downloaded.

## Main Data Flow

```text
User input or saved JSON
        |
        v
subber + anime title + episode + resolution
        |
        v
Nyaa RSS URL
        |
        v
RSS item title/link parsing
        |
        v
title match check
        |
        v
torrent download
        |
        v
save .torrent file and update JSON
```
