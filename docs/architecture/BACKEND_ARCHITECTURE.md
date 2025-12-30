# ConvoScope Backend Architecture

## Technology Stack

### Core Framework
- **Flask 3.x** - Lightweight Python web framework
- **Flask-CORS** - Cross-Origin Resource Sharing
- **Flask-SocketIO** - WebSocket support
- **python-socketio** - Socket.IO server

### Background Processing
- **Threading** - Built-in Python threading for analysis
- **Queue** - Thread-safe queues for job management

### File Handling
- **Werkzeug** - Secure file uploads
- **hashlib** - File integrity checks

### API
- **RESTful** endpoints for CRUD operations
- **WebSocket** for real-time updates

## Project Structure

```
backend/
├── app.py                  # Main Flask application
├── config.py               # Configuration
├── wsgi.py                 # Production WSGI entry point
│
├── routes/                 # API route handlers
│   ├── __init__.py
│   ├── upload.py           # File upload endpoints
│   ├── analysis.py         # Analysis endpoints
│   ├── export.py           # Export endpoints
│   └── health.py           # Health check endpoints
│
├── services/               # Business logic
│   ├── __init__.py
│   ├── analyzer_service.py # Analysis orchestration
│   ├── websocket_service.py # WebSocket event handlers
│   ├── cache_service.py    # Caching logic
│   └── export_service.py   # Export generation
│
├── models/                 # Data models
│   ├── __init__.py
│   └── analysis_job.py     # Analysis job model
│
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── validators.py       # Input validation
│   ├── file_utils.py       # File operations
│   └── hash_utils.py       # Hashing utilities
│
└── requirements.txt        # Python dependencies
```

## API Endpoints

### Upload Endpoints

**POST /api/upload**
- Upload conversation JSON file
- Validates file format
- Returns file hash and metadata

```python
Request:
  Content-Type: multipart/form-data
  Body: { file: File }

Response:
  {
    "file_id": "abc123",
    "file_hash": "sha256:...",
    "metadata": {
      "size": 15728640,
      "conversations": 847,
      "messages": 12394,
      "date_range": ["2024-01-01", "2024-12-30"]
    }
  }
```

**GET /api/upload/:file_id**
- Get upload metadata
- Check if file exists in cache

### Analysis Endpoints

**POST /api/analysis**
- Start analysis job
- Returns job ID for tracking

```python
Request:
  {
    "file_id": "abc123",
    "options": {
      "enable_privacy": true,
      "enable_quality": true,
      "enable_temporal": true,
      "enable_visualizations": true
    }
  }

Response:
  {
    "job_id": "job_xyz",
    "status": "pending",
    "estimated_duration": 60
  }
```

**GET /api/analysis/:job_id**
- Get analysis status and results

```python
Response:
  {
    "job_id": "job_xyz",
    "status": "complete",  // pending | processing | complete | failed
    "progress": 100,
    "results": {
      "summary": {...},
      "topics": {...},
      "quality": {...},
      "temporal": {...}
    }
  }
```

**DELETE /api/analysis/:job_id**
- Cancel running analysis
- Delete cached results

### Export Endpoints

**POST /api/export**
- Generate export files

```python
Request:
  {
    "job_id": "job_xyz",
    "formats": ["csv", "xlsx", "pdf", "html"],
    "options": {
      "include_pii": false,
      "filter": {...}
    }
  }

Response:
  {
    "export_id": "export_123",
    "files": [
      {
        "format": "csv",
        "url": "/api/export/export_123/file/data.csv",
        "size": 2048576
      }
    ]
  }
```

**GET /api/export/:export_id/file/:filename**
- Download export file

### Health Endpoints

**GET /api/health**
- Health check endpoint

```python
Response:
  {
    "status": "healthy",
    "version": "2.0.0",
    "uptime": 3600
  }
```

## WebSocket Events

### Client → Server

**connect**
- Client connects to WebSocket

**subscribe**
- Subscribe to analysis job updates
```python
{
  "job_id": "job_xyz"
}
```

**unsubscribe**
- Unsubscribe from job updates

### Server → Client

**progress**
- Analysis progress update
```python
{
  "job_id": "job_xyz",
  "progress": 67,
  "current_step": "Analyzing sentiment",
  "message": "Processed 8,234 of 12,394 messages",
  "insights": [
    "Found 13 different topics",
    "Redacted 127 email addresses"
  ]
}
```

**complete**
- Analysis completed
```python
{
  "job_id": "job_xyz",
  "status": "complete",
  "results_url": "/api/analysis/job_xyz"
}
```

**error**
- Analysis failed
```python
{
  "job_id": "job_xyz",
  "error": "Invalid JSON format",
  "details": "..."
}
```

## Service Layer

### Analyzer Service

```python
class AnalyzerService:
    def __init__(self):
        self.job_queue = Queue()
        self.active_jobs = {}
        self.worker_thread = Thread(target=self._process_jobs)
        self.worker_thread.start()

    def start_analysis(self, file_id: str, options: dict) -> str:
        """Start new analysis job"""
        job_id = generate_job_id()
        job = AnalysisJob(job_id, file_id, options)
        self.job_queue.put(job)
        self.active_jobs[job_id] = job
        return job_id

    def _process_jobs(self):
        """Background worker that processes jobs"""
        while True:
            job = self.job_queue.get()
            try:
                self._run_analysis(job)
            except Exception as e:
                self._handle_error(job, e)

    def _run_analysis(self, job: AnalysisJob):
        """Run the actual analysis"""
        from src.advanced_analyzer import AdvancedConversationAnalyzer

        # Load file
        file_path = get_file_path(job.file_id)
        self._emit_progress(job, 10, "Loading data...")

        # Initialize analyzer
        analyzer = AdvancedConversationAnalyzer(
            file_path,
            **job.options
        )

        # Load data
        analyzer.load_data()
        self._emit_progress(job, 30, "Parsing conversations...")

        # Parse conversations with progress tracking
        def progress_callback(current, total):
            progress = 30 + (current / total * 40)
            self._emit_progress(
                job,
                progress,
                f"Analyzed {current:,} of {total:,} messages"
            )

        df = analyzer.parse_conversations_advanced(
            progress_callback=progress_callback
        )

        self._emit_progress(job, 70, "Generating reports...")

        # Generate reports
        outputs = analyzer.generate_comprehensive_report(
            f"results_{job.job_id}"
        )

        self._emit_progress(job, 90, "Finalizing...")

        # Store results
        job.results = self._prepare_results(df, outputs)
        job.status = "complete"

        self._emit_complete(job)

    def _emit_progress(self, job: AnalysisJob, progress: int, message: str):
        """Emit progress update via WebSocket"""
        socketio.emit('progress', {
            'job_id': job.job_id,
            'progress': progress,
            'message': message
        }, room=job.job_id)
```

### WebSocket Service

```python
class WebSocketService:
    def __init__(self, socketio):
        self.socketio = socketio
        self.subscriptions = {}

    def subscribe(self, client_id: str, job_id: str):
        """Subscribe client to job updates"""
        if job_id not in self.subscriptions:
            self.subscriptions[job_id] = set()
        self.subscriptions[job_id].add(client_id)
        join_room(job_id)

    def unsubscribe(self, client_id: str, job_id: str):
        """Unsubscribe client from job updates"""
        if job_id in self.subscriptions:
            self.subscriptions[job_id].discard(client_id)
        leave_room(job_id)

    def emit_to_job(self, job_id: str, event: str, data: dict):
        """Emit event to all subscribers of a job"""
        self.socketio.emit(event, data, room=job_id)
```

### Cache Service

```python
class CacheService:
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def get(self, file_hash: str) -> Optional[dict]:
        """Get cached analysis results"""
        cache_file = self.cache_dir / f"{file_hash}.json"
        if cache_file.exists():
            with open(cache_file) as f:
                return json.load(f)
        return None

    def set(self, file_hash: str, results: dict):
        """Cache analysis results"""
        cache_file = self.cache_dir / f"{file_hash}.json"
        with open(cache_file, 'w') as f:
            json.dump(results, f)

    def clear(self, file_hash: Optional[str] = None):
        """Clear cache"""
        if file_hash:
            (self.cache_dir / f"{file_hash}.json").unlink(missing_ok=True)
        else:
            for file in self.cache_dir.glob("*.json"):
                file.unlink()

    def get_size(self) -> int:
        """Get total cache size in bytes"""
        return sum(f.stat().st_size for f in self.cache_dir.glob("*"))
```

## Configuration

### Development Config
```python
class DevelopmentConfig:
    DEBUG = True
    TESTING = False

    # Flask
    SECRET_KEY = os.urandom(32)

    # CORS
    CORS_ORIGINS = ["http://localhost:3000"]

    # Upload
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    UPLOAD_FOLDER = ".uploads"

    # Cache
    CACHE_FOLDER = ".cache"
    CACHE_MAX_SIZE = 1024 * 1024 * 1024  # 1GB

    # Analysis
    MAX_CONCURRENT_JOBS = 2
    JOB_TIMEOUT = 600  # 10 minutes
```

### Production Config
```python
class ProductionConfig(DevelopmentConfig):
    DEBUG = False

    # Use environment variables
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Stricter settings
    MAX_CONCURRENT_JOBS = 1
    CACHE_MAX_SIZE = 512 * 1024 * 1024  # 512MB
```

## Security Features

### File Upload Validation
```python
ALLOWED_EXTENSIONS = {'json'}

def allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_json_structure(data: dict) -> bool:
    """Validate Claude export JSON structure"""
    return (
        isinstance(data, dict) and
        'conversations' in data and
        isinstance(data['conversations'], list)
    )
```

### File Integrity
```python
def calculate_file_hash(file_path: str) -> str:
    """Calculate SHA-256 hash of file"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
```

### Input Sanitization
```python
def sanitize_filename(filename: str) -> str:
    """Remove dangerous characters from filename"""
    return secure_filename(filename)
```

## Error Handling

### Global Error Handler
```python
@app.errorhandler(Exception)
def handle_error(error):
    """Global error handler"""
    if isinstance(error, ValidationError):
        return jsonify({
            'error': 'Validation error',
            'message': str(error)
        }), 400
    elif isinstance(error, FileNotFoundError):
        return jsonify({
            'error': 'File not found',
            'message': 'The requested file does not exist'
        }), 404
    else:
        logger.exception("Unhandled error")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
```

## Logging

### Logger Configuration
```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    """Configure application logging"""
    handler = RotatingFileHandler(
        'convoscope.log',
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
```

## Testing

### Unit Tests
```python
# tests/test_analyzer_service.py
def test_start_analysis():
    service = AnalyzerService()
    job_id = service.start_analysis("file_123", {})
    assert job_id is not None
    assert job_id in service.active_jobs
```

### Integration Tests
```python
# tests/test_api.py
def test_upload_endpoint(client):
    data = {'file': (io.BytesIO(b'{}'), 'test.json')}
    response = client.post('/api/upload', data=data)
    assert response.status_code == 200
    assert 'file_id' in response.json
```

## Performance Optimizations

### Caching Strategy
- Cache analysis results by file hash
- Incremental cache invalidation
- LRU eviction when cache full

### Background Processing
- Non-blocking analysis execution
- Thread pool for concurrent jobs
- Job queue with priority support

### Resource Management
```python
# Limit concurrent jobs
MAX_CONCURRENT_JOBS = 2

# Job timeout
JOB_TIMEOUT = 600  # 10 minutes

# Auto-cleanup old files
def cleanup_old_files():
    """Remove files older than 24 hours"""
    cutoff = time.time() - 86400
    for file in Path(UPLOAD_FOLDER).glob("*"):
        if file.stat().st_mtime < cutoff:
            file.unlink()
```

## Deployment

### Development Server
```bash
python backend/app.py
```

### Production Server (Gunicorn)
```bash
gunicorn --bind 0.0.0.0:5000 \
         --workers 4 \
         --worker-class eventlet \
         backend.wsgi:app
```

### Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export CACHE_FOLDER=/var/cache/convoscope
export UPLOAD_FOLDER=/var/uploads/convoscope
```

## Monitoring

### Health Checks
```python
@app.route('/api/health')
def health_check():
    return {
        'status': 'healthy',
        'version': VERSION,
        'uptime': time.time() - START_TIME,
        'active_jobs': len(analyzer_service.active_jobs),
        'cache_size': cache_service.get_size()
    }
```

### Metrics
- Request rate
- Error rate
- Average analysis time
- Cache hit rate
- Active WebSocket connections

## Future Enhancements

- [ ] Redis for distributed caching
- [ ] Celery for distributed task queue
- [ ] PostgreSQL for job metadata
- [ ] Rate limiting
- [ ] API authentication (optional)
- [ ] Batch analysis support
- [ ] Incremental analysis (analyze only new conversations)
- [ ] Plugin system for custom analyzers
