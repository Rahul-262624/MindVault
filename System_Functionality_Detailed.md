# MindVault System Functionality Specification

## 1. System Overview
MindVault is an AI-powered therapeutic memory system designed to act as a long-term emotional companion. Unlike stateless chatbots that forget context after a session, MindVault persists emotional experiences and the effectiveness of coping strategies using a vector database (Qdrant). This allows it to recall what worked effectively in the past for similar situations and recommend proven strategies.

## 2. Core Architecture

### 2.1 Technology Stack
*   **Language**: Python 3.8+
*   **Vector Database**: Qdrant (supports both Local persistence and Cloud).
*   **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional vectors).
*   **User Interface**: CLI (Command Line Interface) built with `rich` for interactive menus and visual feedback.

### 2.2 Key Components
*   **`MindVaultCore` (Backend)**: Handles all database interactions.
    *   Manages the Qdrant connection.
    *   Generates vector embeddings for text inputs.
    *   Performs semantic search (`query_points`).
    *   Updates experience scores (`set_payload`).
*   **`main.py` (Frontend)**: Handles user interaction.
    *   Displays the interactive menu.
    *   Manages the simulation loops (e.g., the 3-week feedback cycle).

## 3. Functional Features

### 3.1 Main Menu
Upon launching (`python main.py`), the user is presented with a central navigation hub:
1.  **Find Help (Search)**: Access the retrieval and recommendation engine.
2.  **Add New Memory**: contribute new knowledge to the system.
3.  **Exit**: Terminate the session.

### 3.2 Feature: Find Help (The Recommendation Engine)
This is the core "Therapeutic" loop.
1.  **Input**: The user describes their current emotional state (e.g., "I feel anxious about public speaking").
2.  **Semantic Retrieval**:
    *   The input is converted to a vector.
    *   Qdrant searches the `mindvault_memories` collection for the nearest neighbors (semantically similar past experiences).
3.  **Hybrid Ranking**:
    *   Results are not ranked just by similarity. A custom scoring logic is applied:
    *   `Final Score = (Similarity * 0.7) + (Effectiveness_Score * 0.3)`
    *   This ensures that strategies that *worked well* in the past are prioritized, even if the situation isn't an exact text match.
4.  **Recommendation**: The top-ranked strategy is displayed to the user.

### 3.3 Feature: 3-Week Feedback Simulation
If the user accepts a recommendation, the system enters a simulated longitudinal feedback loop:
*   **Concept**: Habits take time to form. A single "did it work?" check is insufficient.
*   **Process**:
    *   **Week 1**: User is asked for an effectiveness score (0-10). The memory in Qdrant is updated immediately.
    *   **Week 2**: User is asked again. The memory is updated again.
    *   **Week 3**: Final check. The memory is updated.
*   **Outcome**: The system "learns" over time. If a strategy consistently gets low scores, its `Acceptance Score` drops, and it will be less likely to be recommended in the future.

### 3.4 Feature: Add New Memory
Users can expand the system's knowledge base manually.
*   **Inputs**:
    *   **Experience**: The situation description.
    *   **Strategy**: What was done to cope.
    *   **Emotion**: The dominant feeling.
    *   **Score**: How well it worked (0-10).
*   **Storage**: This data is immediately vectorized and upserted into Qdrant. It becomes available for retrieval in the "Find Help" mode instantly.

### 3.5 Feature: Cloud & Local Support
*   **Local Default**: By default, data is stored in `./qdrant_storage` for privacy and offline usage.
*   **Cloud Ready**: The system is capable of connecting to Qdrant Cloud Cluster if an API Key and URL are provided during initialization.

## 4. Data Model
Each memory consists of:
*   **Vector**: 384-float array representing the semantics of the "Experience".
*   **Payload** (Metadata):
    *   `experience_text`: String (e.g., "Felt panic during exam")
    *   `strategy_text`: String (e.g., "Deep breathing")
    *   `emotion_label`: String (e.g., "Panic")
    *   `acceptance_score`: Float (0.0 to 1.0) - The dynamic "success metric" of the memory.
    *   `timestamp`: ISO datetime string.

## 5. Summary of Recent Improvements
*   **Bug Fix `AttributeError`**: Replaced deprecated `search` method with `query_points`.
*   **Bug Fix Score Logic**: Fixed logic to ensure existing memories are updated in-place (Reinforcement Learning) rather than creating duplicates.
*   **New Feature**: Added the 3-Week Feedback Loop for granular score tracking.
*   **New Feature**: Added the "Add Memory" menu for user-driven database expansion.
