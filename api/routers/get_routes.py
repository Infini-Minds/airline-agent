from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import get_db

router = APIRouter()

# --- Aircraft ---
@router.get("/aircraft/", response_model=List[schemas.Aircraft])
def get_aircrafts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Aircraft).offset(skip).limit(limit).all()

# --- Aircraft Maintenance ---
@router.get("/aircraft_maintenance/", response_model=List[schemas.AircraftMaintenance])
def get_aircraft_maintenance(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.AircraftMaintenance).offset(skip).limit(limit).all()

# --- Airport ---
@router.get("/airport/", response_model=List[schemas.Airport])
def get_airports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Airport).offset(skip).limit(limit).all()

# --- Crew ---
@router.get("/crew/", response_model=List[schemas.Crew])
def get_crew(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Crew).offset(skip).limit(limit).all()

# --- Crew Assignment ---
@router.get("/crew_assignment/", response_model=List[schemas.CrewAssignment])
def get_crew_assignments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.CrewAssignment).offset(skip).limit(limit).all()

# --- Crew Duty Time ---
@router.get("/crew_duty_time/", response_model=List[schemas.CrewDutyTime])
def get_crew_duty_time(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.CrewDutyTime).offset(skip).limit(limit).all()

# --- Disruption ---
@router.get("/disruption/", response_model=List[schemas.Disruption])
def get_disruptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Disruption).offset(skip).limit(limit).all()

# --- Disruption Resolution ---
@router.get("/disruption_resolution/", response_model=List[schemas.DisruptionResolution])
def get_disruption_resolutions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.DisruptionResolution).offset(skip).limit(limit).all()

# --- Flight ---
@router.get("/flight/", response_model=List[schemas.Flight])
def get_flights(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Flight).offset(skip).limit(limit).all()

# --- Flight Disruption ---
@router.get("/flight_disruption/", response_model=List[schemas.FlightDisruption])
def get_flight_disruptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.FlightDisruption).offset(skip).limit(limit).all()

# --- Flight Segment ---
@router.get("/flight_segment/", response_model=List[schemas.FlightSegment])
def get_flight_segments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.FlightSegment).offset(skip).limit(limit).all()

# --- Hotel Booking ---
@router.get("/hotel_booking/", response_model=List[schemas.HotelBooking])
def get_hotel_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.HotelBooking).offset(skip).limit(limit).all()

# --- Hotel Details ---
@router.get("/hotel_details/", response_model=List[schemas.HotelDetails])
def get_hotel_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.HotelDetails).offset(skip).limit(limit).all()

# --- Passenger ---
@router.get("/passenger/", response_model=List[schemas.Passenger])
def get_passengers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Passenger).offset(skip).limit(limit).all()

# --- Passenger Booking ---
@router.get("/passenger_booking/", response_model=List[schemas.PassengerBooking])
def get_passenger_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.PassengerBooking).offset(skip).limit(limit).all()

# --- Rebooking ---
@router.get("/rebooking/", response_model=List[schemas.Rebooking])
def get_rebookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Rebooking).offset(skip).limit(limit).all()

# --- Voucher ---
@router.get("/voucher/", response_model=List[schemas.Voucher])
def get_vouchers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Voucher).offset(skip).limit(limit).all()
