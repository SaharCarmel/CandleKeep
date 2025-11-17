"""Database session management for CandleKeep."""

from pathlib import Path
from typing import Optional
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models import Base


def get_db_path() -> Path:
    """Get the database file path.

    Returns:
        Path to SQLite database file
    """
    return Path.home() / ".candlekeep" / "candlekeep.db"


def get_connection_string() -> str:
    """Get SQLite connection string.

    Returns:
        SQLAlchemy connection string for SQLite
    """
    db_path = get_db_path()
    return f"sqlite:///{db_path}"


class DatabaseManager:
    """Manages database connections and sessions."""

    def __init__(self):
        """Initialize database manager with SQLite."""
        self.db_path = get_db_path()
        self.connection_string = get_connection_string()
        self.engine = None
        self.SessionLocal = None

    def connect(self):
        """Create database engine and session factory."""
        # Ensure database directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.engine = create_engine(
            self.connection_string,
            connect_args={"check_same_thread": False},  # For SQLite
            echo=False,  # Set to True for SQL debugging
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    @contextmanager
    def get_session(self):
        """Get a database session with automatic cleanup.

        Yields:
            Session: SQLAlchemy session
        """
        if self.SessionLocal is None:
            raise RuntimeError("Database not connected. Call connect() first.")

        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def close(self):
        """Close database connection."""
        if self.engine:
            self.engine.dispose()


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """Get the global database manager instance.

    Returns:
        DatabaseManager instance

    Raises:
        RuntimeError: If database manager not initialized
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
        _db_manager.connect()
    return _db_manager
