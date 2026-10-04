"""Four API-based, read-only local observations and an intentional network omission. No connectivity request."""
import os
import platform
import time
from datetime import datetime, timezone
import psutil
from .model import Observation, State

NETWORK_REASON = "This prototype does not perform connectivity probes or inspect network identifiers."

KEYS = ("os", "ram", "disk", "uptime", "network")


def collect():
    stamp = datetime.now(timezone.utc).isoformat()

    def disk():
        # Current drive root only; the path is never included in the report.
        volume = os.path.abspath(os.sep)
        usage = psutil.disk_usage(volume)
        return f"{usage.free / 2**30:.2f} GiB free / {usage.total / 2**30:.2f} GiB total"

    checks = (
        ("os", lambda: platform.system() + " " + platform.release(), "", "platform.system/release"),
        ("ram", lambda: psutil.virtual_memory().total, "bytes", "psutil.virtual_memory.total"),
        ("disk", disk, "", "psutil.disk_usage, os.path.abspath(os.sep): current drive root"),
        ("uptime", lambda: max(0, time.time() - psutil.boot_time()), "seconds", "psutil.boot_time"),
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
    result.append(Observation("network", state=State.NOT_CHECKED,
                              reason=NETWORK_REASON))
    return result
