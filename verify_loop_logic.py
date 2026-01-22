from mindvault_core import MindVaultCore
import sys

system = MindVaultCore()
recs = system.find_recommendation("overwhelmed")
if not recs:
    print("No memory found.")
    sys.exit(1)

mem_id = recs[0]['id']
print(f"Target Memory: {recs[0]['similar_experience']}")

simulate_inputs = [5, 7, 9]

for i, feedback in enumerate(simulate_inputs):
    new_score = feedback / 10.0
    print(f"Week {i+1} update: {new_score}")
    system.update_feedback(mem_id, new_score)

# Final check
# We need to re-fetch/search to get updated data
recs = system.find_recommendation("overwhelmed")
# Find the specific memory ID in case order changed (unlikely with just score update)
final_mem = next((m for m in recs if m['id'] == mem_id), None)

if final_mem:
    print(f"Final Score in DB: {final_mem['acceptance']}")
    if abs(final_mem['acceptance'] - 0.9) < 0.001:
        print("SUCCESS: Loop logic updated score correctly.")
    else:
        print("FAILURE: Score mismatch.")
else:
    print("FAILURE: Memory lost??")
