import os
import time
import random
import requests
from faker import Faker
from dotenv import load_dotenv

load_dotenv()
fake = Faker()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook-test/datadog-incident")

DATADOG_ALERTS = [
    {
        "title": "[Triggered] Unauthorized SSH Brute Force Detected",
        "alert_type": "error",
        "text": "Multiple failed SSH login attempts detected from single IP over 60s window.",
        "tags": ["env:production", "service:auth-service", "security:critical"]
    },
    {
        "title": "[Triggered] High CPU Utilization on Core Database",
        "alert_type": "warning",
        "text": "Database host CPU usage sustained > 90% for past 10 minutes.",
        "tags": ["env:production", "service:postgres", "team:database"]
    },
    {
        "title": "[Triggered] Anomalous Outbound Traffic Spike",
        "alert_type": "error",
        "text": "Unusual outbound egress data volume detected on edge router.",
        "tags": ["env:production", "service:gateway", "security:high"]
    },
    {
        "title": "[OK] Memory Usage Normalizing",
        "alert_type": "info",
        "text": "Memory utilization dropped below 60% threshold.",
        "tags": ["env:staging", "service:cache", "team:ops"]
    }
]

def generate_datadog_payload():
    alert = random.choice(DATADOG_ALERTS)
    event_id = str(random.randint(1000000000, 9999999999))
    hostname = f"prod-node-{random.randint(100, 999)}.datadoghq.internal"
    
    return {
        "id": event_id,
        "title": alert["title"],
        "text": alert["text"],
        "date": int(time.time()),
        "event_type": "metric_alert_monitor",
        "alert_type": alert["alert_type"],
        "hostname": hostname,
        "source_ip": fake.ipv4(),
        "tags": alert["tags"],
        "link": f"https://app.datadoghq.com/event/event?id={event_id}"
    }

def run_generator(interval=8):
    print(f"📡 Datadog Telemetry Generator active. Pushing webhooks to {N8N_WEBHOOK_URL} every {interval}s...")
    while True:
        payload = generate_datadog_payload()
        try:
            res = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=5)
            print(f"[{payload['alert_type'].upper()}] Pushed: {payload['title']} -> n8n HTTP {res.status_code}")
        except Exception as e:
            print(f"⚠️ Connection error to n8n webhook: {e}")
        time.sleep(interval)

if __name__ == "__main__":
    run_generator(interval=8)