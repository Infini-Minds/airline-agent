from langchain_openai import ChatOpenAI
import sqlparse
from tools.generate_and_execute_query import generate_and_execute_query

from database import get_pool
from tools.send_email import send_email


async def notify_rescheduled_passengers():
    pool = await get_pool()  # Use your existing pool
    results = []

    async with pool.acquire() as conn:
        rows = await conn.fetch("""
                SELECT booking_id, flight_id, passenger_id, passenger_name, passenger_email,
                       airport_code, reason, rescheduled_at
                FROM public.rescheduled_bookings
            """)

    for row in rows:
        booking_id = row['booking_id']
        flight_id = row['flight_id']
        passenger_id = row['passenger_id']
        passenger_name = row['passenger_name']
        passenger_email = row['passenger_email']
        airport_code = row['airport_code']
        reason = row['reason']
        rescheduled_at = row['rescheduled_at']

        if not passenger_email:
            print(f"[notify_agent] No email for passenger {passenger_id}")
            results.append({
                "passenger_id": passenger_id,
                "status": "email_missing"
            })
            continue

        # Compose email
        subject = f"Flight {flight_id} Rescheduled Notification"
        body = f"""
Dear {passenger_name},

Your flight {flight_id} scheduled at {airport_code} has been rescheduled.

Reason: {reason}
New rescheduled time: {rescheduled_at.strftime('%Y-%m-%d %H:%M:%S')}

Please follow the airline instructions for your updated flight.

Regards,
Airline Operations Team
"""

        # Send email
        email_status = send_email(passenger_email, subject, body)
        status = "email_sent" if email_status else "email_failed"

        if email_status:
            print(f"[notify_agent] Email sent to {passenger_email}")
        else:
            print(f"[notify_agent] Email FAILED to {passenger_email}")

        results.append({
            "passenger_id": passenger_id,
            "email": passenger_email,
            "status": status,
            "booking_id": booking_id,
            "flight_id": flight_id,
            "rescheduled_at": rescheduled_at,
            "reason": reason
        })

    await conn.close()

    return {
        "status": "completed",
        "total_passengers": len(rows),
        "results": results
    }


async def weather_agent(event):
    """
    Weather agent responsible for rescheduling bookings
    affected by high severity weather incidents.
    """
    print("[weather_agent] Handling event:", event.get("event_id"))

    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o-mini"
    )

    # The SQL generator expects a LIST of incidents
    incidents = [event]

    await generate_and_execute_query(llm, incidents)
    await notify_rescheduled_passengers()

    return {
        "status": "rescheduling_completed",
        "event_id": event.get("incident_id")
    }
