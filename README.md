# Hunger Bens Simulator

Enhanced simulation of whimsical arena events with tributes, morale, notoriety, alliances, and global events.

## Running (CLI)
Examples:

```
python main.py --seed 42 --max-days 15
python main.py --quiet --export-log run.json
python main.py --roster custom_roster.json --strict-shutdown 10
```

Interactive (legacy) mode:

```
python main.py --interactive
```

## Windows GUI
On Windows you can launch a Tkinter GUI:

```
python main.py --gui
```

GUI Features:
- Enter seed (optional) for reproducibility
- Set Max Days and optional Strict Shutdown day
- Toggle Verbose (controls console printing; GUI always captures log)
- Optional export JSON filename (Browse to pick path)
- Load a custom roster JSON (list or dict format; see below)
- Run Simulation: displays live log lines in scrollable window
- Clear Output / Quit buttons

Roster file format examples:

List form:
```json
[
	{"key": "c1", "name": "Alpha", "gender": "f", "age": 20, "district": 3},
	{"key": "c2", "name": "Beta", "gender": "m", "age": 19, "district": 7}
]
```

Dict form:
```json
{
	"c1": {"name": "Alpha", "gender": "f", "age": 20, "district": 3},
	"c2": {"name": "Beta", "gender": "m", "age": 19, "district": 7}
}
```

## Export Log
Use `--export-log myrun.json` or specify path in GUI to save full simulation details (tributes, death log, events, stats, alliances, seed).

## Reproducibility
Providing a `--seed` or GUI seed ensures identical event sequence across runs with same roster and parameters.

## License
Unspecified; add a license file if distributing.

## Web Version (GitHub Pages)
This repository includes a simplified browser version under `docs/` using Pyodide.

Deploy steps:
1. Commit and push the `docs/` folder (already added).
2. In GitHub repo settings enable Pages with Source = `main` branch `/docs` folder.
3. After build, visit the published URL (e.g. `https://<username>.github.io/hunger-bens/`).
4. Use the form to set seed, max days, strict shutdown, optional roster JSON, then Run.
5. Download JSON log via the button after completion.

Notes:
- Browser version is intentionally lighter (fewer events) for fast load; it does not mirror full desktop simulation.
- Roster JSON supports list or dict forms (same as CLI).
- All computation runs in-browser; no server required.

## Credit:

- [Sun Valley](https://github.com/rdbende/Sun-Valley-ttk-theme): Windows gui theme
- [Pyodide](https://pyodide.org/): Used for GitHub Pages functionality
