from qdrant_client import QdrantClient
import sys

client = QdrantClient(path="./qdrant_storage")
collection_name = "mindvault_memories"

model_name = "all-MiniLM-L6-v2"
# We can't easily encode without the model, so let's just scroll/scan
# Or just list all points?

print(f"Counting points in {collection_name}...")
count = client.count(collection_name).count
print(f"Total count: {count}")

print("Scanning points...")
scroll_result, _ = client.scroll(
    collection_name=collection_name,
    limit=10,
    with_payload=True
)

for point in scroll_result:
    p = point.payload
    if "overwhelmed" in p.get("experience_text", "").lower():
        print(f"ID: {point.id}")
        print(f"Text: {p.get('experience_text')}")
        print(f"Score: {p.get('acceptance_score')}")
        print("-" * 20)

sys.stdout.flush()
