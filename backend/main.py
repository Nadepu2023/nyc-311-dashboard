from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, text

from database import SessionLocal, engine, Base
from models import Complaint

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NYC 311 Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "NYC 311 Dashboard API is running"}


@app.get("/api/summary")
def summary(db: Session = Depends(get_db)):
    total = db.query(Complaint).count()
    return {"total_complaints": total}


@app.get("/api/top-complaints")
def top_complaints(db: Session = Depends(get_db)):
    results = (
        db.query(Complaint.complaint_type, func.count(Complaint.id))
        .group_by(Complaint.complaint_type)
        .order_by(func.count(Complaint.id).desc())
        .limit(10)
        .all()
    )

    return [
        {"complaint_type": r[0], "count": r[1]}
        for r in results
    ]


@app.get("/api/complaints-by-borough")
def complaints_by_borough(db: Session = Depends(get_db)):
    results = (
        db.query(Complaint.borough, func.count(Complaint.id))
        .group_by(Complaint.borough)
        .order_by(func.count(Complaint.id).desc())
        .all()
    )

    return [
        {"borough": r[0], "count": r[1]}
        for r in results
    ]

@app.get("/api/borough/{borough_name}")
def complaints_for_borough(
    borough_name: str,
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            Complaint.complaint_type,
            func.count(Complaint.id)
        )
        .filter(
            Complaint.borough == borough_name.upper()
        )
        .group_by(Complaint.complaint_type)
        .order_by(func.count(Complaint.id).desc())
        .limit(10)
        .all()
    )

    return [
        {
            "complaint_type": r[0],
            "count": r[1]
        }
        for r in results
    ]

@app.get("/api/average-response-time")
def average_response_time(db: Session = Depends(get_db)):
    complaints = (
        db.query(Complaint)
        .filter(Complaint.closed_date != None)
        .filter(Complaint.created_date != None)
        .all()
    )

    total_seconds = 0
    count = 0

    for complaint in complaints:
        time_difference = complaint.closed_date - complaint.created_date
        total_seconds += time_difference.total_seconds()
        count += 1

    if count == 0:
        return {"average_response_time_hours": None, "closed_complaints_count": 0}

    average_seconds = total_seconds / count
    average_hours = average_seconds / 3600

    return {
        "average_response_time_hours": round(average_hours, 2),
        "closed_complaints_count": count
    }

@app.get("/api/top-agencies")
def top_agencies(db: Session = Depends(get_db)):
    results = (
        db.query(Complaint.agency, func.count(Complaint.id))
        .group_by(Complaint.agency)
        .order_by(func.count(Complaint.id).desc())
        .limit(10)
        .all()
    )

    return [
        {"agency": r[0], "count": r[1]}
        for r in results
    ]

@app.get("/api/top-zipcodes")
def top_zipcodes(db: Session = Depends(get_db)):
    results = (
        db.query(Complaint.incident_zip, func.count(Complaint.id))
        .filter(Complaint.incident_zip != None)
        .group_by(Complaint.incident_zip)
        .order_by(func.count(Complaint.id).desc())
        .limit(10)
        .all()
    )

    return [
        {"zipcode": r[0], "count": r[1]}
        for r in results
    ]

@app.get("/api/search")
def search_complaints(
    borough: str = None,
    complaint_type: str = None,
    agency: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Complaint)

    if borough:
        query = query.filter(Complaint.borough == borough.upper())

    if complaint_type:
        query = query.filter(Complaint.complaint_type == complaint_type)

    if agency:
        query = query.filter(Complaint.agency == agency)

    results = query.limit(50).all()

    return [
        {
            "unique_key": complaint.unique_key,
            "borough": complaint.borough,
            "complaint_type": complaint.complaint_type,
            "agency": complaint.agency,
            "status": complaint.status,
        }
        for complaint in results
    ]

