import streamlit as st
import requests
import json
import time

# --- Configuration ---
# Since both run in the same container on Render, localhost is correct
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="DataWorks Agent",
    page_icon="🤖",
    layout="wide"
)

# --- Header ---
st.title("🤖 DataWorks Automation Agent")
st.markdown("""
Welcome to your intelligent file operations agent. 
Describe your task in plain English, and the agent will execute it securely.
""")

# --- Sidebar: System Status & File Viewer ---
with st.sidebar:
    st.header("🔌 System Status")
    try:
        # Simple health check
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            st.success("API is Online")
        else:
            st.error(f"API Error: {response.status_code}")
    except Exception as e:
        st.error("API Connection Failed")
        st.caption(f"Details: {e}")
    
    st.divider()
    
    st.header("📂 File Viewer")
    st.caption("View files from the /data directory")
    file_path = st.text_input("Path:", value="data/logs-recent.txt")
    
    if st.button("Read File"):
        try:
            # Call the /read endpoint
            res = requests.get(f"{API_URL}/read", params={"path": file_path})
            if res.status_code == 200:
                st.code(res.text)
            else:
                st.error("Error reading file")
                st.write(res.json())
        except Exception as e:
            st.error(f"Connection Error: {e}")

# --- Main Interaction Area ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🛠️ Task Execution")
    
    # Input for the user task
    task_input = st.text_area(
        "Enter your instruction:", 
        height=100,
        placeholder="Example: Sort the contacts in /data/contacts.json..."
    )
    
    run_button = st.button("🚀 Run Task", type="primary")
    
    if run_button and task_input:
        with st.spinner("Agent is thinking & executing..."):
            try:
                # Call the /run endpoint
                payload = {"task": task_input}
                response = requests.post(f"{API_URL}/run", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Task Completed Successfully!")
                    st.json(result)
                    st.balloons()
                else:
                    st.error("❌ Task Failed")
                    try:
                        st.error(response.json().get('detail'))
                    except:
                        st.error(response.text)
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")

# --- Example Tasks Helper ---
with col2:
    st.subheader("💡 Example Tasks")
    st.info("Click to copy & paste:")
    
    examples = [
        "Sort the contacts in /data/contacts.json by last_name",
        "Count the number of Mondays in /data/dates.txt",
        "Format the markdown file /data/format.md",
        "Extract the sender email from /data/email.txt",
        "Extract the credit card number from /data/credit-card.png"
    ]
    
    for ex in examples:
        st.code(ex, language="text")

# --- Footer ---
st.divider()
st.caption("Powered by FastAPI & Google Gemini 2.0")