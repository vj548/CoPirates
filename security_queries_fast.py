from coral_executor import CoralExecutor

coral = CoralExecutor()

# Fast queries only - no heavy filters
queries = [
    "SELECT name, private FROM github.repositories LIMIT 5",
    "SELECT login FROM github.user",
    "SELECT name FROM github.repositories LIMIT 3"
]

print("🔐 Security Investigation Results")
print("=" * 50)

for query in queries:
    print(f"\n📝 Query: {query}")
    result = coral.execute_query(query)
    print(f"   ✅ {result.get('row_count', 0)} rows returned")
    if result.get('data'):
        print(f"   📝 Sample: {result['data'][0]}")
