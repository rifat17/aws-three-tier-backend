# Gunicorn Production Upgrade Guide

## Why Use Gunicorn?

### Current Setup Issues
- **Flask Development Server**: Not designed for production use
- **Single Process**: Can only handle one request at a time
- **No Process Management**: If the app crashes, it stays down
- **Security Concerns**: Development server has known vulnerabilities

### Gunicorn Benefits
- **Production WSGI Server**: Industry standard for Python web applications
- **Multiple Workers**: Handle concurrent requests efficiently
- **Process Management**: Automatic worker restarts and graceful shutdowns
- **Better Performance**: Optimized for production workloads
- **Load Balancing**: Built-in worker load balancing
- **Monitoring**: Better logging and process monitoring

## Implementation Plan

### 1. Update Dependencies
**File**: `requirements.txt`
```
Flask
PyMySQL
Flask-CORS
python-dotenv
gunicorn  # Add this line
```

### 2. Modify Flask Application
**File**: `app.py`
- Remove the development server startup block:
```python
# Remove this block:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
```
- Keep the Flask app object accessible for Gunicorn

### 3. Update Systemd Service
**File**: `deployment/aws-backend.service`
- Change ExecStart from:
```
ExecStart=/home/ubuntu/aws-three-tier-backend/venv/bin/python app.py
```
- To (using config file):
```
ExecStart=/home/ubuntu/aws-three-tier-backend/venv/bin/gunicorn --config deployment/gunicorn.conf.py app:app
```
- Or (using command line options):
```
ExecStart=/home/ubuntu/aws-three-tier-backend/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 2 app:app
```

### 4. Create Gunicorn Configuration (Optional)
**File**: `deployment/gunicorn.conf.py`
```python
bind = "0.0.0.0:5000"
workers = 2
worker_class = "sync"
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
```

**Usage**: Reference this config file in the systemd service:
```
ExecStart=.../gunicorn --config deployment/gunicorn.conf.py app:app
```

### 5. Update Documentation
**File**: `README.md`
- Add Gunicorn installation instructions
- Update production deployment section
- Explain the benefits to students

## Performance Comparison

| Metric | Flask Dev Server | Gunicorn |
|--------|------------------|----------|
| Concurrent Requests | 1 | Multiple (based on workers) |
| Production Ready | ❌ | ✅ |
| Process Management | ❌ | ✅ |
| Auto Restart | ❌ | ✅ |
| Performance | Low | High |
| Security | Development Only | Production Ready |

## Learning Outcomes for Students

1. **Production Deployment**: Understanding the difference between development and production servers
2. **WSGI Concepts**: Learning about Python web server interfaces
3. **Process Management**: Understanding worker processes and load balancing
4. **Performance Optimization**: Seeing real-world performance improvements
5. **Industry Standards**: Using tools commonly found in production environments

## Implementation Steps

1. **Add gunicorn to requirements.txt**
2. **Remove Flask dev server code from app.py**
3. **Update systemd service file**
4. **Test the deployment**
5. **Monitor performance improvements**

## Testing the Upgrade

```bash
# Install new dependencies
pip install -r requirements.txt

# Test Gunicorn locally
gunicorn --bind 0.0.0.0:5000 --workers 2 app:app

# Update and restart service
sudo systemctl daemon-reload
sudo systemctl restart aws-backend
sudo systemctl status aws-backend
```

This upgrade transforms the application from a development setup to a production-ready deployment, giving students hands-on experience with industry-standard tools and practices.