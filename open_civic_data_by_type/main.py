import os
import json
from pathlib import Path
from datetime import datetime
from handlers import bills, vote_events, events, organizations
from utils.file_utils import record_error_file
from utils.interactive import prompt_for_session_fix, clear_output_folder


# -------------------------
# CONFIGURATION
# -------------------------
BASE_FOLDER = Path(__file__).parent
INPUT_FOLDER = BASE_FOLDER / "sample_scraped_data"
DATA_OUTPUT = BASE_FOLDER / "data_output"
ERROR_FOLDER = DATA_OUTPUT / "data_not_processed"
OUTPUT_FOLDER = DATA_OUTPUT / "data_processed"
SESSION_LOG_PATH = DATA_OUTPUT / "new_sessions_added.txt"

# ALLOW_SESSION_FIX = True
# SESSION_MAPPING = {}  # replace with logic if sessions are known ahead of time


# def load_json_files(input_folder):
#     all_data = []
#     for filename in os.listdir(input_folder):
#         if filename.endswith(".json"):
#             filepath = os.path.join(input_folder, filename)
#             try:
#                 with open(filepath, "r", encoding="utf-8") as f:
#                     data = json.load(f)
#                     all_data.append((filename, data))
#             except json.JSONDecodeError:
#                 print(f"❌ Skipping {filename}: could not parse JSON")
#                 with open(filepath, "r", encoding="utf-8") as f:
#                     raw_text = f.read()
#                 record_error_file(
#                     ERROR_FOLDER,
#                     "invalid_json",
#                     filename,
#                     {"error": "Could not parse JSON", "raw": raw_text},
#                     original_filename=filename,
#                 )
#     return all_data


# def route_handler(filename, content, session_folder):
#     if "bill_" in filename:
#         return bills.handle_bill(
#             content, session_folder, OUTPUT_FOLDER, ERROR_FOLDER, filename
#         )
#     elif "vote_event_" in filename:
#         return vote_events.handle_vote_event(
#             content, session_folder, OUTPUT_FOLDER, ERROR_FOLDER, filename
#         )
#     elif "event_" in filename:
#         return events.handle_event(
#             content, session_folder, OUTPUT_FOLDER, ERROR_FOLDER, filename
#         )
#     elif "organization_" in filename:
#         return organizations.handle_organization(
#             content, session_folder, OUTPUT_FOLDER, ERROR_FOLDER, filename
#         )
#     else:
#         print(f"❓ Unrecognized file type: {filename}")


# def process_and_save(data):
#     for filename, content in data:
#         session_name = content.get("legislative_session")
#         if not session_name:
#             print(f"⚠️ Skipping {filename}, missing legislative_session")
#             record_error_file(ERROR_FOLDER, "missing_session", filename, content)
#             continue

#         session_folder = SESSION_MAPPING.get(session_name)
#         if not session_folder and ALLOW_SESSION_FIX:
#             new_session = prompt_for_session_fix(
#                 filename, session_name, log_path=SESSION_LOG_PATH
#             )
#             if new_session:
#                 SESSION_MAPPING[session_name] = new_session
#                 session_folder = new_session
#         if not session_folder:
#             record_error_file(ERROR_FOLDER, "unknown_session", filename, content)
#             continue

#         route_handler(filename, content, session_folder)

#     print("\n✅ File processing complete.")


def main():
    print("Base folder:", BASE_FOLDER)
    print("Input folder:", INPUT_FOLDER)
    print("Output folder:", OUTPUT_FOLDER)
    print("Input exists:", INPUT_FOLDER.exists())
    # clear_output_folder(DATA_OUTPUT)
    # all_json_files = load_json_files(INPUT_FOLDER)
    # process_and_save(all_json_files)


if __name__ == "__main__":
    main()
