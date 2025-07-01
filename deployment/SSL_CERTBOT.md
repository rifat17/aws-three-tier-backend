# SSL Certificate Management with Certbot

## What is Certbot?

Certbot is a free, open-source software tool for automatically using Let's Encrypt certificates on manually-administrated websites to enable HTTPS.

### Why Use Certbot?
- **Free SSL Certificates**: Let's Encrypt provides free SSL certificates
- **Automatic Installation**: Certbot automatically configures Nginx
- **Auto-Renewal**: Certificates renew automatically before expiration
- **Easy Management**: Simple commands for certificate operations
- **Trusted**: Certificates are trusted by all major browsers

## Prerequisites

### 1. Domain Name Required
- You **must** have a domain name pointing to your EC2 instance
- IP addresses alone won't work with Let's Encrypt
- Update your domain's DNS A record to point to your EC2 public IP

### 2. Nginx Must Be Running
- Nginx should be installed and serving your application
- Port 80 must be accessible from the internet
- Your site should be working over HTTP first

## Installation

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install snapd
sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

### Amazon Linux/RHEL
```bash
sudo yum install epel-release
sudo yum install certbot python3-certbot-nginx
```

## How Certbot Works

### 1. Domain Validation Process
```
1. You request certificate for your-domain.com
2. Let's Encrypt sends a challenge
3. Certbot places challenge file in /.well-known/acme-challenge/
4. Let's Encrypt verifies the file via HTTP
5. Certificate is issued and installed
```

### 2. Certificate Storage
- Certificates stored in: `/etc/letsencrypt/live/your-domain.com/`
- Files created:
  - `fullchain.pem` - Certificate + intermediate certificates
  - `privkey.pem` - Private key
  - `cert.pem` - Certificate only
  - `chain.pem` - Intermediate certificates

## Certificate Installation

### Method 1: Automatic Nginx Configuration (Recommended)
```bash
# This will automatically modify your Nginx config
sudo certbot --nginx -d your-domain.com

# For multiple domains
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### Method 2: Certificate Only (Manual Nginx Config)
```bash
# Get certificate without modifying Nginx config
sudo certbot certonly --nginx -d your-domain.com
```

## Manual Nginx Configuration

If using Method 2, update your Nginx config:

**File**: `/etc/nginx/sites-available/aws-backend`
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # SSL Security Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Certificate Renewal

### Automatic Renewal (Recommended)
Certbot automatically sets up a cron job or systemd timer:

```bash
# Check if auto-renewal is working
sudo certbot renew --dry-run

# View renewal timer status
sudo systemctl status snap.certbot.renew.timer
```

### Manual Renewal
```bash
# Renew all certificates
sudo certbot renew

# Renew specific certificate
sudo certbot renew --cert-name your-domain.com

# Renew and reload Nginx
sudo certbot renew --post-hook "systemctl reload nginx"
```

### Renewal Process
1. Certbot checks certificates expiring in 30 days
2. Requests new certificate from Let's Encrypt
3. Replaces old certificate files
4. Reloads Nginx (if configured)

## Certificate Management Commands

### View Certificates
```bash
# List all certificates
sudo certbot certificates

# Show certificate details
sudo certbot show_account
```

### Delete Certificate
```bash
# Delete certificate and remove from Nginx
sudo certbot delete --cert-name your-domain.com
```

### Expand Certificate (Add Domains)
```bash
# Add www subdomain to existing certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com --expand
```

## Troubleshooting

### Common Issues

#### 1. Domain Not Pointing to Server
```bash
# Test DNS resolution
nslookup your-domain.com
dig your-domain.com

# Should return your EC2 public IP
```

#### 2. Port 80 Not Accessible
```bash
# Check if Nginx is listening on port 80
sudo netstat -tlnp | grep :80

# Test HTTP access
curl -I http://your-domain.com
```

#### 3. Firewall/Security Groups
- Ensure Security Groups allow HTTP (80) and HTTPS (443)
- Check if UFW or iptables is blocking ports

#### 4. Rate Limits
- Let's Encrypt has rate limits (5 certificates per domain per week)
- Use `--dry-run` for testing
- Wait if you hit rate limits

### Log Files
```bash
# Certbot logs
sudo tail -f /var/log/letsencrypt/letsencrypt.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

## Security Best Practices

### 1. SSL Configuration Test
```bash
# Test SSL configuration
curl -I https://your-domain.com

# Online SSL test
# Visit: https://www.ssllabs.com/ssltest/
```

### 2. HTTP to HTTPS Redirect
Ensure all HTTP traffic redirects to HTTPS:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### 3. Security Headers
Add security headers to your Nginx config:
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options DENY always;
add_header X-Content-Type-Options nosniff always;
```

## Complete Setup Example

### Step-by-Step SSL Setup
```bash
# 1. Ensure domain points to your EC2 IP
nslookup your-domain.com

# 2. Install Certbot
sudo snap install --classic certbot

# 3. Get certificate and configure Nginx
sudo certbot --nginx -d your-domain.com

# 4. Test renewal
sudo certbot renew --dry-run

# 5. Verify HTTPS is working
curl -I https://your-domain.com
```

## Learning Outcomes for Students

1. **SSL/TLS Concepts**: Understanding HTTPS and certificate validation
2. **Certificate Authority**: Learning about Let's Encrypt and trust chains
3. **Domain Validation**: Understanding how domain ownership is verified
4. **Certificate Lifecycle**: Installation, renewal, and management
5. **Security Best Practices**: HTTPS redirects and security headers
6. **Automation**: Setting up automatic certificate renewal

## Cost Comparison

| Solution | Cost | Complexity | Auto-Renewal |
|----------|------|------------|--------------|
| Let's Encrypt + Certbot | Free | Low | Yes |
| Commercial SSL | $50-200/year | Medium | Manual |
| AWS Certificate Manager | Free* | Low | Yes |
| Self-Signed | Free | High | Manual |

*AWS ACM certificates only work with AWS load balancers, not directly with EC2

This setup provides production-grade SSL certificates with automatic renewal, giving students hands-on experience with industry-standard security practices.