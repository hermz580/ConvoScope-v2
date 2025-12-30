"""WebSocket event handlers"""
import logging
from flask_socketio import join_room, leave_room, emit

logger = logging.getLogger(__name__)


def register_websocket_events(socketio, analyzer_service):
    """Register WebSocket event handlers"""

    @socketio.on('connect')
    def handle_connect():
        logger.info('Client connected')
        emit('connected', {'message': 'Connected to ConvoScope server'})

    @socketio.on('disconnect')
    def handle_disconnect():
        logger.info('Client disconnected')

    @socketio.on('subscribe')
    def handle_subscribe(data):
        """Subscribe to job updates"""
        job_id = data.get('job_id')
        if job_id:
            join_room(job_id)
            logger.info(f'Client subscribed to job {job_id}')
            emit('subscribed', {'job_id': job_id})

    @socketio.on('unsubscribe')
    def handle_unsubscribe(data):
        """Unsubscribe from job updates"""
        job_id = data.get('job_id')
        if job_id:
            leave_room(job_id)
            logger.info(f'Client unsubscribed from job {job_id}')
            emit('unsubscribed', {'job_id': job_id})

    @socketio.on('ping')
    def handle_ping():
        """Ping/pong for keeping connection alive"""
        emit('pong')
