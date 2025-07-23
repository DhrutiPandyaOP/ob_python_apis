from flask import Blueprint, render_template_string
from config import Config
from datetime import datetime

welcome_bp = Blueprint('welcome', __name__)

WELCOME_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask API Service - Welcome</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #333;
        }

        .container {
            background-color: rgba(255, 255, 255, 0.95);
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            max-width: 800px;
            width: 90%;
            backdrop-filter: blur(10px);
        }

        .header {
            text-align: center;
            margin-bottom: 2rem;
        }

        h1 {
            color: #333;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background-color: #10b981;
            color: white;
            border-radius: 30px;
            font-size: 0.875rem;
            font-weight: 500;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background-color: white;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }

        .info-card {
            background-color: #f9fafb;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
        }

        .info-card h3 {
            color: #6b7280;
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .info-card p {
            color: #374151;
            font-size: 1.25rem;
            font-weight: 600;
        }

        .endpoints-section {
            background-color: #f3f4f6;
            padding: 2rem;
            border-radius: 12px;
            margin-top: 2rem;
        }

        .endpoints-section h2 {
            color: #374151;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
        }

        .endpoint-grid {
            display: grid;
            gap: 1rem;
        }

        .endpoint-card {
            background-color: white;
            padding: 1.25rem;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .endpoint-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        .endpoint-method {
            background-color: #3b82f6;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        .endpoint-method.get {
            background-color: #10b981;
        }

        .endpoint-path {
            color: #4b5563;
            font-family: 'Courier New', monospace;
            font-size: 0.875rem;
            flex: 1;
            margin: 0 1rem;
        }

        .endpoint-desc {
            color: #6b7280;
            font-size: 0.875rem;
        }

        .footer {
            text-align: center;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #e5e7eb;
            color: #6b7280;
            font-size: 0.875rem;
        }

        .footer a {
            color: #6366f1;
            text-decoration: none;
            font-weight: 500;
        }

        .footer a:hover {
            text-decoration: underline;
        }

        @media (max-width: 640px) {
            .endpoint-card {
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
            }

            .endpoint-path {
                margin: 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Python API Service</h1>
            <div class="status-badge">
                <span class="status-dot"></span>
                Service Running
            </div>
        </div>
        <p style="text-align: center; color: #6b7280; margin-bottom: 2rem;">
            Welcome to the Flask API Service. All systems are operational and ready to process requests.
        </p>
        <div class="info-grid">
            <div class="info-card">
                <h3>Server</h3>
                <p>{{ host }}:{{ port }}</p>
            </div>
            <div class="info-card">
                <h3>Environment</h3>
                <p>{{ env }}</p>
            </div>
        </div>
        <div class="endpoints-section">
            <h2>Available API Endpoints</h2>
            <div class="endpoint-grid">
                <div class="endpoint-card">
                    <span class="endpoint-method">POST</span>
                    <span class="endpoint-path">/api/detect-company-name</span>
                    <span class="endpoint-desc">Detect company name placeholders</span>
                </div>
                <div class="endpoint-card">
                    <span class="endpoint-method get">GET</span>
                    <span class="endpoint-path">/api/health</span>
                    <span class="endpoint-desc">Health check endpoint</span>
                </div>
                <div class="endpoint-card">
                    <span class="endpoint-method get">GET</span>
                    <span class="endpoint-path">/api/status</span>
                    <span class="endpoint-desc">Detailed status information</span>
                </div>
                <div class="endpoint-card">
                    <span class="endpoint-method get">GET</span>
                    <span class="endpoint-path">/api/logs</span>
                    <span class="endpoint-desc">View application logs</span>
                </div>
                <div class="endpoint-card">
                    <span class="endpoint-method get">GET</span>
                    <span class="endpoint-path">/api/logs/levels</span>
                    <span class="endpoint-desc">Get available log levels</span>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>
                Current Time: {{ current_time }} |
                <a href="/api/health">Check API Health</a> |
                <a href="/api/logs">View Logs</a>
            </p>
            <p style="margin-top: 0.5rem;">
                Flask API Service © {{ year }}
            </p>
        </div>
    </div>
</body>
</html>
'''

@welcome_bp.route('/')
def welcome():
    """Welcome page route"""
    return render_template_string(WELCOME_HTML,
        host=Config.HOST,
        port=Config.PORT,
        env=Config.FLASK_ENV,
        current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        year=datetime.now().year
    )
