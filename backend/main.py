"""
AI Predictive Maintenance System - Main Backend
FastAPI application with real ML-based anomaly detection
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
import asyncio
import json
from datetime import datetime, timedelta
import random
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import sqlite3
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Predictive Maintenance System",
    description="Real-time equipment monitoring with ML-based failure prediction",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization
DB_PATH = Path(__file__).parent / "maintenance.db"

def init_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Equipment table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            location TEXT,
            install_date TEXT,
            last_maintenance TEXT,
            status TEXT DEFAULT 'healthy'
        )
    """)
    
    # Sensor readings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id INTEGER,
            timestamp TEXT NOT NULL,
            temperature REAL,
            vibration REAL,
            pressure REAL,
            power_consumption REAL,
            efficiency REAL,
            FOREIGN KEY (equipment_id) REFERENCES equipment (id)
        )
    """)
    
    # Predictions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id INTEGER,
            timestamp TEXT NOT NULL,
            prediction_type TEXT,
            confidence REAL,
            predicted_failure_date TEXT,
            recommendation TEXT,
            FOREIGN KEY (equipment_id) REFERENCES equipment (id)
        )
    """)
    
    # Maintenance schedule table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id INTEGER,
            task TEXT NOT NULL,
            scheduled_date TEXT NOT NULL,
            priority TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT,
            FOREIGN KEY (equipment_id) REFERENCES equipment (id)
        )
    """)
    
    # Alerts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id INTEGER,
            timestamp TEXT NOT NULL,
            severity TEXT,
            title TEXT,
            description TEXT,
            acknowledged INTEGER DEFAULT 0,
            FOREIGN KEY (equipment_id) REFERENCES equipment (id)
        )
    """)
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

# Initialize database on startup
init_database()

# Pydantic models
class SensorReading(BaseModel):
    equipment_id: int
    temperature: float
    vibration: float
    pressure: Optional[float] = None
    power_consumption: float
    efficiency: float

class Equipment(BaseModel):
    id: int
    name: str
    type: str
    location: Optional[str] = None
    status: str = "healthy"

class Prediction(BaseModel):
    equipment_id: int
    prediction_type: str
    confidence: float
    predicted_failure_date: Optional[str] = None
    recommendation: str

class MaintenanceTask(BaseModel):
    equipment_id: int
    task: str
    scheduled_date: str
    priority: str

class Alert(BaseModel):
    equipment_id: int
    severity: str
    title: str
    description: str

# ML Model for Anomaly Detection
class AnomalyDetector:
    """Machine Learning based anomaly detection using Isolation Forest"""
    
    def __init__(self):
        self.model = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def train(self, data: np.ndarray):
        """Train the anomaly detection model"""
        if len(data) < 10:
            logger.warning("Not enough data to train model")
            return False
            
        scaled_data = self.scaler.fit_transform(data)
        self.model.fit(scaled_data)
        self.is_trained = True
        logger.info(f"Model trained with {len(data)} samples")
        return True
    
    def predict(self, data: np.ndarray) -> tuple:
        """Predict anomaly score and classification"""
        if not self.is_trained:
            return 0, 0.5
            
        scaled_data = self.scaler.transform(data)
        prediction = self.model.predict(scaled_data)[0]
        score = self.model.score_samples(scaled_data)[0]
        
        # Convert to confidence (0-100)
        # Lower scores indicate anomalies
        confidence = max(0, min(100, (1 - abs(score)) * 100))
        
        return prediction, confidence

# Global anomaly detector
anomaly_detector = AnomalyDetector()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.active_connections.remove(connection)

manager = ConnectionManager()

# Helper functions
def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def seed_initial_data():
    """Seed database with initial equipment data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM equipment")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    equipment_data = [
        (1, 'Hydraulic Press #1', 'press', 'Factory Floor A', '2020-03-15', '2024-11-01', 'healthy'),
        (2, 'CNC Mill #3', 'mill', 'Workshop B', '2019-07-22', '2024-10-15', 'healthy'),
        (3, 'Compressor Unit A', 'compressor', 'Utility Room', '2021-01-10', '2024-11-20', 'healthy'),
        (4, 'Conveyor Belt #2', 'conveyor', 'Assembly Line', '2020-05-18', '2024-11-10', 'healthy'),
        (5, 'Injection Molder #1', 'molder', 'Production Zone C', '2018-11-30', '2024-10-25', 'healthy'),
        (6, 'Packaging Robot #4', 'robot', 'Packaging Area', '2022-02-14', '2024-12-01', 'healthy'),
    ]
    
    cursor.executemany(
        "INSERT INTO equipment VALUES (?, ?, ?, ?, ?, ?, ?)",
        equipment_data
    )
    
    conn.commit()
    conn.close()
    logger.info("Initial equipment data seeded")

seed_initial_data()

# API Endpoints

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "AI Predictive Maintenance System API",
        "version": "1.0.0",
        "endpoints": {
            "equipment": "/api/equipment",
            "sensor_data": "/api/sensor-data/{equipment_id}",
            "predictions": "/api/predictions",
            "alerts": "/api/alerts",
            "maintenance": "/api/maintenance",
            "websocket": "/ws"
        }
    }

@app.get("/api/equipment")
async def get_equipment():
    """Get all equipment with current status"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT e.*, 
               (SELECT COUNT(*) FROM alerts a WHERE a.equipment_id = e.id AND a.acknowledged = 0) as alert_count
        FROM equipment e
    """)
    
    equipment = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {"equipment": equipment}

@app.get("/api/equipment/{equipment_id}")
async def get_equipment_detail(equipment_id: int):
    """Get detailed information about specific equipment"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM equipment WHERE id = ?", (equipment_id,))
    equipment = cursor.fetchone()
    
    if not equipment:
        conn.close()
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    # Get recent sensor readings
    cursor.execute("""
        SELECT * FROM sensor_readings 
        WHERE equipment_id = ? 
        ORDER BY timestamp DESC 
        LIMIT 100
    """, (equipment_id,))
    
    readings = [dict(row) for row in cursor.fetchall()]
    
    # Get latest prediction
    cursor.execute("""
        SELECT * FROM predictions 
        WHERE equipment_id = ? 
        ORDER BY timestamp DESC 
        LIMIT 1
    """, (equipment_id,))
    
    prediction = cursor.fetchone()
    
    conn.close()
    
    return {
        "equipment": dict(equipment),
        "recent_readings": readings,
        "latest_prediction": dict(prediction) if prediction else None
    }

@app.post("/api/sensor-data")
async def record_sensor_data(reading: SensorReading):
    """Record new sensor reading and run anomaly detection"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    
    # Insert sensor reading
    cursor.execute("""
        INSERT INTO sensor_readings 
        (equipment_id, timestamp, temperature, vibration, pressure, power_consumption, efficiency)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        reading.equipment_id, timestamp, reading.temperature, reading.vibration,
        reading.pressure, reading.power_consumption, reading.efficiency
    ))
    
    # Get historical data for training
    cursor.execute("""
        SELECT temperature, vibration, COALESCE(pressure, 0) as pressure, 
               power_consumption, efficiency
        FROM sensor_readings
        WHERE equipment_id = ?
        ORDER BY timestamp DESC
        LIMIT 200
    """, (reading.equipment_id,))
    
    historical_data = np.array([list(row) for row in cursor.fetchall()])
    
    # Train or retrain model if enough data
    if len(historical_data) >= 20:
        anomaly_detector.train(historical_data)
    
    # Run anomaly detection on current reading
    current_data = np.array([[
        reading.temperature, reading.vibration, reading.pressure or 0,
        reading.power_consumption, reading.efficiency
    ]])
    
    prediction, confidence = anomaly_detector.predict(current_data)
    
    # Determine status and create prediction/alert if needed
    status = "healthy"
    alert_created = False
    
    if prediction == -1:  # Anomaly detected
        if confidence > 85:
            status = "critical"
            severity = "critical"
        else:
            status = "warning"
            severity = "warning"
        
        # Create prediction record
        predicted_failure = (datetime.now() + timedelta(days=random.randint(1, 7))).isoformat()
        recommendation = generate_recommendation(reading, status)
        
        cursor.execute("""
            INSERT INTO predictions 
            (equipment_id, timestamp, prediction_type, confidence, predicted_failure_date, recommendation)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            reading.equipment_id, timestamp, 'anomaly_detected', 
            confidence, predicted_failure, recommendation
        ))
        
        # Create alert
        cursor.execute("SELECT name FROM equipment WHERE id = ?", (reading.equipment_id,))
        equipment_name = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO alerts (equipment_id, timestamp, severity, title, description)
            VALUES (?, ?, ?, ?, ?)
        """, (
            reading.equipment_id, timestamp, severity,
            f"{equipment_name} - Anomaly Detected",
            f"AI detected unusual patterns. {recommendation}"
        ))
        
        alert_created = True
        
        # Update equipment status
        cursor.execute(
            "UPDATE equipment SET status = ? WHERE id = ?",
            (status, reading.equipment_id)
        )
    
    conn.commit()
    conn.close()
    
    # Broadcast update via WebSocket
    if alert_created:
        await manager.broadcast({
            "type": "alert",
            "equipment_id": reading.equipment_id,
            "status": status,
            "confidence": confidence
        })
    
    return {
        "status": "success",
        "anomaly_detected": prediction == -1,
        "confidence": confidence,
        "equipment_status": status
    }

def generate_recommendation(reading: SensorReading, status: str) -> str:
    """Generate maintenance recommendation based on sensor data"""
    recommendations = []
    
    if reading.temperature > 80:
        recommendations.append("Temperature exceeds normal range. Check cooling system.")
    if reading.vibration > 7:
        recommendations.append("High vibration detected. Inspect bearings and alignment.")
    if reading.pressure and reading.pressure > 140:
        recommendations.append("Pressure levels elevated. Check seals and valves.")
    if reading.efficiency < 80:
        recommendations.append("Efficiency below optimal. Schedule maintenance.")
    
    if not recommendations:
        if status == "critical":
            recommendations.append("Multiple parameters show concerning trends. Immediate inspection recommended.")
        else:
            recommendations.append("Minor deviation detected. Monitor closely.")
    
    return " ".join(recommendations)

@app.get("/api/predictions")
async def get_predictions():
    """Get all predictions"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.*, e.name as equipment_name
        FROM predictions p
        JOIN equipment e ON p.equipment_id = e.id
        ORDER BY p.timestamp DESC
        LIMIT 50
    """)
    
    predictions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {"predictions": predictions}

@app.get("/api/alerts")
async def get_alerts(acknowledged: Optional[bool] = None):
    """Get alerts, optionally filtered by acknowledgment status"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT a.*, e.name as equipment_name
        FROM alerts a
        JOIN equipment e ON a.equipment_id = e.id
    """
    
    params = []
    if acknowledged is not None:
        query += " WHERE a.acknowledged = ?"
        params.append(1 if acknowledged else 0)
    
    query += " ORDER BY a.timestamp DESC LIMIT 50"
    
    cursor.execute(query, params)
    alerts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {"alerts": alerts}

@app.post("/api/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: int):
    """Acknowledge an alert"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE alerts SET acknowledged = 1 WHERE id = ?", (alert_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Alert not found")
    
    conn.commit()
    conn.close()
    
    return {"status": "success", "alert_id": alert_id}

@app.get("/api/maintenance")
async def get_maintenance_schedule():
    """Get maintenance schedule"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT m.*, e.name as equipment_name
        FROM maintenance_schedule m
        JOIN equipment e ON m.equipment_id = e.id
        WHERE m.status != 'completed'
        ORDER BY m.scheduled_date ASC
    """)
    
    schedule = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {"schedule": schedule}

@app.post("/api/maintenance")
async def create_maintenance_task(task: MaintenanceTask):
    """Create new maintenance task"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO maintenance_schedule 
        (equipment_id, task, scheduled_date, priority, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        task.equipment_id, task.task, task.scheduled_date,
        task.priority, datetime.now().isoformat()
    ))
    
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    
    return {"status": "success", "task_id": task_id}

@app.get("/api/dashboard-stats")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Equipment online
    cursor.execute("SELECT COUNT(*) FROM equipment")
    total_equipment = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM equipment WHERE status = 'healthy'")
    healthy_equipment = cursor.fetchone()[0]
    
    # Active alerts
    cursor.execute("SELECT COUNT(*) FROM alerts WHERE acknowledged = 0")
    active_alerts = cursor.fetchone()[0]
    
    # Calculate cost savings (simplified estimation)
    cursor.execute("""
        SELECT COUNT(*) FROM predictions 
        WHERE timestamp >= date('now', '-30 days')
    """)
    predictions_last_month = cursor.fetchone()[0]
    estimated_savings = predictions_last_month * 3500  # $3500 per prevented failure
    
    conn.close()
    
    return {
        "equipment_online": f"{healthy_equipment}/{total_equipment}",
        "active_alerts": active_alerts,
        "cost_saved_mtd": f"${estimated_savings/1000:.1f}K",
        "total_equipment": total_equipment,
        "healthy_count": healthy_equipment,
        "warning_count": total_equipment - healthy_equipment - active_alerts,
        "critical_count": active_alerts
    }

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming"""
    await manager.connect(websocket)
    
    try:
        while True:
            # Keep connection alive and send periodic updates
            await asyncio.sleep(5)
            
            # Send current stats
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name, status FROM equipment
            """)
            equipment_status = [dict(row) for row in cursor.fetchall()]
            
            conn.close()
            
            await websocket.send_json({
                "type": "status_update",
                "data": equipment_status,
                "timestamp": datetime.now().isoformat()
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# Background task to generate simulated sensor data
async def generate_sensor_data():
    """Generate simulated sensor data for demonstration"""
    await asyncio.sleep(5)  # Wait for startup
    
    equipment_ids = [1, 2, 3, 4, 5, 6]
    
    # Base parameters for each equipment
    base_params = {
        1: {"temp": 75, "vib": 3.5, "press": 120, "power": 85, "eff": 92},
        2: {"temp": 68, "vib": 2.8, "press": 95, "power": 78, "eff": 94},
        3: {"temp": 65, "vib": 2.0, "press": 110, "power": 88, "eff": 96},
        4: {"temp": 58, "vib": 1.5, "press": None, "power": 45, "eff": 95},
        5: {"temp": 72, "vib": 3.2, "press": 125, "power": 92, "eff": 91},
        6: {"temp": 62, "vib": 2.3, "press": None, "power": 55, "eff": 97},
    }
    
    iteration = 0
    
    while True:
        try:
            for eq_id in equipment_ids:
                params = base_params[eq_id]
                
                # Add some variation
                temp = params["temp"] + random.uniform(-3, 3)
                vib = params["vib"] + random.uniform(-0.5, 0.5)
                press = params["press"] + random.uniform(-5, 5) if params["press"] else None
                power = params["power"] + random.uniform(-3, 3)
                eff = params["eff"] + random.uniform(-2, 2)
                
                # Occasionally introduce anomalies (equipment 1 and 5)
                if eq_id in [1, 5] and iteration % 20 == 0:
                    temp += random.uniform(10, 20)
                    vib += random.uniform(3, 6)
                    if press:
                        press += random.uniform(15, 25)
                    eff -= random.uniform(10, 20)
                
                # Create sensor reading
                reading = SensorReading(
                    equipment_id=eq_id,
                    temperature=round(temp, 1),
                    vibration=round(max(0, vib), 1),
                    pressure=round(press, 1) if press else None,
                    power_consumption=round(max(0, power), 1),
                    efficiency=round(min(100, max(0, eff)), 1)
                )
                
                # Record data
                await record_sensor_data(reading)
                
                # Small delay between equipment
                await asyncio.sleep(0.5)
            
            iteration += 1
            # Wait before next cycle
            await asyncio.sleep(10)
            
        except Exception as e:
            logger.error(f"Error generating sensor data: {e}")
            await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    """Start background tasks on application startup"""
    asyncio.create_task(generate_sensor_data())
    logger.info("Application started successfully")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
