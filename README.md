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

*Created for the Chicago-based *Windy Civi* civic tech community 🏛️*

---

## 🛡 License

Distributed under the [MIT License](LICENSE).\
Free to use, modify, and build upon.\
Civic data belongs to the people.
