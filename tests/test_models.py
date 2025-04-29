from models import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
import pytest

#setting up a test database
@pytest.fixture(scope="module")
def db_session():

    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_url_entry(db_session):
    
    url_entry = URL(original_url="https://example.com", short_code="abc123")
    db_session.add(url_entry)
    db_session.commit()

    result = db_session.query(URL).filter_by(short_code="abc123").first()
    assert result is not None
    assert result.original_url == "https://example.com"

    