"""
SQLAlchemy database schema for Git Commit Visualization Utilities.

This module provides optional database storage for commit data and
generated chart metadata using SQLAlchemy ORM.
"""

from sqlalchemy import (
    Column, Integer, String, DateTime, Float, Boolean, Text, 
    ForeignKey, UniqueConstraint, Index, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional, Dict, Any
import json
import os

Base = declarative_base()


class Repository(Base):
    """Repository information table."""
    __tablename__ = 'repositories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    remote_url = Column(String(500))
    current_branch = Column(String(100))
    total_commits = Column(Integer, default=0)
    first_commit_date = Column(DateTime)
    last_commit_date = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    commits = relationship("Commit", back_populates="repository", cascade="all, delete-orphan")
    charts = relationship("Chart", back_populates="repository", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Repository(name='{self.name}', commits={self.total_commits})>"


class Commit(Base):
    """Individual commit data table."""
    __tablename__ = 'commits'
    
    id = Column(Integer, primary_key=True)
    repository_id = Column(Integer, ForeignKey('repositories.id'), nullable=False)
    commit_hash = Column(String(40), nullable=False)  # Git SHA-1 hash
    timestamp = Column(DateTime, nullable=False)
    hour = Column(Integer, nullable=False)  # 0-23
    day_of_week = Column(Integer, nullable=False)  # 0-6 (Sunday=0)
    month = Column(Integer, nullable=False)  # 1-12
    year = Column(Integer, nullable=False)
    author_name = Column(String(255), nullable=False)
    author_email = Column(String(255))
    message = Column(Text, nullable=False)
    files_changed = Column(Integer, default=0)
    insertions = Column(Integer, default=0)
    deletions = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    repository = relationship("Repository", back_populates="commits")
    
    # Constraints and indexes
    __table_args__ = (
        UniqueConstraint('repository_id', 'commit_hash', name='uq_repo_commit'),
        Index('idx_commit_timestamp', 'timestamp'),
        Index('idx_commit_hour', 'hour'),
        Index('idx_commit_day', 'day_of_week'),
        Index('idx_commit_month', 'month'),
        Index('idx_commit_author', 'author_name'),
    )
    
    def __repr__(self):
        return f"<Commit(hash='{self.commit_hash[:8]}', author='{self.author_name}')>"


class CommitSummary(Base):
    """Aggregated commit statistics table."""
    __tablename__ = 'commit_summaries'
    
    id = Column(Integer, primary_key=True)
    repository_id = Column(Integer, ForeignKey('repositories.id'), nullable=False)
    period_type = Column(String(10), nullable=False)  # 'hour', 'day', 'month'
    period_value = Column(Integer, nullable=False)  # 0-23, 0-6, 1-12
    commit_count = Column(Integer, nullable=False, default=0)
    total_insertions = Column(Integer, default=0)
    total_deletions = Column(Integer, default=0)
    unique_authors = Column(Integer, default=0)
    first_commit = Column(DateTime)
    last_commit = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    repository = relationship("Repository")
    
    # Constraints and indexes
    __table_args__ = (
        UniqueConstraint('repository_id', 'period_type', 'period_value', 
                        name='uq_repo_period'),
        Index('idx_summary_period', 'period_type', 'period_value'),
    )
    
    def __repr__(self):
        return f"<CommitSummary(type='{self.period_type}', value={self.period_value}, count={self.commit_count})>"


class Chart(Base):
    """Generated chart metadata table."""
    __tablename__ = 'charts'
    
    id = Column(Integer, primary_key=True)
    repository_id = Column(Integer, ForeignKey('repositories.id'), nullable=False)
    chart_type = Column(String(50), nullable=False)  # 'hour_bar', 'day_pie', etc.
    title = Column(String(500), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(1000), nullable=False)
    file_size = Column(Integer)  # File size in bytes
    dpi = Column(Integer, default=300)
    width = Column(Integer)  # Image width in pixels
    height = Column(Integer)  # Image height in pixels
    color_primary = Column(String(7))  # Hex color
    color_secondary = Column(String(7))  # Hex color
    data_period_start = Column(DateTime)  # Start of data range
    data_period_end = Column(DateTime)  # End of data range
    total_commits_shown = Column(Integer, default=0)
    configuration = Column(Text)  # JSON configuration used
    schema_org_data = Column(Text)  # JSON-LD schema.org data
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    repository = relationship("Repository", back_populates="charts")
    
    # Indexes
    __table_args__ = (
        Index('idx_chart_type', 'chart_type'),
        Index('idx_chart_created', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Chart(type='{self.chart_type}', title='{self.title}')>"
    
    def get_configuration(self) -> Dict[str, Any]:
        """Get configuration as dictionary."""
        if self.configuration:
            return json.loads(self.configuration)
        return {}
    
    def set_configuration(self, config: Dict[str, Any]) -> None:
        """Set configuration from dictionary."""
        self.configuration = json.dumps(config, indent=2)
    
    def get_schema_org_data(self) -> Dict[str, Any]:
        """Get schema.org data as dictionary."""
        if self.schema_org_data:
            return json.loads(self.schema_org_data)
        return {}
    
    def set_schema_org_data(self, schema_data: Dict[str, Any]) -> None:
        """Set schema.org data from dictionary."""
        self.schema_org_data = json.dumps(schema_data, indent=2)


class DataFile(Base):
    """Data file metadata table."""
    __tablename__ = 'data_files'
    
    id = Column(Integer, primary_key=True)
    repository_id = Column(Integer, ForeignKey('repositories.id'), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(1000), nullable=False)
    file_type = Column(String(20), nullable=False)  # 'logs', 'hour_counts', etc.
    format = Column(String(10), default='txt')  # 'txt', 'csv', 'json'
    file_size = Column(Integer)
    record_count = Column(Integer, default=0)
    last_modified = Column(DateTime)
    checksum = Column(String(64))  # SHA-256 checksum
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    repository = relationship("Repository")
    
    # Constraints and indexes
    __table_args__ = (
        UniqueConstraint('repository_id', 'file_type', name='uq_repo_file_type'),
        Index('idx_file_type', 'file_type'),
    )
    
    def __repr__(self):
        return f"<DataFile(type='{self.file_type}', records={self.record_count})>"


# Database management functions
class DatabaseManager:
    """Database management utilities."""
    
    def __init__(self, database_url: str = "sqlite:///./Generated Data/git_viz.db"):
        """Initialize database manager."""
        self.database_url = database_url
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self) -> None:
        """Create all database tables."""
        # Ensure directory exists for SQLite
        if self.database_url.startswith('sqlite:'):
            db_path = self.database_url.replace('sqlite:///', '')
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Get database session."""
        return self.SessionLocal()
    
    def get_or_create_repository(self, name: str, remote_url: Optional[str] = None) -> Repository:
        """Get existing repository or create new one."""
        session = self.get_session()
        try:
            repo = session.query(Repository).filter(Repository.name == name).first()
            if not repo:
                repo = Repository(name=name, remote_url=remote_url)
                session.add(repo)
                session.commit()
                session.refresh(repo)
            return repo
        finally:
            session.close()
    
    def add_commit(self, repo_id: int, commit_data: Dict[str, Any]) -> Commit:
        """Add commit to database."""
        session = self.get_session()
        try:
            # Check if commit already exists
            existing = session.query(Commit).filter(
                Commit.repository_id == repo_id,
                Commit.commit_hash == commit_data['commit_hash']
            ).first()
            
            if existing:
                return existing
            
            commit = Commit(
                repository_id=repo_id,
                commit_hash=commit_data['commit_hash'],
                timestamp=commit_data['timestamp'],
                hour=commit_data['timestamp'].hour,
                day_of_week=commit_data['timestamp'].weekday(),
                month=commit_data['timestamp'].month,
                year=commit_data['timestamp'].year,
                author_name=commit_data['author_name'],
                author_email=commit_data.get('author_email'),
                message=commit_data['message'],
                files_changed=commit_data.get('files_changed', 0),
                insertions=commit_data.get('insertions', 0),
                deletions=commit_data.get('deletions', 0)
            )
            
            session.add(commit)
            session.commit()
            session.refresh(commit)
            return commit
        finally:
            session.close()
    
    def update_commit_summaries(self, repo_id: int) -> None:
        """Update aggregated commit summaries."""
        session = self.get_session()
        try:
            # Clear existing summaries
            session.query(CommitSummary).filter(
                CommitSummary.repository_id == repo_id
            ).delete()
            
            # Generate hourly summaries
            for hour in range(24):
                commits = session.query(Commit).filter(
                    Commit.repository_id == repo_id,
                    Commit.hour == hour
                ).all()
                
                if commits:
                    summary = CommitSummary(
                        repository_id=repo_id,
                        period_type='hour',
                        period_value=hour,
                        commit_count=len(commits),
                        total_insertions=sum(c.insertions for c in commits),
                        total_deletions=sum(c.deletions for c in commits),
                        unique_authors=len(set(c.author_name for c in commits)),
                        first_commit=min(c.timestamp for c in commits),
                        last_commit=max(c.timestamp for c in commits)
                    )
                    session.add(summary)
            
            # Generate daily summaries
            for day in range(7):
                commits = session.query(Commit).filter(
                    Commit.repository_id == repo_id,
                    Commit.day_of_week == day
                ).all()
                
                if commits:
                    summary = CommitSummary(
                        repository_id=repo_id,
                        period_type='day',
                        period_value=day,
                        commit_count=len(commits),
                        total_insertions=sum(c.insertions for c in commits),
                        total_deletions=sum(c.deletions for c in commits),
                        unique_authors=len(set(c.author_name for c in commits)),
                        first_commit=min(c.timestamp for c in commits),
                        last_commit=max(c.timestamp for c in commits)
                    )
                    session.add(summary)
            
            # Generate monthly summaries
            for month in range(1, 13):
                commits = session.query(Commit).filter(
                    Commit.repository_id == repo_id,
                    Commit.month == month
                ).all()
                
                if commits:
                    summary = CommitSummary(
                        repository_id=repo_id,
                        period_type='month',
                        period_value=month,
                        commit_count=len(commits),
                        total_insertions=sum(c.insertions for c in commits),
                        total_deletions=sum(c.deletions for c in commits),
                        unique_authors=len(set(c.author_name for c in commits)),
                        first_commit=min(c.timestamp for c in commits),
                        last_commit=max(c.timestamp for c in commits)
                    )
                    session.add(summary)
            
            session.commit()
        finally:
            session.close()
    
    def add_chart(self, repo_id: int, chart_data: Dict[str, Any]) -> Chart:
        """Add chart metadata to database."""
        session = self.get_session()
        try:
            chart = Chart(
                repository_id=repo_id,
                chart_type=chart_data['chart_type'],
                title=chart_data['title'],
                filename=chart_data['filename'],
                file_path=chart_data['file_path'],
                file_size=chart_data.get('file_size'),
                dpi=chart_data.get('dpi', 300),
                width=chart_data.get('width'),
                height=chart_data.get('height'),
                color_primary=chart_data.get('color_primary'),
                color_secondary=chart_data.get('color_secondary'),
                data_period_start=chart_data.get('data_period_start'),
                data_period_end=chart_data.get('data_period_end'),
                total_commits_shown=chart_data.get('total_commits_shown', 0)
            )
            
            if 'configuration' in chart_data:
                chart.set_configuration(chart_data['configuration'])
            
            if 'schema_org_data' in chart_data:
                chart.set_schema_org_data(chart_data['schema_org_data'])
            
            session.add(chart)
            session.commit()
            session.refresh(chart)
            return chart
        finally:
            session.close()
    
    def get_commit_statistics(self, repo_id: int) -> Dict[str, Any]:
        """Get comprehensive commit statistics."""
        session = self.get_session()
        try:
            repo = session.query(Repository).get(repo_id)
            if not repo:
                return {}
            
            total_commits = session.query(Commit).filter(
                Commit.repository_id == repo_id
            ).count()
            
            # Get summaries
            hour_summaries = session.query(CommitSummary).filter(
                CommitSummary.repository_id == repo_id,
                CommitSummary.period_type == 'hour'
            ).all()
            
            day_summaries = session.query(CommitSummary).filter(
                CommitSummary.repository_id == repo_id,
                CommitSummary.period_type == 'day'
            ).all()
            
            month_summaries = session.query(CommitSummary).filter(
                CommitSummary.repository_id == repo_id,
                CommitSummary.period_type == 'month'
            ).all()
            
            return {
                'repository': repo.name,
                'total_commits': total_commits,
                'hourly_distribution': {s.period_value: s.commit_count for s in hour_summaries},
                'daily_distribution': {s.period_value: s.commit_count for s in day_summaries},
                'monthly_distribution': {s.period_value: s.commit_count for s in month_summaries},
                'date_range': {
                    'start': repo.first_commit_date,
                    'end': repo.last_commit_date
                }
            }
        finally:
            session.close()


# Example usage and utility functions
def initialize_database(database_url: str = "sqlite:///./Generated Data/git_viz.db") -> DatabaseManager:
    """Initialize database with all tables."""
    db_manager = DatabaseManager(database_url)
    db_manager.create_tables()
    return db_manager


def import_commit_data_from_files(db_manager: DatabaseManager, repo_name: str) -> None:
    """Import and update commit summary data from existing text files."""
    from schemas import validate_commit_data_file, PeriodType
    
    repo = db_manager.get_or_create_repository(repo_name)
    session = db_manager.get_session()

    def _update_summaries_from_file(file_path: str, period_type: PeriodType):
        """Helper to process a single data file and update summaries."""
        try:
            commit_data = validate_commit_data_file(file_path)
            print(f"Found {len(commit_data)} records in {os.path.basename(file_path)}")
            
            for item in commit_data:
                # Find existing summary or create a new one
                summary = session.query(CommitSummary).filter_by(
                    repository_id=repo.id,
                    period_type=period_type.value,
                    period_value=item.period
                ).first()
                
                if not summary:
                    summary = CommitSummary(
                        repository_id=repo.id,
                        period_type=period_type.value,
                        period_value=item.period
                    )
                
                # Update data and add to session
                summary.commit_count = item.count
                session.add(summary)
                
        except FileNotFoundError:
            print(f"Warning: Data file not found: {file_path}")
        except ValueError as e:
            print(f"Error validating {file_path}: {e}")

    try:
        # Process all data files
        _update_summaries_from_file("./commit_counts.txt", PeriodType.HOUR)
        _update_summaries_from_file("./commit_counts_day.txt", PeriodType.DAY)
        _update_summaries_from_file("./commit_counts_month.txt", PeriodType.MONTH)
        
        # Commit all changes
        session.commit()
        print(f"Successfully imported and updated summaries for repository: {repo_name}")
        
    except Exception as e:
        session.rollback()
        print(f"An error occurred during import: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    # Example usage
    print("Initializing database...")
    db_manager = initialize_database()
    print("Database initialized successfully!")
    
    # Define a repository name (replace with dynamic detection if needed)
    repo_name = "RepoViz"
    print(f"\nImporting data for repository: {repo_name}")
    
    # Run the import process
    import_commit_data_from_files(db_manager, repo_name)
    
    # Verify by getting statistics
    repo = db_manager.get_or_create_repository(repo_name)
    stats = db_manager.get_commit_statistics(repo.id)
    print("\n--- Verification ---")
    print(f"Statistics for {repo.name}:")
    print(f"  Total Commits (from summaries): {sum(stats.get('hourly_distribution', {}).values())}")
    print(f"  Hourly data points: {len(stats.get('hourly_distribution', {}))}")
    print(f"  Daily data points: {len(stats.get('daily_distribution', {}))}")
    print(f"  Monthly data points: {len(stats.get('monthly_distribution', {}))}")
    print("--------------------")

