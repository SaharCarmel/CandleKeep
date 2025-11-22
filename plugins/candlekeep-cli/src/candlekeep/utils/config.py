"""Configuration management for CandleKeep."""

import os
from pathlib import Path
from typing import Optional, Dict, Any

import yaml


class Config:
    """CandleKeep configuration manager."""

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize configuration manager.

        Args:
            config_dir: Configuration directory (default: ~/.candlekeep)
        """
        self.config_dir = config_dir or Path.home() / ".candlekeep"
        self.config_file = self.config_dir / "config.yaml"
        self.library_dir = self.config_dir / "library"
        self.originals_dir = self.config_dir / "originals"
        self.images_dir = self.config_dir / "images"
        self._config_data: Optional[Dict[str, Any]] = None

    def exists(self) -> bool:
        """Check if configuration file exists.

        Returns:
            True if config file exists
        """
        return self.config_file.exists()

    def load(self) -> Dict[str, Any]:
        """Load configuration from file.

        Returns:
            Configuration dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
        """
        if not self.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_file}\n"
                "Run 'candlekeep init' to create configuration."
            )

        with open(self.config_file, "r") as f:
            self._config_data = yaml.safe_load(f)

        return self._config_data

    def save(self, config_data: Dict[str, Any]):
        """Save configuration to file.

        Args:
            config_data: Configuration dictionary to save
        """
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)

        with open(self.config_file, "w") as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)

        self._config_data = config_data

    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration.

        Returns:
            Database configuration dictionary
        """
        if self._config_data is None:
            self.load()

        return self._config_data.get("database", {})

    def get_connection_string(self) -> str:
        """Get MySQL connection string.

        Returns:
            SQLAlchemy connection string
        """
        db_config = self.get_database_config()

        user = db_config.get("user")
        password = db_config.get("password")
        host = db_config.get("host", "localhost")
        port = db_config.get("port", 3306)
        database = db_config.get("database", "candlekeep")

        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    def create_directories(self):
        """Create all required directories."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.library_dir.mkdir(parents=True, exist_ok=True)
        self.originals_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)

    @property
    def is_initialized(self) -> bool:
        """Check if CandleKeep is initialized.

        Returns:
            True if directories are set up and database exists
        """
        db_path = self.config_dir / "candlekeep.db"
        return (
            self.config_dir.exists()
            and self.library_dir.exists()
            and self.originals_dir.exists()
            and db_path.exists()
        )


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance.

    Returns:
        Config instance
    """
    global _config
    if _config is None:
        _config = Config()
    return _config
