from mindvault_core import MindVaultCore

system = MindVaultCore()
count = system.client.count(collection_name=system.collection_name).count
print(f"Collection count: {count}")
if count > 0:
    print("Verification SUCCESS: Data found.")
else:
    print("Verification FAILED: Collection is empty.")
