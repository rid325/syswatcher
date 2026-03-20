"""
Anomaly detection via baseline sampling.

On first run, SysWatcher collects N samples to establish a baseline mean
and standard deviation for CPU and RAM. After that, any reading that
deviates more than THRESHOLD standard deviations from the mean is flagged
as anomalous.
"""

import math

BASELINE_SAMPLES = 10   # number of readings to build the baseline
THRESHOLD_STDDEV = 2.0  # how many std deviations = anomaly


class AnomalyDetector:
    def __init__(self):
        self._samples: dict[str, list[float]] = {"cpu": [], "ram": []}
        self._baseline: dict[str, dict] = {}  # {"cpu": {"mean": x, "std": y}, ...}

    @property
    def is_ready(self) -> bool:
        """True once enough samples have been collected to form a baseline."""
        return len(self._samples["cpu"]) >= BASELINE_SAMPLES

    def add_sample(self, cpu_percent: float, ram_percent: float) -> None:
        """Feed a new reading into the detector."""
        if not self.is_ready:
            self._samples["cpu"].append(cpu_percent)
            self._samples["ram"].append(ram_percent)

            # compute baseline once we have enough samples
            if self.is_ready:
                for key in ("cpu", "ram"):
                    vals = self._samples[key]
                    mean = sum(vals) / len(vals)
                    std = math.sqrt(sum((v - mean) ** 2 for v in vals) / len(vals))
                    self._baseline[key] = {"mean": mean, "std": max(std, 2.0)}

    def check(self, cpu_percent: float, ram_percent: float) -> list[str]:
        """
        Returns a list of anomaly messages if any metric deviates
        beyond THRESHOLD_STDDEV from the baseline.
        """
        if not self.is_ready:
            remaining = BASELINE_SAMPLES - len(self._samples["cpu"])
            return [f"Baseline building... ({remaining} samples left)"]

        anomalies = []
        checks = {"cpu": cpu_percent, "ram": ram_percent}

        for key, value in checks.items():
            b = self._baseline[key]
            deviation = abs(value - b["mean"]) / b["std"]
            if deviation >= THRESHOLD_STDDEV:
                direction = "high" if value > b["mean"] else "low"
                anomalies.append(
                    f"ANOMALY: {key.upper()} is unusually {direction} "
                    f"({value:.1f}% vs baseline {b['mean']:.1f}% "
                    f"± {b['std']:.1f}%)"
                )

        return anomalies
