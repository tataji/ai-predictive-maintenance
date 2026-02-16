# AI Predictive Maintenance System - Project Structure

```
ai-predictive-maintenance/
│
├── backend/                          # Backend application
│   ├── main.py                       # Main FastAPI application
│   ├── requirements.txt              # Python dependencies
│   ├── venv/                         # Virtual environment (created during install)
│   └── maintenance.db                # SQLite database (auto-created)
│
├── frontend/                         # Frontend web application
│   └── index.html                    # Main web interface
│
├── install.sh                        # Installation script
├── test_api.py                       # API testing script
├── README.md                         # Main documentation
├── DEPLOYMENT.md                     # Deployment guide
├── Dockerfile                        # Docker configuration
├── docker-compose.yml                # Docker Compose configuration
├── nginx.conf                        # Nginx configuration
└── .gitignore                        # Git ignore file

```

## File Descriptions

### Backend (`backend/`)

**main.py** (500+ lines)
- FastAPI application with all endpoints
- ML-based anomaly detection using Isolation Forest
- WebSocket manager for real-time updates
- Database initialization and management
- Background task for sensor data generation
- Complete API with:
  - Equipment management
  - Sensor data collection
  - Predictions and alerts
  - Maintenance scheduling
  - Dashboard statistics

**requirements.txt**
- All Python dependencies
- FastAPI, Uvicorn for web server
- scikit-learn for ML
- NumPy for numerical operations
- Pydantic for data validation

### Frontend (`frontend/`)

**index.html** (700+ lines)
- Production-ready web interface
- Real-time WebSocket connection
- Interactive equipment cards
- Plotly.js charts for analytics
- Alert management UI
- Maintenance schedule view
- Responsive design
- No build process required

### Configuration & Deployment

**install.sh**
- Automated installation script
- Sets up virtual environment
- Installs dependencies
- Provides usage instructions

**Dockerfile**
- Multi-stage Docker build
- Backend and frontend containers
- Optimized for production

**docker-compose.yml**
- Multi-container orchestration
- Backend + Frontend services
- Volume management
- Health checks

**nginx.conf**
- Production web server config
- API proxying
- WebSocket support
- Gzip compression

### Documentation

**README.md**
- Complete system overview
- Installation instructions
- API reference
- Architecture diagrams
- Monetization models
- Customization guide

**DEPLOYMENT.md**
- Platform-specific deployment guides
- AWS, Azure, GCP instructions
- Production checklist
- Security best practices
- Monitoring setup

### Testing

**test_api.py**
- Comprehensive API tests
- Stress testing capabilities
- Validates all endpoints
- Easy to run: `python test_api.py`

## Database Schema

The SQLite database (`maintenance.db`) contains:

1. **equipment** - Equipment inventory and status
2. **sensor_readings** - Time-series sensor data
3. **predictions** - ML model predictions
4. **alerts** - System-generated alerts
5. **maintenance_schedule** - Upcoming maintenance tasks

## Technology Stack Summary

**Backend:**
- Framework: FastAPI (Python 3.8+)
- ML: scikit-learn (Isolation Forest)
- Database: SQLite (production: PostgreSQL/MySQL)
- Real-time: WebSockets
- Validation: Pydantic

**Frontend:**
- HTML5/CSS3/JavaScript (Vanilla)
- Charts: Plotly.js
- Real-time: WebSocket API
- No build tools required

**Deployment:**
- Containerization: Docker
- Orchestration: Docker Compose
- Web Server: Nginx
- Cloud: AWS/Azure/GCP ready

## Key Features Implementation

### 1. Real-time Monitoring
- WebSocket connection for live updates
- Auto-refresh every 5 seconds
- Equipment status cards
- Live data indicator

### 2. ML Anomaly Detection
- Isolation Forest algorithm
- 200-point historical training
- Confidence scoring
- Automatic retraining

### 3. Alert System
- Severity levels (critical/warning)
- Acknowledgment tracking
- Real-time notifications
- Detailed recommendations

### 4. Maintenance Scheduling
- AI-driven task generation
- Priority-based sorting
- Date tracking
- Status management

### 5. Analytics Dashboard
- Multi-metric visualization
- Trend analysis
- Performance charts
- Cost savings tracking

## Extension Points

### Add New Equipment
Edit `backend/main.py` in `seed_initial_data()` function

### Customize ML Model
Modify `AnomalyDetector` class parameters:
- Contamination rate
- Number of estimators
- Training data size

### Add New Sensors
Update `SensorReading` model in `main.py`
Update database schema
Modify frontend cards

### Integrate External APIs
Add endpoints in `main.py`
Update frontend API calls
Extend data models

### Add Authentication
Install: `pip install python-jose passlib`
Add JWT middleware
Update frontend with tokens

## Production Deployment Paths

### Small Scale (1-100 machines)
- Single EC2/VM instance
- SQLite database
- Docker Compose deployment
- Cost: $50-100/month

### Medium Scale (100-1000 machines)
- Multiple app servers
- PostgreSQL database
- Load balancer
- Redis caching
- Cost: $300-800/month

### Large Scale (1000+ machines)
- Kubernetes cluster
- Managed database (RDS/Cloud SQL)
- CDN for static assets
- Message queue (RabbitMQ/SQS)
- Cost: $2000+/month

## Development Workflow

1. **Local Development**
   ```bash
   ./install.sh
   cd backend && source venv/bin/activate && python main.py
   ```

2. **Testing**
   ```bash
   python test_api.py
   python test_api.py --stress
   ```

3. **Docker Build**
   ```bash
   docker-compose up --build
   ```

4. **Production Deploy**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## Maintenance & Updates

### Regular Tasks
- Monitor logs: `docker-compose logs -f`
- Check database size: `ls -lh backend/maintenance.db`
- Review alerts: Visit dashboard
- Update dependencies: `pip install -r requirements.txt --upgrade`

### Backup Database
```bash
cp backend/maintenance.db backend/maintenance.db.backup
```

### Clear Old Data
```bash
# Add to main.py or run manually
cursor.execute("DELETE FROM sensor_readings WHERE timestamp < date('now', '-30 days')")
```

## Support Resources

- API Documentation: http://localhost:8000/docs
- Interactive API: http://localhost:8000/redoc
- GitHub Issues: [Create issue tracker]
- Email Support: [Add support email]

---

This project structure is designed for:
✓ Easy deployment
✓ Simple maintenance
✓ Straightforward customization
✓ Production readiness
✓ Scalability
