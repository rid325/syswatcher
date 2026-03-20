import time
from syswatcher.cpu import get_cpu_usage, display_cpu
from syswatcher.memory import get_memory_usage, display_memory
from syswatcher.disk import get_disk_usage, display_disk
from syswatcher.network import get_network_connections, get_network_io, display_network
from syswatcher.alerts import check_alerts, display_alerts
from syswatcher.logger import setup_logger, log_alerts, log_snapshot

REFRESH_INTERVAL = 2  # seconds between each update


def run():
    logger = setup_logger()
    logger.info("SysWatcher started")
    print("=== SysWatcher ===\n")

    try:
        while True:
            print("-" * 40)
            cpu = get_cpu_usage(interval=1.0)
            memory = get_memory_usage()
            disk = get_disk_usage()

            display_cpu(cpu)
            print()
            display_memory(memory)
            print()
            display_disk(disk)
            print()
            display_network(get_network_connections(), get_network_io())
            print()

            alerts = check_alerts(cpu, memory, disk)
            display_alerts(alerts)
            log_alerts(logger, alerts)
            log_snapshot(logger, cpu, memory)

            time.sleep(REFRESH_INTERVAL)
    except KeyboardInterrupt:
        logger.info("SysWatcher stopped")
        print("\nSysWatcher stopped.")


if __name__ == "__main__":
    run()
