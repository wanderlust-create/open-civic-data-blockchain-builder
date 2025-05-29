import json
from pathlib import Path
import shutil


def attach_events_to_bills(
    event_folder: Path, bill_folder: Path, error_folder: Path = None
):
    """
    Iterates through archived event JSON files and links them to referenced bills.

    For each event file:
    - Parses agenda[].related_entities[]
    - If an entity refers to a bill, copies the event log into that bill's /files/ directory
    - If successful and error_folder is provided, delete the event from missing_session folder

    Args:
        event_folder (Path): Path to archived raw event files.
        bill_folder (Path): Path to processed bill folders.
        error_folder (Path, optional): Path to error folder (used to remove from missing_session if linked).
    """
    if not event_folder.exists():
        print(f"⚠️ Event folder {event_folder} does not exist")
        return

    for event_file in event_folder.glob("event_*.json"):
        try:
            with open(event_file, "r", encoding="utf-8") as f:
                event_data = json.load(f)

            related_bills = []
            for agenda_item in event_data.get("agenda", []):
                for entity in agenda_item.get("related_entities", []):
                    if entity.get("entity_type") == "bill":
                        raw_ref = entity.get("bill_id") or entity.get("name")
                        if raw_ref:
                            clean_ref = (
                                raw_ref.replace(" ", "_")
                                .replace('"', "")
                                .strip("~{}()")
                            )
                            related_bills.append(clean_ref)

            if related_bills:
                for bill_id in related_bills:
                    target_folder = bill_folder / bill_id / "files"
                    target_folder.mkdir(parents=True, exist_ok=True)
                    dest_path = target_folder / f"linked_event__{event_file.name}"
                    shutil.copy(event_file, dest_path)
                    print(f"🔗 Linked {event_file.name} → {bill_id}/files/")

                # Optional: clean up from error folder if present
                if error_folder:
                    error_event_path = (
                        error_folder / "missing_session" / event_file.name
                    )
                    if error_event_path.exists():
                        error_event_path.unlink()
                        print(f"🔍 Removed from error folder: {error_event_path}")

        except Exception as e:
            print(f"❌ Failed to attach event {event_file.name}: {e}")
