from mindvault_core import MindVaultCore
import sys

system = MindVaultCore()
query = "overwhelmed"

print(f"Finding memory for '{query}'...")
recs = system.find_recommendation(query)
if not recs:
    print("No memory found.")
    sys.exit(1)

target_memory = recs[0]
score = target_memory['acceptance']
print(f"Final Score: {score}")

if abs(score - 0.9) < 0.001:
    print("SUCCESS: Final score matches last feedback (0.9).")
else:
    print(f"FAILURE: Final score {score} != 0.9")
