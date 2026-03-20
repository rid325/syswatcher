# SysWatcher

A lightweight Unix-based system and network monitoring tool built in Python.

## Features (in progress)
- [x] CPU monitoring
- [x] Memory monitoring
- [x] Disk monitoring
- [x] Network connections monitoring
- [x] Alerting system
- [x] Logging

## Requirements
- Python 3.8+
- psutil

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## Usage

Run `main.py` and SysWatcher will continuously display system stats. Press `Ctrl+C` to stop.

Logs are written to `syswatcher.log` in the project root. Each run appends to the file — snapshots at DEBUG level, alerts at WARNING level.
