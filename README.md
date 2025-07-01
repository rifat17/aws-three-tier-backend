# AWS Three-Tier Backend

A Flask-based backend API for a three-tier architecture application with MySQL database integration.

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd aws-three-tier-backend

# Run with Docker (easiest)
docker-compose up --build
```

Application will be available at `http://localhost:5000`

## Setup Instructions

### 1. Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

**Docker:** Uses default environment variables (no setup needed)

**Local development:** Create `.env` file:

```env
DB_HOST=localhost
DB_NAME=mydatabase
DB_USER=appuser
DB_PASS=password
```

### 3. Database Setup

**Docker:** Database setup is automatic via `init.sql`

**Local development:** Execute these SQL commands:

```sql
CREATE DATABASE IF NOT EXISTS mydatabase;
CREATE USER IF NOT EXISTS 'appuser'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON mydatabase.* TO 'appuser'@'%';
FLUSH PRIVILEGES;

-- Create messages table
USE mydatabase;
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    timestamp DATETIME NOT NULL
);
```

## Running the Application

### Docker (Recommended)

```bash
docker-compose up --build
```

### Local Development

```bash
source venv/bin/activate
python app.py
```

## API Endpoints

- `GET /` - Health check endpoint
- `GET /api/data` - Retrieve the latest message from database
- `POST /api/add-message` - Add a new message to database

### Example API Usage

```bash
# Add a message
curl -X POST http://localhost:5000/api/add-message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello World!"}'

# Get latest message
curl http://localhost:5000/api/data
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|----------|
| `DB_HOST` | Database host | `localhost` |
| `DB_NAME` | Database name | `mydatabase` |
| `DB_USER` | Database username | `appuser` |
| `DB_PASS` | Database password | `mypassword` |

## Dependencies

- Flask 2.3.2 - Web framework
- PyMySQL - MySQL database connector
- Flask-CORS 4.0.0 - Cross-origin resource sharing
- python-dotenv - Environment variable management
- cryptography - Required for PyMySQL