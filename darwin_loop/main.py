import json 
import os 
from datetime import datetime 
 
class DarwinLoop: 
    def __init__(self): 
        self.loop_count = 0 
        self.mutations = self.load_mutations() 
 
    def load_mutations(self): 
        path = "darwin_loop/memory/mutations.json" 
        if os.path.exists(path): 
            return json.load(open(path)) 
        return {"mutations": []} 
 
    def investigate(self, incident_id, query): 
        print(f"Investigating {incident_id}") 
        self.loop_count += 1 
        return {"incident_id": incident_id, "loops": self.loop_count} 
 
if __name__ == "__main__": 
    darwin = DarwinLoop() 
    result = darwin.investigate("TEST-001", "SELECT * FROM github.pulls") 
    print(result) 
