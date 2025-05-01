# Open Civic Data Blockchain Builder

This project parses civic legislative JSON files and saves them into a blockchain-style folder structure for versioned, transparent archival.

🛠️ Built with modular Python, real-time error tracking, and interactive recovery prompts

---

## Features

- 📂 Saves each bill and vote event into timestamped `.json` files
- 🧱 Organizes output by session, chamber, and bill identifier
- 🗃️ Logs every processing step to `data_processed/` and error cases to `data_not_processed/`
- 🧾 Auto-creates placeholder files when votes reference missing bills
- 🧠 Prompts user for missing legislative_session (optional toggle), enabling real-time error correction without restarting the script
- 📝 Tracks new sessions entered via prompt in `new_sessions_added.txt`
- 🔧 Modular file structure using `handlers/`, `utils/`, and `main.py`

---

## Project Structure

```plaintext
open_civic_data_blockchain/
├── data_processed/           # Successfully parsed, structured output
├── data_not_processed/       # Skipped/error files categorized by reason
├── main.py                   # Entry point script
├── handlers/                 # Handlers for each data type
├── utils/                    # Helper functions, prompts, config
```

---

# Sample Input Files

This folder contains a curated set of real legislative JSON files sourced from public government data.

These files are used to:
- ✅ Demonstrate successful processing (e.g. valid bills and vote events)
- ⚠️ Trigger and test error handling pathways (e.g. missing fields, unknown sessions, malformed JSON)

---

## File Categories

- `bill_*.json` and `vote_event_*.json` — Real-world examples of structured legislative data
- Files missing keys like `identifier`, `bill_identifier`, or `legislative_session` — included intentionally to test how the system routes malformed files to `data_not_processed/`
- One intentionally malformed JSON file (`bad_json.json`) is included to verify `JSONDecodeError` handling

---

## Notes

- All data comes from public sources and contains no private or sensitive information.
- You can run the pipeline with this folder to see both success and failure paths in action.

---

## Getting Started

Make sure you have **Python 3.9+** installed.

Clone the repo and run:

```bash
python main.py
```

You’ll be prompted before clearing any output folders.

If a file is missing a `legislative_session`, you can optionally enter a valid session name interactively (e.g., `"104th"`), and the script will continue processing.

---

## Example Use Cases

This tool is ideal for projects that aim to:

- Archive legislative activity in a structured, tamper-evident way
- Monitor new actions on bills in real time
- Provide visibility into vote events tied to specific legislation
- Support civic engagement and open government initiatives

---

## Coming Soon

- [ ] One file per action for each bill (for real-time bill tracking)
- [ ] Optional archiving of placeholder files once resolved
- [ ] CLI flags for batch vs interactive modes

---

## 👩🏽‍💻 Contributors

- **Tamara Dowis**
  [GitHub](https://github.com/wanderlust-create) | [LinkedIn](https://www.linkedin.com/in/tamara-dowis/)
- 🤖 With pair programming support from her AI assistant “Hypatia” (powered by ChatGPT)

*Created for the Chicago-based *Windy Civi* civic tech community* 🏛️

---

## 🛡 License

Distributed under the [MIT License](LICENSE).\
Free to use, modify, and build upon.\
Civic data belongs to the people.
