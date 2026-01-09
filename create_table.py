import psycopg2

DB_HOST = "mydb.cb24kyiao58a.eu-north-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "admin_db"
DB_PASS = "adityavasudev"
DB_PORT = "5432"

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE predictions (
      id SERIAL PRIMARY KEY,
      input_json JSONB,
      diagnosis INTEGER,
      created_at TIMESTAMPTZ DEFAULT now()
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

    print(" Table 'predictions' created successfully!")

except Exception as e:
    print(" Error:", e)
