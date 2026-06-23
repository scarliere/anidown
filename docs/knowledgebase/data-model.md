# Data Model

## Active Episode List

Path:

```text
data/latest_episodetest.json
```

Current active shape:

```json
{
    "oshi no ko": [
        "[SubsPlease]",
        0
    ]
}
```

Meaning:

- Object key: anime title used for searches.
- Index `0`: release group/subber string expected in Nyaa titles.
- Index `1`: latest tracked episode number.

The GUI writes this shape when a download succeeds:

```json
{
    "Anime Title": [
        "[SubsPlease]",
        12
    ]
}
```

## Legacy or Alternate Episode List

Path:

```text
data/latest_episodes.json
```

Current shape:

```json
{
    "horimiya": 12,
    "shingeki no kyojin": 72,
    "Dr. Stone": 10,
    "jujutsu kaisen": 23
}
```

This file does not match the active code's expected `[subber, episode]` value shape. The current application path constants point to `latest_episodetest.json`, so this file appears to be legacy data or sample data.

## Download Output

Default path:

```text
downloads/torrents/
```

The GUI can override this per download with a user-selected destination.

Torrent filename format:

```text
<safe RSS title>.torrent
```

Invalid Windows filename characters are replaced with `_`.

## Episode Number Formatting

Episode matching normalizes target episodes as follows:

- `1` through `9` become `01` through `09`.
- `10` and above are used as plain strings.

The matcher then requires the episode number to appear as a standalone number in the RSS item title.
