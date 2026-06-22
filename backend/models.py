from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)

    unique_key = Column(String, unique=True)

    created_date = Column(DateTime)
    closed_date = Column(DateTime)

    agency = Column(String)

    complaint_type = Column(String)
    descriptor = Column(String)

    borough = Column(String)

    incident_zip = Column(String)

    status = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)