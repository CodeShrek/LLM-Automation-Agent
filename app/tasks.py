import os
import json
import subprocess
import sqlite3
import datetime
import glob
import logging
import numpy as np
import mdformat  # <--- NEW: Import mdformat
from dateutil import parser
from app.utils import secure_path
from app.services.llm_service import llm_client

# --- A1. Install UV and Run Datagen ---
async def install_uv_datagen(user_email: str = "test@example.com"):
    try:
        # 1. Install uv
        subprocess.run(["pip", "install", "uv"], check=True)
        
        # 2. Download datagen.py
        url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
        subprocess.run(["curl", "-o", "datagen.py", url], check=True)
        
        # 3. Run datagen.py
        subprocess.run(["python", "datagen.py", user_email], check=True)
        return "UV installed and Data Generation completed."
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Script execution failed: {e}")

# --- A2. Format Markdown (UPDATED: Pure Python) ---
async def format_markdown(file_path: str):
    path = secure_path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist.")
    
    try:
        # Read content
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Format using Python library (No Node.js needed!)
        formatted = mdformat.text(content)
        
        # Write back
        with open(path, "w", encoding="utf-8") as f:
            f.write(formatted)
            
        return f"Formatted {file_path} successfully."
    except Exception as e:
        raise RuntimeError(f"Formatting failed: {e}")

# --- A3. Count Weekdays ---
async def count_weekdays(file_path: str, target_weekday_name: str, output_file: str):
    input_path = secure_path(file_path)
    output_path = secure_path(output_file)
    
    weekday_map = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
        "Friday": 4, "Saturday": 5, "Sunday": 6
    }
    target_idx = weekday_map.get(target_weekday_name)
    if target_idx is None:
        raise ValueError("Invalid weekday name.")

    count = 0
    with open(input_path, 'r') as f:
        for line in f:
            try:
                dt = parser.parse(line.strip())
                if dt.weekday() == target_idx:
                    count += 1
            except:
                continue
    
    with open(output_path, 'w') as f:
        f.write(str(count))
    return f"Counted {count} {target_weekday_name}s."

# --- A4. Sort JSON ---
async def sort_json(file_path: str, sort_keys: list, output_file: str):
    input_path = secure_path(file_path)
    output_path = secure_path(output_file)
    
    with open(input_path, 'r') as f:
        data = json.load(f)
    
    # Sort data
    data.sort(key=lambda x: tuple(x.get(k, "") for k in sort_keys))
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    return f"Sorted JSON saved to {output_file}."

# --- A5. Recent Logs ---
async def extract_recent_logs(logs_dir: str, output_file: str, count: int = 10):
    logs_path = secure_path(logs_dir)
    output_path = secure_path(output_file)
    
    log_files = sorted(glob.glob(str(logs_path / "*.log")), key=os.path.getmtime, reverse=True)
    recent_files = log_files[:count]
    
    extracted_lines = []
    for log_file in recent_files:
        with open(log_file, 'r') as f:
            first_line = f.readline().strip()
            extracted_lines.append(first_line)
            
    with open(output_path, 'w') as f:
        f.write("\n".join(extracted_lines))
    return f"Extracted lines from {len(recent_files)} log files."

# --- A6. Index Markdown ---
async def create_index(docs_dir: str, output_file: str):
    docs_path = secure_path(docs_dir)
    output_path = secure_path(output_file)
    
    index = {}
    for md_file in docs_path.glob("**/*.md"):
        with open(md_file, 'r') as f:
            for line in f:
                if line.startswith("# "):
                    rel_path = str(md_file.relative_to(docs_path))
                    index[rel_path] = line.strip("# ").strip()
                    break
    
    with open(output_path, 'w') as f:
        json.dump(index, f, indent=2)
    return "Index created."

# --- A7. Extract Email Sender ---
async def extract_email_sender(file_path: str, output_file: str):
    input_path = secure_path(file_path)
    output_path = secure_path(output_file)
    
    with open(input_path, 'r') as f:
        content = f.read()
    
    prompt = f"Extract the sender's email address from this text. Return ONLY the email address.\n\nTEXT:\n{content}"
    result = await llm_client.model.generate_content_async(prompt)
    email = result.text.strip()
    
    with open(output_path, 'w') as f:
        f.write(email)
    return f"Email extracted: {email}"

# --- A8. Extract Credit Card ---
async def extract_credit_card(image_path: str, output_file: str):
    input_path = secure_path(image_path)
    output_path = secure_path(output_file)
    
    with open(input_path, 'rb') as img_file:
        image_data = img_file.read()
        
    prompt = "Extract the credit card number from this image. Return ONLY the numbers, no spaces."
    card_number = await llm_client.get_image_content(image_data, prompt)
    
    with open(output_path, 'w') as f:
        f.write(card_number.replace(" ", ""))
    return "Credit card extracted."

# --- A9. Similar Comments ---
async def find_similar_comments(file_path: str, output_file: str):
    input_path = secure_path(file_path)
    output_path = secure_path(output_file)
    
    with open(input_path, 'r') as f:
        comments = [line.strip() for line in f if line.strip()]
    
    if len(comments) < 2:
        return "Not enough comments to compare."

    embeddings = [await llm_client.get_embedding(c) for c in comments]
    
    max_sim = -1
    best_pair = ("", "")
    
    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            sim = np.dot(embeddings[i], embeddings[j])
            if sim > max_sim:
                max_sim = sim
                best_pair = (comments[i], comments[j])
                
    with open(output_path, 'w') as f:
        f.write(f"{best_pair[0]}\n{best_pair[1]}")
    return "Similar comments found."

# --- A10. Query Database ---
async def query_database(db_path: str, query: str, output_file: str):
    db_full_path = secure_path(db_path)
    output_path = secure_path(output_file)
    
    conn = sqlite3.connect(db_full_path)
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        
        with open(output_path, 'w') as f:
            if len(result) == 1 and len(result[0]) == 1:
                f.write(str(result[0][0]))
            else:
                json.dump(result, f)
    finally:
        conn.close()
    return "Database query executed."