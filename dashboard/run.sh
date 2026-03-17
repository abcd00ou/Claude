#!/bin/bash
# SanDisk Intelligence Hub 실행
cd "$(dirname "$0")"
streamlit run app.py --server.port 8502 --server.headless false
