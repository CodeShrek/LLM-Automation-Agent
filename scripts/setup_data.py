import os
import json
import random
from datetime import datetime, timedelta

# Configuration
# Ensures data is created in the project root's 'data' folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "logs"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "docs"), exist_ok=True)

print(f"🚀 Generating Test Data in {DATA_DIR}...")

# 1. Generate Log Files (for extraction tasks)
print("- Creating Log files...")
for i in range(5):
    timestamp = datetime.now() - timedelta(days=i)
    log_content = f"""[INFO] {timestamp.isoformat()} Server started.
[ERROR] Database connection failed at {timestamp.time()}
[INFO] Retrying connection...
[DEBUG] User payload: {{id: {random.randint(1000,9999)}}}
"""
    with open(os.path.join(DATA_DIR, "logs", f"server_v{i}.log"), "w") as f:
        f.write(log_content)

# 2. Generate Messy Contacts (for sorting tasks)
print("- Creating Contacts JSON...")
contacts = [
    {"id": 1, "first_name": "John", "last_name": "Doe", "email": "john@example.com"},
    {"id": 2, "first_name": "Alice", "last_name": "Smith", "email": "alice@corp.net"},
    {"id": 3, "first_name": "Bob", "last_name": "Jones", "email": "bob@gmail.com"},
    {"id": 4, "first_name": "Charlie", "last_name": "Brown", "email": "charlie@xyz.org"}
]
random.shuffle(contacts)
with open(os.path.join(DATA_DIR, "contacts.json"), "w") as f:
    json.dump(contacts, f, indent=4)

# 3. Generate Email Text (for AI extraction)
print("- Creating Email Text...")
email_txt = """
From: security-alert@bank.com
To: user@example.com
Subject: Action Required
Date: 2024-05-20

Dear Customer, we noticed a login from IP 192.168.1.1. 
Please verify this activity immediately.
"""
with open(os.path.join(DATA_DIR, "email.txt"), "w") as f:
    f.write(email_txt)

# 4. Generate Markdown (for formatting & indexing)
print("- Creating Markdown files...")
md_text = """#    Project Header
This is a   list:
* item 1
* item 2
"""
with open(os.path.join(DATA_DIR, "format.md"), "w") as f:
    f.write(md_text)

doc_text = """# API Documentation
This is the API documentation.
"""
with open(os.path.join(DATA_DIR, "docs", "api.md"), "w") as f:
    f.write(doc_text)

# 5. Generate Dates (for counting weekdays)
print("- Creating Dates file...")
dates = [
    "2024-01-01", # Monday
    "2024-01-03", # Wednesday
    "2024-01-10", # Wednesday
    "2024-05-20", # Monday
]
with open(os.path.join(DATA_DIR, "dates.txt"), "w") as f:
    f.write("\n".join(dates))

# 6. Create Dummy Credit Card Image (Placeholder)
print("- Creating Dummy Credit Card file...")
# Creating a minimal valid PNG header for testing
with open(os.path.join(DATA_DIR, "credit-card.png"), "wb") as f:
    f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')

print("✅ Data Generation Complete!")