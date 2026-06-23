# anidown

Simple agent to automatically download new episodes of anime from Nyaa.si.

The application reads `data/latest_episodetest.json`, checks each configured title, searches Nyaa's RSS feed, and downloads the first matching `.torrent` file. It tries `1080p` first, then falls back to lower resolutions.

See the [knowledgebase](knowledgebase/index.md) for app intent, architecture, data model, operations, and function-level documentation.

Run from the repository root:

```powershell
python main.py
```
