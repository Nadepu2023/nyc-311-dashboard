-- Total complaints
SELECT COUNT(*) FROM complaints;

-- Top complaint types
SELECT complaint_type, COUNT(*) as count
FROM complaints
GROUP BY complaint_type
ORDER BY count DESC
LIMIT 10;

-- Complaints by borough
SELECT borough, COUNT(*) as count
FROM complaints
GROUP BY borough
ORDER BY count DESC
LIMIT 10;

-- Response time avg
SELECT AVG((julianday(closed_date) - julianday(created_date)) * 24) as average_response_time_hours
FROM complaints
WHERE closed_date IS NOT NULL AND created_date IS NOT NULL;

-- Complaints over time
SELECT strftime('%Y-%m', created_date) as month, COUNT(*) as count
FROM complaints
WHERE created_date IS NOT NULL
GROUP BY month
ORDER BY month;

-- Top agencies
SELECT agency, COUNT(*) as count
FROM complaints
GROUP BY agency
ORDER BY count DESC
LIMIT 10;

-- Top zipcodes
SELECT incident_zip, COUNT(*) as count
FROM complaints
GROUP BY incident_zip
ORDER BY count DESC
LIMIT 10;

-- Search complaints
SELECT unique_key, borough, complaint_type, agency, status
FROM complaints
WHERE borough = 'QUEENS' AND complaint_type = 'Noise' AND agency = 'NYPD'
LIMIT 50;



