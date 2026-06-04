from db import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP,
    city VARCHAR(100),
    temperature FLOAT,
    humidity FLOAT,
    condition VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()

cur.close()
conn.close()

print("✅ weather_data table created")