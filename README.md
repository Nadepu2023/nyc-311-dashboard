# NYC 311 Complaints Dashboard

A full-stack web dashboard for exploring NYC 311 service request data. Built with a FastAPI backend, SQLite database, and a vanilla JavaScript frontend using Chart.js.

## Features

- **Summary stats** — total complaints, average response time, top agency
- **Interactive charts** — top agencies (bar), top complaint types (horizontal bar), complaints by borough (pie)
- **Search & filter** — filter complaints by borough, complaint type, and agency with results displayed in a table
- **Raw SQL** — see `backend/queries.sql` for the SQL queries behind each API endpoint

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy, SQLite
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **Data:** [NYC Open Data — 311 Service Requests](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9)

## Project Structure

```
nyc-311-dashboard/
├── backend/
│   ├── main.py          # FastAPI routes
│   ├── models.py        # SQLAlchemy models
│   ├── database.py      # Database connection
│   ├── load_data.py     # CSV → SQLite loader
│   └── queries.sql      # Raw SQL for each endpoint
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
└── data/
    └── 311_sample.csv
```

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/nyc-311-dashboard.git
cd nyc-311-dashboard
```

**2. Set up the backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Load the data**
```bash
python load_data.py
```

**4. Start the API server**
```bash
uvicorn main:app --reload
```

**5. Open the frontend**

Open `frontend/index.html` in your browser. The dashboard will load data from the API at `http://127.0.0.1:8000`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/summary` | Total complaint count |
| GET | `/api/top-complaints` | Top 10 complaint types |
| GET | `/api/complaints-by-borough` | Complaint counts by borough |
| GET | `/api/top-agencies` | Top 10 agencies by complaint volume |
| GET | `/api/average-response-time` | Average time to close a complaint |
| GET | `/api/top-zipcodes` | Top 10 zip codes by complaint volume |
| GET | `/api/complaints-over-time` | Complaint counts grouped by month |
| GET | `/api/search` | Filter complaints by borough, complaint type, and/or agency |
