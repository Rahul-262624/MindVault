import os
import uuid
import datetime
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import numpy as np

class MindVaultCore:
    def __init__(self, collection_name: str = "mindvault_memories", persistence_path: str = "./qdrant_storage", url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize MindVault with Qdrant and Embedding Model.
        """
        self.collection_name = collection_name
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize Qdrant (Persistent Local Storage or Cloud)
        if url and api_key:
             self.client = QdrantClient(url=url, api_key=api_key)
        else:
             self.client = QdrantClient(path=persistence_path)
        
        self._ensure_collection()

    def _ensure_collection(self):
        """
        Create the Qdrant collection if it doesn't exist.
        """
        collections = self.client.get_collections()
        exists = any(c.name == self.collection_name for c in collections.collections)

        if not exists:
            # Vector size for all-MiniLM-L6-v2 is 384
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=384,
                    distance=models.Distance.COSINE
                )
            )
            print(f"Created collection: {self.collection_name}")

    def add_experience(self, 
                      experience_text: str, 
                      strategy_text: str, 
                      emotion_label: str,
                      acceptance_score: float = 0.5) -> str:
        """
        Store a new memory: Experience + Strategy + Outcome.
        """
        vector = self.embedding_model.encode(experience_text).tolist()
        memory_id = str(uuid.uuid4())
        
        payload = {
            "experience_text": experience_text,
            "strategy_text": strategy_text,
            "emotion_label": emotion_label,
            "acceptance_score": acceptance_score,
            "timestamp": datetime.datetime.now().isoformat()
        }

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=memory_id,
                    vector=vector,
                    payload=payload
                )
            ]
        )
        return memory_id

    def find_recommendation(self, current_experience: str, top_k: int = 3) -> List[Dict]:
        """
        Find relevant strategies based on semantic similarity to current experience.
        Ranks by a combination of Similarity + Acceptance Score.
        """
        query_vector = self.embedding_model.encode(current_experience).tolist()

        # 1. Retrieve similar past cases from Qdrant
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k * 2,  # Fetch more to re-rank
            with_payload=True
        ).points

        recommendations = []
        for hit in search_result:
            payload = hit.payload
            similarity = hit.score
            acceptance = payload.get("acceptance_score", 0.5)
            
            # 2. Ranking Logic: Hybrid Score
            # Weight similarity high (relevance) but boost by success history
            # Score = (Similarity * 0.7) + (AcceptanceScore * 0.3)
            final_score = (similarity * 0.7) + (acceptance * 0.3)
            
            recommendations.append({
                "id": hit.id,
                "strategy": payload.get("strategy_text"),
                "similar_experience": payload.get("experience_text"),
                "emotion": payload.get("emotion_label"),
                "similarity": similarity,
                "acceptance": acceptance,
                "final_score": final_score
            })

        # Sort by final hybrid score
        recommendations.sort(key=lambda x: x["final_score"], reverse=True)
        return recommendations[:top_k]

    def update_feedback(self, memory_id: str, new_score: float):
        """
        Update the acceptance score of a specific memory after the 21-day cycle.
        """
        # Qdrant supports payload updates
        self.client.set_payload(
            collection_name=self.collection_name,
            payload={
                "acceptance_score": new_score,
                "last_updated": datetime.datetime.now().isoformat()
            },
            points=[memory_id]
        )
