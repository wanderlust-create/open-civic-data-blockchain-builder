import json
from pathlib import Path
import shutil


def attach_events_to_bills(
    event_folder: Path,
    bill_folder: Path,
    missing_session_folder: Path | None,
):
    """
    Iterates through archived event JSON files and links them to referenced bills.

    For each event file:
    - Parses agenda[].related_entities[]
    - If an entity refers to a bill, copies the event log into that bill's /files/ directory
    - If successfully linked, deletes the event file from both missing_session_folder and event_folder

    Args:
        event_folder (Path): Path to archived raw event files.
        bill_folder (Path): Path to processed bill folders.
        error_folder (Path): Path to log or store errors.
        missing_session_folder (Path, optional): Path to delete previously skipped event files.
    """
    if not event_folder.exists():
        print(f"\u26a0\ufe0f Event folder {event_folder} does not exist")
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

            if not related_bills:
                continue

            for bill_id in related_bills:
                target_folder = bill_folder / bill_id / "files"
                target_folder.mkdir(parents=True, exist_ok=True)
                dest_path = target_folder / f"linked_event__{event_file.name}"
                shutil.copy(event_file, dest_path)
                print(f"\U0001f517 Linked {event_file.name} → {bill_id}/files/")

            # Delete from missing_session_folder if applicable
            if missing_session_folder:
                missing_file = missing_session_folder / event_file.name
                if missing_file.exists():
                    missing_file.unlink()

            # Delete from event_folder after successful linking
            event_file.unlink()

        except Exception as e:
            print(f"\u274c Failed to attach event {event_file.name}: {e}")
