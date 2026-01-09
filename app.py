from flask import Flask, request, jsonify
import boto3
import joblib
import psycopg2
import json
import os
from io import BytesIO

app = Flask(__name__)

# --- Config from Environment Variables ---
S3_BUCKET = os.getenv("S3_BUCKET")
S3_KEY = os.getenv("S3_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT", "5432")
LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH", "/opt/models/model.pkl")

# --- Load Model (from S3 or Local) ---
def load_model():
    if os.path.exists(LOCAL_MODEL_PATH):
        return joblib.load(LOCAL_MODEL_PATH)
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
    model = joblib.load(BytesIO(obj["Body"].read()))
    return model

model = load_model()
print("✅ Model loaded successfully")

# --- DB Connection Helper ---
def get_db_conn():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

# --- Routes ---
@app.route("/")
def home():
    return jsonify({"message": "Breast Cancer Predictor API is running!"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    try:
        X = [[
            data["mean_radius"],
            data["mean_texture"],
            data["mean_perimeter"],
            data["mean_area"],
            data["mean_smoothness"]
        ]]

        y_pred = model.predict(X)[0]

        # Save to DB
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO predictions (input_json, diagnosis) VALUES (%s, %s);",
            [json.dumps(data), int(y_pred)]
        )
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "prediction": int(y_pred),
            "message": "✅ Prediction saved to database"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
