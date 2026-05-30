#!/usr/bin/env python3
import requests
import uuid

THEHIVE_URL = "http://localhost:9000"
THEHIVE_API_KEY = "4lhBlNvV6lgDcUiKHj+FHpfI7Ozu/SYl"

CORTEX_URL = "http://localhost:9001"
CORTEX_API_KEY = "oYMPnNSpR/Mz3i83uNuOhgIhTywimHSx"

print("🔌 Security Trinity Integration - TheHive 3.x")
print("="*50)

headers = {
    "Authorization": f"Bearer {THEHIVE_API_KEY}",
    "Content-Type": "application/json"
}

# 1. Create a Case
print("\n📡 Creating case in TheHive...")
case_data = {
    "title": "[Security Trinity] Coral Cross-Source Investigation",
    "description": """
    Security Trinity detected patterns across:
    - GitHub: jrieken (12,778 contributions)
    - Slack: social channel  
    - Sentry: javascript-nextjs project
    
    Darwin mutation: GitHub contributors correlate with Slack channels
    """,
    "severity": 2,
    "tags": ["coral", "github", "slack", "sentry", "darwin"],
    "tlp": 2,
    "pap": 1
}

try:
    resp = requests.post(f"{THEHIVE_URL}/api/case", headers=headers, json=case_data)
    if resp.status_code in [200, 201]:
        case = resp.json()
        print(f"✅ Case created!")
        print(f"   ID: {case.get('id')}")
        print(f"   Case Number: {case.get('caseId')}")
        print(f"   View: {THEHIVE_URL}/case/{case.get('id')}")
    else:
        print(f"❌ Failed: {resp.status_code}")
        print(f"   {resp.text[:200]}")
except Exception as e:
    print(f"❌ Error: {e}")

# 2. Create an Alert
print("\n📡 Creating alert...")
alert_data = {
    "title": "[Security Trinity] Suspicious Activity Alert",
    "description": "Coral cross-source join detected unusual patterns",
    "type": "coral",
    "source": "SecurityTrinity",
    "sourceRef": f"ST-{uuid.uuid4().hex[:8]}",
    "severity": 2,
    "tags": ["coral", "auto-detected"]
}

try:
    resp = requests.post(f"{THEHIVE_URL}/api/alert", headers=headers, json=alert_data)
    if resp.status_code in [200, 201]:
        alert = resp.json()
        print(f"✅ Alert created!")
        print(f"   ID: {alert.get('id')}")
    else:
        print(f"⚠️ Alert creation: {resp.status_code}")
except Exception as e:
    print(f"❌ Alert error: {e}")

# 3. Test Cortex Connection
print("\n📡 Testing Cortex...")
try:
    resp = requests.get(f"{CORTEX_URL}/api/analyzer", auth=("admin", CORTEX_API_KEY))
    if resp.status_code == 200:
        print(f"✅ Cortex connected! {len(resp.json())} analyzers available")
    else:
        print(f"⚠️ Cortex: {resp.status_code}")
except Exception as e:
    print(f"❌ Cortex error: {e}")

print("\n" + "="*50)
print("🏴‍☠️ Check TheHive UI: http://localhost:9000")