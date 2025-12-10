# Airlines IRROPS - demo

## Prereqs
- Python 3.10+
- docker & docker-compose (optional, for Postgres)
- OpenAI API key

## Setup

1. Copy .env.example -> .env and set OPENAI_API_KEY and DB credentials
2. Start Postgres:
   - Option A (docker): `docker-compose up -d`
   - Option B (local Postgres): create DB and run init_db.sql

3. Install deps:
   pip install -r requirements.txt

4. Run FastAPI:
   uvicorn app:app --reload --host 0.0.0.0 --port 8000

5. Run the Python UI script:
   python gradio_ui/ui.py

You can access the UI in your browser at:
   http://localhost:7860

The endpoint returns parsed events and the AI routing decision for each event.

