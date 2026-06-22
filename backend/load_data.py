import pandas as pd
from database import engine, SessionLocal, Base
from models import Complaint

Base.metadata.create_all(bind=engine)

df = pd.read_csv("../data/311_sample.csv")
df.columns = df.columns.str.strip()
print(df.columns.tolist())

df = df[
    [
        "unique_key",
        "created_date",
        "closed_date",
        "agency",
        "complaint_type",
        "descriptor",
        "borough",
        "incident_zip",
        "status",
        "latitude",
        "longitude",
    ]
]

df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
df["closed_date"] = pd.to_datetime(df["closed_date"], errors="coerce")

df = df.dropna(subset=["unique_key", "created_date", "complaint_type", "borough"])

db = SessionLocal()

for _, row in df.iterrows():
    complaint = Complaint(
        unique_key=str(row["unique_key"]),
        created_date=row["created_date"] if pd.notna(row["created_date"]) else None,
        closed_date=row["closed_date"] if pd.notna(row["closed_date"]) else None,
        agency=row["agency"],
        complaint_type=row["complaint_type"],
        descriptor=row["descriptor"],
        borough=row["borough"],
        incident_zip=str(row["incident_zip"]),
        status=row["status"],
        latitude=float(row["latitude"]) if pd.notna(row["latitude"]) else None,
        longitude=float(row["longitude"]) if pd.notna(row["longitude"]) else None,
    )

    try:
        db.merge(complaint)
    except Exception as e:
        print("Problem row:")
        print(row)
        raise e


db.commit()
db.close()

print("Data loaded successfully.")