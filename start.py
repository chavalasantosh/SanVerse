#!/usr/bin/env python3
"""
Startup script for Railway deployment
Reads PORT from environment variable and starts uvicorn
"""
import os
import sys

# Try to use config utilities if available
try:
    from santok.utils.config import Config
    from santok.utils.logging_config import setup_logging, get_logger
    SANTOK_UTILS_AVAILABLE = True
    logger = get_logger(__name__)
except ImportError:
    SANTOK_UTILS_AVAILABLE = False
    logger = None
from typing import NoReturn

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def get_port() -> int:
    """Get PORT from environment variable with validation"""
    if SANTOK_UTILS_AVAILABLE:
        try:
            from santok.utils.validation import validate_port
            port_str = os.environ.get("PORT", "8000")
            return validate_port(int(port_str), param_name="PORT")
        except Exception:
            # Fallback to default if validation fails
            return Config.DEFAULT_PORT
    else:
        # Fallback implementation without utils
        try:
            port_str = os.environ.get("PORT", "8000")
            port = int(port_str)
            if port < 1 or port > 65535:
                raise ValueError(f"Port must be between 1 and 65535, got {port}")
            return port
        except (ValueError, TypeError):
            port = 8000
            print(f"[WARNING] Invalid PORT env var, using default: {port}", file=sys.stderr)
            return port

def main() -> NoReturn:
    """Main function to start the server"""
    # Set up logging if available
    if SANTOK_UTILS_AVAILABLE:
        log_level = Config.get_log_level()
        log_file = Config.get_log_file()
        setup_logging(level=log_level, log_file=log_file)
        if logger:
            logger.info("Starting SanTOK API Server")
    
    port = get_port()
    
    if logger:
        logger.info(f"Starting server on port {port}")
        logger.info(f"Server will be available at: http://0.0.0.0:{port}")
        logger.info(f"API Documentation at: http://0.0.0.0:{port}/docs")
    else:
        print(f"[START] Starting SanTOK API Server on port {port}...")
        print(f"[INFO] Server will be available at: http://0.0.0.0:{port}")
        print(f"[INFO] API Documentation at: http://0.0.0.0:{port}/docs")
        print(f"[INFO] Python path: {sys.path}")
        print("=" * 50)
    
    # Import uvicorn and start the server
    try:
        import uvicorn
    except ImportError:
        print("[ERROR] uvicorn is not installed. Install it with: pip install uvicorn", file=sys.stderr)
        sys.exit(1)
    
    try:
        uvicorn.run(
            "src.servers.main_server:app",
            host="0.0.0.0",
            port=port,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Failed to start server: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
