#!/bin/bash
set -xe
BUCKET="$1"
# install updates & python
apt-get update -y
apt-get install -y python3-pip python3-venv awscli

# create app dir
mkdir -p /opt/myapp
cd /opt/myapp

# pull app files from S3
aws s3 cp s3://$BUCKET/app.py /opt/myapp/app.py || true
aws s3 cp s3://$BUCKET/predict_and_store.py /opt/myapp/predict_and_store.py || true
aws s3 cp s3://$BUCKET/model.pkl /opt/myapp/model.pkl || true
aws s3 cp s3://$BUCKET/requirements.txt /opt/myapp/requirements.txt || true

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
else
  pip install flask boto3 joblib psycopg2-binary scikit-learn gunicorn flask-cors
fi

# create systemd service for the app
cat > /etc/systemd/system/myapp.service <<'SERVICE'
[Unit]
Description=Gunicorn for myapp
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/venv/bin/gunicorn --workers 2 --bind 0.0.0.0:8080 app:app
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable myapp
systemctl start myapp
