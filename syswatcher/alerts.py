from datetime import datetime

# Default thresholds (percentage)
DEFAULT_THRESHOLDS = {
    "cpu": 85.0,
    "memory": 80.0,
    "disk": 90.0,
}


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def check_alerts(cpu_stats: dict, memory_stats: dict, disk_partitions: list,
                 thresholds: dict = None) -> list[str]:
    """
    Checks CPU, memory, and disk stats against thresholds.
    Returns a list of alert messages for any breached threshold.
    """
    t = thresholds or DEFAULT_THRESHOLDS
    alerts = []

    # CPU alert
    if cpu_stats["percent"] >= t["cpu"]:
        alerts.append(
            f"[{_now()}] ALERT: CPU usage is {cpu_stats['percent']}% "
            f"(threshold: {t['cpu']}%)"
        )

    # Memory alert
    if memory_stats["ram"]["percent"] >= t["memory"]:
        alerts.append(
            f"[{_now()}] ALERT: RAM usage is {memory_stats['ram']['percent']}% "
            f"(threshold: {t['memory']}%)"
        )

    # Disk alert — check each partition
    for p in disk_partitions:
        if "_error" in p:
            continue
        if p["percent"] >= t["disk"]:
            alerts.append(
                f"[{_now()}] ALERT: Disk '{p['mountpoint']}' is {p['percent']}% full "
                f"(threshold: {t['disk']}%)"
            )

    return alerts


def display_alerts(alerts: list[str]) -> None:
    """Prints alerts if any exist."""
    if not alerts:
        return
    print("*** ALERTS ***")
    for alert in alerts:
        print(f"  {alert}")
