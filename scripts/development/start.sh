#!/bin/bash
# Startup script for Railway deployment
# Reads PORT from environment variable

PORT=${PORT:-8000}
exec uvicorn src.servers.main_server:app --host 0.0.0.0 --port $PORT

