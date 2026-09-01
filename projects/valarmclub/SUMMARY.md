# ValarmClub Repo Summary

> Generated 2026-08-31 from `/Users/admin/github_code/ValarmClub` (remote: `https://github.com/zzz562/ValarmClub.git`)

## 1. What it is

**A PyQt5 desktop stock-selection tool for the A-share (Chinese) market** — "ValarmClub - 股票选股系统". The README self-describes it as *"A Lab of Stock Selection UI coded with PyQt"*.

- **Data source**: Tushare Pro API (daily K-lines + stock basic info), stored locally in **SQLite** (`data/market_data.db`).
- **UI**: Left panel = stock info header + interactive K-line chart (Plotly candlestick rendered inside `QWebEngineView`) + operation log terminal. Right panel = data-update controls + stock-list tabs (`自定义` / custom, `特征选` / feature-selected) + feature-selector form + filter input.
- **Status**: early-stage lab project. Only 4 git commits (Nov 2024 → Mar 2025); much of the code is scaffold/stub; the interesting selection logic is partially proven in Jupyter notebooks and partially wired into the app.

Repo layout (top level, git-tracked):

| Path | Role |
|------|------|
| `main_app.py` | Entry point: QApplication, splash, QSS theme, fonts, window placement, tray |
| `ui/` | PyQt5 views: `main_window.py` + `components/` (stock_list, feature_selector, kline_view, stock_details, stock_filter_input, data_update_controls, system_tray) + `dialogs/` |
| `viewmodels/` | `main_viewmodel.py` (signal bridge between UI and models), `feature_processor.py` |
| `models/` | `data_storage.py` (SQLite schema + CRUD), `data_updater.py` (Tushare fetch, rate-limit, incremental sync, DTW similarity), `stock_data.py`, `feature_extraction.py`, `clustering.py` (**empty**) |
| `stockselection/` | Experiment notebook (`workshop_00.ipynb`) + generated outputs (similar-stock lists, demo K-line CSVs) |
| `data/` | SQLite DB + `storage/` (JSON/SQLite storage abstraction — mostly stubs) |
| `tests/` | Smoke-test scripts, not a real test suite (`test_ui.py` empty, `test_viewmodels.py` 1 line) |
| `setup.py` | py2app packaging for macOS |

Not tracked by git (scratch/experiments): `_StockSelection/` — the **earlier CSV-based prototype**: `src/tushare_daq.py` (fetch all stocks' daily K-lines to per-stock CSVs with a progress file + 1.2 s sleep rate limit), `src/feature_mining.py` (mass feature extraction), per-stock `chart/*_kline_chart.html`, plus two GUI experiments (`GUI_PyQt/`, `GUI_Tkinter/` — the Tkinter one is a hello-world placeholder).

## 2. Business logic (选股业务逻辑)

### Data pipeline
1. **Fetch**: `DataUpdater` pulls `stock_basic` (17 fields incl. name, industry, area, actual controller, enterprise type) and daily K-lines from Tushare Pro. Rate-limited to 200 requests/min; a progress log callback streams to the UI terminal.
2. **Storage**: SQLite with 4 tables — `daily_kline` (PK `ts_code+trade_date`), `stock_info`, `sync_log` (per-stock last sync date), `stock_selection_cache` (per-tab saved stock lists).
3. **Incremental sync**: `update_all_data()` / `sync_all_data()` only fetch from `last_sync_date + 1` to today (default history start `20150101`), resumable across runs.

### Stock-selection strategies
Two modes coexist in `MainViewModel.apply_features()`:

1. **Waveform pattern matching (the core idea — "找相似走势")**
   - User enters a **target stock code + date window** (default last 90 days).
   - The app extracts the target's close-price series, normalizes it (min-max), and compares it against every candidate stock over the **same date window** using **DTW (Dynamic Time Warping)** distance (`dtaidistance`).
   - Stocks below a user-set similarity threshold are returned, capped at `max_matches` (default 20), and shown in the 特征选 tab.
   - Same algorithm appears standalone in the notebook (`workshop_00.ipynb` cell 7), which scans the whole DB and exports a formatted `('自定义', 'ts_code')` list to `output/similar_stock_list.txt` — i.e. the app was born from this experiment.

2. **Classic filters (stub/simple)**: industry dropdown (金融/科技/制造/医药/消费/能源/其他), minimum market cap, and a placeholder "apply features" path (`FeatureExtractor` only computes MA5/MA20 cross + volatility).

### Feature mining (old CSV pipeline, `_StockSelection/src/feature_mining.py`)
The experiment phase extracted a wide feature matrix per stock per window:
- **Statistical**: mean/std/max/min/skew/kurtosis of close
- **Time-series**: SMA-10, EMA-10, momentum of relative change
- **Pattern**: peak/valley counts via `scipy.signal.find_peaks`
- **Volatility**: ATR(14)
- **Signal**: FFT dominant frequency/amplitude + top-5 components
- **Custom (2024-specific)**: Feb low, overall low, relative min, max increase, limit-up (涨停) detection with avg 7-day retracement after limit-up, box-platform (箱体) detection over full and trailing-90-day windows

This suggests the intended workflow: **mine features → cluster/rank stocks → let the user pick chart-similar candidates** — but clustering.py is empty, so clustering was never implemented in the app.

### User workflow in the app
Pick a stock (click row / type code) → K-line chart + info header update → optionally adjust the date window → run feature selection (waveform match or filters) → results populate 特征选 tab → promote interesting picks to 自定义 tab (persisted in `stock_selection_cache`) → click any row to inspect its chart. Closing the window hides to the system tray.

## 3. Code development logic (代码开发逻辑)

### Architecture: MVVM-lite with Qt signals
```
main_app.py → MainWindow (ui/) ──PyQt signals──▶ MainViewModel (viewmodels/) ──▶ models/ (DataUpdater/DataStorage)
```
- **UI (views)** emit signals / call ViewModel methods; they never touch SQL or Tushare directly.
- **ViewModel** owns `DataUpdater`, exposes `set_selected_stock`, `apply_features`, `update_all_data`, `sync_data`, and re-emits model data through typed signals (`stock_info_updated`, `kline_updated`, `basic_info_updated`, `log_message`).
- **Models** are plain Python (sqlite3 + pandas), agnostic of Qt.
- UI components subscribe to ViewModel signals (`viewmodel.kline_updated.connect(...)`) and feed the shared log terminal via a `log_message` signal — a simple observer pattern.

### Development style: notebook-first, then productize
- The selection logic was **prototyped in Jupyter** (`workshop_00.ipynb`, `_StockSelection/src/*.ipynb`) against the real SQLite DB — price-range queries, DTW scan, export lists.
- Proven pieces were then **re-implemented inside the PyQt app** (`DataUpdater.calculate_similarity` mirrors the notebook's DTW code, including the same min-max normalization and truncation-to-shorter-series handling).
- The `_StockSelection/` CSV prototype was **left in place, untracked** — the repo keeps both the old batch prototype and the new DB-backed app side by side.

### Pragmatic lab choices (with rough edges)
- **Rate limiting via wall-clock counting** (200 requests then sleep), not a token-bucket; progress persisted in `progress.csv` for resumability.
- **Test files are smoke scripts** that make live Tushare calls (`test_models.py`), not assertions — the "tests" double as runnable examples.
- Hardcoded dev-machine specifics: Tushare **API token committed in `data_updater.py`** (also `.env` staged), macOS-specific `QTWEBENGINEPROCESS_PATH` in `main_app.py`, hardcoded seed stock list in `stock_selection_cache`.
- Multiple unfinished seams: `clustering.py` empty, `FeatureProcessor`/`FeatureExtractor` near-stubs, `filter_stock()` is a TODO, delete-from-list doesn't delete from DB, storage abstraction (`StorageManager`) unused, py2app + PyInstaller both present.

### Packaging
- `setup.py` (py2app) for a macOS `.app`; PyInstaller specs inside `_StockSelection/GUI_PyQt/` and `GUI_Tkinter/`.

## 4. Quick takeaways

- **Core asset**: the DTW-based "find stocks whose recent chart resembles a target" workflow + the SQLite/Tushare incremental data layer.
- **Biggest gaps if continuing**: real feature/clustering engine (both stubbed), replacing committed secrets with env config, and turning smoke scripts into an actual test suite.
