import json
import hashlib
from datetime import datetime
from pathlib import Path

class MutationEngine:
    def __init__(self, memory_path="mutations.json"):
        self.memory_path = Path(memory_path)
        self.mutations = self._load_mutations()
    
    def _load_mutations(self):
        if self.memory_path.exists():
            return json.loads(self.memory_path.read_text())
        return {"mutations": []}
    
    def learn_pattern(self, query: str, result: dict, investigation_id: str):
        if result.get("row_count", 0) > 0:
            pattern = f"Query returned {result['row_count']} rows"
            mutation = {
                "id": hashlib.md5(pattern.encode()).hexdigest()[:8],
                "pattern": pattern,
                "query": query[:50],
                "investigation_id": investigation_id,
                "created_at": datetime.now().isoformat()
            }
            self.mutations["mutations"].append(mutation)
            self._save()
            return mutation
        return None
    
    def _save(self):
        self.memory_path.write_text(json.dumps(self.mutations, indent=2))
