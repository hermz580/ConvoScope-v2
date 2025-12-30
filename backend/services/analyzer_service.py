"""Analysis service for processing conversations"""
import sys
import json
import logging
import threading
from queue import Queue
from pathlib import Path
from typing import Dict, Optional, Callable
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

# Add parent directory to path to import ConvoScope modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class AnalysisJob:
    """Represents an analysis job"""

    def __init__(self, job_id: str, file_path: Path, options: Dict):
        self.job_id = job_id
        self.file_path = file_path
        self.options = options
        self.status = 'pending'  # pending, processing, complete, failed
        self.progress = 0
        self.current_step = ''
        self.results = None
        self.error = None
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None

    def to_dict(self):
        """Convert job to dictionary"""
        return {
            'job_id': self.job_id,
            'status': self.status,
            'progress': self.progress,
            'current_step': self.current_step,
            'results': self.results,
            'error': str(self.error) if self.error else None,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }


class AnalyzerService:
    """Service for managing analysis jobs"""

    def __init__(self, config: Dict, socketio):
        self.config = config
        self.socketio = socketio
        self.job_queue = Queue()
        self.active_jobs = {}
        self.worker_thread = None
        self.running = False

    def start(self):
        """Start the worker thread"""
        if not self.running:
            self.running = True
            self.worker_thread = threading.Thread(target=self._process_jobs, daemon=True)
            self.worker_thread.start()
            logger.info("Analyzer service started")

    def stop(self):
        """Stop the worker thread"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        logger.info("Analyzer service stopped")

    def create_job(self, file_path: Path, options: Dict) -> str:
        """Create a new analysis job"""
        job_id = str(uuid.uuid4())
        job = AnalysisJob(job_id, file_path, options)
        self.active_jobs[job_id] = job
        self.job_queue.put(job)
        logger.info(f"Created job {job_id}")

        # Start worker if not running
        if not self.running:
            self.start()

        return job_id

    def get_job(self, job_id: str) -> Optional[AnalysisJob]:
        """Get job by ID"""
        return self.active_jobs.get(job_id)

    def cancel_job(self, job_id: str) -> bool:
        """Cancel a job"""
        job = self.active_jobs.get(job_id)
        if job and job.status in ['pending', 'processing']:
            job.status = 'failed'
            job.error = 'Cancelled by user'
            logger.info(f"Cancelled job {job_id}")
            return True
        return False

    def _process_jobs(self):
        """Worker thread that processes jobs"""
        logger.info("Worker thread started")
        while self.running:
            try:
                job = self.job_queue.get(timeout=1)
                if job.status != 'failed':  # Skip if already cancelled
                    self._run_analysis(job)
            except:
                # Queue empty, continue
                continue
        logger.info("Worker thread stopped")

    def _run_analysis(self, job: AnalysisJob):
        """Run the analysis for a job"""
        try:
            job.status = 'processing'
            job.started_at = datetime.now()
            logger.info(f"Starting analysis for job {job.job_id}")

            # Import here to avoid circular imports
            from src.advanced_analyzer import AdvancedConversationAnalyzer

            # Emit initial progress
            self._emit_progress(job, 5, "Loading data...")

            # Initialize analyzer
            analyzer = AdvancedConversationAnalyzer(
                str(job.file_path),
                enable_privacy=job.options.get('enable_privacy', True),
                enable_quality_analysis=job.options.get('enable_quality', True),
                enable_temporal_analysis=job.options.get('enable_temporal', True),
                enable_visualizations=job.options.get('enable_visualizations', False)
            )

            # Load data
            analyzer.load_data()
            self._emit_progress(job, 15, "Data loaded successfully")

            # Parse conversations
            logger.info(f"Parsing conversations for job {job.job_id}")
            self._emit_progress(job, 25, "Analyzing conversations...")

            df = analyzer.parse_conversations_advanced()

            self._emit_progress(job, 70, f"Analyzed {len(df):,} messages")

            # Prepare results
            job.results = {
                'summary': {
                    'total_conversations': len(df['conversation_id'].unique()),
                    'total_messages': len(df),
                    'user_messages': len(df[df['role'] == 'user']),
                    'assistant_messages': len(df[df['role'] == 'assistant']),
                    'avg_message_length': int(df['content_length'].mean()),
                    'avg_words_per_message': round(df['word_count'].mean(), 1),
                },
                'data': df.to_dict(orient='records')[:1000],  # Limit to first 1000 for performance
                'topics': self._get_topic_distribution(df),
                'sentiment': self._get_sentiment_distribution(df),
                'quality': self._get_quality_metrics(df),
            }

            job.status = 'complete'
            job.completed_at = datetime.now()
            job.progress = 100

            logger.info(f"Analysis complete for job {job.job_id}")
            self._emit_complete(job)

        except Exception as e:
            logger.error(f"Analysis failed for job {job.job_id}: {e}", exc_info=True)
            job.status = 'failed'
            job.error = str(e)
            job.completed_at = datetime.now()
            self._emit_error(job, str(e))

    def _emit_progress(self, job: AnalysisJob, progress: int, message: str):
        """Emit progress update via WebSocket"""
        job.progress = progress
        job.current_step = message

        self.socketio.emit('progress', {
            'job_id': job.job_id,
            'progress': progress,
            'message': message,
            'status': job.status
        }, room=job.job_id)

    def _emit_complete(self, job: AnalysisJob):
        """Emit completion event"""
        self.socketio.emit('complete', {
            'job_id': job.job_id,
            'status': 'complete'
        }, room=job.job_id)

    def _emit_error(self, job: AnalysisJob, error: str):
        """Emit error event"""
        self.socketio.emit('error', {
            'job_id': job.job_id,
            'error': error,
            'status': 'failed'
        }, room=job.job_id)

    def _get_topic_distribution(self, df):
        """Get topic distribution from dataframe"""
        topic_counts = {}
        for topics_str in df['topics'].dropna():
            if isinstance(topics_str, str):
                for topic in topics_str.split('|'):
                    topic = topic.strip()
                    topic_counts[topic] = topic_counts.get(topic, 0) + 1
        return sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    def _get_sentiment_distribution(self, df):
        """Get sentiment distribution from dataframe"""
        return df['sentiment'].value_counts().to_dict()

    def _get_quality_metrics(self, df):
        """Get quality metrics from dataframe"""
        if 'collaboration_quality' in df.columns:
            return {
                'collaboration': df['collaboration_quality'].value_counts().to_dict(),
                'task_completion': df['task_completion_status'].value_counts().to_dict() if 'task_completion_status' in df.columns else {},
            }
        return {}
