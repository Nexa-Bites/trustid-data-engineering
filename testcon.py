import psycopg2

DB_URL = "postgresql://postgres.kzlhfmtpmxhbujfengke:Hack#2024@aws-0-eu-central-1.pooler.supabase.com:5432/postgres"

try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print("Connected to:", db_version)

    cur.close()
    conn.close()
    print("Connection closed.")
except Exception as e:
    print("Connection failed:", e)
