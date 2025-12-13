import asyncpg
from database import get_pool


async def crew_agent(event):
    pool = await get_pool()
    flight_id = event.get("flight_id")

    async with pool.acquire() as conn:
        flight = await conn.fetchrow(
            "SELECT * FROM flight WHERE flight_id=$1", flight_id
        )
        if not flight:
            return {"error": "flight_not_found"}

        # Compute time to departure (hours)
        ttd = await conn.fetchval(
            """
            SELECT EXTRACT(EPOCH FROM (
                (scheduled_departure AT TIME ZONE 'UTC') - now()
            ))/3600
            FROM flight WHERE flight_id=$1
        """,
            flight_id,
        )

        # Get legal local crew
        crew = await conn.fetch(
            """
            SELECT * FROM crew
            WHERE current_location=$1
              AND certification_status='valid'
              AND status='active'
              AND remaining_hours >= 2
              AND requires_rest=false
        """,
            flight["origin_airport"],
        )

        if crew:
            c = crew[0]
            await conn.execute(
                """
                INSERT INTO crew_assignment(crew_id, flight_id, role, status)
                VALUES($1,$2,$3,'assigned')
            """,
                c["crew_id"],
                flight_id,
                c["role"],
            )

            return {
                "flight_id": flight_id,
                "assigned": {"crew_id": c["crew_id"], "role": c["role"]},
                "action": "assign_local_crew",
                "ttd_hours": float(ttd),
            }

        # Passenger policy
        if ttd < 8:
            action = "reschedule"
        elif ttd <= 24:
            action = "reschedule_and_hotel"
        else:
            action = "cancel_and_voucher"

        return {
            "flight_id": flight_id,
            "assigned": None,
            "action": action,
            "ttd_hours": float(ttd),
        }
