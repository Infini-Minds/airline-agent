# api/services/bomb_threat_service.py

from datetime import datetime, timedelta
from api.airline_console.airline_engine import get_airports_by_city, get_flights_by_airports, get_bookings_by_flight_ids, \
    get_crews_and_aircraft, create_disruption, close_airports, save_flight_disruptions, \
    deallocate_crews_and_aircraft, get_available_hotels, save_hotel_bookings, save_vouchers

from api.models import *
from api.reader import get_session_and_engine
from sqlalchemy.orm import joinedload

from datetime import datetime, timedelta
import random
import string
# api/airline_service/threat_service.py
from api.airline_console.airline_engine import *
from api.models import *
from datetime import datetime, timedelta
import random, string

from geopy.geocoders import Nominatim
from functools import lru_cache



def _generate_event_id() -> str:
    return f"BT-{int(datetime.utcnow().timestamp() * 1000)}"


def _decide_flight_action(flight, airport_codes, alternate_airport):
    if (alternate_airport and flight.status in ("En Route")  \
                        and flight.destination_airport in airport_codes):
        
        return "Rerouted", alternate_airport
    return "Cancelled", flight.destination_airport

def allocate_hotels(session, affected_crews, affected_passengers, airport_code):
    """
    Allocate hotels for crews and passengers affected by flight disruptions.
    If no hotel rooms are available, issue meal vouchers.
    """
    hotels = get_available_hotels(session, airport_code)
    hotel_bookings = []
    vouchers = []
    booking_counter = 1060

    # Helper to generate voucher reference
    def _generate_voucher_ref():
        return f"V{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"

    # Allocate hotels to crews first
    for crew in affected_crews:
        now = datetime.utcnow()
        booked = False
        for hotel in hotels:
            if hotel.rooms_available <= 0:
                continue
            # Update hotel availability
            hotel.rooms_available -= 1
            hotel.rooms_booked += 1

            # Create hotel booking record
            hotel_bookings.append(
                HotelBooking(
                    hotel_booking_id=f"HB{booking_counter}",
                    crew_id=crew.crew_id,
                    passenger_id=None,
                    hotel_name=hotel.hotel_name,
                    hotel_address=hotel.hotel_location,
                    check_in = now + timedelta(hours=1),
                    check_out = now+ timedelta(hours=24),
                    booking_status="Confirmed",
                    booking_reference=f"{hotel.hotel_id}{booking_counter}",
                )
            )
            booking_counter += 1
            booked = True
            break
        if not booked:
            vouchers.append(
                Voucher(
                    booking_id=None,
                    passenger_id=None,
                    voucher_type="Meal Voucher",
                    expiry_date=datetime.utcnow() + timedelta(days=1),
                    status="Issued",
                    voucher_reference=_generate_voucher_ref()
                )
            )

    for passenger in affected_passengers:
        booked = False
        for hotel in hotels:
            if hotel.rooms_available <= 0:
                continue
            hotel.rooms_available -= 1
            hotel.rooms_booked += 1

            hotel_bookings.append(
                HotelBooking(
                    hotel_booking_id=f"HB{booking_counter}",
                    crew_id=None,
                    passenger_id=passenger.passenger_id,
                    hotel_name=hotel.hotel_name,
                    hotel_address=hotel.hotel_location,
                    check_in=datetime.utcnow(),
                    check_out=datetime.utcnow() + timedelta(hours=24),
                    booking_status="Confirmed",
                    booking_reference=f"{hotel.hotel_id}{booking_counter}",
                )
            )
            booking_counter += 1
            booked = True
            break 
        if not booked:

            vouchers.append(
                Voucher(
                    booking_id=None,
                    passenger_id=passenger.passenger_id,
                    voucher_type="Meal Voucher",
                    expiry_date=datetime.utcnow() + timedelta(days=1),
                    status="Issued",
                    voucher_reference=_generate_voucher_ref()
                )
            )

    save_hotel_bookings(session, hotel_bookings)
    save_vouchers(session, vouchers)



def _generate_event_id() -> str:
    return f"BT-{int(datetime.utcnow().timestamp() * 1000)}"


def create_bomb_threat_disruption(session, city: str, airport_codes: list[str]) -> Disruption:
    disruption = Disruption(
        event_id=_generate_event_id(),
        event_type="Bomb Threat",
        severity="Critical",
        airport_code=",".join(airport_codes),
        impact_description=f"Bomb threat reported in {city}",
        start_time=datetime.utcnow(),
        end_time=None,
    )
    create_disruption(session, disruption)
    return disruption


def get_flights_to_handle(session, airport_codes: list[str], alternate_airport: str | None):
    flights = get_flights_by_airports(session, airport_codes)
    flight_disruptions = []
    affected_flight_ids = []

    for i, flight in enumerate(flights):
        new_status, new_dest = _decide_flight_action(flight, airport_codes, alternate_airport)
        flight.status = new_status
        flight.destination_airport = new_dest
        affected_flight_ids.append(flight.flight_id)

        flight_disruptions.append(
            FlightDisruption(
                disruption_id=f"{_generate_event_id()}{i}",
                flight_id=flight.flight_id,
                event_type="Bomb Threat",
                severity="Critical",
                affected_passengers=flight.available_seats,
                status=new_status,
                requires_escalation="Yes",
            )
        )

    return flights, flight_disruptions, affected_flight_ids


def suspend_crews_and_aircraft(session, affected_flight_ids: list[str]):
    crews, aircrafts = get_crews_and_aircraft(session, affected_flight_ids)
    for crew in crews:
        crew.status = "Suspended"
    for aircraft in aircrafts:
        aircraft.status = "Security Hold"
    return crews, aircrafts


def handle_passenger_hotels(session, crews, passengers, airport_codes: list[str]):
    for airport_code in airport_codes:
        allocate_hotels(session, crews, passengers, airport_code)


def process_city_bomb_threat(city: str, alternate_airport: str | None = None):
    session, _ = get_session_and_engine()
    try:
        with session.begin():
            airports = get_airports_by_city(session, city)
            if not airports:
                raise ValueError(f"No airports found for city: {city}")

            airport_codes = [a.airport_code for a in airports]

            # 1. Create disruption record
            disruption = create_bomb_threat_disruption(session, city, airport_codes)

            # 2. Close affected airports
            close_airports(session, airport_codes)

            # 3. Handle flights
            flights, flight_disruptions, affected_flight_ids = get_flights_to_handle(session, airport_codes, alternate_airport)
            if flight_disruptions:
                save_flight_disruptions(session, flight_disruptions)

            # 4. Suspend crews and aircraft
            crews, aircrafts = suspend_crews_and_aircraft(session, affected_flight_ids)

            # 5. Handle affected passengers
            passengers = get_bookings_by_flight_ids(session, affected_flight_ids)
            handle_passenger_hotels(session, crews, passengers, airport_codes)

        return {
            "city": city,
            "affected_airports": airport_codes,
            "flights_affected": len(flights),
            "disruption_id": disruption.event_id,
        }

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

# -------- Bomb Threat Service (existing) --------
def create_bomb_threat(session, city: str, alternate_airport: str | None = None):
    # same logic as before
    airports = get_airports_by_city(session, city)
    if not airports:
        raise ValueError(f"No airports found for city: {city}")
    airport_codes = [a.airport_code for a in airports]

    disruption = Disruption(
        event_id=f"BT-{int(datetime.utcnow().timestamp() * 1000)}",
        event_type="Bomb Threat",
        severity="Critical",
        airport_code=",".join(airport_codes),
        impact_description=f"Bomb threat reported in {city}",
        start_time=datetime.utcnow(),
        end_time=None
    )
    session.add(disruption)
    session.flush()

    for a in airports:
        a.operational_status = "Closed"

    flights = get_flights_by_airports(session, airport_codes)
    flight_disruptions = []
    affected_flight_ids = []

    for i, flight in enumerate(flights):
        if alternate_airport and flight.status == "En Route" and flight.destination_airport in airport_codes:
            flight.status = "Rerouted"
            flight.destination_airport = alternate_airport
        else:
            flight.status = "Cancelled"
        affected_flight_ids.append(flight.flight_id)

        flight_disruptions.append(
            FlightDisruption(
                disruption_id=f"FD-{int(datetime.utcnow().timestamp()*1000)}-{i}",
                flight_id=flight.flight_id,
                event_type="Bomb Threat",
                severity="Critical",
                affected_passengers=flight.available_seats,
                status=flight.status,
                requires_escalation="Yes"
            )
        )
    session.bulk_save_objects(flight_disruptions)

    crews, aircrafts = get_crews_and_aircraft(session, affected_flight_ids)
    for c in crews: c.status = "Suspended"
    for a in aircrafts: a.status = "Security Hold"

    passengers = get_bookings_by_flight_ids(session, affected_flight_ids)
    _allocate_hotels(session, crews, passengers, airport_codes)

    return {
        "city": city,
        "affected_airports": airport_codes,
        "flights_affected": len(flights),
        "disruption_id": disruption.event_id
    }


# -------- Helper: Allocate hotels & vouchers --------
def _allocate_hotels(session, crews, passengers, airport_codes):
    hotels = []
    for airport_code in airport_codes:
        hotels += session.query(HotelDetails).filter(
            HotelDetails.airport_code == airport_code,
            HotelDetails.rooms_available > 0
        ).all()

    hotel_bookings = []
    vouchers = []
    booking_counter = 1000

    def _gen_voucher_ref():
        return f"V{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"

    for crew in crews:
        booked = False
        for h in hotels:
            if h.rooms_available <= 0: continue
            h.rooms_available -= 1
            h.rooms_booked += 1
            hotel_bookings.append(
                HotelBooking(
                    hotel_booking_id=f"HB{booking_counter}",
                    crew_id=crew.crew_id,
                    passenger_id=None,
                    hotel_name=h.hotel_name,
                    hotel_address=h.hotel_location,
                    check_in=datetime.utcnow(),
                    check_out=datetime.utcnow()+timedelta(hours=24),
                    booking_status="Confirmed",
                    booking_reference=f"{h.hotel_id}{booking_counter}"
                )
            )
            booking_counter += 1
            booked = True
            break
        if not booked:
            vouchers.append(
                Voucher(
                    booking_id=None,
                    passenger_id=None,
                    voucher_type="Meal Voucher",
                    expiry_date=datetime.utcnow()+timedelta(days=1),
                    status="Issued",
                    voucher_reference=_gen_voucher_ref()
                )
            )

    for p in passengers:
        booked = False
        for h in hotels:
            if h.rooms_available <= 0: continue
            h.rooms_available -= 1
            h.rooms_booked += 1
            hotel_bookings.append(
                HotelBooking(
                    hotel_booking_id=f"HB{booking_counter}",
                    crew_id=None,
                    passenger_id=p.passenger_id,
                    hotel_name=h.hotel_name,
                    hotel_address=h.hotel_location,
                    check_in=datetime.utcnow(),
                    check_out=datetime.utcnow()+timedelta(hours=24),
                    booking_status="Confirmed",
                    booking_reference=f"{h.hotel_id}{booking_counter}"
                )
            )
            booking_counter += 1
            booked = True
            break
        if not booked:
            vouchers.append(
                Voucher(
                    booking_id=None,
                    passenger_id=p.passenger_id,
                    voucher_type="Meal Voucher",
                    expiry_date=datetime.utcnow()+timedelta(days=1),
                    status="Issued",
                    voucher_reference=_gen_voucher_ref()
                )
            )

    session.bulk_save_objects(hotel_bookings + vouchers)


# -------- Dashboard Service --------
def get_dashboard_summary(session):
    incidents = session.query(FlightDisruption).all()
    total_incidents = len(incidents)
    escalated = len([i for i in incidents if i.requires_escalation=="Yes"])
    passengers_affected = sum([i.affected_passengers for i in incidents])
    automated_actions = total_incidents  # placeholder
    return {
        "Total Incidents": total_incidents,
        "Escalated": escalated,
        "Passengers Affected": passengers_affected,
        "Automated Actions": automated_actions
    }

def get_incident_feed(session):
    incidents = session.query(FlightDisruption).all()
    data = [{
        "Flight": i.flight_id,
        "Issue Type": i.event_type,
        "Status": i.status,
        "Agent Action": "Auto" if i.status!="Resolved" else "Manual",
        "Escalated": i.requires_escalation,
        "Passengers Affected": i.affected_passengers
    } for i in incidents]
    return data

def get_incident_map_data(session):
    incidents = session.query(FlightDisruption).all()
    data = []
    for i in incidents:
        flight = session.query(Flight).filter_by(flight_id=i.flight_id).first()
        airport = session.query(Airport).filter_by(airport_code=flight.origin_airport).first() if flight else None
        data.append({
            "Flight": i.flight_id,
            "City": airport.city if airport else "Unknown",
            "Latitude": 0,
            "Longitude": 0,
            "Status": i.status
        })
    return data

def get_bookings(session, flight_id=None, city=None):
    flight_ids = []
    if flight_id:
        flight_ids.append(flight_id)
    elif city:
        airports = get_airports_by_city(session, city)
        airport_codes = [a.airport_code for a in airports]
        flights = session.query(Flight).filter(
            (Flight.origin_airport.in_(airport_codes)) |
            (Flight.destination_airport.in_(airport_codes))
        ).all()
        flight_ids = [f.flight_id for f in flights]
    bookings = get_bookings_by_flight_ids(session, flight_ids)
    data = [{
        "Flight": b.flight_id,
        "Passenger ID": b.passenger_id,
        "Booking Status": b.booking_status,
        "Voucher Issued": b.is_disrupted
    } for b in bookings]
    return data

def get_status_distribution(session):
    incidents = session.query(FlightDisruption).all()
    counts = {}
    for i in incidents:
        counts[i.status] = counts.get(i.status, 0) + 1
    return counts

def get_escalation_rate(session):
    incidents = session.query(FlightDisruption).all()
    total = len(incidents)
    escalated = len([i for i in incidents if i.requires_escalation=="Yes"])
    rate = (escalated/total*100) if total else 0
    return {"Escalation Rate (%)": rate}



geolocator = Nominatim(user_agent="airline_ops_dashboard")

@lru_cache(maxsize=128)
def resolve_airport_location(airport_code: str, city: str, country: str):
    """
    Returns (lat, lon) for an airport using geopy.
    Cached to avoid repeated API calls.
    """
    try:
        query = f"{airport_code} airport, {country}"
        location = geolocator.geocode(query, timeout=10)
        if location:
            return location.latitude, location.longitude
    except Exception:
        pass

    return None, None



def get_dashboard_map_data(session):
    disruptions = (
        session.query(FlightDisruption)
        .options(
            joinedload(FlightDisruption.flight)
            .joinedload(Flight.destination)
        )
        .all()
    )

    result = []

    for d in disruptions:
        flight = d.flight
        airport = flight.destination if flight else None

        if not airport:
            continue

        lat, lon = resolve_airport_location(
            airport.airport_code,
            airport.city,
            airport.country
        )

        if lat is None or lon is None:
            print("can find the lat and lon", airport.city)
            continue
        print(lat, lon)

        result.append({
            "flight_number": flight.flight_number,
            "city": airport.city,
            "airport": airport.airport_name,
            "status": d.status,
            "event_type": d.event_type,
            "affected_passengers": d.affected_passengers,
            "latitude": lat,
            "longitude": lon,
        })
    return result
