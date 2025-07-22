import os
from dotenv import load_dotenv

load_dotenv()

# Server socket
bind = f"{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '5003')}"
backlog = 2048

# Worker processes
workers = 4  # Adjust based on your server's CPU cores (2*cores + 1 is recommended)
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = 'info'

# Process naming
proc_name = 'flask-api-service'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Auto-reload in development (DO NOT use in production)
reload = os.getenv('FLASK_ENV') == 'development'
reload_engine = 'auto'
reload_extra_files = []

# SSL (if needed)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'
