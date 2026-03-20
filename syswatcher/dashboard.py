from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()


def _bar(percent: float, width: int = 20) -> Text:
    """Renders a colored ASCII progress bar."""
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    color = "green" if percent < 60 else "yellow" if percent < 85 else "red"
    return Text(f"[{bar}] {percent:.1f}%", style=color)


def build_cpu_panel(cpu: dict) -> Panel:
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    table.add_column("label", style="bold cyan", width=12)
    table.add_column("bar")

    table.add_row("Overall", _bar(cpu["percent"]))
    for i, usage in enumerate(cpu["per_core"]):
        table.add_row(f"Core {i}", _bar(usage))

    return Panel(table, title="[bold]CPU[/bold]", border_style="cyan")


def build_memory_panel(memory: dict) -> Panel:
    ram = memory["ram"]
    swap = memory["swap"]

    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    table.add_column("label", style="bold magenta", width=12)
    table.add_column("bar")

    table.add_row("RAM", _bar(ram["percent"]))
    used_gb = ram["used"] / 1024 ** 3
    total_gb = ram["total"] / 1024 ** 3
    table.add_row("", Text(f"{used_gb:.2f} GB / {total_gb:.2f} GB", style="dim"))

    if swap["total"] > 0:
        table.add_row("Swap", _bar(swap["percent"]))
    else:
        table.add_row("Swap", Text("not configured", style="dim"))

    return Panel(table, title="[bold]Memory[/bold]", border_style="magenta")


def build_disk_panel(partitions: list) -> Panel:
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    table.add_column("mount", style="bold yellow", width=28)
    table.add_column("bar")

    for p in partitions:
        if "_error" in p:
            continue
        table.add_row(p["mountpoint"], _bar(p["percent"]))

    return Panel(table, title="[bold]Disk[/bold]", border_style="yellow")


def build_network_panel(connections: list, io: dict) -> Panel:
    sent_mb = io["bytes_sent"] / 1024 ** 2
    recv_mb = io["bytes_recv"] / 1024 ** 2

    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    table.add_column("label", style="bold blue", width=12)
    table.add_column("value")

    table.add_row("Sent", Text(f"{sent_mb:.2f} MB", style="blue"))
    table.add_row("Received", Text(f"{recv_mb:.2f} MB", style="blue"))

    if connections and "_error" in connections[0]:
        table.add_row("Connections", Text(connections[0]["_error"], style="dim"))
    else:
        table.add_row("Active", Text(str(len(connections)), style="bold"))
        for c in connections[:5]:
            table.add_row(
                f"  {c['process'][:10]}",
                Text(f"{c['remote']}  [{c['status']}]", style="dim")
            )

    return Panel(table, title="[bold]Network[/bold]", border_style="blue")


def build_alerts_panel(alerts: list) -> Panel:
    if not alerts:
        content = Text("All systems normal", style="green")
    else:
        content = Text("\n".join(alerts), style="bold red")
    return Panel(content, title="[bold]Alerts[/bold]", border_style="red" if alerts else "green")


def render_dashboard(cpu: dict, memory: dict, disk: list,
                     connections: list, io: dict, alerts: list) -> None:
    """Clears the terminal and renders the full dashboard."""
    console.clear()
    console.print(Panel("[bold white]SysWatcher[/bold white]",
                        subtitle="Press Ctrl+C to stop", border_style="white"))
    console.print(build_cpu_panel(cpu))
    console.print(build_memory_panel(memory))
    console.print(build_disk_panel(disk))
    console.print(build_network_panel(connections, io))
    console.print(build_alerts_panel(alerts))
