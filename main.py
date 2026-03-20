import time
from syswatcher.cpu import get_cpu_usage
from syswatcher.memory import get_memory_usage
from syswatcher.disk import get_disk_usage
from syswatcher.network import get_network_connections, get_network_io
from syswatcher.alerts import check_alerts
from syswatcher.logger import setup_logger, log_alerts, log_snapshot
from syswatcher.dashboard import render_dashboard

REFRESH_INTERVAL = 2  # seconds between each update


def run():
    logger = setup_logger()
    logger.info("SysWatcher started")

    try:
        while True:
            cpu = get_cpu_usage(interval=1.0)
            memory = get_memory_usage()
            disk = get_disk_usage()
            connections = get_network_connections()
            io = get_network_io()
            alerts = check_alerts(cpu, memory, disk)

            render_dashboard(cpu, memory, disk, connections, io, alerts)
            log_alerts(logger, alerts)
            log_snapshot(logger, cpu, memory)

            time.sleep(REFRESH_INTERVAL)
    except KeyboardInterrupt:
        logger.info("SysWatcher stopped")
        print("\nSysWatcher stopped.")


if __name__ == "__main__":
    run()
