import re


def normalize_address(address: str) -> str:
    cleaned = address.lower().strip()
    replacements = {
        " street": " st",
        " avenue": " ave",
        " road": " rd",
        " drive": " dr",
        " lane": " ln",
        " boulevard": " blvd",
    }
    for source, target in replacements.items():
        cleaned = cleaned.replace(source, target)
    cleaned = re.sub(r"[^a-z0-9\s]", "", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()
