from mindvault_core import MindVaultCore
import sys

system = MindVaultCore()
query = "overwhelmed"

# 1. Find the memory
print(f"Finding memory for '{query}'...")
recs = system.find_recommendation(query)
if not recs:
    print("No memory found to update.")
    sys.exit(1)

target_memory = recs[0]
mem_id = target_memory['id']
print(f"Target Memory ID: {mem_id}")
print(f"Current Score: {target_memory['acceptance']}")

# 2. Update the score
new_score = 0.123
print(f"Updating score to {new_score}...")
system.update_feedback(mem_id, new_score)

# 3. Verify
print("Verifying update...")
# We need to fetch directly or search again
# Fetching by ID is safer but search is what we use.
# Let's search again.
recs_after = system.find_recommendation(query)
updated_memory = next((m for m in recs_after if m['id'] == mem_id), None)

if updated_memory:
    print(f"New Score: {updated_memory['acceptance']}")
    if abs(updated_memory['acceptance'] - new_score) < 0.001:
        print("SUCCESS: Score updated correctly.")
    else:
        print("FAILURE: Score did not match.")
else:
    print("FAILURE: Could not find memory after update.")
