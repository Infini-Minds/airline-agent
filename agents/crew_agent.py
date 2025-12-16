"""
Crew Disruption Agent - LangChain Implementation

Handles:
- Crew duty time exceeded
- Crew unavailable
- Crew legality / rest issues
"""

import json
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

from tools.tools import (
    get_flights,
    get_crew,
    get_crew_assignment,
    get_crew_duty_time,
    get_disruption,
)

load_dotenv()

TOOLS = [get_flights, get_crew, get_crew_assignment, get_crew_duty_time, get_disruption]

AGENT_PROMPT = PromptTemplate.from_template(
    """
You are a Crew Disruption Resolution Agent for an airline operations center.

Your task is to resolve crew-related disruptions such as:
- Crew duty time exceeded
- Crew unavailable
- Crew legality issues

You MUST:
1. Use get_disruption to understand the crew issue
2. Use get_flights to identify the affected flight
3. Use get_crew_assignment to find current crew
4. Use get_crew_duty_time to validate legality
5. Use get_crew to find available replacement crew

Decision rules:
- If legal replacement crew exists → ASSIGN_CREW
- If no crew and departure < 8 hours → RESCHEDULE
- If no crew and departure 8–24 hours → RESCHEDULE_AND_HOTEL
- If no crew and departure > 24 hours → CANCEL_AND_VOUCHER

Return the response in EXACT JSON format:
{{
  "status": "completed",
  "flight_id": <flight_id>,
  "action": "<assign_crew | reschedule | reschedule_and_hotel | cancel_and_voucher>",
  "assigned_crew": {{
    "crew_id": <id>,
    "role": "<role>"
  }},
  "reason": "<short explanation>"
}}

IMPORTANT:
- Use ONLY the tools
- Filter data yourself
- Do NOT invent data
- Return ONLY JSON

You have access to the following tools:
{tools}

Tool names:
{tool_names}

Use the following format:
Thought: analyze crew disruption
Action: <tool name>
Action Input: <tool input>
Observation: <tool output>
...
Thought: I have enough information
Final Answer: <JSON>

Begin!

Event:
{input}
{agent_scratchpad}
"""
)


def create_crew_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    agent = create_react_agent(llm=llm, tools=TOOLS, prompt=AGENT_PROMPT)

    return AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=8,
    )


# ENTRYPOINT FOR decision_worker
async def crew_agent(event: dict) -> dict:
    print(f"[crew_agent] Handling event: {event.get('event_id')}")

    try:
        agent_executor = create_crew_agent()
        event_input = json.dumps(event, indent=2)

        result = await agent_executor.ainvoke({"input": event_input})

        output = result.get("output", "{}")

        try:
            response = json.loads(output)
        except json.JSONDecodeError:
            response = {
                "status": "completed",
                "raw_response": output,
                "event_id": event.get("event_id"),
            }

        print(f"[crew_agent] Completed: {response}")
        return response

    except Exception as e:
        print(f"[crew_agent] Error: {e}")
        return {"status": "error", "event_id": event.get("event_id"), "error": str(e)}
