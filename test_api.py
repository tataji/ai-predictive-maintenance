#!/usr/bin/env python3
"""
API Testing Script for AI Predictive Maintenance System
Tests all major endpoints and functionality
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Root endpoint: {data['message']}")
    return True

def test_equipment_list():
    """Test equipment listing"""
    print("\nTesting equipment list...")
    response = requests.get(f"{BASE_URL}/api/equipment")
    assert response.status_code == 200
    data = response.json()
    equipment_count = len(data['equipment'])
    print(f"✓ Found {equipment_count} equipment")
    return data['equipment']

def test_equipment_detail(equipment_id):
    """Test equipment detail endpoint"""
    print(f"\nTesting equipment detail for ID {equipment_id}...")
    response = requests.get(f"{BASE_URL}/api/equipment/{equipment_id}")
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Equipment: {data['equipment']['name']}")
    return data

def test_sensor_data_submission():
    """Test sensor data submission"""
    print("\nTesting sensor data submission...")
    
    sensor_data = {
        "equipment_id": 1,
        "temperature": 85.5,
        "vibration": 7.2,
        "pressure": 135.0,
        "power_consumption": 92.0,
        "efficiency": 78.0
    }
    
    response = requests.post(
        f"{BASE_URL}/api/sensor-data",
        json=sensor_data
    )
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Sensor data recorded: {data['status']}")
    print(f"  Anomaly detected: {data['anomaly_detected']}")
    print(f"  Confidence: {data['confidence']:.2f}%")
    return data

def test_alerts():
    """Test alerts endpoint"""
    print("\nTesting alerts...")
    response = requests.get(f"{BASE_URL}/api/alerts?acknowledged=false")
    assert response.status_code == 200
    data = response.json()
    alert_count = len(data['alerts'])
    print(f"✓ Found {alert_count} active alerts")
    return data['alerts']

def test_predictions():
    """Test predictions endpoint"""
    print("\nTesting predictions...")
    response = requests.get(f"{BASE_URL}/api/predictions")
    assert response.status_code == 200
    data = response.json()
    prediction_count = len(data['predictions'])
    print(f"✓ Found {prediction_count} predictions")
    return data['predictions']

def test_maintenance_schedule():
    """Test maintenance schedule"""
    print("\nTesting maintenance schedule...")
    response = requests.get(f"{BASE_URL}/api/maintenance")
    assert response.status_code == 200
    data = response.json()
    schedule_count = len(data['schedule'])
    print(f"✓ Found {schedule_count} scheduled maintenance tasks")
    return data['schedule']

def test_create_maintenance_task():
    """Test creating maintenance task"""
    print("\nTesting maintenance task creation...")
    
    task = {
        "equipment_id": 1,
        "task": "Test maintenance task",
        "scheduled_date": "2024-12-25",
        "priority": "medium"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/maintenance",
        json=task
    )
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Maintenance task created: ID {data['task_id']}")
    return data

def test_dashboard_stats():
    """Test dashboard statistics"""
    print("\nTesting dashboard statistics...")
    response = requests.get(f"{BASE_URL}/api/dashboard-stats")
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Dashboard stats:")
    print(f"  Equipment online: {data['equipment_online']}")
    print(f"  Active alerts: {data['active_alerts']}")
    print(f"  Cost saved MTD: {data['cost_saved_mtd']}")
    return data

def test_acknowledge_alert(alert_id):
    """Test acknowledging an alert"""
    print(f"\nTesting alert acknowledgment for ID {alert_id}...")
    response = requests.post(f"{BASE_URL}/api/alerts/{alert_id}/acknowledge")
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Alert acknowledged: {data['status']}")
    return data

def run_comprehensive_test():
    """Run all tests"""
    print("="*60)
    print("AI Predictive Maintenance System - API Test Suite")
    print("="*60)
    
    try:
        # Test basic endpoints
        test_root()
        equipment = test_equipment_list()
        
        if equipment:
            test_equipment_detail(equipment[0]['id'])
        
        # Test sensor data and ML
        test_sensor_data_submission()
        
        # Wait a moment for processing
        time.sleep(1)
        
        # Test analysis endpoints
        predictions = test_predictions()
        alerts = test_alerts()
        test_maintenance_schedule()
        
        # Test dashboard
        test_dashboard_stats()
        
        # Test task creation
        test_create_maintenance_task()
        
        # Test alert acknowledgment
        if alerts:
            test_acknowledge_alert(alerts[0]['id'])
        
        print("\n" + "="*60)
        print("✓ All tests passed successfully!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except requests.exceptions.ConnectionError:
        print("\n✗ Connection error: Is the backend running on http://localhost:8000?")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False
    
    return True

def stress_test_sensor_data(count=100):
    """Stress test with multiple sensor readings"""
    print(f"\nStress testing with {count} sensor readings...")
    import random
    
    success_count = 0
    anomaly_count = 0
    
    for i in range(count):
        sensor_data = {
            "equipment_id": random.randint(1, 6),
            "temperature": 65 + random.uniform(-10, 25),
            "vibration": 2 + random.uniform(-1, 8),
            "pressure": 110 + random.uniform(-15, 35) if random.random() > 0.3 else None,
            "power_consumption": 80 + random.uniform(-15, 15),
            "efficiency": 90 + random.uniform(-15, 8)
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/sensor-data",
                json=sensor_data
            )
            if response.status_code == 200:
                success_count += 1
                if response.json()['anomaly_detected']:
                    anomaly_count += 1
        except:
            pass
        
        if (i + 1) % 20 == 0:
            print(f"  Progress: {i + 1}/{count}")
    
    print(f"✓ Stress test complete:")
    print(f"  Successful submissions: {success_count}/{count}")
    print(f"  Anomalies detected: {anomaly_count}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--stress":
        stress_test_sensor_data(100)
    else:
        run_comprehensive_test()
