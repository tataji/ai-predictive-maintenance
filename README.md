# AI Predictive Maintenance System

A production-ready, full-stack AI-powered predictive maintenance system with real-time equipment monitoring, machine learning-based anomaly detection, and automated maintenance scheduling.

## 🎯 Features

### Core Capabilities
- **Real-time Equipment Monitoring** - WebSocket-based live data streaming
- **ML-Based Anomaly Detection** - Isolation Forest algorithm for failure prediction
- **Automated Alerting** - Intelligent alert generation with severity levels
- **Maintenance Scheduling** - AI-driven maintenance task automation
- **RESTful API** - Complete backend API for integration
- **Interactive Dashboard** - Modern, responsive web interface
- **Historical Analytics** - Trend analysis and performance tracking

### Technical Stack

**Backend:**
- FastAPI (Python) - High-performance async API framework
- SQLite - Embedded database for data persistence
- scikit-learn - Machine learning for anomaly detection
- WebSockets - Real-time bidirectional communication
- Pydantic - Data validation and serialization

**Frontend:**
- Vanilla JavaScript - No framework dependencies
- Plotly.js - Interactive charts and visualizations
- WebSocket Client - Real-time updates
- Responsive CSS - Mobile-friendly design

## 📋 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Web App)                       │
│  - Real-time Dashboard                                       │
│  - Equipment Monitoring                                      │
│  - Alert Management                                          │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ HTTP/WebSocket
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                  Backend API (FastAPI)                       │
│  ┌────────────────────────────────────────────────────┐    │
│  │  REST Endpoints                                     │    │
│  │  - Equipment Management                             │    │
│  │  - Sensor Data Collection                           │    │
│  │  - Predictions & Alerts                             │    │
│  │  - Maintenance Scheduling                           │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  ML Engine (Isolation Forest)                       │    │
│  │  - Anomaly Detection                                │    │
│  │  - Confidence Scoring                               │    │
│  │  - Failure Prediction                               │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  WebSocket Manager                                  │    │
│  │  - Real-time Broadcasting                           │    │
│  │  - Connection Management                            │    │
│  └────────────────────────────────────────────────────┘    │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                    Database (SQLite)                         │
│  - Equipment                                                 │
│  - Sensor Readings                                           │
│  - Predictions                                               │
│  - Alerts                                                    │
│  - Maintenance Schedule                                      │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone or download the project**
   ```bash
   cd ai-predictive-maintenance
   ```

2. **Run the installation script**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

   Or install manually:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Running the System

**Option 1: Backend + Frontend (Recommended)**

Terminal 1 - Start Backend:
```bash
cd backend
source venv/bin/activate
python main.py
```

Terminal 2 - Serve Frontend:
```bash
cd frontend
python -m http.server 8080
```

Access the application:
- Frontend: http://localhost:8080
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

**Option 2: Backend Only (API Development)**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 Database Schema

### Equipment Table
```sql
CREATE TABLE equipment (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    location TEXT,
    install_date TEXT,
    last_maintenance TEXT,
    status TEXT DEFAULT 'healthy'
);
```

### Sensor Readings Table
```sql
CREATE TABLE sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id INTEGER,
    timestamp TEXT NOT NULL,
    temperature REAL,
    vibration REAL,
    pressure REAL,
    power_consumption REAL,
    efficiency REAL,
    FOREIGN KEY (equipment_id) REFERENCES equipment (id)
);
```

### Predictions Table
```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id INTEGER,
    timestamp TEXT NOT NULL,
    prediction_type TEXT,
    confidence REAL,
    predicted_failure_date TEXT,
    recommendation TEXT,
    FOREIGN KEY (equipment_id) REFERENCES equipment (id)
);
```

### Alerts Table
```sql
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id INTEGER,
    timestamp TEXT NOT NULL,
    severity TEXT,
    title TEXT,
    description TEXT,
    acknowledged INTEGER DEFAULT 0,
    FOREIGN KEY (equipment_id) REFERENCES equipment (id)
);
```

### Maintenance Schedule Table
```sql
CREATE TABLE maintenance_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id INTEGER,
    task TEXT NOT NULL,
    scheduled_date TEXT NOT NULL,
    priority TEXT,
    status TEXT DEFAULT 'pending',
    created_at TEXT,
    FOREIGN KEY (equipment_id) REFERENCES equipment (id)
);
```

## 🔌 API Reference

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Equipment Management

**Get All Equipment**
```http
GET /api/equipment
```

**Get Equipment Details**
```http
GET /api/equipment/{equipment_id}
```

#### Sensor Data

**Submit Sensor Reading**
```http
POST /api/sensor-data
Content-Type: application/json

{
    "equipment_id": 1,
    "temperature": 75.5,
    "vibration": 3.2,
    "pressure": 120.0,
    "power_consumption": 85.0,
    "efficiency": 92.0
}
```

#### Predictions

**Get All Predictions**
```http
GET /api/predictions
```

#### Alerts

**Get Alerts**
```http
GET /api/alerts?acknowledged=false
```

**Acknowledge Alert**
```http
POST /api/alerts/{alert_id}/acknowledge
```

#### Maintenance

**Get Maintenance Schedule**
```http
GET /api/maintenance
```

**Create Maintenance Task**
```http
POST /api/maintenance
Content-Type: application/json

{
    "equipment_id": 1,
    "task": "Replace hydraulic seals",
    "scheduled_date": "2024-12-20",
    "priority": "high"
}
```

#### Dashboard

**Get Dashboard Statistics**
```http
GET /api/dashboard-stats
```

### WebSocket

**Real-time Updates**
```javascript
ws://localhost:8000/ws
```

Messages:
- `status_update` - Equipment status changes
- `alert` - New alerts generated

## 🤖 Machine Learning Model

### Anomaly Detection Algorithm

The system uses **Isolation Forest**, an unsupervised learning algorithm designed for anomaly detection.

**How it works:**
1. Collects historical sensor data (temperature, vibration, pressure, power, efficiency)
2. Trains the model with 200 most recent readings per equipment
3. Standardizes data using StandardScaler
4. Detects anomalies by isolating observations
5. Generates confidence scores (0-100%)
6. Creates predictions and alerts for detected anomalies

**Model Configuration:**
```python
IsolationForest(
    contamination=0.1,  # Expected anomaly rate
    random_state=42,
    n_estimators=100    # Number of trees
)
```

**Prediction Logic:**
- Score > 85% confidence → Critical alert
- Score 70-85% confidence → Warning alert
- Score < 70% → Monitoring

## 📈 Data Flow

1. **Sensor Data Collection**
   - IoT sensors send real-time readings
   - Data posted to `/api/sensor-data`
   - Stored in `sensor_readings` table

2. **ML Processing**
   - Historical data retrieved
   - Model trained/updated if needed
   - Current reading analyzed
   - Anomaly score calculated

3. **Alert Generation**
   - If anomaly detected (prediction = -1)
   - Severity determined by confidence
   - Alert created in database
   - WebSocket broadcast sent

4. **Maintenance Scheduling**
   - Based on predictions
   - Prioritized by severity
   - Added to schedule table

5. **Dashboard Update**
   - WebSocket pushes updates
   - Frontend refreshes data
   - Charts and metrics updated

## 🔒 Security Considerations

For production deployment:

1. **Authentication & Authorization**
   - Add JWT token-based auth
   - Role-based access control
   - API key management

2. **Database Security**
   - Use PostgreSQL instead of SQLite
   - Encrypt sensitive data
   - Regular backups

3. **Network Security**
   - Enable HTTPS/WSS
   - CORS configuration
   - Rate limiting

4. **Data Validation**
   - Input sanitization (already implemented via Pydantic)
   - SQL injection prevention
   - XSS protection

## 📊 Monetization Models

### SaaS Pricing Tiers

**Starter - $299/month**
- Up to 10 equipment units
- 1 GB sensor data storage
- Email alerts
- 30-day data retention

**Professional - $799/month**
- Up to 50 equipment units
- 10 GB sensor data storage
- SMS + Email alerts
- 90-day data retention
- Advanced analytics
- API access

**Enterprise - $2,499/month**
- Unlimited equipment
- Unlimited storage
- Multi-channel alerts
- Unlimited retention
- Custom ML models
- Dedicated support
- White-label option

### Cost Savings Calculation

For a manufacturing facility with 50 machines:
- **Prevented downtime**: $50K-$100K/year
- **Optimized maintenance**: $30K-$60K/year
- **Extended equipment life**: $20K-$40K/year
- **Total annual ROI**: $100K-$200K

System cost: $9,588/year (Professional plan)
**Net savings: $90K-$190K/year**

## 🛠️ Customization

### Adding New Equipment Types

Edit `main.py` to add equipment in `seed_initial_data()`:
```python
(7, 'Custom Machine', 'custom_type', 'Location', '2024-01-01', '2024-11-01', 'healthy')
```

### Adjusting ML Model Parameters

Modify model configuration in `AnomalyDetector` class:
```python
self.model = IsolationForest(
    contamination=0.15,  # Adjust anomaly threshold
    n_estimators=150     # Increase for better accuracy
)
```

### Customizing Alert Thresholds

Edit `record_sensor_data()` function:
```python
if prediction == -1:
    if confidence > 90:  # More strict
        status = "critical"
```

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python3 --version`
- Verify virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`

### Frontend shows "Disconnected"
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify WebSocket URL in frontend code

### No sensor data appearing
- Backend generates simulated data automatically
- Wait 10-15 seconds after startup
- Check backend logs for errors

### Database errors
- Delete `maintenance.db` and restart
- Database will auto-recreate

## 📝 License

This is a demonstration project for educational and commercial use.

## 🤝 Support

For questions, issues, or feature requests, consult the API documentation at `/docs` endpoint.

## 🚀 Deployment to Production

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
```bash
DATABASE_URL=postgresql://user:pass@host:5432/dbname
API_SECRET_KEY=your-secret-key-here
CORS_ORIGINS=https://yourdomain.com
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8080;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

**Built with ❤️ for predictive maintenance and industrial IoT**
