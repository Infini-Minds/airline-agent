from sqlalchemy import Column, String, Integer, DateTime, Date, Boolean, Float, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
class Aircraft(Base):
    __tablename__ = "aircraft"
    aircraft_id = Column(String, primary_key=True, index=True)
    registration_number = Column(String)
    aircraft_type = Column(String)
    manufacturer = Column(String)
    total_seats = Column(Integer)
    economy_seats = Column(Integer)
    business_seats = Column(Integer)
    first_seats = Column(Integer)
    current_location = Column(String)
    maintenance_status = Column(String)
    last_maintenance = Column(String) 
    next_maintenance = Column(String)

class AircraftMaintenance(Base):
    __tablename__ = "aircraft_maintenance"
    maintenance_id = Column(String, primary_key=True, index=True)
    aircraft_id = Column(String, index=True)
    maintenance_type = Column(String)
    scheduled_start = Column(String)
    scheduled_end = Column(String)
    actual_start = Column(String)
    actual_end = Column(String)
    status = Column(String)
    description = Column(Text)

class Airport(Base):
    __tablename__ = "airport"
    airport_code = Column(String, primary_key=True, index=True)
    airport_name = Column(String)
    city = Column(String)
    country = Column(String)
    timezone = Column(String)
    max_hourly_slots = Column(Integer)
    operational_status = Column(String) 

class Crew(Base):
    __tablename__ = "crew"
    crew_id = Column(String, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    crew_role = Column(String)
    base_airport = Column(String)
    certification = Column(String)
    is_available = Column(String)
    last_duty = Column(String)

class CrewAssignment(Base):
    __tablename__ = "crew_assignment"
    assignment_id = Column(String, primary_key=True, index=True)
    crew_id = Column(String, index=True)
    flight_id = Column(String, index=True)
    role = Column(String)
    assignment_date = Column(String)
    status = Column(String)

class CrewDutyTime(Base):
    __tablename__ = "crew_duty_time"
    duty_id = Column(String, primary_key=True, index=True)
    crew_id = Column(String, index=True)
    duty_start = Column(String)
    duty_end = Column(String)
    hours_worked = Column(Float)
    remaining_hours = Column(Float)
    requires_rest = Column(String)

class Disruption(Base):
    __tablename__ = "disruption"
    event_id = Column(String, primary_key=True, index=True)
    event_type = Column(String)
    severity = Column(String)
    impact_description = Column(Text)
    airport_code = Column(String)
    start_time = Column(String)
    end_time = Column(String)

class DisruptionResolution(Base):
    __tablename__ = "disruption_resolution"
    disruption_id = Column(String, primary_key=True, index=True)
    resolution_type = Column(String)
    resolved_at = Column(String)
    resolution_status = Column(String)
    passengers_booked = Column(Integer)
    hotel_bookings_made = Column(Integer)
    vouchers_issued = Column(Integer)

class Flight(Base):
    __tablename__ = "flight"
    flight_id = Column(String, primary_key=True, index=True)
    flight_number = Column(String)
    aircraft_id = Column(String)
    origin_airport = Column(String)
    destination_airport = Column(String)
    layover_airport = Column(String)
    scheduled_departure = Column(String)
    scheduled_arrival = Column(String)
    actual_departure = Column(String)
    actual_arrival = Column(String)
    status = Column(String)
    available_seats = Column(Integer)

class FlightDisruption(Base):
    __tablename__ = "flight_disruption"
    disruption_id = Column(String, primary_key=True)
    flight_id = Column(String, primary_key=True)
    event_type = Column(String)
    severity = Column(String)
    affected_passengers = Column(Integer)
    status = Column(String)
    requires_escalation = Column(String)

class FlightSegment(Base):
    __tablename__ = "flight_segment"
    flight_prefix = Column(String, primary_key=True) # Assuming prefix identifies this lookup table
    primary_airline_name = Column(String)
    parent_company_airline_group = Column(String)
    co_company = Column(String)

class HotelBooking(Base):
    __tablename__ = "hotel_booking"
    hotel_booking_id = Column(String, primary_key=True, index=True)
    crew_id = Column(String)
    passenger_id = Column(String)
    hotel_name = Column(String)
    hotel_address = Column(String)
    check_in = Column(String)
    check_out = Column(String)
    booking_status = Column(String)
    booking_reference = Column(String)

class HotelDetails(Base):
    __tablename__ = "hotel_details"
    hotel_id = Column(String, primary_key=True, index=True)
    hotel_name = Column(String)
    airport_code = Column(String)
    hotel_location = Column(String)
    rooms_available = Column(Integer)
    rooms_booked = Column(Integer)
    available_from = Column(String)
    available_till = Column(String)

class Passenger(Base):
    __tablename__ = "passenger"
    passenger_id = Column(String, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    frequent_flyer_number = Column(String)
    loyalty_tier = Column(String)
    preferred_contact_method = Column(String)

class PassengerBooking(Base):
    __tablename__ = "passenger_booking"
    booking_id = Column(String, primary_key=True, index=True)
    passenger_id = Column(String, index=True)
    flight_id = Column(String, index=True)
    pnr = Column(String)
    seat_number = Column(String)
    cabin_class = Column(String)
    ticket_price = Column(Float)
    booking_status = Column(String)
    # booking_date = Column(String)
    is_disrupted = Column(String)

class Rebooking(Base):
    __tablename__ = "rebooking"
    booking_id = Column(String, primary_key=True) # Assuming this is new booking id
    old_booking_id = Column(String)
    flight_id = Column(String)
    old_flight_id = Column(String)
    rebooking_reason = Column(String)
    auto_rebooked = Column(String)
    confirmation_status = Column(String)

class Voucher(Base):
    __tablename__ = "voucher"
    voucher_id = Column(String, primary_key=True, index=True)
    booking_id = Column(String)
    voucher_type = Column(String)
    expiry_date = Column(String)
    status = Column(String)
