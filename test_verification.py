from mindvault_core import MindVaultCore
import shutil
import os

# Clean up previous test runs
if os.path.exists("./qdrant_storage_test"):
    shutil.rmtree("./qdrant_storage_test")

print("Initializing MindVault Core...")
system = MindVaultCore(persistence_path="./qdrant_storage_test")

print("\n1. Seeding Data...")
seed_data = [
    ("I am anxious about exams", "Deep Breathing", "Anxiety", 0.9),
    ("I feel sad and alone", "Call a friend", "Sadness", 0.8)
]
for exp, strat, emo, score in seed_data:
    system.add_experience(exp, strat, emo, score)
    print(f"Added: {exp} -> {strat}")

print("\n2. Testing Search...")
query = "I am really worried about my upcoming test"
print(f"Query: {query}")
recs = system.find_recommendation(query, top_k=1)

if recs:
    print("✓ Success! Recommendation found:")
    print(recs[0])
    assert "Deep Breathing" in recs[0]['strategy']
else:
    print("✗ Failure: No recommendation found.")
    exit(1)

print("\n3. Testing Feedback Loop...")
memory_id = recs[0]['id']
new_score = 1.0
system.update_feedback(memory_id, new_score)
print(f"Updated score to {new_score}")

# Verify update
# Need to search/retrieve again to check payload, or just trust the method for now. 
# Let's simple search again.
recs_after = system.find_recommendation(query, top_k=1)
print(f"New Score in DB: {recs_after[0]['acceptance']}")
assert recs_after[0]['acceptance'] == 1.0

print("\n✓ SYSTEM VERIFIED SUCCESSFULLY")
