"""Conservative text omissions, not a guarantee of complete redaction."""
import re
from ipaddress import IPv6Address


def redact(text):
    # Validate colon-separated candidates as IPv6; clock times are not addresses.
    def omit_ipv6(match):
        try:
            IPv6Address(match.group())
        except ValueError:
            return match.group()
        return "[omitted]"

    text = re.sub(r"(?i)(?<![\w:])[0-9a-f:]*:[0-9a-f:]*:[0-9a-f:]*(?![\w:])", omit_ipv6, text)
    patterns = (
        r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b",
        r"(?i)\b(?:https?://|www\.)\S+",
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        r"(?i)\b(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}\b",
        r"(?i)(?:[a-z]:\\|\\\\|/Users/|/home/|/Volumes/)\S+",
        r"(?i)\b(?:password|token|api[_ -]?key|authentication code|username|hostname|ssid|server)\s*[:=]\s*\S+",
    )
    for pattern in patterns:
        text = re.sub(pattern, "[omitted]", text)
    return text
