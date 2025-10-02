"""
Configuration management with dependency injection pattern.
Replaces global state with proper singleton and context management.
"""
from typing import Optional, Dict, Any
import os
import json
from pathlib import Path
from threading import Lock


class ConfigManager:
    """
    Thread-safe configuration manager that replaces global state.

    Usage:
        config = ConfigManager.get_instance()
        value = config.get('KEY_NAME', default='default_value')
    """

    _instance: Optional['ConfigManager'] = None
    _lock: Lock = Lock()

    def __init__(self):
        """Initialize config manager. Use get_instance() instead."""
        self._cache: Dict[str, Any] = {}
        self._env_cache: Dict[str, str] = {}
        self._loaded = False

    @classmethod
    def get_instance(cls) -> 'ConfigManager':
        """Get singleton instance of ConfigManager."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset singleton (useful for testing)."""
        with cls._lock:
            cls._instance = None

    def _load_from_file(self, filepath: str) -> Optional[Dict[str, Any]]:
        """Load configuration from a JSON file."""
        try:
            if not os.path.isfile(filepath):
                return None
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
        except Exception:
            pass
        return None

    def _load_global_config(self) -> Dict[str, Any]:
        """Load global configuration from standard paths."""
        search_paths = [
            "/mt/web/data/configs.json",
            "/mt/web/configs/configs.json",
            "/tmp/farbox_bucket_configs.json",
        ]

        for path in search_paths:
            data = self._load_from_file(path)
            if data:
                return data

        return {}

    def _get_from_env(self, key: str) -> Optional[str]:
        """Get value from environment variables or config files."""
        # Check cache first
        if key in self._env_cache:
            return self._env_cache[key]

        # Check environment variables
        for variant in [key, key.lower(), key.upper()]:
            value = os.environ.get(variant)
            if value:
                self._env_cache[key] = value
                return value

        # Check config files
        filenames = [key, f'{key}.json', f'{key}.txt', key.lower(), f'{key.lower()}.txt']
        search_dirs = ['/tmp/env', '/env', '/mt/web/configs']

        for directory in search_dirs:
            for filename in filenames:
                filepath = os.path.join(directory, filename)
                try:
                    if os.path.isfile(filepath) and os.path.getsize(filepath) < 10 * 1024:
                        with open(filepath, 'rb') as f:
                            content = f.read().decode('utf-8').strip()
                        if content:
                            self._env_cache[key] = content
                            # Cache in environment for compatibility
                            os.environ[key] = content
                            return content
                except Exception:
                    continue

        return None

    def load(self) -> None:
        """Load all configuration sources."""
        if self._loaded:
            return

        # Load global config
        self._cache = self._load_global_config()
        self._loaded = True

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        if not self._loaded:
            self.load()

        # Check cache first
        lower_key = key.lower()
        if lower_key in self._cache:
            value = self._cache.get(lower_key)
            if value is not None and value != "":
                return value

        # Try environment
        env_value = self._get_from_env(key)
        if env_value:
            return env_value

        return default

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.

        Args:
            key: Configuration key
            value: Value to set
        """
        self._cache[key.lower()] = value

    def reload(self) -> None:
        """Reload configuration from sources."""
        self._loaded = False
        self._cache.clear()
        self._env_cache.clear()
        self.load()


# Singleton instance for backward compatibility
_default_config = ConfigManager.get_instance()


def get_config(key: str, default: Any = None) -> Any:
    """
    Get configuration value (backward compatible function).

    Args:
        key: Configuration key
        default: Default value if not found

    Returns:
        Configuration value
    """
    return _default_config.get(key, default)


def get_env(key: str) -> Optional[str]:
    """
    Get environment variable (backward compatible function).

    Args:
        key: Environment variable key

    Returns:
        Environment variable value or None
    """
    return _default_config.get(key)
