from datetime import datetime
from pathlib import Path

from utils.io_utils import load_json_files
from utils.file_utils import ensure_session_mapping
from utils.interactive import clear_output_folder
from utils.process_utils import process_and_save
from postprocessors.event_linker import attach_events_to_bills

# Define state abbreviation and paths
STATE_ABBR = "usa"
BASE_FOLDER = Path(__file__).parent
INPUT_FOLDER = BASE_FOLDER / "scraped_state_data" / STATE_ABBR
DATA_OUTPUT = BASE_FOLDER / "data_output" / STATE_ABBR
ERROR_FOLDER = DATA_OUTPUT / "data_not_processed"
OUTPUT_FOLDER = DATA_OUTPUT / "data_processed"
EVENT_ARCHIVE_FOLDER = DATA_OUTPUT / "event_archive"
EVENT_ARCHIVE_FOLDER.mkdir(parents=True, exist_ok=True)
SESSION_LOG_PATH = DATA_OUTPUT / "new_sessions_added.txt"
SESSION_MAPPING = {}


def main():
    # 1. Clean previous outputs
    clear_output_folder(DATA_OUTPUT)

    # 2. Ensure session mapping is available
    SESSION_MAPPING.update(
        ensure_session_mapping(STATE_ABBR, BASE_FOLDER, INPUT_FOLDER)
    )

    # 3. Load and parse all input JSON files
    all_json_files = load_json_files(INPUT_FOLDER, EVENT_ARCHIVE_FOLDER, ERROR_FOLDER)

    # 4. Route and process by handler (defined elsewhere)
    process_and_save(
        STATE_ABBR, all_json_files, ERROR_FOLDER, SESSION_MAPPING, SESSION_LOG_PATH, OUTPUT_FOLDER
    )

    # 5. Link archived event logs to bill folders based on references
    print("\n🔗 Linking event references to related bills...")
    attach_events_to_bills(
        event_folder=EVENT_ARCHIVE_FOLDER,
        bill_folder=OUTPUT_FOLDER
        / f"country:us"
        / f"state:{STATE_ABBR}"
        / "sessions"
        / "ocd-session"
        / f"country:us"
        / f"state:{STATE_ABBR}"
        / "bills",
        missing_session_folder=ERROR_FOLDER / "missing_session",
    )


if __name__ == "__main__":
    main()
