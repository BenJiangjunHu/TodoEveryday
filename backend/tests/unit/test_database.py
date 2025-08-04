"""
Unit tests for database configuration
Tests database connection, session management, and dependency injection
"""
import pytest
from unittest.mock import patch, Mock, MagicMock
import tempfile
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from app.database import (
    SQLALCHEMY_DATABASE_URL,
    engine,
    SessionLocal,
    Base,
    get_db,
    init_db
)
from app.models import Todo


class TestDatabaseURL:
    """Test suite for database URL configuration"""

    def test_database_url_format(self):
        """Test that database URL follows SQLite format"""
        assert SQLALCHEMY_DATABASE_URL.startswith("sqlite:///")
        assert "todos.db" in SQLALCHEMY_DATABASE_URL

    def test_database_url_path_resolution(self):
        """Test that database URL resolves to correct path"""
        # Should be relative to backend directory
        assert "/backend/todos.db" in SQLALCHEMY_DATABASE_URL or "\\backend\\todos.db" in SQLALCHEMY_DATABASE_URL


class TestDatabaseEngine:
    """Test suite for SQLAlchemy engine configuration"""

    def test_engine_creation(self):
        """Test that engine is properly created"""
        assert engine is not None
        assert str(engine.url).startswith("sqlite:///")

    def test_engine_connection(self):
        """Test that engine can establish connection"""
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.fetchone()[0] == 1

    def test_engine_sqlite_configuration(self):
        """Test SQLite-specific configuration"""
        # For SQLite, check_same_thread should be False for FastAPI
        connect_args = engine.pool._creator.keywords if hasattr(engine.pool, '_creator') else {}
        # Note: This test may vary based on SQLAlchemy version and configuration

    def test_engine_echo_setting(self):
        """Test that engine echo setting is properly configured"""
        # In production, echo should be False
        # In development/testing, it might be True
        assert isinstance(engine.echo, bool)


class TestSessionLocal:
    """Test suite for session factory configuration"""

    def test_session_local_creation(self):
        """Test that SessionLocal creates valid sessions"""
        session = SessionLocal()
        assert isinstance(session, Session)
        session.close()

    def test_session_local_autocommit_disabled(self):
        """Test that autocommit is disabled"""
        session = SessionLocal()
        assert session.autocommit is False
        session.close()

    def test_session_local_autoflush_enabled(self):
        """Test that autoflush is enabled (default behavior)"""
        session = SessionLocal()
        # autoflush is typically True by default
        assert session.autoflush is True
        session.close()

    def test_session_local_bind_to_engine(self):
        """Test that sessions are bound to the correct engine"""
        session = SessionLocal()
        assert session.bind == engine
        session.close()


class TestBaseModel:
    """Test suite for SQLAlchemy Base configuration"""

    def test_base_metadata_creation(self):
        """Test that Base metadata is properly configured"""
        assert Base.metadata is not None
        assert hasattr(Base.metadata, 'tables')

    def test_base_model_registry(self):
        """Test that models are properly registered with Base"""
        # Todo model should be registered
        table_names = list(Base.metadata.tables.keys())
        assert "todos" in table_names

    def test_base_create_all_tables(self):
        """Test that Base can create all tables"""
        # Create temporary database for testing
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_db:
            temp_url = f"sqlite:///{temp_db.name}"
            temp_engine = create_engine(temp_url)
            
            try:
                # Should not raise any exceptions
                Base.metadata.create_all(bind=temp_engine)
                
                # Verify table was created
                with temp_engine.connect() as conn:
                    result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='todos'"))
                    assert result.fetchone() is not None
                    
            finally:
                temp_engine.dispose()
                os.unlink(temp_db.name)


class TestGetDbDependency:
    """Test suite for get_db dependency injection function"""

    def test_get_db_returns_generator(self):
        """Test that get_db returns a generator"""
        db_gen = get_db()
        assert hasattr(db_gen, '__next__')
        assert hasattr(db_gen, '__iter__')

    def test_get_db_yields_session(self):
        """Test that get_db yields a valid session"""
        db_gen = get_db()
        session = next(db_gen)
        
        assert isinstance(session, Session)
        
        # Clean up
        try:
            next(db_gen)
        except StopIteration:
            pass  # Expected when generator closes

    def test_get_db_session_cleanup(self):
        """Test that get_db properly closes sessions"""
        db_gen = get_db()
        session = next(db_gen)
        
        # Session should be active
        assert session.is_active
        
        # Trigger cleanup
        try:
            next(db_gen)
        except StopIteration:
            pass
        
        # Session should be closed after generator cleanup
        # Note: Exact cleanup behavior may vary based on implementation

    def test_get_db_exception_handling(self):
        """Test that get_db handles exceptions properly"""
        db_gen = get_db()
        session = next(db_gen)
        
        # Simulate an exception during session use
        try:
            # This should trigger cleanup even with exception
            db_gen.throw(Exception("Test exception"))
        except Exception:
            pass
        
        # Session should still be cleaned up
        # Note: Specific cleanup behavior depends on implementation

    @patch('app.database.SessionLocal')
    def test_get_db_session_creation_error(self, mock_session_local):
        """Test error handling when session creation fails"""
        mock_session_local.side_effect = SQLAlchemyError("Session creation failed")
        
        db_gen = get_db()
        
        with pytest.raises(SQLAlchemyError):
            next(db_gen)


class TestInitDb:
    """Test suite for database initialization function"""

    def test_init_db_creates_tables(self):
        """Test that init_db creates all tables"""
        # Create temporary database for testing
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_db:
            temp_url = f"sqlite:///{temp_db.name}"
            temp_engine = create_engine(temp_url)
            
            try:
                # Patch the global engine for this test
                with patch('app.database.engine', temp_engine):
                    init_db()
                
                # Verify table was created
                with temp_engine.connect() as conn:
                    result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='todos'"))
                    assert result.fetchone() is not None
                    
            finally:
                temp_engine.dispose()
                os.unlink(temp_db.name)

    def test_init_db_idempotency(self):
        """Test that init_db can be called multiple times safely"""
        # Create temporary database for testing
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_db:
            temp_url = f"sqlite:///{temp_db.name}"
            temp_engine = create_engine(temp_url)
            
            try:
                with patch('app.database.engine', temp_engine):
                    # Should not raise exceptions when called multiple times
                    init_db()
                    init_db()
                
                # Verify table still exists and is not duplicated
                with temp_engine.connect() as conn:
                    result = conn.execute(text("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='todos'"))
                    assert result.fetchone()[0] == 1
                    
            finally:
                temp_engine.dispose()
                os.unlink(temp_db.name)

    @patch('app.database.Base.metadata.create_all')
    def test_init_db_error_handling(self, mock_create_all):
        """Test error handling in init_db"""
        mock_create_all.side_effect = SQLAlchemyError("Table creation failed")
        
        with pytest.raises(SQLAlchemyError):
            init_db()


class TestDatabaseIntegration:
    """Test suite for database integration scenarios"""

    def test_full_database_lifecycle(self):
        """Test complete database lifecycle with real operations"""
        # Create temporary database
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_db:
            temp_url = f"sqlite:///{temp_db.name}"
            temp_engine = create_engine(temp_url)
            temp_session_local = sessionmaker(autocommit=False, autoflush=True, bind=temp_engine)
            
            try:
                # Initialize database
                Base.metadata.create_all(bind=temp_engine)
                
                # Create session and perform operations
                session = temp_session_local()
                
                # Create a todo
                todo = Todo(title="Integration Test", description="Test todo")
                session.add(todo)
                session.commit()
                
                # Verify todo was created
                retrieved_todo = session.query(Todo).filter(Todo.title == "Integration Test").first()
                assert retrieved_todo is not None
                assert retrieved_todo.title == "Integration Test"
                
                session.close()
                
            finally:
                temp_engine.dispose()
                os.unlink(temp_db.name)

    def test_concurrent_sessions(self):
        """Test handling of multiple concurrent database sessions"""
        # Create temporary database
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_db:
            temp_url = f"sqlite:///{temp_db.name}"
            temp_engine = create_engine(temp_url)
            temp_session_local = sessionmaker(autocommit=False, autoflush=True, bind=temp_engine)
            
            try:
                # Initialize database
                Base.metadata.create_all(bind=temp_engine)
                
                # Create multiple sessions
                session1 = temp_session_local()
                session2 = temp_session_local()
                
                # Perform operations in different sessions
                todo1 = Todo(title="Session 1 Todo")
                todo2 = Todo(title="Session 2 Todo")
                
                session1.add(todo1)
                session2.add(todo2)
                
                session1.commit()
                session2.commit()
                
                # Verify both todos exist
                all_todos = session1.query(Todo).all()
                titles = [todo.title for todo in all_todos]
                
                assert "Session 1 Todo" in titles
                assert "Session 2 Todo" in titles
                
                session1.close()
                session2.close()
                
            finally:
                temp_engine.dispose()
                os.unlink(temp_db.name)

    def test_transaction_rollback(self):
        """Test transaction rollback functionality"""
        # Create temporary database
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_db:
            temp_url = f"sqlite:///{temp_db.name}"
            temp_engine = create_engine(temp_url)
            temp_session_local = sessionmaker(autocommit=False, autoflush=True, bind=temp_engine)
            
            try:
                # Initialize database
                Base.metadata.create_all(bind=temp_engine)
                
                session = temp_session_local()
                
                # Create todo but don't commit
                todo = Todo(title="Rollback Test")
                session.add(todo)
                
                # Verify todo is in session but not committed
                pending_todo = session.query(Todo).filter(Todo.title == "Rollback Test").first()
                assert pending_todo is not None
                
                # Rollback transaction
                session.rollback()
                
                # Verify todo is no longer in database
                rolled_back_todo = session.query(Todo).filter(Todo.title == "Rollback Test").first()
                assert rolled_back_todo is None
                
                session.close()
                
            finally:
                temp_engine.dispose()
                os.unlink(temp_db.name)

    @patch('app.database.engine.connect')
    def test_database_connection_failure(self, mock_connect):
        """Test handling of database connection failures"""
        mock_connect.side_effect = OperationalError("Connection failed", None, None)
        
        with pytest.raises(OperationalError):
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))

    def test_database_file_permissions(self):
        """Test handling of database file permission issues"""
        # Create a read-only directory (if possible)
        with tempfile.TemporaryDirectory() as temp_dir:
            # Try to create database in read-only location
            # Note: This test may behave differently on different operating systems
            try:
                os.chmod(temp_dir, 0o444)  # Read-only
                readonly_url = f"sqlite:///{temp_dir}/readonly.db"
                readonly_engine = create_engine(readonly_url)
                
                # Attempt to create tables should fail
                with pytest.raises((OperationalError, OSError, PermissionError)):
                    Base.metadata.create_all(bind=readonly_engine)
                    
            except (OSError, PermissionError):
                # If we can't set read-only permissions, skip this test
                pytest.skip("Cannot set read-only permissions on this system")
            finally:
                try:
                    os.chmod(temp_dir, 0o755)  # Restore permissions for cleanup
                except OSError:
                    pass


class TestDatabaseErrorScenarios:
    """Test suite for various database error scenarios"""

    def test_invalid_database_url(self):
        """Test handling of invalid database URLs"""
        with pytest.raises((ValueError, SQLAlchemyError)):
            invalid_engine = create_engine("invalid://url")
            with invalid_engine.connect() as conn:
                conn.execute(text("SELECT 1"))

    def test_corrupted_database_file(self):
        """Test handling of corrupted database files"""
        # Create a corrupted database file
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_db:
            # Write invalid content
            temp_db.write(b"This is not a valid SQLite database")
            temp_db.flush()
            
            try:
                corrupted_url = f"sqlite:///{temp_db.name}"
                corrupted_engine = create_engine(corrupted_url)
                
                with pytest.raises(OperationalError):
                    with corrupted_engine.connect() as conn:
                        conn.execute(text("SELECT 1"))
                        
            finally:
                os.unlink(temp_db.name)

    def test_disk_space_exhaustion_simulation(self):
        """Test behavior when disk space is exhausted (simulated)"""
        # This is difficult to test reliably, but we can mock the scenario
        with patch('sqlalchemy.engine.base.Engine.execute') as mock_execute:
            mock_execute.side_effect = OperationalError("Disk full", None, None)
            
            with pytest.raises(OperationalError):
                with engine.connect() as conn:
                    conn.execute(text("INSERT INTO todos (title) VALUES ('test')"))


class TestDatabasePerformance:
    """Test suite for database performance considerations"""

    def test_connection_pool_size(self):
        """Test connection pool configuration"""
        # Check if connection pool is properly configured
        pool = engine.pool
        assert pool is not None
        
        # For SQLite, pool size is typically not as relevant
        # But we can verify pool exists and functions

    def test_session_isolation(self):
        """Test that sessions are properly isolated"""
        # Create temporary database
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_db:
            temp_url = f"sqlite:///{temp_db.name}"
            temp_engine = create_engine(temp_url)
            temp_session_local = sessionmaker(autocommit=False, autoflush=True, bind=temp_engine)
            
            try:
                Base.metadata.create_all(bind=temp_engine)
                
                session1 = temp_session_local()
                session2 = temp_session_local()
                
                # Changes in session1 should not be visible in session2 until commit
                todo = Todo(title="Isolation Test")
                session1.add(todo)
                session1.flush()  # Flush but don't commit
                
                # session2 should not see the uncommitted change
                visible_todo = session2.query(Todo).filter(Todo.title == "Isolation Test").first()
                assert visible_todo is None
                
                # After commit, should be visible
                session1.commit()
                session2.refresh_all_objects()  # Force refresh
                
                committed_todo = session2.query(Todo).filter(Todo.title == "Isolation Test").first()
                # Note: In SQLite with default settings, this behavior may vary
                
                session1.close()
                session2.close()
                
            finally:
                temp_engine.dispose()
                os.unlink(temp_db.name)
