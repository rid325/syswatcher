import psutil


def get_disk_usage() -> list[dict]:
    """
    Returns usage stats for all mounted disk partitions.
    Skips pseudo/virtual filesystems (e.g. tmpfs, devfs).
    """
    partitions = []

    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            partitions.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
            })
        except PermissionError:
            # some mountpoints are not accessible
            continue

    return partitions


def _to_gb(bytes_val: int) -> str:
    return f"{bytes_val / (1024 ** 3):.2f} GB"


def display_disk(partitions: list[dict]) -> None:
    """Prints disk usage stats for each partition."""
    print(f"Disk Usage  : ({len(partitions)} partition(s))")
    for p in partitions:
        print(f"  {p['mountpoint']} ({p['fstype']})")
        print(f"    Used : {p['percent']}%  "
              f"{_to_gb(p['used'])} / {_to_gb(p['total'])}  "
              f"(free: {_to_gb(p['free'])})")
