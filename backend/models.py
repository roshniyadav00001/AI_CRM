


from sqlalchemy import Column, Integer, String, Text

from database import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(255))
    hospital = Column(String(255))
    notes = Column(Text)
    summary = Column(Text)
    sentiment = Column(String(50))