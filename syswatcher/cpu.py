import psutil


def get_cpu_usage(interval: float = 1.0) -> dict:
    """
    Returns CPU usage stats.
    - percent: overall CPU usage %
    - per_core: usage % per logical core
    - core_count: number of logical cores
    """
    return {
        "percent": psutil.cpu_percent(interval=interval),
        "per_core": psutil.cpu_percent(interval=interval, percpu=True),
        "core_count": psutil.cpu_count(logical=True),
    }


def display_cpu(stats: dict) -> None:
    """Prints CPU stats in a readable format."""
    print(f"CPU Usage   : {stats['percent']}%  ({stats['core_count']} logical cores)")
    for i, usage in enumerate(stats["per_core"]):
        print(f"  Core {i:<3}  : {usage}%")
