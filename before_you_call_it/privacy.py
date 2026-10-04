"""Conservative text omissions, not a guarantee of complete redaction."""
import re


def redact(text):
    patterns = (
        r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b",
        r"(?i)\b(?:https?://|www\.)\S+",
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        r"(?i)\b(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}\b",
        r"(?i)\b[0-9a-f]{0,4}(?::[0-9a-f]{0,4}){2,7}\b",
        r"(?i)(?:[a-z]:\\|\\\\|/Users/|/home/|/Volumes/)\S+",
        r"(?i)\b(?:password|token|api[_ -]?key|authentication code|username|hostname|ssid|server)\s*[:=]\s*\S+",
    )
    for pattern in patterns:
        text = re.sub(pattern, "[omitted]", text)
    return text
