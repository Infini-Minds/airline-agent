from langchain_openai import ChatOpenAI
import sqlparse
from tools.generate_and_execute_query import generate_and_execute_query


async def weather_agent(event):
    """
    Weather agent responsible for rescheduling bookings
    affected by high severity weather incidents.
    """
    print("[weather_agent] Handling event:", event.get("event_id"))

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    # The SQL generator expects a LIST of incidents
    incidents = [event]

    await generate_and_execute_query(llm, incidents)

    return {"status": "rescheduling_completed", "event_id": event.get("incident_id")}
