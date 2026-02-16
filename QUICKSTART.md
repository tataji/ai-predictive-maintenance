# 🚀 Quick Start Guide - AI Predictive Maintenance System

Get the system running in 5 minutes!

## Prerequisites Check

```bash
# Check Python version (need 3.8+)
python3 --version

# Check if pip is installed
pip3 --version
```

## Installation (2 minutes)

### Option 1: Automated Installation (Recommended)
```bash
cd ai-predictive-maintenance
chmod +x install.sh
./install.sh
```

### Option 2: Manual Installation
```bash
cd ai-predictive-maintenance/backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the System (1 minute)

### Terminal 1: Start Backend
```bash
cd backend
source venv/bin/activate
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Serve Frontend
```bash
# Option A: Python HTTP server
cd frontend
python -m http.server 8080

# Option B: Just open the file
# Open frontend/index.html in your browser
```

## Access the System

Open your browser and go to:

**Frontend Dashboard:** http://localhost:8080 (or open frontend/index.html)
**Backend API:** http://localhost:8000
**API Documentation:** http://localhost:8000/docs

## What You'll See

1. **Equipment Dashboard** - 6 pre-configured equipment units
2. **Real-time Updates** - Live data every 5 seconds
3. **AI Predictions** - Anomaly detection in action
4. **Active Alerts** - System-generated warnings
5. **Maintenance Schedule** - AI-driven task recommendations

## Testing the API (Optional)

```bash
# Run comprehensive tests
python test_api.py

# Run stress test (100 sensor readings)
python test_api.py --stress
```

## Docker Alternative (If you prefer containers)

```bash
# Start everything with Docker
docker-compose up

# Access at:
# Frontend: http://localhost:8080
# Backend: http://localhost:8000
```

## Troubleshooting

### "Module not found" error
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Port 8000 already in use
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn main:app --port 8001
```

### Frontend shows "Disconnected"
- Make sure backend is running on port 8000
- Check browser console for errors
- Wait 10 seconds for initial data generation

### No sensor data appearing
- Backend auto-generates simulated data
- Wait 10-15 seconds after startup
- Check backend terminal for logs

## Next Steps

1. **Explore the API** - Visit http://localhost:8000/docs
2. **Customize Equipment** - Edit `backend/main.py` 
3. **Adjust ML Model** - Modify `AnomalyDetector` class
4. **Deploy to Production** - See DEPLOYMENT.md

## System Overview

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  Frontend   │ ◄─────► │   Backend    │ ◄─────► │  Database   │
│  (Browser)  │ WebSocket│   (FastAPI)  │         │  (SQLite)   │
│             │         │   + ML Model │         │             │
└─────────────┘         └──────────────┘         └─────────────┘
```

## Key URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:8080 | Main dashboard |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| ReDoc | http://localhost:8000/redoc | Alternative API docs |

## Sample API Calls

### Get Equipment List
```bash
curl http://localhost:8000/api/equipment
```

### Submit Sensor Data
```bash
curl -X POST http://localhost:8000/api/sensor-data \
  -H "Content-Type: application/json" \
  -d '{
    "equipment_id": 1,
    "temperature": 85.5,
    "vibration": 7.2,
    "pressure": 135.0,
    "power_consumption": 92.0,
    "efficiency": 78.0
  }'
```

### Get Alerts
```bash
curl http://localhost:8000/api/alerts?acknowledged=false
```

## Features to Try

✓ Click on equipment cards for details
✓ Filter equipment by status (All/Critical/Warning/Healthy)
✓ Watch real-time sensor data updates
✓ See ML predictions and confidence scores
✓ Acknowledge alerts
✓ View maintenance schedule

## Getting Help

- Read the full **README.md** for detailed documentation
- Check **DEPLOYMENT.md** for production deployment
- Review **PROJECT_STRUCTURE.md** for architecture details
- Visit http://localhost:8000/docs for API reference

## Common Questions

**Q: Can I use real sensor data?**
A: Yes! Just POST to `/api/sensor-data` endpoint with your data.

**Q: How do I connect my IoT devices?**
A: Use the REST API endpoints documented at `/docs`.

**Q: Can I change the database?**
A: Yes, edit the database connection in `main.py`. For production, use PostgreSQL.

**Q: Is this production-ready?**
A: The core system is production-ready. Add authentication, use PostgreSQL, and follow the production checklist in DEPLOYMENT.md.

**Q: How do I add more equipment?**
A: Edit the `seed_initial_data()` function in `backend/main.py`.

---

**You're ready to go! 🎉**

The system is now monitoring equipment and detecting anomalies in real-time.
