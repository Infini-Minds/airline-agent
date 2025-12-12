from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

import models, schemas
from database import get_db

router = APIRouter()

# --- Aircraft ---
@router.get("/aircraft/", response_model=List[schemas.Aircraft])
async def get_aircrafts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Aircraft).offset(skip).limit(limit))
    return result.scalars().all()

# --- Aircraft Maintenance ---
@router.get("/aircraft_maintenance/", response_model=List[schemas.AircraftMaintenance])
async def get_aircraft_maintenance(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.AircraftMaintenance).offset(skip).limit(limit))
    return result.scalars().all()

# --- Airport ---
@router.get("/airport/", response_model=List[schemas.Airport])
async def get_airports(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Airport).offset(skip).limit(limit))
    return result.scalars().all()

# --- Crew ---
@router.get("/crew/", response_model=List[schemas.Crew])
async def get_crew(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Crew).offset(skip).limit(limit))
    return result.scalars().all()

# --- Crew Assignment ---
@router.get("/crew_assignment/", response_model=List[schemas.CrewAssignment])
async def get_crew_assignments(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.CrewAssignment).offset(skip).limit(limit))
    return result.scalars().all()

# --- Crew Duty Time ---
@router.get("/crew_duty_time/", response_model=List[schemas.CrewDutyTime])
async def get_crew_duty_time(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.CrewDutyTime).offset(skip).limit(limit))
    return result.scalars().all()

# --- Disruption ---
@router.get("/disruption/", response_model=List[schemas.Disruption])
async def get_disruptions(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Disruption).offset(skip).limit(limit))
    return result.scalars().all()

# --- Disruption Resolution ---
@router.get("/disruption_resolution/", response_model=List[schemas.DisruptionResolution])
async def get_disruption_resolutions(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.DisruptionResolution).offset(skip).limit(limit))
    return result.scalars().all()

# --- Flight ---
@router.get("/flight/", response_model=List[schemas.Flight])
async def get_flights(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Flight).offset(skip).limit(limit))
    return result.scalars().all()

# --- Flight Disruption ---
@router.get("/flight_disruption/", response_model=List[schemas.FlightDisruption])
async def get_flight_disruptions(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.FlightDisruption).offset(skip).limit(limit))
    return result.scalars().all()

# --- Flight Segment ---
@router.get("/flight_segment/", response_model=List[schemas.FlightSegment])
async def get_flight_segments(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.FlightSegment).offset(skip).limit(limit))
    return result.scalars().all()

# --- Hotel Booking ---
@router.get("/hotel_booking/", response_model=List[schemas.HotelBooking])
async def get_hotel_bookings(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.HotelBooking).offset(skip).limit(limit))
    return result.scalars().all()

# --- Hotel Details ---
@router.get("/hotel_details/", response_model=List[schemas.HotelDetails])
async def get_hotel_details(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.HotelDetails).offset(skip).limit(limit))
    return result.scalars().all()

# --- Passenger ---
@router.get("/passenger/", response_model=List[schemas.Passenger])
async def get_passengers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Passenger).offset(skip).limit(limit))
    return result.scalars().all()

# --- Passenger Booking ---
@router.get("/passenger_booking/", response_model=List[schemas.PassengerBooking])
async def get_passenger_bookings(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.PassengerBooking).offset(skip).limit(limit))
    return result.scalars().all()

# --- Rebooking ---
@router.get("/rebooking/", response_model=List[schemas.Rebooking])
async def get_rebookings(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Rebooking).offset(skip).limit(limit))
    return result.scalars().all()

# --- Voucher ---
@router.get("/voucher/", response_model=List[schemas.Voucher])
async def get_vouchers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Voucher).offset(skip).limit(limit))
    return result.scalars().all()
