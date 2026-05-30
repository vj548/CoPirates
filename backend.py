from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
import requests
from datetime import datetime
import os

app = FastAPI()

# Enable CORS for dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Coral path
CORAL_PATH = "/mnt/c/Users/GOUSHIK/OneDrive/Desktop/CoPirates/coral.exe"

# Cortex endpoints
CORTEX_URL = "http://localhost:9001"
THEHIVE_URL = "http://localhost:9000"

# Shannon workspace
SHANNON_WORKSPACE = "/home/goushik/shannon-with-deepseek"

# Darwin mutations file
MUTATIONS_FILE = "darwin_mutations.json"

@app.get("/api/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/coral/query")
def coral_query(sql: str):
    """Execute Coral SQL query"""
    try:
        result = subprocess.run(
            [CORAL_PATH, "sql", sql],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {"success": True, "output": result.stdout, "error": result.stderr}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Query timeout"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/coral/sources")
def coral_sources():
    """List all Coral sources"""
    try:
        result = subprocess.run(
            [CORAL_PATH, "source", "list"],
            capture_output=True,
            text=True
        )
        return {"success": True, "sources": result.stdout}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/darwin/mutations")
def get_mutations():
    """Get Darwin learned mutations"""
    if os.path.exists(MUTATIONS_FILE):
        with open(MUTATIONS_FILE, 'r') as f:
            return json.load(f)
    return {"mutations": []}

@app.post("/api/darwin/mutations")
def add_mutation(mutation: dict):
    """Add a new mutation learned by Darwin"""
    mutations = []
    if os.path.exists(MUTATIONS_FILE):
        with open(MUTATIONS_FILE, 'r') as f:
            mutations = json.load(f)
    
    mutation["id"] = f"MUT-{len(mutations)+1}"
    mutation["created_at"] = datetime.now().isoformat()
    mutations.append(mutation)
    
    with open(MUTATIONS_FILE, 'w') as f:
        json.dump(mutations, f, indent=2)
    
    return {"success": True, "mutation": mutation}

@app.get("/api/cortex/status")
def cortex_status():
    """Check if Cortex is running"""
    try:
        response = requests.get(f"{CORTEX_URL}/api/status", timeout=5)
        return {"running": response.status_code == 200, "version": response.json().get("version")}
    except:
        return {"running": False, "error": "Cortex not reachable"}

@app.get("/api/thehive/status")
def thehive_status():
    """Check if TheHive is running"""
    try:
        response = requests.get(f"{THEHIVE_URL}/api/v1/status", timeout=5)
        return {"running": response.status_code == 200}
    except:
        return {"running": False, "error": "TheHive not reachable"}

@app.get("/api/shannon/status")
def shannon_status():
    """Check Shannon worker status"""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=shannon", "--format", "json"],
            capture_output=True,
            text=True
        )
        return {"running": "shannon" in result.stdout}
    except:
        return {"running": False}

@app.post("/api/shannon/scan")
def start_shannon_scan(target_url: str, repo_path: str):
    """Start a Shannon scan"""
    try:
        result = subprocess.run(
            ["docker", "run", "--rm", "shannon-worker", "scan", "-u", target_url, "-r", repo_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        return {"success": True, "output": result.stdout}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/investigation/full")
def full_investigation(incident_id: str):
    """Run full Security Trinity investigation"""
    # Step 1: Run Coral query across all sources
    coral_query = """
    SELECT 
        g.login as github_user,
        g.contributions,
        s.name as slack_channel,
        p.slug as sentry_project,
        'Connected' as pagerduty_status
    FROM github.repo_contributors g
    CROSS JOIN slack.channels s
    CROSS JOIN sentry.projects p
    WHERE g.owner = 'microsoft' 
      AND g.repo = 'vscode'
    LIMIT 3
    """
    
    coral_result = subprocess.run(
        [CORAL_PATH, "sql", coral_query],
        capture_output=True,
        text=True
    )
    
    # Step 2: Learn pattern (Darwin mutation)
    mutation = {
        "pattern": "GitHub contributors correlate with Slack channels and Sentry projects",
        "source": "full_investigation",
        "incident_id": incident_id
    }
    
    with open(MUTATIONS_FILE, 'a') as f:
        json.dump(mutation, f)
        f.write("\n")
    
    return {
        "incident_id": incident_id,
        "coral_results": coral_result.stdout,
        "darwin_mutation": mutation,
        "cortex_status": "ready",
        "thehive_status": "ready",
        "shannon_status": "idle",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)