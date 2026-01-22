# MindVault

**Qdrant-Powered Therapeutic Memory System**

MindVault is a proof-of-concept AI agent that acts as a long-term emotional memory. It remembers past emotional experiences and the strategies that helped resolve them, allowing it to offer personalized, evidence-based recommendations to users.

### Features
- **Semantic Search**: Uses `all-MiniLM-L6-v2` embeddings and Qdrant to find semantically similar past experiences.
- **Evidence-Based Recommendations**: Suggests coping strategies that have a high "Acceptance Score" impact in similar contexts.
- **Reinforcement Learning**: Updates the effectiveness of strategies based on user feedback (simulated 21-day cycle).
- **Privacy-First**: Uses local Qdrant storage (no cloud required for this demo).

---

## Setup & Installation

1. **Prerequisites**: Python 3.8+

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python main.py
   ```

---

## Usage Guide

### 1. Seed the Memory (First Run)
To make the system useful immediately, populate it with some initial "proven" strategies:

```bash
python main.py --seed
```
*Output: `✓ seeded test memories into Qdrant.`*

### 2. Interactive Session
Start the interactive advisor:
```bash
python main.py
```

**Example Flow:**
1. **Input**: Type how you are feeling (e.g., *"I am feeling very stressed about my upcoming deadline."*)
2. **Recommendation**: The system will search its memory for similar stress-related cases and propose a strategy (e.g., *Pomodoro Technique*).
3. **Context**: It will explain *why* it chose this, citing a past memory.
4. **Simulation**: You can choose to "try" the strategy. The system will then ask for feedback (simulating a 21-day follow-up) and update its memory with your new score, making the system smarter for next time.

---

## File Structure
- `mindvault_core.py`: Logic for Qdrant interaction, embeddings, and ranking.
- `main.py`: CLI interface and simulation logic.
- `MindVault_Report.md`: Full project documentation and design rationale.
- `qdrant_storage/`: Local data folder for Qdrant (auto-created).

---

### Author
Designed for Qdrant Convolve 4.0 Hackathon.
