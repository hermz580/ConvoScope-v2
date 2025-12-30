"""ConvoScope Flask Backend Application"""
import os
import logging
from pathlib import Path
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO

from config import get_config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(get_config())

# Initialize CORS
CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

# Initialize SocketIO
socketio = SocketIO(
    app,
    cors_allowed_origins=app.config['CORS_ORIGINS'],
    async_mode='eventlet'
)

# Setup logging
logging.basicConfig(
    level=logging.INFO if app.config['DEBUG'] else logging.WARNING,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

# Initialize services
from services.analyzer_service import AnalyzerService
from services.cache_service import CacheService

analyzer_service = AnalyzerService(app.config, socketio)
cache_service = CacheService(app.config['CACHE_FOLDER'])

# Make services available to routes
app.analyzer_service = analyzer_service
app.cache_service = cache_service

# Register routes
from routes import upload, analysis, export, health

app.register_blueprint(upload.bp)
app.register_blueprint(analysis.bp)
app.register_blueprint(export.bp)
app.register_blueprint(health.bp)

# Register WebSocket events
from services.websocket_service import register_websocket_events
register_websocket_events(socketio, analyzer_service)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Internal error: {error}')
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        'error': 'File too large',
        'message': f'Maximum file size is {app.config["MAX_CONTENT_LENGTH"] // (1024*1024)}MB'
    }), 413


# Root endpoint
@app.route('/')
def index():
    return jsonify({
        'name': 'ConvoScope API',
        'version': '2.0.0',
        'status': 'running',
        'documentation': '/api/health'
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.logger.info(f'Starting ConvoScope backend on port {port}')
    app.logger.info(f'CORS enabled for: {app.config["CORS_ORIGINS"]}')

    socketio.run(
        app,
        host='127.0.0.1',  # Localhost only for privacy
        port=port,
        debug=app.config['DEBUG']
    )
