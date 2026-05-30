from coral_executor import CoralExecutor
import json

coral = CoralExecutor()

# Lightweight security queries (no heavy ORDER BY)
queries = [
    "SELECT name, private FROM github.repositories LIMIT 5",
    "SELECT login, type FROM github.user",
    "SELECT name FROM github.repositories WHERE stargazers_count > 100 LIMIT 3"
]

print("🔐 Security Investigation Results")
print("=" * 50)

for query in queries:
    print(f"\n📝 Query: {query}")
    result = coral.execute_query(query)
    print(f"   Results: {result.get('row_count', 0)} rows")
    if result.get('data'):
        for row in result['data'][:3]:
            print(f"   → {row}")
