import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from handlers.bill import handle_bill
from handlers.vote_event import handle_vote_event
import handlers.other as handle_other
from utils.file_utils import record_error_file
from utils.interactive import prompt_for_session_fix
from utils.interactive import clear_output_folder

# -------------------------
# CONFIGURATION
# -------------------------
INPUT_FOLDER = "sample_input_files"
BASE_FOLDER = Path(__file__).resolve().parent
PROJECT_ROOT = Path(BASE_FOLDER) / "open_civic_data_blockchain"
ERROR_FOLDER = PROJECT_ROOT / "data_not_processed"
OUTPUT_FOLDER = PROJECT_ROOT / "data_processed"
SESSION_LOG_PATH = PROJECT_ROOT / "new_sessions_added.txt"

ALLOW_SESSION_FIX = True  # Set to False to disable interactive fixing


SESSION_MAPPING = {
    "104th": "2023-2024",
    "103rd": "2021-2022",
    # Add more mappings later
}


def load_json_files(input_folder):
    all_data = []
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(input_folder, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    all_data.append((filename, data))
            except json.JSONDecodeError:
                print(f"❌ Skipping {filename}: could not parse JSON")
                with open(filepath, "r", encoding="utf-8") as f:
                    raw_text = f.read()
                record_error_file(
                    ERROR_FOLDER,
                    "from_load_json_not_json",
                    filename,
                    {"error": "Could not parse JSON", "raw": raw_text},
                    original_filename=filename,
                )
    return all_data


def process_and_save(data, output_folder, error_folder):
    for filename, content in data:
        session_name = content.get("legislative_session")

        if not session_name:
            print(f"⚠️ Skipping {filename}, missing legislative_session")
            record_error_file(
                error_folder,
                "from_process_and_save_missing_legislative_session",
                filename,
                content,
                original_filename=filename,
            )
            continue

        session_folder = SESSION_MAPPING.get(session_name)
        if not session_folder:
            if ALLOW_SESSION_FIX:
                new_session = prompt_for_session_fix(
                    filename, session_name, log_path=SESSION_LOG_PATH
                )
                if new_session:
                    SESSION_MAPPING[session_name] = new_session
                    session_folder = new_session
                    print(f"✅ Mapped '{session_name}' to '{new_session}'")
                else:
                    record_error_file(
                        error_folder,
                        "from_process_and_save_unknown_session",
                        filename,
                        content,
                        original_filename=filename,
                    )
                    continue
            else:
                record_error_file(
                    error_folder,
                    "from_process_and_save_unknown_session",
                    filename,
                    content,
                    original_filename=filename,
                )
                continue

        if "bill_" in filename:
            handle_bill(content, session_folder, output_folder)
        elif "vote_event_" in filename:
            handle_vote_event(content, session_folder, output_folder)
        else:
            handle_other(content, session_folder, output_folder)

    print("\n✅ File processing complete.")


def main():
    clear_output_folder(OUTPUT_FOLDER)
    all_json_files = load_json_files(INPUT_FOLDER)
    process_and_save(all_json_files, OUTPUT_FOLDER, ERROR_FOLDER)


if __name__ == "__main__":
    main()
