# Nginx Reverse Proxy Setup Guide

## Why Use Nginx?

### Current Setup Limitations
- **Direct Application Exposure**: Gunicorn serves directly on port 5000
- **No SSL Termination**: HTTPS must be handled by the application
- **Limited Static File Serving**: Flask serves static files inefficiently
- **No Load Balancing**: Single point of failure
- **Security Concerns**: Application server exposed directly to internet

### Nginx Benefits
- **Reverse Proxy**: Hide application server behind Nginx
- **SSL Termination**: Handle HTTPS certificates at Nginx level
- **Static File Serving**: Efficiently serve static content
- **Load Balancing**: Distribute requests across multiple app instances
- **Security**: Additional security layer and request filtering
- **Caching**: Built-in caching capabilities
- **Standard Port**: Serve on port 80/443 instead of 5000

## Implementation Plan

### 1. Install Nginx
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx

# Amazon Linux/RHEL
sudo yum install nginx
# or
sudo amazon-linux-extras install nginx1
```

### 2. Create Nginx Configuration
**File**: `deployment/nginx.conf`
```nginx
server {
    listen 80;
    server_name your-domain.com your-ec2-ip;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Optional: Serve static files directly
    location /static {
        alias /home/ubuntu/aws-three-tier-backend/static;
        expires 30d;
    }
}
```

### 3. Update Gunicorn Configuration
**File**: `deployment/gunicorn.conf.py`
```python
# Change bind from public to localhost only
bind = "127.0.0.1:5000"  # Only accept local connections
workers = 2
worker_class = "sync"
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
```

### 4. Update Security Groups
- **Remove**: Direct access to port 5000
- **Add**: HTTP (port 80) and HTTPS (port 443) access
- **Keep**: SSH (port 22) for management

### 5. SSL Configuration (Optional)
**File**: `deployment/nginx-ssl.conf`
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Architecture Comparison

### Before Nginx
```
Internet → EC2:5000 → Gunicorn → Flask App
```

### After Nginx
```
Internet → EC2:80/443 → Nginx → 127.0.0.1:5000 → Gunicorn → Flask App
```

## Benefits Comparison

| Feature | Without Nginx | With Nginx |
|---------|---------------|------------|
| Port | 5000 (non-standard) | 80/443 (standard) |
| SSL | Application handles | Nginx handles |
| Static Files | Flask serves | Nginx serves |
| Security | Direct exposure | Proxy protection |
| Caching | None | Built-in |
| Load Balancing | Single instance | Multiple instances |

## Implementation Steps

### 1. Install and Configure Nginx
```bash
# Install Nginx
sudo apt install nginx

# Copy configuration
sudo cp deployment/nginx.conf /etc/nginx/sites-available/aws-backend
sudo ln -s /etc/nginx/sites-available/aws-backend /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t
```

### 2. Update Gunicorn to Bind Localhost Only
```bash
# Update gunicorn config to bind 127.0.0.1:5000
# Restart the application service
sudo systemctl restart aws-backend
```

### 3. Start Nginx
```bash
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl status nginx
```

### 4. Update Security Groups
- Remove inbound rule for port 5000
- Add inbound rules for ports 80 and 443

### 5. Test the Setup
```bash
# Test HTTP access
curl http://your-ec2-ip/

# Test API endpoints
curl http://your-ec2-ip/api/data
```

## Learning Outcomes for Students

1. **Reverse Proxy Concepts**: Understanding how Nginx forwards requests
2. **Web Server vs Application Server**: Learning the difference and roles
3. **Security Best Practices**: Not exposing application servers directly
4. **SSL Termination**: Understanding where HTTPS is handled
5. **Production Architecture**: Industry-standard web application deployment
6. **Performance Optimization**: Static file serving and caching

## Troubleshooting

### Common Issues
1. **Port 5000 still accessible**: Update security groups
2. **502 Bad Gateway**: Check if Gunicorn is running on 127.0.0.1:5000
3. **Permission denied**: Check Nginx user permissions
4. **Configuration errors**: Run `sudo nginx -t` to test config

### Log Files
- Nginx access log: `/var/log/nginx/access.log`
- Nginx error log: `/var/log/nginx/error.log`
- Application logs: `sudo journalctl -u aws-backend`

This setup transforms the deployment into a production-ready architecture with proper separation of concerns between the web server (Nginx) and application server (Gunicorn).