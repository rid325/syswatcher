import psutil


def get_network_connections() -> list[dict]:
    """
    Returns active network connections with status and process info.
    Filters out connections without a remote address (idle/listening sockets).
    Returns empty list with a warning if permissions are insufficient (macOS).
    """
    try:
        raw = psutil.net_connections(kind="inet")
    except psutil.AccessDenied:
        return [{"_error": "Permission denied — run with sudo to see connections"}]

    connections = []
    for conn in raw:
        if not conn.raddr:
            continue

        try:
            process = psutil.Process(conn.pid).name() if conn.pid else "unknown"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            process = "unknown"

        connections.append({
            "pid": conn.pid,
            "process": process,
            "local": f"{conn.laddr.ip}:{conn.laddr.port}",
            "remote": f"{conn.raddr.ip}:{conn.raddr.port}",
            "status": conn.status,
            "type": "TCP" if conn.type.name == "SOCK_STREAM" else "UDP",
        })

    return connections


def get_network_io() -> dict:
    """Returns total bytes sent and received since boot."""
    io = psutil.net_io_counters()
    return {
        "bytes_sent": io.bytes_sent,
        "bytes_recv": io.bytes_recv,
    }


def _to_mb(bytes_val: int) -> str:
    return f"{bytes_val / (1024 ** 2):.2f} MB"


def display_network(connections: list[dict], io: dict) -> None:
    """Prints active network connections and I/O stats."""
    print(f"Network I/O : sent {_to_mb(io['bytes_sent'])}  /  "
          f"recv {_to_mb(io['bytes_recv'])}")

    # handle permission error
    if connections and "_error" in connections[0]:
        print(f"Connections : {connections[0]['_error']}")
        return

    print(f"Connections : {len(connections)} active")
    for c in connections[:10]:  # cap display at 10 to avoid flooding terminal
        print(f"  [{c['type']}] {c['process']} (pid {c['pid']})")
        print(f"    {c['local']}  ->  {c['remote']}  [{c['status']}]")

    if len(connections) > 10:
        print(f"  ... and {len(connections) - 10} more")
