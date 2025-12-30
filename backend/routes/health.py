"""Health check endpoints"""
from flask import Blueprint, jsonify, current_app
import time

bp = Blueprint('health', __name__, url_prefix='/api')

# Track start time
START_TIME = time.time()


@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'uptime': int(time.time() - START_TIME),
        'active_jobs': len(current_app.analyzer_service.active_jobs),
        'cache_size': current_app.cache_service.get_size()
    })
