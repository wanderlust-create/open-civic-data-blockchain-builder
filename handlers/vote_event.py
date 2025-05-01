from pathlib import Path
import json

from utils.file_utils import format_timestamp, record_error_file


def handle_vote_event(content, session_folder, output_folder, error_folder, filename):
    """
    Handles vote event files by routing them into the appropriate bill folder.
    If the referenced bill does not yet exist, a placeholder is created.
    Logs and skips files missing a bill_identifier.

    Args:
        content (dict): Parsed JSON vote event.
        session_folder (str): Session folder (e.g., "2023-2024").
        output_folder (Path): Path to processed data root.
        error_folder (Path): Path to not-processed data root.
        filename (str): Original filename (used in logs).
    """
    referenced_bill_id = content.get("bill_identifier")
    if not referenced_bill_id:
        print("⚠️ Warning: Vote missing bill_identifier")
        record_error_file(
            error_folder,
            "from_handle_vote_event_missing_bill_identifier",
            filename,
            content,
            original_filename=filename,
        )
        return

    save_path = Path(output_folder).joinpath(
        "country:us",
        "state:il",
        "sessions",
        "ocd-session",
        "country:us",
        "state:il",
        session_folder,
        "bills",
        referenced_bill_id,
    )
    (save_path / "logs").mkdir(parents=True, exist_ok=True)
    (save_path / "files").mkdir(parents=True, exist_ok=True)

    placeholder_file = save_path / "placeholder.json"
    if not placeholder_file.exists():
        placeholder_content = {"identifier": referenced_bill_id, "placeholder": True}
        with open(placeholder_file, "w", encoding="utf-8") as f:
            json.dump(placeholder_content, f, indent=2)
        print(f"📝 Created placeholder for missing bill {referenced_bill_id}")

    start_date = content.get("start_date")
    timestamp = format_timestamp(start_date) if start_date else None

    if not timestamp:
        print(f"⚠️ Warning: Vote event missing start_date")
        timestamp = "unknown"

    file_id = content.get("_id", "unknown_id")
    filename = f"{timestamp}_vote_event.json"
    output_file = save_path.joinpath("logs", filename)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)
    print(f"✅ Saved vote event {file_id} under bill {referenced_bill_id}")
