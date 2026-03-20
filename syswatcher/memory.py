import psutil


def get_memory_usage() -> dict:
    """
    Returns RAM and swap memory stats.
    - ram: total, used, available, percent
    - swap: total, used, free, percent
    """
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
        "ram": {
            "total": ram.total,
            "used": ram.used,
            "available": ram.available,
            "percent": ram.percent,
        },
        "swap": {
            "total": swap.total,
            "used": swap.used,
            "free": swap.free,
            "percent": swap.percent,
        },
    }


def _to_gb(bytes_val: int) -> str:
    """Converts bytes to a human-readable GB string."""
    return f"{bytes_val / (1024 ** 3):.2f} GB"


def display_memory(stats: dict) -> None:
    """Prints memory stats in a readable format."""
    ram = stats["ram"]
    swap = stats["swap"]

    print(f"RAM Usage   : {ram['percent']}%  "
          f"(used {_to_gb(ram['used'])} / total {_to_gb(ram['total'])})")
    print(f"  Available : {_to_gb(ram['available'])}")

    if swap["total"] > 0:
        print(f"Swap Usage  : {swap['percent']}%  "
              f"(used {_to_gb(swap['used'])} / total {_to_gb(swap['total'])})")
    else:
        print("Swap Usage  : not configured")
