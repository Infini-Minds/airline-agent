# agents/routing_ai.py
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# ---- STRICT SYSTEM PROMPT (PUT THIS IN YOUR FILE) ----
SYSTEM_PROMPT = """
You are an aviation IRROPS Decision Engine.

Your ONLY job:
1. Read the incoming EVENT (already pre-cleaned text from PDF).
2. Decide which operational agents must be triggered.
3. Output STRICT JSON only. No explanations. No commentary.

------------------------------------
### EVENT CATEGORIES
- weather_agent → weather disruptions, wind, fog, storms, crosswinds, METAR/SIGMET issues.
- crew_agent → crew legality, hours, flight duty time, rest issues, crew shortage.
- traffic_agent → runway closure, taxiway congestion, ATC flow programs, airport capacity.
- maintenance_agent → mechanical failures, MEL/CDL, technical faults.
- monitoring_agent → everything else / low severity / not enough info.

------------------------------------
### RULES
1. Output JSON in this exact schema:
{
  "selected_agents": ["agent_name1", "agent_name2"],
  "reason": "short explanation"
}
2. ALWAYS return an array of agents.
3. NEVER output text outside JSON.
4. If uncertain, include "monitoring_agent".
5. If the PDF text contains multiple signals, include multiple agents.
6. The JSON MUST be valid and parseable.

------------------------------------
### MASTER DECISION TABLE LOGIC
Whatever agents you select will be stored in `master_decision_table` and executed by downstream workers.
So be precise and avoid guessing unrelated agents.

------------------------------------
"""


def _call_openai_sync(prompt: str, max_tokens: int = 200):
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message["content"].strip()


async def ai_decide_agent(event: dict, db_rules: list = None) -> dict:
    """
    Returns:
      {
        "selected_agents": [...],
        "reason": "..."
      }
    """

    # Build user prompt
    prompt = (
        "EVENT:\n"
        + json.dumps(event, indent=2)
        + "\n\nDB_RULES:\n"
        + json.dumps(db_rules or [], indent=2)
        + "\n\nRespond ONLY with JSON."
    )

    loop = asyncio.get_event_loop()

    with ThreadPoolExecutor(max_workers=1) as exe:
        raw = await loop.run_in_executor(exe, _call_openai_sync, prompt)

    # Attempt strict JSON decode
    try:
        return json.loads(raw)

    except Exception:
        # If the model ever breaks JSON, force safe fallback
        return {
            "selected_agents": ["monitoring_agent"],
            "reason": "fallback - invalid JSON from model",
        }
