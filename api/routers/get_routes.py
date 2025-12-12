from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

import models, schemas
from database import get_db

router = APIRouter()

# --- Aircraft ---
@router.get("/aircraft/", response_model=List[schemas.Aircraft])
async def get_aircrafts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Aircraft))
    return result.scalars().all()

# --- Aircraft Maintenance ---
@router.get("/aircraft_maintenance/", response_model=List[schemas.AircraftMaintenance])
async def get_aircraft_maintenance(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.AircraftMaintenance))
    return result.scalars().all()

# --- Airport ---
@router.get("/airport/", response_model=List[schemas.Airport])
async def get_airports(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Airport))
    return result.scalars().all()

# --- Crew ---
@router.get("/crew/", response_model=List[schemas.Crew])
async def get_crew(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Crew))
    return result.scalars().all()

# --- Crew Assignment ---
@router.get("/crew_assignment/", response_model=List[schemas.CrewAssignment])
async def get_crew_assignments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.CrewAssignment))
    return result.scalars().all()

# --- Crew Duty Time ---
@router.get("/crew_duty_time/", response_model=List[schemas.CrewDutyTime])
async def get_crew_duty_time(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.CrewDutyTime))
    return result.scalars().all()

# --- Disruption ---
@router.get("/disruption/", response_model=List[schemas.Disruption])
async def get_disruptions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Disruption))
    return result.scalars().all()

# --- Disruption Resolution ---
@router.get("/disruption_resolution/", response_model=List[schemas.DisruptionResolution])
async def get_disruption_resolutions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.DisruptionResolution))
    return result.scalars().all()

# --- Flight ---
@router.get("/flight/", response_model=List[schemas.Flight])
async def get_flights(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Flight))
    return result.scalars().all()

# --- Flight Disruption ---
@router.get("/flight_disruption/", response_model=List[schemas.FlightDisruption])
async def get_flight_disruptions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.FlightDisruption))
    return result.scalars().all()

# --- Flight Segment ---
@router.get("/flight_segment/", response_model=List[schemas.FlightSegment])
async def get_flight_segments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.FlightSegment))
    return result.scalars().all()

# --- Hotel Booking ---
@router.get("/hotel_booking/", response_model=List[schemas.HotelBooking])
async def get_hotel_bookings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.HotelBooking))
    return result.scalars().all()

# --- Hotel Details ---
@router.get("/hotel_details/", response_model=List[schemas.HotelDetails])
async def get_hotel_details(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.HotelDetails))
    return result.scalars().all()

# --- Passenger ---
@router.get("/passenger/", response_model=List[schemas.Passenger])
async def get_passengers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Passenger))
    return result.scalars().all()

# --- Passenger Booking ---
@router.get("/passenger_booking/", response_model=List[schemas.PassengerBooking])
async def get_passenger_bookings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.PassengerBooking))
    return result.scalars().all()

# --- Rebooking ---
@router.get("/rebooking/", response_model=List[schemas.Rebooking])
async def get_rebookings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Rebooking))
    return result.scalars().all()

# --- Voucher ---
@router.get("/voucher/", response_model=List[schemas.Voucher])
async def get_vouchers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Voucher))
    return result.scalars().all()
