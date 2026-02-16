# Deployment Guide - AI Predictive Maintenance System

Complete guide for deploying the system to various platforms and environments.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [AWS Deployment](#aws-deployment)
4. [Azure Deployment](#azure-deployment)
5. [Google Cloud Deployment](#google-cloud-deployment)
6. [Production Checklist](#production-checklist)

---

## Local Development

### Quick Start
```bash
# Install dependencies
./install.sh

# Start backend
cd backend
source venv/bin/activate
python main.py

# In another terminal, serve frontend
cd frontend
python -m http.server 8080
```

Access:
- Frontend: http://localhost:8080
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Docker Deployment

### Single Container (Backend Only)
```bash
# Build
docker build -t maintenance-backend --target backend .

# Run
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  --name maintenance-backend \
  maintenance-backend
```

### Multi-Container with Docker Compose
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access:
- Frontend: http://localhost:8080
- Backend: http://localhost:8000

### Production Docker Setup
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start with environment variables
docker-compose -f docker-compose.prod.yml up -d
```

---

## AWS Deployment

### Option 1: EC2 with Docker

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t3.medium or larger
   - Security Group: Allow ports 80, 443, 8000, 8080

2. **Install Docker**
```bash
ssh ubuntu@your-ec2-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. **Deploy Application**
```bash
# Clone repository
git clone your-repo-url
cd ai-predictive-maintenance

# Start services
docker-compose up -d
```

4. **Configure Nginx (Optional)**
```bash
sudo apt update
sudo apt install nginx

# Copy nginx config
sudo cp nginx.conf /etc/nginx/sites-available/maintenance
sudo ln -s /etc/nginx/sites-available/maintenance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 2: ECS (Elastic Container Service)

1. **Create ECR Repository**
```bash
aws ecr create-repository --repository-name maintenance-backend
aws ecr create-repository --repository-name maintenance-frontend
```

2. **Build and Push Images**
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Build and push backend
docker build -t maintenance-backend --target backend .
docker tag maintenance-backend:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/maintenance-backend:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/maintenance-backend:latest

# Build and push frontend
docker build -t maintenance-frontend --target frontend .
docker tag maintenance-frontend:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/maintenance-frontend:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/maintenance-frontend:latest
```

3. **Create ECS Task Definition**
```json
{
  "family": "maintenance-system",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/maintenance-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ]
    }
  ]
}
```

4. **Create ECS Service**
```bash
aws ecs create-service \
  --cluster your-cluster \
  --service-name maintenance-backend \
  --task-definition maintenance-system \
  --desired-count 2 \
  --launch-type FARGATE
```

### Option 3: Elastic Beanstalk

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize Application**
```bash
eb init -p docker maintenance-system
eb create maintenance-prod
```

3. **Deploy**
```bash
eb deploy
eb open
```

---

## Azure Deployment

### Option 1: Azure Container Instances

1. **Create Resource Group**
```bash
az group create --name maintenance-rg --location eastus
```

2. **Create Container Registry**
```bash
az acr create --resource-group maintenance-rg \
  --name maintenanceacr --sku Basic

az acr login --name maintenanceacr
```

3. **Build and Push**
```bash
docker build -t maintenance-backend --target backend .
docker tag maintenance-backend maintenanceacr.azurecr.io/backend:latest
docker push maintenanceacr.azurecr.io/backend:latest
```

4. **Deploy Container**
```bash
az container create \
  --resource-group maintenance-rg \
  --name maintenance-backend \
  --image maintenanceacr.azurecr.io/backend:latest \
  --cpu 1 --memory 1 \
  --registry-login-server maintenanceacr.azurecr.io \
  --registry-username $(az acr credential show --name maintenanceacr --query "username" -o tsv) \
  --registry-password $(az acr credential show --name maintenanceacr --query "passwords[0].value" -o tsv) \
  --dns-name-label maintenance-api \
  --ports 8000
```

### Option 2: Azure App Service

1. **Create App Service Plan**
```bash
az appservice plan create \
  --name maintenance-plan \
  --resource-group maintenance-rg \
  --is-linux \
  --sku B1
```

2. **Create Web App**
```bash
az webapp create \
  --resource-group maintenance-rg \
  --plan maintenance-plan \
  --name maintenance-backend \
  --deployment-container-image-name maintenanceacr.azurecr.io/backend:latest
```

3. **Configure**
```bash
az webapp config appsettings set \
  --resource-group maintenance-rg \
  --name maintenance-backend \
  --settings WEBSITES_PORT=8000
```

---

## Google Cloud Deployment

### Option 1: Cloud Run

1. **Build and Push to Container Registry**
```bash
# Configure gcloud
gcloud config set project your-project-id

# Build and push
gcloud builds submit --tag gcr.io/your-project-id/maintenance-backend

# Deploy
gcloud run deploy maintenance-backend \
  --image gcr.io/your-project-id/maintenance-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Option 2: Google Kubernetes Engine (GKE)

1. **Create Cluster**
```bash
gcloud container clusters create maintenance-cluster \
  --num-nodes=2 \
  --zone=us-central1-a
```

2. **Deploy Application**
```bash
kubectl create deployment maintenance-backend \
  --image=gcr.io/your-project-id/maintenance-backend

kubectl expose deployment maintenance-backend \
  --type=LoadBalancer \
  --port 80 \
  --target-port 8000
```

3. **Get External IP**
```bash
kubectl get service maintenance-backend
```

---

## Production Checklist

### Security
- [ ] Enable HTTPS/SSL certificates
- [ ] Implement authentication (JWT)
- [ ] Add API rate limiting
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Enable database encryption
- [ ] Implement audit logging
- [ ] Set up secrets management

### Database
- [ ] Migrate from SQLite to PostgreSQL/MySQL
- [ ] Set up automated backups
- [ ] Configure connection pooling
- [ ] Implement database monitoring
- [ ] Set up read replicas (if needed)

### Monitoring
- [ ] Set up application monitoring (Datadog, New Relic)
- [ ] Configure error tracking (Sentry)
- [ ] Set up log aggregation (ELK, CloudWatch)
- [ ] Create health check endpoints
- [ ] Configure alerts for critical metrics
- [ ] Set up uptime monitoring

### Performance
- [ ] Enable caching (Redis)
- [ ] Configure CDN for static assets
- [ ] Implement database indexing
- [ ] Set up load balancing
- [ ] Enable gzip compression
- [ ] Optimize Docker images

### Scalability
- [ ] Configure auto-scaling
- [ ] Set up horizontal pod autoscaling (k8s)
- [ ] Implement message queuing (if needed)
- [ ] Configure session management
- [ ] Set up database sharding (if needed)

### Backup & Recovery
- [ ] Automated database backups
- [ ] Disaster recovery plan
- [ ] Test restore procedures
- [ ] Document recovery steps

### Documentation
- [ ] API documentation up-to-date
- [ ] Deployment runbooks
- [ ] Incident response procedures
- [ ] Architecture diagrams
- [ ] User guides

### Cost Optimization
- [ ] Right-size instances
- [ ] Use reserved instances/savings plans
- [ ] Configure auto-shutdown for dev environments
- [ ] Implement cost monitoring
- [ ] Review and remove unused resources

---

## Environment Variables

### Backend
```bash
# .env file
DATABASE_URL=postgresql://user:pass@host:5432/maintenance
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=https://yourdomain.com
LOG_LEVEL=INFO
REDIS_URL=redis://localhost:6379
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password
```

### Docker Compose
```yaml
environment:
  - DATABASE_URL=${DATABASE_URL}
  - SECRET_KEY=${SECRET_KEY}
  - CORS_ORIGINS=${CORS_ORIGINS}
```

---

## SSL/TLS Configuration

### Let's Encrypt with Certbot
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
sudo certbot renew --dry-run
```

### Nginx SSL Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # ... rest of config
}
```

---

## Monitoring Setup

### Prometheus + Grafana
```yaml
# docker-compose.monitoring.yml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Example Prometheus Config
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'maintenance-backend'
    static_configs:
      - targets: ['backend:8000']
```

---

## Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose logs backend

# Check database connection
docker exec -it maintenance-backend python -c "import sqlite3; print('DB OK')"

# Verify port availability
netstat -tuln | grep 8000
```

### High memory usage
```bash
# Check container stats
docker stats

# Limit memory in docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
```

### WebSocket connection issues
```bash
# Verify WebSocket endpoint
wscat -c ws://localhost:8000/ws

# Check nginx WebSocket config
# Ensure proper headers are set
```

---

## Support & Maintenance

### Regular Tasks
- Weekly: Review logs and alerts
- Monthly: Update dependencies
- Quarterly: Security audit
- Annually: Architecture review

### Update Procedure
```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose build

# Deploy with zero downtime
docker-compose up -d --no-deps --build backend
```

---

**For additional help, refer to the main README.md or API documentation at /docs**
