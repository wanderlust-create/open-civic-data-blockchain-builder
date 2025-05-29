from pathlib import Path
from datetime import datetime
from handlers import bill, vote_event, event, organization
from utils.file_utils import record_error_file, ensure_session_mapping
from utils.interactive import prompt_for_session_fix

ALLOW_SESSION_FIX = True


def route_handler(
    STATE_ABBR, filename, content, session_folder, ERROR_FOLDER, OUTPUT_FOLDER
):
    if "bill_" in filename:
        return bill.handle_bill(
            STATE_ABBR, content, session_folder, OUTPUT_FOLDER, ERROR_FOLDER, filename
        )
    elif "vote_event_" in filename:
        return vote_event.handle_vote_event(
            STATE_ABBR, content, session_folder, OUTPUT_FOLDER, ERROR_FOLDER, filename
        )
    elif "event_" in filename:
        return event.handle_event(
            STATE_ABBR, content, session_folder, OUTPUT_FOLDER, ERROR_FOLDER, filename
        )
    elif "organization_" in filename:
        return organization.handle_organization(
            STATE_ABBR, content, session_folder, OUTPUT_FOLDER, ERROR_FOLDER, filename
        )
    else:
        print(f"❓ Unrecognized file type: {filename}")


def process_and_save(
    STATE_ABBR, data, ERROR_FOLDER, SESSION_MAPPING, SESSION_LOG_PATH, OUTPUT_FOLDER
):
    for filename, content in data:
        session_name = content.get("legislative_session")
        if not session_name:
            print(f"⚠️ Skipping {filename}, missing legislative_session")
            record_error_file(ERROR_FOLDER, "missing_session", filename, content)
            continue

        session_folder = SESSION_MAPPING.get(session_name)
        if not session_folder and ALLOW_SESSION_FIX:
            new_session = prompt_for_session_fix(
                filename, session_name, log_path=SESSION_LOG_PATH
            )
            if new_session:
                SESSION_MAPPING[session_name] = new_session
                session_folder = new_session
        if not session_folder:
            record_error_file(ERROR_FOLDER, "unknown_session", filename, content)
            continue

        route_handler(
            STATE_ABBR, filename, content, session_folder, ERROR_FOLDER, OUTPUT_FOLDER
        )

    print("\n✅ File processing complete.")
