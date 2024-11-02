import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import logging
import platform

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Configure logging for better security monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security headers for protection
@app.after_request
def set_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self';"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# Root route
@app.route("/", methods=["GET"])
def home():
    return "Welcome to Project Maya! This project is a work in progress."

# Enhanced secure command execution
@app.route("/execute", methods=["POST"])
def execute_command():
    try:
        # Extract and sanitize user input
        command = request.json.get("command", "")
        if not command:
            return jsonify({"error": "No command provided"}), 400

        # Safe commands whitelist
        if platform.system() == "Windows":
            allowed_commands = {
                "list_files": "dir",
                "current_directory": "cd",
                "system_info": "systeminfo",
                "disk_usage": "wmic logicaldisk get size,freespace,caption",
                "cpu_usage": "wmic cpu get loadpercentage",
                "network_status": "ipconfig",
                "ping_google": "ping google.com"
            }
        else:  # Linux/macOS
            allowed_commands = {
                "list_files": "ls",
                "current_directory": "pwd",
                "system_info": "uname -a",
                "disk_usage": "df -h",
                "cpu_usage": "top -bn1 | grep 'Cpu'",
                "network_status": "ifconfig",
                "ping_google": "ping -c 4 google.com"
            }

        # Check if the command is in the whitelist
        if command not in allowed_commands:
            return jsonify({"error": "Command not allowed"}), 403

        # Execute the whitelisted command
        output = os.popen(allowed_commands[command]).read()
        return jsonify({"output": output})
    
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


# Start the app using secure configuration
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)
