# SysWatcher

A lightweight, real-time system and network monitoring tool for Unix-based systems (Linux & macOS), built entirely in Python.

SysWatcher gives you a live terminal dashboard showing CPU, memory, disk, and network activity — with smart alerting, anomaly detection, and geo-location of active network connections. Designed to be simple to run, easy to read, and genuinely useful for understanding what your system is doing.

---

## Features

### System Monitoring
- **CPU** — overall usage percentage + per-core breakdown with color-coded progress bars
- **Memory** — RAM and swap usage in GB with visual indicators
- **Disk** — usage across all mounted partitions, skipping virtual/pseudo filesystems

### Network Monitoring
- **Active connections** — lists live TCP/UDP connections with process name and PID
- **Network I/O** — total bytes sent and received since boot
- **Geo-lookup** — resolves remote IPs to city and country in real time (no API key needed), with in-memory caching to avoid redundant lookups

### Alerting
- Threshold-based alerts for CPU (>85%), RAM (>80%), and disk (>90%)
- Alerts are shown on the dashboard and written to the log file
- Thresholds are configurable by passing a custom dict to `check_alerts()`

### Anomaly Detection
- Builds a statistical baseline of your system over the first 10 readings
- Flags CPU or RAM readings that deviate more than 2 standard deviations from the baseline
- Smarter than fixed thresholds — adapts to your system's normal behavior

### Terminal Dashboard
- Clean, refreshing UI built with `rich` — no scrolling output
- Color-coded panels: green = healthy, yellow = warning, red = critical
- Separate panels for CPU, Memory, Disk, Network, Alerts, and Anomaly Detection

### Logging
- All activity is logged to `syswatcher.log` in the project root
- Periodic snapshots logged at DEBUG level
- Alerts logged at WARNING level
- Log file persists across runs (append mode)

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.8+ | Core language |
| [psutil](https://github.com/giampaolo/psutil) | Cross-platform system metrics (CPU, memory, disk, network) |
| [rich](https://github.com/Textualize/rich) | Terminal dashboard UI with panels, tables, and color |
| [requests](https://docs.python-requests.org/) | HTTP calls to ip-api.com for geo-lookup |
| logging (stdlib) | File and console logging |

---

## Project Structure

```
syswatcher/
├── syswatcher/
│   ├── __init__.py
│   ├── cpu.py          # CPU usage stats
│   ├── memory.py       # RAM and swap stats
│   ├── disk.py         # Disk partition usage
│   ├── network.py      # Active connections and I/O
│   ├── alerts.py       # Threshold-based alerting
│   ├── anomaly.py      # Baseline anomaly detection
│   ├── dashboard.py    # Rich terminal UI
│   ├── geo.py          # IP geo-lookup with caching
│   └── logger.py       # File + console logging setup
├── main.py             # Entry point
├── requirements.txt
└── syswatcher.log      # Generated at runtime (gitignored)
```

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/rid325/syswatcher.git
cd syswatcher
```

**2. Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run**
```bash
python main.py
```

> On macOS, network connections require elevated permissions. Run with `sudo python main.py` to see live connections with geo-location data.

Press `Ctrl+C` to stop.

---

## Compatibility

| OS | Status |
|----|--------|
| macOS | Fully supported |
| Linux | Fully supported |
| Windows | Not supported (Unix-based tool) |

---

## Roadmap

- [ ] Config file support (custom thresholds via `config.yaml`)
- [ ] Process monitor (top N by CPU/memory, kill by PID)
- [ ] Historical trend sparklines in the dashboard
- [ ] Export snapshots to JSON/CSV
- [ ] System health score (single 0–100 composite metric)

---

## License

MIT
