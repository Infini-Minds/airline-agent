import asyncio

async def crew_agent(event):
    # placeholder: find replacement crew, update rosters, rebook passengers if needed
    print("[crew_agent] Handling event:", event.get("event_id"))
    return {"status": "crew_rerouted", "event_id": event.get("event_id")}
