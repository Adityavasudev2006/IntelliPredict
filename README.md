# 🩺 IntelliPredict: Cloud-Native Multi-Cancer Prediction Pipeline

[![AWS](https://img.shields.io/badge/AWS-Cloud%20Native-232F3E?logo=amazon-aws&style=flat-square)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&style=flat-square)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-REST%20API-000000?logo=flask&style=flat-square)](https://flask.palletsprojects.com/)
[![Infrastructure as Code](https://img.shields.io/badge/IaC-CloudFormation-FF9900?logo=amazonaws&style=flat-square)](https://aws.amazon.com/cloudformation/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **A robust, scalable, and automated Machine Learning inference pipeline deployed on AWS. IntelliPredict detects multiple cancer types (Lung, Breast, Colorectal, Skin) using a secure, high-availability architecture.**

---

## 🚀 Project Overview

**IntelliPredict** is an end-to-end Machine Learning web application designed to bridge the gap between model training and production deployment.

Unlike simple local scripts, this project demonstrates a **production-grade cloud architecture**. It leverages AWS services to ensure the application is scalable (Auto Scaling), resilient (Multi-AZ RDS), and automated (CloudFormation & CI/CD).

### 🎯 Key Objectives

- **Multi-Disease Detection:** Predictive capabilities for Lung, Breast, Colorectal, and Skin cancer.
- **Scalability:** Handles fluctuating traffic loads using EC2 Auto Scaling Groups.
- **Automation:** "One-Click Deployment" utilizing AWS CloudFormation (IaC).
- **Security:** Implements HTTPS via NGINX/Certbot and strict IAM roles/Security Groups.

---

## 🏗️ System Architecture (Cloud Architecture)

The system follows a 3-tier web architecture (Presentation, Logic, Data) fully hosted on the AWS Cloud.

![System Architecture](images/Cloud%20Architecture.png)

### 🔄 The Workflow

1.  **User Access:** Users access the secure web UI via HTTPS (NGINX Reverse Proxy).
2.  **Compute Layer (EC2):** A Flask REST API receives the request.
    - _Bootstrapping:_ EC2 instances use `User Data Scripts` to install dependencies and fetch the latest code/model from **S3**.
3.  **Inference:** The ML model (`model.pkl`) predicts the outcome based on user input.
4.  **Data Persistence (RDS):** Prediction results and user logs are securely stored in a managed **PostgreSQL/MySQL** database.
5.  **Monitoring (CloudWatch):** System metrics and application logs are tracked in real-time.
6.  **Alerting (SNS/Lambda):** If high load or critical errors occur, SNS triggers immediate alerts (Email/SMS).

---

## 🛠️ Tech Stack & Services

### ☁️ AWS Cloud Infrastructure

| Service                | Usage in Project                                                                                  |
| :--------------------- | :------------------------------------------------------------------------------------------------ |
| **CloudFormation**     | **Infrastructure as Code (IaC)** to provision the entire stack (VPC, EC2, RDS, S3) automatically. |
| **EC2 & Auto Scaling** | Compute resources that scale horizontally based on CPU utilization.                               |
| **S3**                 | Centralized object storage for model artifacts (`model.pkl`), static assets, and logs.            |
| **RDS**                | Managed Relational Database for persistent data storage with automated backups.                   |
| **CloudWatch**         | Real-time monitoring of CPU, RAM, and application logs.                                           |
| **SNS**                | Simple Notification Service for critical system alerts.                                           |
| **IAM**                | Granular permission management for secure service-to-service communication.                       |

### 💻 Backend & DevOps

- **Language:** Python 3.x
- **Framework:** Flask (REST API)
- **Web Server:** NGINX (Reverse Proxy) + Gunicorn
- **Security:** Certbot (Let's Encrypt SSL/TLS)
- **CI/CD:** GitHub Actions / Pytest for automated backend testing.

---

## ✨ Key Features

### 1. Infrastructure as Code (IaC) 🏗️

No manual server setup. The entire environment is defined in **AWS CloudFormation** templates. This ensures environment consistency and rapid disaster recovery.

### 2. Auto-Scaling & High Availability 📈

The application utilizes **Auto Scaling Groups (ASG)**.

- _Traffic Spike?_ -> Spins up new EC2 instances automatically.
- _Low Traffic?_ -> Terminates instances to save costs.

### 3. Automated Monitoring & Alerts 🚨

**CloudWatch** integration allows for:

- Log aggregation from all active instances.
- **SNS** Alarms trigger emails to admins if model latency increases or error rates spike.

### 4. Secure Data Handling 🔒

- **Encryption:** Data in transit is encrypted via HTTPS.
- **Isolation:** Database is protected by Security Groups, allowing access only from the App Server.
- **IAM Roles:** EC2 instances access S3 via roles, eliminating the need for hardcoded AWS keys.

---

## ⚙️ Installation & Deployment

### Local Development

```bash
# Clone the repository
git clone https://github.com/your-username/IntelliPredict.git
cd IntelliPredict

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask App
python app.py
```

### AWS Deployment (CloudFormation)

1. Upload `model.pkl` and `app.zip` to your S3 bucket.
2. Navigate to the **AWS CloudFormation** console.
3. Click **Create Stack** -> Upload `infrastructure.yaml` (provided in this repo).
4. Wait for the stack to reach `CREATE_COMPLETE`.
5. Access the Load Balancer DNS / Public IP provided in the outputs.

## 📊 Outcomes

- ✅ **Reduced Deployment Time:** From hours to minutes using CloudFormation.
- ✅ **99.9% Uptime:** Achieved via Auto Scaling and managed RDS services.
- ✅ **Secure Pipeline:** Zero hardcoded credentials; full HTTPS encryption.
