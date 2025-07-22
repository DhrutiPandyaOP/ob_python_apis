from flask import Blueprint, jsonify
from datetime import datetime
from logger_config import Logger

bp = Blueprint('health', __name__)
logger = Logger.get_logger()

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        return jsonify({
            "status": "healthy",
            "service": "flask-api-service",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }), 200

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

@bp.route('/status', methods=['GET'])
def status_check():
    """Detailed status endpoint"""
    try:
        # Get recent logs count by level
        recent_logs = Logger.get_logs(limit=100)
        log_counts = {}
        for log in recent_logs:
            level = log['level']
            log_counts[level] = log_counts.get(level, 0) + 1

        return jsonify({
            "status_code": 200,
            "data": {
                "service_status": "running",
                "timestamp": datetime.now().isoformat(),
                "recent_logs_summary": log_counts,
                "total_recent_logs": len(recent_logs)
            }
        }), 200

    except Exception as e:
        logger.error(f"Status check failed: {str(e)}")
        return jsonify({
            "status_code": 500,
            "error": f"Status check failed: {str(e)}"
        }), 500
