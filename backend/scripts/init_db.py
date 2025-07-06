#!/usr/bin/env python3
"""
Database initialization script for HTML Page Generator.

This script initializes the database by running Alembic migrations.
It can be used for initial setup or to upgrade to the latest schema.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.config import settings
from app.core.logging import get_logger, setup_logging

# Setup logging
setup_logging()
logger = get_logger(__name__)


def run_alembic_command(command: list[str]) -> bool:
    """Run an alembic command and return success status"""
    try:
        logger.info(f"Running: alembic {' '.join(command)}")
        result = subprocess.run(
            ["alembic"] + command,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        logger.info(f"Command output: {result.stdout}")
        if result.stderr:
            logger.warning(f"Command stderr: {result.stderr}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Alembic command failed: {e}")
        logger.error(f"stdout: {e.stdout}")
        logger.error(f"stderr: {e.stderr}")
        return False


def check_database_exists() -> bool:
    """Check if database file exists"""
    if "sqlite" in settings.DATABASE_URL:
        # Extract path from sqlite URL
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        if not db_path.startswith("/"):
            db_path = project_root / db_path
        else:
            db_path = Path(db_path)
        
        logger.info(f"Checking SQLite database at: {db_path}")
        return db_path.exists()
    else:
        # For PostgreSQL/MySQL, we assume the database server exists
        # Real check would require connecting to the database
        logger.info("Non-SQLite database detected, assuming it exists")
        return True


def init_database():
    """Initialize the database"""
    logger.info("Starting database initialization...")
    logger.info(f"Database URL: {settings.DATABASE_URL}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    # Check if this is a fresh install
    db_exists = check_database_exists()
    
    if not db_exists:
        logger.info("Database doesn't exist, creating new database...")
    else:
        logger.info("Database exists, checking for pending migrations...")
    
    # Get current database revision
    current_revision = None
    try:
        result = subprocess.run(
            ["alembic", "current"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        # Parse the output to get revision ID
        for line in result.stdout.strip().split('\n'):
            if line and not line.startswith('INFO'):
                current_revision = line.split()[0] if line.split() else None
                break
    except subprocess.CalledProcessError:
        logger.info("No current revision found (fresh database)")
    
    logger.info(f"Current database revision: {current_revision or 'None'}")
    
    # Run migrations
    if not run_alembic_command(["upgrade", "head"]):
        logger.error("Failed to run database migrations")
        return False
    
    logger.info("Database initialization completed successfully!")
    return True


def main():
    """Main function"""
    print("HTML Page Generator - Database Initialization")
    print("=" * 50)
    
    try:
        success = init_database()
        if success:
            print("\n✅ Database initialization successful!")
            sys.exit(0)
        else:
            print("\n❌ Database initialization failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Database initialization cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {e}")
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
