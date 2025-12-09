# 🤖 LLM Automation Agent

**A smart, agentic API that translates natural language into secure file operations and data processing tasks.**

---

## 🚀 Motivation & Goal

### The Problem
Developers and data analysts often spend countless hours on repetitive tasks: formatting files, extracting specific data points, querying databases, or organizing logs. While scripts can do this, writing a new script for every variation is inefficient and time-consuming.

### The Goal
To build a **Universal Automation Interface** where a user can simply *describe* a task in plain English (e.g., *"Find the most similar comments in this file"*), and the system intelligently:
1.  **Understands** the intent using a Large Language Model (LLM).
2.  **Selects** the correct tool for the job.
3.  **Executes** the code securely within a sandboxed environment.

### The Solution
This project implements a **FastAPI-based Agent** powered by **Google Gemini**. It features a modular "Tool Dispatcher" system that maps natural language intents to specific Python functions, ensuring deterministic and safe execution of arbitrary tasks.

---

## ✨ Key Features

This agent is equipped with a suite of specialized tools:

*   **🛠️ System Automation**: Installs dependencies (like `uv`) and runs dynamic data generation scripts.
*   **📄 Markdown Management**: Formats markdown files (Prettier-style) and indexes H1 headers.
*   **📊 Data Processing**: Sorts complex JSON arrays and counts occurrences in text files (e.g., specific weekdays).
*   **🔍 Log Analysis**: Extracts recent entries from log directories.
*   **🧠 Intelligent Extraction (LLM)**: Extracts specific entities (like email senders) from unstructured text.
*   **👁️ Computer Vision**: Reads and extracts data (like credit card numbers) from images.
*   **📐 Vector Similarity**: Finds similar text pairs using Embeddings.
*   **🗄️ Database Querying**: Executes SQL queries on SQLite databases and saves results safely.

---

## 🏗️ Architecture

The system follows a strict **Client-Server-Agent** flow:

1.  **Input**: User sends a POST request with a natural language task.
    *   *Example:* `"Sort contacts.json by last name."`
2.  **LLM Layer (Brain)**: `app/services/llm_service.py` sends the prompt to **Google Gemini**. The model analyzes the request and returns a structured JSON object identifying the **Tool** and **Arguments**.
3.  **Dispatcher Layer**: `app/dispatcher.py` validates the tool name and routes the arguments to the correct function in `app/tasks.py`.
4.  **Execution Layer**: The specific Python function executes the task.
5.  **Security Layer**: `app/utils.py` enforces a **Security Sandbox**, ensuring the agent can *only* read/write files inside the `/data/` directory, preventing system-wide access.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/LLM-Automation_agent.git
cd LLM-Automation_agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file in the root directory:

```ini
GEMINI_API_KEY="your_google_api_key_here"
GEMINI_MODEL="gemini-1.5-flash-latest" # or another supported model
```
> **Tip**: Run `python scripts/check_models.py` to see which models your API key supports.

### 4. Initialize Test Data
Generate dummy files (logs, json, images) and the database for testing:

```bash
# Generate files
python scripts/setup_data.py

# Create the SQLite database
python scripts/create_db.py
```

---

## ⚡ Execution & Usage

### Start the API Server
```bash
python app/main.py
```
The server will start on `http://0.0.0.0:8000`.

### Running Tasks (Examples)
You can interact with the agent using Postman, cURL, or any HTTP client.

#### 1. Sort a JSON File
```bash
curl -X POST "http://localhost:8000/run" \
     -H "Content-Type: application/json" \
     -d '{"task": "Sort the contacts in /data/contacts.json by last_name and save to /data/contacts-sorted.json"}'
```

#### 2. Analyze an Image (Vision)
```bash
curl -X POST "http://localhost:8000/run" \
     -H "Content-Type: application/json" \
     -d '{"task": "Extract the credit card number from /data/credit-card.png and save it to /data/credit-card.txt"}'
```

#### 3. Run SQL Query
```bash
curl -X POST "http://localhost:8000/run" \
     -H "Content-Type: application/json" \
     -d '{"task": "Run query \"SELECT * FROM tickets\" on /data/ticket-sales.db and save result to /data/ticket-sales-output.txt"}'
```

---

## 🧪 Testing & Verification

We provide a comprehensive Postman Collection to verify all functionalities.

1.  Locate `llm_automation_postman_collection.json` in the project root.
2.  Import this file into Postman (`File` -> `Import`).
3.  Run the requests in the collection to test each agent capability (Sorting, Counting, API Status, etc.).

---

## 📂 Project Structure

```
LLM-Automation_agent/
├── app/
│   ├── main.py            # FastAPI Entry Point
│   ├── tasks.py           # Tool Implementations (The logic)
│   ├── dispatcher.py      # Routes LLM intent to tools
│   ├── utils.py           # Security & Path validation
│   └── services/
│       └── llm_service.py # Google Gemini Integration
├── data/                  # SANDBOX: All file operations happen here
├── scripts/
│   ├── setup_data.py      # Generates dummy test files
│   ├── create_db.py       # Creates dummy SQLite DB
│   └── check_models.py    # Verifies API Key & Models
├── requirements.txt       # Python dependencies
├── .env                   # API Keys (Not committed)
└── README.md              # Project Documentation
```

---

## 🛡️ License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
