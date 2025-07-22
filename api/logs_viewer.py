from flask import Blueprint, jsonify, request
from logger_config import Logger

bp = Blueprint('logs_viewer', __name__)
logger = Logger.get_logger()

@bp.route('/logs', methods=['GET'])
def get_logs():
    """Get application logs"""
    try:
        # Get query parameters
        limit = request.args.get('limit', 100, type=int)
        level = request.args.get('level', None, type=str)

        # Validate limit
        if limit > 1000:
            limit = 1000

        # Get logs from memory
        logs = Logger.get_logs(limit=limit, level=level)

        return jsonify({
            "status_code": 200,
            "data": {
                "logs": logs,
                "total": len(logs),
                "limit": limit,
                "level_filter": level
            }
        }), 200

    except Exception as e:
        logger.error(f"Error retrieving logs: {str(e)}")
        return jsonify({
            "status_code": 500,
            "error": f"Failed to retrieve logs: {str(e)}"
        }), 500

@bp.route('/logs/levels', methods=['GET'])
def get_log_levels():
    """Get available log levels"""
    try:
        levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        return jsonify({
            "status_code": 200,
            "data": {
                "available_levels": levels
            }
        }), 200

    except Exception as e:
        logger.error(f"Error getting log levels: {str(e)}")
        return jsonify({
            "status_code": 500,
            "error": f"Failed to get log levels: {str(e)}"
        }), 500
