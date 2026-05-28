import json
import time
from coral_executor import CoralExecutor
from pathlib import Path

class DarwinLoop:
    def __init__(self):
        self.coral = CoralExecutor()
        self.mutations_file = Path("mutations.json")
        self.mutations = self._load_mutations()
    
    def _load_mutations(self):
        if self.mutations_file.exists():
            return json.loads(self.mutations_file.read_text())
        return {"mutations": []}
    
    def _save_mutations(self):
        self.mutations_file.write_text(json.dumps(self.mutations, indent=2))
    
    def learn(self, query: str, result: dict):
        if result.get("row_count", 0) > 0:
            mutation = {
                "pattern": f"Query '{query[:50]}' returned {result['row_count']} rows",
                "timestamp": time.time()
            }
            self.mutations["mutations"].append(mutation)
            self._save_mutations()
            return True
        return False
    
    def investigate(self, incident_id: str, queries: list) -> dict:
        start = time.time()
        
        for i, query in enumerate(queries, 1):
            print(f"\n🔁 Loop {i}: {query}")
            result = self.coral.execute_query(query)
            
            if self.learn(query, result):
                print(f"   🧬 Learned new pattern!")
            print(f"   📊 Returned {result.get('row_count', 0)} rows")
            
            if result.get("row_count", 0) > 0 and result.get("data"):
                print(f"   📝 Sample: {result['data'][0]}")
        
        return {
            "incident_id": incident_id,
            "loops_completed": len(queries),
            "duration_seconds": round(time.time() - start, 2),
            "total_mutations": len(self.mutations["mutations"])
        }

if __name__ == "__main__":
    darwin = DarwinLoop()
    
    queries = [
        "SELECT login FROM github.user LIMIT 1",
        "SELECT name FROM github.repositories LIMIT 2",
        "SELECT login FROM github.user LIMIT 1"
    ]
    
    print("🏴‍☠️ Security Trinity - Darwin Loop")
    print("=" * 40)
    
    result = darwin.investigate("SEC-001", queries)
    
    print("\n" + "=" * 40)
    print("✅ Complete:")
    print(json.dumps(result, indent=2))
    print("\n🧬 Mutations saved to mutations.json")
