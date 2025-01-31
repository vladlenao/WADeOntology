from sqlalchemy import Column, Integer, String, TIMESTAMP
from ..database.connection import Base

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    revoked_at = Column(TIMESTAMP, nullable=False)