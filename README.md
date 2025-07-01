# AWS Three-Tier Backend

Simple Flask API for AWS learning.

## Setup on EC2

```bash
git clone <repository-url>
cd aws-three-tier-backend
pip3 install -r requirements.txt
cp .env.example .env
# Edit .env with your RDS details
python3 app.py
```

## Test API

```bash
# Check if running
curl http://your-ec2-ip:5000

# Add message
curl -X POST http://your-ec2-ip:5000/api/add-message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello AWS!"}'

# Get message
curl http://your-ec2-ip:5000/api/data
```

## AWS Setup

1. **RDS MySQL** - Create database
2. **EC2** - Run this Flask app
3. **Security Groups** - Allow port 5000