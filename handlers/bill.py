from pathlib import Path
import json
from utils.file_utils import format_timestamp, record_error_file


def handle_bill(content, session_folder, output_folder, error_folder, filename):
    """
    Handles bill JSON files. Saves the file using a timestamp derived from the bill's earliest action.
    Logs and skips if the bill is missing an identifier.

    Args:
        content (dict): The parsed JSON for the bill.
        session_folder (str): The mapped folder name for the session (e.g. '2023-2024').
        output_folder (Path): Path to the processed data root folder.
        error_folder (Path): Path to the not-processed data root folder.
        filename (str): The original filename for logging and recovery.
    """
    bill_identifier = content.get("identifier")
    if not bill_identifier:
        print("⚠️ Warning: Bill missing identifier")
        record_error_file(
            error_folder,
            "from_handle_bill_missing_identifier",
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
        bill_identifier,
    )
    (save_path / "logs").mkdir(parents=True, exist_ok=True)
    (save_path / "files").mkdir(parents=True, exist_ok=True)

    actions = content.get("actions", [])
    if actions:
        dates = [a.get("date") for a in actions if a.get("date")]
        timestamp = format_timestamp(sorted(dates)[0]) if dates else None
    else:
        timestamp = None

    if not timestamp:
        print(f"⚠️ Warning: Bill {bill_identifier} missing action dates")
        timestamp = "unknown"

    filename = f"{timestamp}_bill_created.json"
    output_file = save_path.joinpath("logs", filename)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)
    print(f"✅ Saved bill {bill_identifier}")
