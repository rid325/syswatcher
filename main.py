import time
from syswatcher.cpu import get_cpu_usage, display_cpu
from syswatcher.memory import get_memory_usage, display_memory

REFRESH_INTERVAL = 2  # seconds between each update


def run():
    print("=== SysWatcher ===\n")
    try:
        while True:
            print("-" * 40)
            display_cpu(get_cpu_usage(interval=1.0))
            print()
            display_memory(get_memory_usage())
            time.sleep(REFRESH_INTERVAL)
    except KeyboardInterrupt:
        print("\nSysWatcher stopped.")


if __name__ == "__main__":
    run()
