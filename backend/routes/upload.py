"""File upload endpoints"""
import json
import logging
from pathlib import Path
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

bp = Blueprint('upload', __name__, url_prefix='/api')


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def validate_json_structure(data):
    """Validate Claude export JSON structure"""
    if not isinstance(data, dict):
        return False, "Invalid JSON: root must be an object"

    if 'conversations' not in data:
        return False, "Invalid JSON: missing 'conversations' field"

    if not isinstance(data['conversations'], list):
        return False, "Invalid JSON: 'conversations' must be an array"

    if len(data['conversations']) == 0:
        return False, "No conversations found in export"

    return True, None


@bp.route('/upload', methods=['POST'])
def upload_file():
    """Upload conversation JSON file"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only JSON files are allowed'}), 400

        # Save file
        filename = secure_filename(file.filename)
        file_path = current_app.config['UPLOAD_FOLDER'] / filename
        file.save(file_path)

        logger.info(f"File uploaded: {filename}")

        # Validate JSON structure
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            valid, error = validate_json_structure(data)
            if not valid:
                file_path.unlink()  # Delete invalid file
                return jsonify({'error': error}), 400

            # Extract metadata
            conversations = data['conversations']
            total_messages = sum(len(conv.get('messages', [])) for conv in conversations)

            # Get date range
            dates = []
            for conv in conversations:
                if 'created_at' in conv:
                    dates.append(conv['created_at'])
                if 'updated_at' in conv:
                    dates.append(conv['updated_at'])

            date_range = [min(dates), max(dates)] if dates else None

            # Calculate file hash
            file_hash = current_app.cache_service.calculate_file_hash(file_path)

            # Check if we have cached results
            cached_results = current_app.cache_service.get(file_hash)

            metadata = {
                'size': file_path.stat().st_size,
                'conversations': len(conversations),
                'messages': total_messages,
                'date_range': date_range,
                'has_cached_results': cached_results is not None
            }

            logger.info(f"File validated: {len(conversations)} conversations, {total_messages} messages")

            return jsonify({
                'file_id': filename,
                'file_hash': file_hash,
                'metadata': metadata
            }), 200

        except json.JSONDecodeError as e:
            file_path.unlink()  # Delete invalid file
            return jsonify({'error': f'Invalid JSON format: {str(e)}'}), 400

    except Exception as e:
        logger.error(f"Upload error: {e}", exc_info=True)
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


@bp.route('/upload/<file_id>', methods=['GET'])
def get_upload_info(file_id):
    """Get information about an uploaded file"""
    try:
        filename = secure_filename(file_id)
        file_path = current_app.config['UPLOAD_FOLDER'] / filename

        if not file_path.exists():
            return jsonify({'error': 'File not found'}), 404

        with open(file_path, 'r') as f:
            data = json.load(f)

        conversations = data['conversations']
        total_messages = sum(len(conv.get('messages', [])) for conv in conversations)

        return jsonify({
            'file_id': filename,
            'metadata': {
                'size': file_path.stat().st_size,
                'conversations': len(conversations),
                'messages': total_messages
            }
        }), 200

    except Exception as e:
        logger.error(f"Get upload info error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500
