from datetime import datetime
import json
from pathlib import Path


def format_timestamp(date_str):
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%Y%m%dT%H%M%SZ")
    except Exception:
        return None


def record_error_file(
    error_folder, category, filename, content, original_filename=None
):
    folder = Path(error_folder) / category
    folder.mkdir(parents=True, exist_ok=True)
    if original_filename:
        content["_original_filename"] = original_filename
    with open(folder / filename, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)
