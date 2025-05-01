import os
import shutil
from pathlib import Path

def clear_output_folder(output_folder):
    """
    Interactively clears the given output folder after confirming with the user.
    Prevents accidental deletion by requiring 'yes' confirmation.
    """
    if os.path.exists(output_folder):
        confirm = (
            input(
                f"⚠️ This will delete everything in {output_folder}. Are you sure? (yes/no): "
            )
            .strip()
            .lower()
        )
        if confirm == "yes":
            shutil.rmtree(output_folder)
            print(f"🧹 Cleared existing output folder: {output_folder}")
        else:
            print("🛑 Aborted clearing output folder.")

def prompt_for_session_fix(filename, original_session_name, log_path=None):
    """
    Prompts the user to supply a corrected session name for a file with an unrecognized session.
    If the user provides one, it is returned and optionally logged to the session log file.

    Args:
        filename (str): The name of the file being processed.
        original_session_name (str): The session name that was not found in SESSION_MAPPING.
        log_path (Path or str, optional): If provided, the new mapping is appended to this file.
            This log helps project maintainers update SESSION_MAPPING manually later.

    Returns:
        str or None: The new session name, or None if the user skips.
    """
    print(f"⚠️ Unknown session for {filename}: '{original_session_name}'")
    new_session = input(
        f"📝 Enter correct session for {filename} (or press Enter to skip): "
    ).strip()

    if new_session and log_path:
        log_path = Path(log_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure folder exists
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"{original_session_name} => {new_session}\\n")

    return new_session or None
