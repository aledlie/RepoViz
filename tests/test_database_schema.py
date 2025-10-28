"""
Unit tests for the SQLAlchemy database schema and manager.
"""

import pytest
from unittest.mock import patch

from database_schema import DatabaseManager, Repository, CommitSummary, import_commit_data_from_files, Base
from schemas import PeriodType

# Use an in-memory SQLite database for testing
TEST_DB_URL = "sqlite:///:memory:"

@pytest.fixture
def db_manager() -> DatabaseManager:
    """Fixture to create a new in-memory database for each test."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    manager = DatabaseManager(database_url=TEST_DB_URL)
    # For in-memory databases, we need to bypass the directory creation
    manager.engine = create_engine(TEST_DB_URL)
    manager.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=manager.engine)
    Base.metadata.create_all(manager.engine)
    return manager

def test_database_initialization(db_manager):
    """Test that tables are created successfully."""
    session = db_manager.get_session()
    # Check if a query on a table works without error
    assert session.query(Repository).count() == 0
    assert session.query(CommitSummary).count() == 0
    session.close()

def test_get_or_create_repository(db_manager):
    """Test creating and retrieving a repository."""
    # Create a new repository
    repo1 = db_manager.get_or_create_repository("TestRepo1", "http://example.com/repo1")
    assert repo1.name == "TestRepo1"
    assert repo1.id is not None

    # Retrieve the same repository
    repo2 = db_manager.get_or_create_repository("TestRepo1")
    assert repo2.id == repo1.id

    # Check that it's in the database
    session = db_manager.get_session()
    count = session.query(Repository).filter_by(name="TestRepo1").count()
    assert count == 1
    session.close()

def test_add_commit_summary(db_manager):
    """Test adding a commit summary record directly."""
    repo = db_manager.get_or_create_repository("TestRepo")
    session = db_manager.get_session()
    
    summary = CommitSummary(
        repository_id=repo.id,
        period_type=PeriodType.HOUR.value,
        period_value=14,
        commit_count=123
    )
    
    session.add(summary)
    session.commit()
    
    retrieved = session.query(CommitSummary).filter_by(repository_id=repo.id).one()
    assert retrieved.period_value == 14
    assert retrieved.commit_count == 123
    session.close()

@patch("schemas.validate_commit_data_file")
def test_import_commit_data_from_files(mock_validate, db_manager):
    """Test the import function, mocking the file validation."""
    from schemas import CommitCount

    # Mock the return value of the validator
    mock_validate.side_effect = [
        # Hourly data
        [CommitCount(period=8, count=10, period_type=PeriodType.HOUR)],
        # Daily data
        [CommitCount(period=1, count=5, period_type=PeriodType.DAY)],
        # Monthly data
        [CommitCount(period=12, count=20, period_type=PeriodType.MONTH)],
    ]

    # Mock os.path.exists to simulate files being present
    with patch('os.path.exists', return_value=True):
        import_commit_data_from_files(db_manager, "ImportTestRepo")

    # Verify the data was imported correctly
    session = db_manager.get_session()
    
    hour_summary = session.query(CommitSummary).filter_by(period_type='hour').one()
    assert hour_summary.period_value == 8
    assert hour_summary.commit_count == 10
    
    day_summary = session.query(CommitSummary).filter_by(period_type='day').one()
    assert day_summary.period_value == 1
    assert day_summary.commit_count == 5
    
    month_summary = session.query(CommitSummary).filter_by(period_type='month').one()
    assert month_summary.period_value == 12
    assert month_summary.commit_count == 20
    
    assert session.query(CommitSummary).count() == 3
    session.close()

def test_get_commit_statistics(db_manager):
    """Test the statistics retrieval function."""
    repo = db_manager.get_or_create_repository("StatsRepo")
    session = db_manager.get_session()
    
    # Add some summary data
    session.add(CommitSummary(repository_id=repo.id, period_type='hour', period_value=10, commit_count=5))
    session.add(CommitSummary(repository_id=repo.id, period_type='hour', period_value=11, commit_count=15))
    session.add(CommitSummary(repository_id=repo.id, period_type='day', period_value=3, commit_count=20))
    session.commit()
    
    stats = db_manager.get_commit_statistics(repo.id)
    
    assert stats['repository'] == 'StatsRepo'
    # Note: total_commits is based on the Commit table, which we haven't populated, so it will be 0.
    # This is expected behavior for this test.
    assert stats['total_commits'] == 0 
    assert stats['hourly_distribution'] == {10: 5, 11: 15}
    assert stats['daily_distribution'] == {3: 20}
    assert stats['monthly_distribution'] == {}
    
    session.close()
