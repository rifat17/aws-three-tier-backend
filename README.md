# AWS Three-Tier Backend

Simple Flask API for AWS learning.

## Setup on EC2

```bash
git clone <repository-url>
cd aws-three-tier-backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your RDS details

# Run application
python app.py
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

## License

MIT License - see [LICENSE](LICENSE) file for details.