import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.dependencies import get_current_user
from app.models.user import User

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(setup_database):
    """Provides a fresh database session for a test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()  # Rollback any uncommitted transactions
        db.close()

@pytest.fixture
def client(db_session):
    """A TestClient with overridden dependencies."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # A mock user for authentication
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
    )
    
    def override_get_current_user():
        return mock_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    with TestClient(app) as c:
        yield c

    # Clear overrides after the test
    app.dependency_overrides.clear()
