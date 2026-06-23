# Operations

## Run the GUI

From the repository root:

```powershell
python main.py
```

The GUI is the default supported user workflow in the current launcher.

## Run the Polling Loop

The polling loop is available in code but is not wired to `main.py`.

Example:

```powershell
python -c "from anidown.app import run; run()"
```

When running this way from the repository root, the package must be importable. Either install the package, set `PYTHONPATH=src`, or run through a small launcher that adds `src` to `sys.path`.

## Dependencies

The code imports these third-party packages:

- `requests`
- `beautifulsoup4`

The GUI uses Python's standard `tkinter` package.

## External Network Requirements

Anidown needs access to:

- `https://nyaa.si/` for RSS search and torrent downloads.
- `https://myanimelist.net/` for total episode-count scraping in the polling loop.

## Important Caveats

- `processor.obtainjson()` retries forever on request exceptions.
- `processor.loadlist()` expects `data/latest_episodetest.json` to exist.
- `processor.processpage()` has unused `url` and `i` parameters.
- `MALScraper.delay` is stored but not used.
- MAL scraping depends on current MyAnimeList HTML structure.
- Nyaa matching requires title text to include the subber, standalone episode number, and a resolution marker like `(1080p)`.
- The active data file is `latest_episodetest.json`, while `latest_episodes.json` appears to use an older format.

## Typical GUI Workflow

1. Start the app with `python main.py`.
2. Enter an anime title.
3. Keep or change the subber value.
4. Enter the next episode to download.
5. Choose a download folder if the default is not desired.
6. Click **Add and Download**.
7. On success, the `.torrent` file is saved and `data/latest_episodetest.json` is updated.
