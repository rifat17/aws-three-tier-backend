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

## Database Setup

### Option 1: Using MySQL Client

Install MySQL client:
```bash
# Ubuntu/Debian
sudo apt install mysql-client

# Amazon Linux/RHEL
sudo yum install mysql

# macOS
brew install mysql-client
```

Run schema:
```bash
mysql -h your-rds-endpoint -u admin -p < database/schema.sql
```

### Option 2: Copy-paste SQL commands

Connect to RDS using any MySQL tool and run the commands from `database/schema.sql`

## Production Deployment

For production deployment with auto-restart:

```bash
# Copy service file
sudo cp deployment/aws-backend.service /etc/systemd/system/

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable aws-backend
sudo systemctl start aws-backend

# Check status
sudo systemctl status aws-backend
```

## AWS Setup

1. **RDS MySQL** - Create database using schema.sql
2. **EC2** - Run this Flask app
3. **Security Groups** - Allow your configured port (default: 5000)

## License

MIT License - see [LICENSE](LICENSE) file for details.