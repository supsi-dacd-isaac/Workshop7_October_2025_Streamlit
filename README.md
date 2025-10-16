# Workshop7_October_2025_Streamlit (uv-enabled)

This repository is a Streamlit app showcasing System Dynamics insights for the Canton Ticino energy transition.

This setup uses uv for fast, reproducible Python environments and dependency management via `pyproject.toml`.

## Requirements
- Python 3.10+
- Linux/macOS/Windows
- uv installed (see below)

## Install uv

Linux/macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Then ensure ~/.local/bin is on your PATH or follow the printed instructions
uv --version
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv --version
```

## Setup the environment

From the project root:

```bash
# Create/refresh the local environment from pyproject.toml (installs deps + dev tools)
uv sync --dev

# Optionally, print the resolved environment info
uv tree
```

Notes:
- This repo is an application, not an installable package (see `[tool.uv].package = false`).
- uv creates a `.venv/` by default; you can activate it if you prefer, but `uv run` works without activation.

## Run the app

```bash
# Run Streamlit directly with uv
uv run streamlit run Home.py
```

Streamlit will print a local URL (default http://localhost:8501).

## Lint and format (optional)

```bash
uv run ruff check .
uv run black .
```

## Data and geospatial dependencies
- The app reads CSV files in `plots_data/`, a GeoPackage `ch.bfe.elektrizitaetsproduktionsanlagen.gpkg`, and a Shapefile in `Limits/`.
- Geospatial stack is provided by `geopandas` and `pyogrio` (fast vector IO). Prebuilt wheels avoid manual GDAL/Fiona builds on most platforms.
- If you hit issues reading files:
  - Ensure file paths exist as in the repo layout and you run from the project root.
  - Confirm your Python matches the `requires-python` in `pyproject.toml`.

## Troubleshooting
- If `streamlit_folium` is missing, ensure `uv sync --dev` ran successfully. It’s specified as a dependency.
- On first run, Streamlit may ask to create a config directory. Accept defaults or run with `--server.port 8501` to change port.
- If you need to clear Streamlit cache: remove `~/.streamlit/cache` or use the menu in the app.

## Project metadata
- Dependencies are declared in `pyproject.toml` under `[project].dependencies`.
- Build backend is `hatchling`; not required for running the app, only if you choose to build a wheel (not needed here).
