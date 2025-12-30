"""Analysis endpoints"""
import logging
from pathlib import Path
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

bp = Blueprint('analysis', __name__, url_prefix='/api')


@bp.route('/analysis', methods=['POST'])
def start_analysis():
    """Start a new analysis job"""
    try:
        data = request.get_json()

        if not data or 'file_id' not in data:
            return jsonify({'error': 'file_id is required'}), 400

        file_id = secure_filename(data['file_id'])
        file_path = current_app.config['UPLOAD_FOLDER'] / file_id

        if not file_path.exists():
            return jsonify({'error': 'File not found'}), 404

        # Get analysis options
        options = data.get('options', {})
        options.setdefault('enable_privacy', True)
        options.setdefault('enable_quality', True)
        options.setdefault('enable_temporal', True)
        options.setdefault('enable_visualizations', False)

        # Create analysis job
        job_id = current_app.analyzer_service.create_job(file_path, options)

        logger.info(f"Analysis job created: {job_id}")

        return jsonify({
            'job_id': job_id,
            'status': 'pending',
            'message': 'Analysis job created successfully'
        }), 200

    except Exception as e:
        logger.error(f"Start analysis error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@bp.route('/analysis/<job_id>', methods=['GET'])
def get_analysis(job_id):
    """Get analysis job status and results"""
    try:
        job = current_app.analyzer_service.get_job(job_id)

        if not job:
            return jsonify({'error': 'Job not found'}), 404

        return jsonify(job.to_dict()), 200

    except Exception as e:
        logger.error(f"Get analysis error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@bp.route('/analysis/<job_id>', methods=['DELETE'])
def cancel_analysis(job_id):
    """Cancel an analysis job"""
    try:
        success = current_app.analyzer_service.cancel_job(job_id)

        if not success:
            return jsonify({'error': 'Job not found or cannot be cancelled'}), 404

        return jsonify({'message': 'Job cancelled successfully'}), 200

    except Exception as e:
        logger.error(f"Cancel analysis error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500
