from pathlib import Path
import json
from utils.file_utils import record_error_file, format_timestamp


def handle_event(
    STATE_ABBR, content, session_folder, output_folder, error_folder, filename
):
    """
    Handles an event JSON file by saving:

    1. A full copy of the event in logs/ using the start_date
       Format: YYYYMMDD_event.json

    Skips and logs errors if required fields are missing.
    """
    event_id = content.get("_id") or filename.replace(".json", "")
    start_date = content.get("start_date")
    if not start_date:
        print(f"⚠️ Event {event_id} missing start_date")
        record_error_file(
            error_folder,
            "from_handle_event_missing_start_date",
            filename,
            content,
            original_filename=filename,
        )
        return

    timestamp = format_timestamp(start_date)
    save_path = Path(output_folder).joinpath(
        f"country:us",
        f"state:{STATE_ABBR}",
        "sessions",
        "ocd-session",
        f"country:us",
        f"state:{STATE_ABBR}",
        session_folder,
        "events",
        event_id,
    )
    (save_path / "logs").mkdir(parents=True, exist_ok=True)
    (save_path / "files").mkdir(parents=True, exist_ok=True)

    output_file = save_path / "logs" / f"{timestamp}_event.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)

    print(f"✅ Saved event: {event_id}")
