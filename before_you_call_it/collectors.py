"""Five API-based, read-only local observations. No connectivity request."""
import os
import platform
import time
from datetime import datetime, timezone
import psutil
from .model import Observation, State

KEYS = ("os", "ram", "disk", "uptime", "network")


def collect():
    stamp = datetime.now(timezone.utc).isoformat()

    def disk():
        # System volume only; the path is never included in the report.
        volume = os.path.abspath(os.sep)
        usage = psutil.disk_usage(volume)
        return f"{usage.free / 2**30:.2f} GiB free / {usage.total / 2**30:.2f} GiB total"

    checks = (
        ("os", lambda: platform.system() + " " + platform.release(), "", "platform.system/release"),
        ("ram", lambda: psutil.virtual_memory().total, "bytes", "psutil.virtual_memory.total"),
        ("disk", disk, "", "psutil.disk_usage, system volume"),
        ("uptime", lambda: max(0, time.time() - psutil.boot_time()), "seconds", "psutil.boot_time"),
        ("network", lambda: any(s.isup for s in psutil.net_if_stats().values()), "", "psutil.net_if_stats.isup only"),
    )
    result = []
    for key, read, unit, method in checks:
        try:
            value = read()
            result.append(Observation(key, value, unit, method, stamp, State.OBSERVED))
        except (OSError, RuntimeError, ValueError, psutil.Error):
            result.append(Observation(key, method=method, timestamp=stamp,
                                      state=State.UNAVAILABLE,
                                      reason="This check could not read the information. You can skip it or tell support what you see in normal system settings."))
    return result
