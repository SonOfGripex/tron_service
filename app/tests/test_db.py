from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.wallet.models import RequestLog, Base

TEST_DB_URL = "sqlite:///./test_tron_service.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def test_db_write():
    db = TestingSessionLocal()
    test_address = "TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy"
    log_entry = RequestLog(address=test_address)
    db.add(log_entry)
    db.commit()

    result = db.query(RequestLog).filter(RequestLog.address == test_address).first()
    assert result is not None
    assert result.address == test_address
