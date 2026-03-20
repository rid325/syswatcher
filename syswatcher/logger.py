import logging
import os

LOG_FILE = "syswatcher.log"


def setup_logger() -> logging.Logger:
    """
    Sets up a logger that writes to both a file and stdout.
    - File: all messages (DEBUG and above)
    - Console: warnings and above only
    """
    logger = logging.getLogger("syswatcher")
    logger.setLevel(logging.DEBUG)

    # avoid adding duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # file handler — logs everything
    fh = logging.FileHandler(LOG_FILE)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # console handler — only warnings and above
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def log_alerts(logger: logging.Logger, alerts: list[str]) -> None:
    """Logs each alert message as a warning."""
    for alert in alerts:
        logger.warning(alert)


def log_snapshot(logger: logging.Logger, cpu: dict, memory: dict) -> None:
    """Logs a periodic system snapshot at DEBUG level."""
    logger.debug(
        f"CPU: {cpu['percent']}%  |  "
        f"RAM: {memory['ram']['percent']}%  |  "
        f"Swap: {memory['swap']['percent']}%"
    )
