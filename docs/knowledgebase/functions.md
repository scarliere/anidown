# Function Catalog

## `main.py`

### Module-level launcher

Intent: start the GUI from the repository root without requiring the package to be installed.

Behavior:

- Sets `sys.dont_write_bytecode = True`.
- Adds the local `src` directory to `sys.path`.
- Imports `run_gui()` from `anidown.gui`.
- Calls `run_gui()` when the file is executed directly.

## `src/anidown/app.py`

### `run(interval_seconds=60)`

Intent: continuously check saved anime and download the next available episode.

Behavior:

- Creates a `MALScraper`.
- Loads saved anime via `processor.loadlist()`.
- Iterates through each saved anime entry.
- Extracts anime name, subber, and current episode with `processor.animeinfo()`.
- Gets total episode count from MAL.
- Stops processing the current list item if the saved episode equals the MAL total.
- Attempts to download the next episode using `processor.processpage_with_resolution_fallback()`.
- Updates the saved episode number after a successful download.
- Saves the edited episode list and sleeps for `interval_seconds`.

Notes:

- This function runs forever.
- It assumes the saved JSON values use the list shape `[subber, latest_episode]`.
- It does not currently handle missing episode-list files.

## `src/anidown/gui.py`

### `load_episode_data()`

Intent: read saved anime data for the GUI.

Behavior:

- Returns `{}` when the episode-list file does not exist.
- Otherwise loads and returns JSON from `EPISODE_LIST_PATH`.

### `save_episode_data(epidump)`

Intent: persist GUI anime tracking data.

Behavior:

- Creates the parent data directory if needed.
- Writes the provided mapping as formatted JSON to `EPISODE_LIST_PATH`.

### `configure_styles(root)`

Intent: configure Tkinter/ttk visual styling for the app.

Behavior:

- Uses the `clam` ttk theme.
- Applies colors and font styles for frames, labels, entries, spinboxes, and buttons.
- Configures active, focus, and disabled button/field states.

### `make_surface(parent, row, title)`

Intent: create a reusable section container for the GUI.

Behavior:

- Creates a padded `ttk.Frame`.
- Places it in the parent grid at the requested row.
- Adds a section title label.
- Configures the middle column to expand.
- Returns the frame for further widget placement.

### `run_gui()`

Intent: launch the desktop GUI and handle one-shot anime torrent downloads.

Behavior:

- Loads saved anime data.
- Builds the main Tk window, scrollable page, input form, saved-anime list, and status label.
- Lets the user choose a download destination.
- Validates anime title, destination, and episode number.
- Disables form controls during a download.
- Runs the download in a daemon thread.
- Calls `processor.processpage_with_resolution_fallback()` with the selected subber, episode, anime name, and destination.
- On success, stores `[subber, next_episode]` for the anime and refreshes the visible list.
- On failure, shows a warning or error message and restores the form state.

Internal callbacks inside `run_gui()`:

- `sync_scroll_region()`: keeps the canvas scroll region aligned with page content.
- `sync_content_width(event)`: keeps the embedded content width aligned with the canvas width.
- `scroll_page(event)`: maps mouse-wheel movement to canvas scrolling.
- `choose_destination()`: opens a folder picker and updates the destination field.
- `refresh_list()`: repopulates the saved-anime listbox from `epidump`.
- `set_status(message, color_key="muted")`: updates status text and color.
- `set_form_state(state)`: enables or disables form widgets.
- `add_and_download()`: validates input and starts the worker thread.
- `worker()`: performs the torrent lookup/download and schedules GUI updates on the main thread.

## `src/anidown/processor.py`

### Constants

- `NYAA_BASE_URL`: base Nyaa URL used to build RSS feed URLs.
- `DEFAULT_RESOLUTIONS`: fallback order: `1080`, `720`, `480`.
- `REQUEST_HEADERS`: user-agent header for HTTP requests.

### `obtainjson(url)`

Intent: fetch a URL with basic retry behavior.

Behavior:

- Calls `requests.get()` with the shared request headers and a 30-second timeout.
- If any exception occurs, sleeps for 5 seconds and recursively retries.

Notes:

- Despite the name, this returns a `requests.Response`, not decoded JSON.
- The retry has no maximum attempt limit.

### `loadlist()`

Intent: load the saved episode list for non-GUI processing.

Behavior:

- Opens `EPISODE_LIST_PATH`.
- Parses and returns JSON.

### `savelist(edited)`

Intent: save the episode list for non-GUI processing.

Behavior:

- Creates the parent data directory if needed.
- Writes formatted JSON to `EPISODE_LIST_PATH`.

### `animeinfo(currentanime)`

Intent: unpack one saved anime entry into named values.

Behavior:

- Expects an item shaped like `(anime_name, [subber, latest_episode])`.
- Returns `(anime_name, subber, latest_episode)`.

### `build_rss_url(query, category="1_2", filter_value="0")`

Intent: construct a Nyaa RSS URL.

Behavior:

- Encodes query parameters with `urllib.parse.urlencode`.
- Defaults to category `1_2`, filter `0`, and `page=rss`.

### `normalize_episode(nextepi)`

Intent: format episode numbers to match common release title patterns.

Behavior:

- Returns zero-padded two-digit strings for episodes below 10.
- Returns the normal string form for episodes 10 and above.

### `safe_filename(name)`

Intent: make torrent titles safe to use as Windows filenames.

Behavior:

- Replaces invalid filename characters with `_`.
- Trims surrounding whitespace.

### `rss_items(rss_text)`

Intent: parse Nyaa RSS XML into title/link pairs.

Behavior:

- Parses XML using `xml.etree.ElementTree`.
- Iterates through `./channel/item`.
- Yields `(title, link)` for each RSS item.

### `title_matches(title, subber, episode, resolution)`

Intent: decide whether an RSS item is the desired release.

Behavior:

- Checks that the subber appears in the title, case-insensitively.
- Checks that the episode appears as a standalone number.
- Checks that the title contains the exact resolution marker, such as `(1080p)`.

### `download_torrent(title, link, destination_dir=None)`

Intent: download a torrent file from a matching RSS item.

Behavior:

- Returns `None` immediately when no link is provided.
- Downloads the link with redirects enabled.
- Raises for HTTP errors.
- Verifies the response looks like a torrent by checking the content type or bencoded payload prefix.
- Creates the destination directory.
- Saves the file as `<safe title>.torrent`.
- Prints the title, link, and saved path.
- Returns the saved `Path`.

### `processpage(url, i, subber, nextepi, resolution, animename, destination_dir=None)`

Intent: search Nyaa RSS for one anime episode at one resolution.

Behavior:

- Prints a processing message.
- Builds a query from subber, anime name, and resolution.
- Fetches the RSS feed with `obtainjson()`.
- Passes the RSS text to `getrows()`.
- Returns the downloaded torrent path or `None`.

Notes:

- The `url` and `i` parameters are currently unused.

### `getrows(rss_text, subber, nextepi, resolution, destination_dir=None)`

Intent: scan RSS items and download the first matching torrent.

Behavior:

- Normalizes the target episode number.
- Iterates through RSS title/link pairs.
- Uses `title_matches()` to find the first acceptable item.
- Calls `download_torrent()` for the match.
- Returns the saved path, or `None` if no match or download failure occurs.

### `processpage_with_resolution_fallback(subber, nextepi, animename, resolutions=DEFAULT_RESOLUTIONS, destination_dir=None)`

Intent: find and download an episode using preferred resolution fallback.

Behavior:

- Tries each resolution in order.
- Calls `processpage()` for each resolution.
- Returns `(resolution, download_path)` after the first successful download.
- Returns `(None, None)` if no resolution finds a match.

## `src/anidown/mal_scraper.py`

### `MALScraper`

Intent: provide MyAnimeList scraping helpers for total episode counts.

Attributes:

- `BASE_URL`: base MAL anime URL, currently not used by the scraper methods.
- `delay`: constructor argument stored on the instance, currently not used.
- `headers`: user-agent headers for MAL requests.

### `MALScraper.__init__(delay=2.0)`

Intent: initialize scraper settings.

Behavior:

- Stores the requested delay.
- Sets HTTP user-agent headers.

### `MALScraper.get_episode_count_by_url(url)`

Intent: fetch an MAL anime detail page and extract the total episode count.

Behavior:

- Requests the given URL.
- Raises when MAL returns a non-200 status.
- Parses HTML with BeautifulSoup.
- Finds the `Episodes:` label.
- Reads and parses the adjacent text as an integer.
- Returns `None` when the episode count is missing or non-numeric.

### `MALScraper.get_episode_count_by_search(title)`

Intent: search MAL by title and get the first result's episode count.

Behavior:

- Builds a MAL search URL with the quoted title.
- Requests the search page.
- Raises when MAL returns a non-200 status.
- Selects the first `a.hoverinfo_trigger` result.
- Raises if no result is found.
- Calls `get_episode_count_by_url()` for the first result URL.

## `src/anidown/paths.py`

### Constants

- `PACKAGE_DIR`: directory containing the `anidown` package.
- `PROJECT_ROOT`: repository root inferred from the package path.
- `DATA_DIR`: `PROJECT_ROOT / "data"`.
- `EPISODE_LIST_PATH`: `DATA_DIR / "latest_episodetest.json"`.
- `TORRENT_DIR`: `PROJECT_ROOT / "downloads" / "torrents"`.
