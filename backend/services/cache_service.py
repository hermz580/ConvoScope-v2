"""Cache service for storing analysis results"""
import json
import hashlib
from pathlib import Path
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class CacheService:
    """Service for caching analysis results"""

    def __init__(self, cache_dir: Path):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def get(self, file_hash: str) -> Optional[Dict]:
        """Get cached analysis results"""
        cache_file = self.cache_dir / f"{file_hash}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    logger.info(f"Cache hit for {file_hash}")
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error reading cache: {e}")
                return None
        logger.info(f"Cache miss for {file_hash}")
        return None

    def set(self, file_hash: str, results: Dict):
        """Cache analysis results"""
        cache_file = self.cache_dir / f"{file_hash}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(results, f)
            logger.info(f"Cached results for {file_hash}")
        except Exception as e:
            logger.error(f"Error writing cache: {e}")

    def delete(self, file_hash: str):
        """Delete cached results"""
        cache_file = self.cache_dir / f"{file_hash}.json"
        if cache_file.exists():
            cache_file.unlink()
            logger.info(f"Deleted cache for {file_hash}")

    def clear_all(self):
        """Clear all cached data"""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
        logger.info("Cleared all cache")

    def get_size(self) -> int:
        """Get total cache size in bytes"""
        return sum(f.stat().st_size for f in self.cache_dir.glob("*.json"))

    @staticmethod
    def calculate_file_hash(file_path: Path) -> str:
        """Calculate SHA-256 hash of file"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
