#!/bin/bash

# 1. Start FastAPI in the background
# We bind it to 0.0.0.0:8000 so the frontend can reach it locally
nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# 2. Start Streamlit in the foreground
# Render expects the web service to listen on the port defined by $PORT
streamlit run frontend.py --server.port=$PORT --server.address=0.0.0.0