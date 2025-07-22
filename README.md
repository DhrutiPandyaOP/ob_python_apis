# 🚀 Flask API Service

A high-performance Flask API service with automatic company name placeholder detection, built-in health monitoring, and comprehensive logging system. Features auto-reload capability for seamless development.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development](#development)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- **Company Name Detection**: Advanced ML-based placeholder detection using sentence transformers
- **Auto-reload**: Automatic server restart on code and configuration changes
- **Health Monitoring**: Built-in health check and status endpoints
- **Comprehensive Logging**: In-memory and file-based logging with rotation
- **RESTful API**: Clean and well-structured API endpoints
- **Production Ready**: Gunicorn WSGI server configuration included
- **Environment Configuration**: Easy configuration via `.env` file

## 🔧 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- 4GB RAM minimum (for ML models)
- Ubuntu/Debian (recommended) or any Linux/MacOS/Windows with WSL

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ob_python_project
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/MacOS:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Or create manually with these contents:

```env
HOST=0.0.0.0
PORT=5008
DEBUG=True
FLASK_ENV=development
FLASK_DEBUG=True

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=app.log
LOG_MAX_BYTES=10485760
LOG_BACKUP_COUNT=5

# API Configuration
API_PREFIX=/api
```

## 🚀 Running the Application

### Development Mode (with Auto-reload)

The application supports multiple ways to run with auto-reload:

#### Option 1: Using Watchmedo (Recommended)

```bash
# Install watchdog if not already installed
pip install watchdog

# Run with auto-reload monitoring Python files and .env
watchmedo auto-restart \
    --directory=./ \
    --patterns="*.py;.env;requirements.txt" \
    --recursive \
    -- gunicorn wsgi:app --config gunicorn_config.py
```

#### Option 2: Using Flask Development Server

```bash
# Simple Flask development server
python main.py
```

#### Option 3: Using the Auto-reload Script

```bash
# Make the script executable
chmod +x auto_reload_server.py

# Run the auto-reload server
python auto_reload_server.py
```

### Production Mode

```bash
# Using Gunicorn directly (no auto-reload)
gunicorn wsgi:app --config gunicorn_config.py

# Or use the production start script
chmod +x start_production.sh
./start_production.sh
```

### Accessing the Application

Once running, access the application at:
- **Welcome Page**: http://localhost:5008 (or http://YOUR_IP:5008)
- **API Endpoints**: http://localhost:5008/api/*

## 📚 API Documentation

### 1. Company Name Detection

**Endpoint**: `POST /api/detect-company-name`

Detects placeholder company names in provided text using advanced ML techniques.

**Request:**
```json
{
  "text_json": [
    {"text": "YOUR COMPANY", "index": 0},
    {"text": "Acme Corporation", "index": 1},
    {"text": "BRAND NAME", "index": 2}
  ],
  "threshold": 0.75,
  "semantic_weight": 0.4,
  "fuzzy_weight": 0.3,
  "format_weight": 0.3
}
```

**Response:**
```json
{
    "status_code": 200,
    "data": {
        "company_name": "YOUR COMPANY",
        "index": 0,
        "similarity": 0.9234,
        "confidence": "VERY_HIGH",
        "detection_method": "EXACT_PATTERN_MATCH"
    }
}
```

### 2. Health Check

**Endpoint**: `GET /api/health`

**Response:**
```json
{
    "status": "healthy",
    "service": "flask-api-service",
    "timestamp": "2025-07-22T10:30:45.123456",
    "version": "1.0.0"
}
```

### 3. Detailed Status

**Endpoint**: `GET /api/status`

**Response:**
```json
{
    "status_code": 200,
    "data": {
        "service_status": "running",
        "timestamp": "2025-07-22T10:30:45.123456",
        "recent_logs_summary": {
            "INFO": 45,
            "ERROR": 2,
            "WARNING": 5
        },
        "total_recent_logs": 52
    }
}
```

### 4. View Logs

**Endpoint**: `GET /api/logs?limit=50&level=ERROR`

**Query Parameters:**
- `limit` (optional): Number of logs to retrieve (max: 1000, default: 100)
- `level` (optional): Filter by log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

**Response:**
```json
{
    "status_code": 200,
    "data": {
        "logs": [
            {
                "timestamp": "2025-07-22T10:30:45.123456",
                "level": "ERROR",
                "message": "Error message",
                "module": "flask_api",
                "function": "detect_placeholder",
                "line": 125
            }
        ],
        "total": 1,
        "limit": 50,
        "level_filter": "ERROR"
    }
}
```

### 5. Log Levels

**Endpoint**: `GET /api/logs/levels`

**Response:**
```json
{
    "status_code": 200,
    "data": {
        "available_levels": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    }
}
```

## 📁 Project Structure

```
ob_python_project/
├── api/                        # API modules directory
│   ├── company_name_detector.py   # Company name detection endpoint
│   ├── health.py                  # Health check endpoints
│   └── logs_viewer.py             # Log viewing endpoints
├── utils/                  # HTML templates (optional)
│   └── __init__.py             # For making this project a package
├── .env                        # Environment variables (create this)
├── .env.example               # Example environment file
├── .gitignore                 # Git ignore file
├── config.py                  # Application configuration
├── gunicorn_config.py         # Gunicorn server configuration
├── logger_config.py           # Logging configuration
├── main.py                    # Main application entry point
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── welcome.py                 # Welcome page routes
└── wsgi.py                   # WSGI application entry point
```

## 🛠️ Development

### Adding New API Endpoints

1. Create a new Python file in the `api/` directory
2. Define a Blueprint with name `bp`
3. Add your routes to the blueprint
4. The application will auto-discover and register it

Example:
```python
# api/new_endpoint.py
from flask import Blueprint, jsonify

bp = Blueprint('new_endpoint', __name__)

@bp.route('/new-route', methods=['GET'])
def new_route():
    return jsonify({"message": "Hello from new endpoint!"}), 200
```

### Modifying Configuration

- Edit `.env` file for environment-specific settings
- Modify `config.py` for application-wide settings
- Update `gunicorn_config.py` for server settings

### Testing

```bash
# Test health endpoint
curl http://localhost:5008/api/health

# Test company name detection
curl -X POST http://localhost:5008/api/detect-company-name \
  -H "Content-Type: application/json" \
  -d '{
    "text_json": [
        {"text": "YOUR COMPANY", "index": 0},
        {"text": "Google Inc", "index": 1}
    ]
  }'
```

## 🚀 Production Deployment

### Using Systemd (Recommended)

1. Create service file:
```bash
sudo nano /etc/systemd/system/flask-api.service
```

2. Add service configuration:
```ini
[Unit]
Description=Flask API Service
After=network.target

[Service]
User=your-user
WorkingDirectory=/path/to/ob_python_project
Environment="PATH=/path/to/ob_python_project/venv/bin"
ExecStart=/path/to/ob_python_project/venv/bin/gunicorn wsgi:app --config gunicorn_config.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable flask-api
sudo systemctl start flask-api
```

### Using Docker

```bash
# Build image
docker build -t flask-api .

# Run container
docker run -d -p 5008:5008 --name flask-api --env-file .env flask-api
```

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port
   lsof -i :5008
   
   # Kill process
   kill -9 <PID>
   ```

2. **Module Import Errors**
    - Ensure virtual environment is activated
    - Reinstall requirements: `pip install -r requirements.txt`

3. **Memory Issues with ML Model**
    - Increase system RAM
    - Reduce worker count in `gunicorn_config.py`

4. **Auto-reload Not Working**
    - Ensure watchdog is installed: `pip install watchdog`
    - Check file permissions
    - Verify pattern matching in watchmedo command

### Viewing Logs

```bash
# Application logs
tail -f app.log

# System logs (if using systemd)
sudo journalctl -u flask-api -f

```

