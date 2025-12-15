# agents/bomb_threat_agent.py
"""
Bomb Threat Agent - LangChain Implementation

Uses shared tools from tools/tools.py and LangChain ReAct agent
to analyze bomb threat events and determine response actions.
"""

import os
import json
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

# Import shared tools from tools folder
from tools.tools import (
    get_flights,
    get_airport,
    get_passenger_booking,
    get_crew_assignment,
    get_disruption
)

load_dotenv()


# Define tools for this agent
TOOLS = [
    get_flights,
    get_airport,
    get_passenger_booking,
    get_crew_assignment,
    get_disruption
]

# Agent prompt template
AGENT_PROMPT = PromptTemplate.from_template("""
You are a Bomb Threat Response Agent for an airline operations center.

Your job is to analyze a bomb threat event and determine the appropriate response actions.

For a bomb threat, you MUST:
1. Get all flights using get_flights - filter those at the affected airport
2. Get all airports using get_airport - find alternatives for rerouting
3. Get passenger bookings using get_passenger_booking - count affected passengers
4. Get crew assignments using get_crew_assignment - identify crew to reassign

Based on the data, provide a response in this EXACT JSON format:
{{
    "status": "completed",
    "affected_airport": "<airport code>",
    "threat_level": "CRITICAL",
    "actions": [
        "Cancel all <N> flights at <airport>",
        "Reroute inbound flights to <nearby airport>",
        "Update <N> crew assignments to Standby",
        "Notify <N> affected passengers"
    ],
    "summary": {{
        "flights_to_cancel": <number>,
        "passengers_affected": <number>,
        "crew_to_reassign": <number>,
        "reroute_destination": "<airport code>"
    }},
    "reroute_options": ["<airport1>", "<airport2>", "<airport3>"]
}}

IMPORTANT:
- Use the tools to get REAL data
- Filter the data yourself based on airport code from the event
- Be concise in your reasoning
- Return ONLY the final JSON, no extra text

You have access to the following tools:
{tools}

Use the following format:
Thought: I need to analyze the bomb threat event
Action: <tool name>
Action Input: <tool input>
Observation: <tool output>
... (repeat Thought/Action/Observation as needed)
Thought: I have all the information needed
Final Answer: <JSON response>

Begin!

Event: {input}
{agent_scratchpad}
""")


def create_bomb_threat_agent():
    """Create and return the LangChain agent"""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )
    
    agent = create_react_agent(
        llm=llm,
        tools=TOOLS,
        prompt=AGENT_PROMPT
    )
    
    agent_executor = AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10
    )
    
    return agent_executor


# MAIN AGENT FUNCTION (Called by decision_worker)
async def bomb_threat_agent(event: dict) -> dict:
    """
    Main bomb threat agent handler - compatible with decision_worker.py
    
    Args:
        event: Dict containing event details from master_decision_table
    
    Returns:
        Dict with status and response actions
    """
    print(f"[bomb_threat_agent] Handling event: {event.get('event_id')}")
    
    try:
        # Create the agent
        agent_executor = create_bomb_threat_agent()
        event_input = json.dumps(event, indent=2)
        result = await agent_executor.ainvoke({"input": event_input})
        output = result.get("output", "{}")
        
        try:
            response = json.loads(output)
        except json.JSONDecodeError:
            response = {
                "status": "completed",
                "raw_response": output,
                "event_id": event.get("event_id")
            }
        
        print(f"[bomb_threat_agent] Completed: {response.get('summary', response)}")
        return response
        
    except Exception as e:
        print(f"[bomb_threat_agent] Error: {e}")
        return {
            "status": "error",
            "event_id": event.get("event_id"),
            "error": str(e)
        }
