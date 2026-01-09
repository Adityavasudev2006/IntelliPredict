import boto3
import joblib
import psycopg2
import json
from io import BytesIO

# --- AWS and DB Configuration ---
S3_BUCKET = "my-ml-model-bucket-1"
MODEL_KEY = "models/model.pkl"

DB_HOST = "mydb.cb24kyiao58a.eu-north-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "admin_db"
DB_PASS = "adityavasudev"
DB_PORT = "5432"

# --- Step 1: Load model from S3 ---
s3 = boto3.client("s3")
obj = s3.get_object(Bucket=S3_BUCKET, Key=MODEL_KEY)
model = joblib.load(BytesIO(obj["Body"].read()))
print("✅ Model loaded from S3!")

# --- Step 2: Example input (you can change this later) ---
sample_input = {
    "mean_radius": 14.5,
    "mean_texture": 20.2,
    "mean_perimeter": 95.0,
    "mean_area": 600.1,
    "mean_smoothness": 0.1
}

X = [[
    sample_input["mean_radius"],
    sample_input["mean_texture"],
    sample_input["mean_perimeter"],
    sample_input["mean_area"],
    sample_input["mean_smoothness"]
]]

# --- Step 3: Make prediction ---
y_pred = model.predict(X)[0]
print(f"🔮 Prediction (diagnosis): {y_pred}")

# --- Step 4: Store result in PostgreSQL ---
conn = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    port=DB_PORT
)
cur = conn.cursor()

cur.execute("""
    INSERT INTO predictions (input_json, diagnosis)
    VALUES (%s, %s);
""", [json.dumps(sample_input), int(y_pred)])

conn.commit()
cur.close()
conn.close()

print("✅ Prediction saved to database!")
