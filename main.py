from fastapi import FastAPI, Request
from datetime import datetime
import bookings_controller

app = FastAPI()

@app.get("/flights")
async def get_flights(
    limit: int = 10,
    offset: int = 0,
    flight_id: int = None,
    departure_airport: str = None,
    arrival_airport: str = None,
    actual_departure: datetime = None,
    actual_arrival: datetime = None,
):
    
    result = bookings_controller.get_flights(
        limit=limit,
        offset=offset,
        flight_id=flight_id,
        departure_airport=departure_airport,
        arrival_airport=arrival_airport,
        actual_departure=actual_departure,
        actual_arrival=actual_arrival,
    )

    return result

@app.get("/airports")
async def get_airports(
    limit: int = 10,
    offset: int = 0,
    name_fragment: str = None,
):
    result = bookings_controller.get_airports(limit=limit, offset=offset, name_fragment=name_fragment)

    return result

@app.get("/boarding_passes")
async def get_boarding_passes(
    limit: int = 10,
    offset: int = 0,
    ticket_id: int = None,
):
    result = bookings_controller.get_boarding_passes(limit=limit, offset=offset, ticket_id=ticket_id)

    return result

@app.get("/tickets")
async def get_tickets(
    limit: int = 10,
    offset: int = 0,
    passenger_id: int = None,
    booking_id: str = None,
    ticket_id: int = None,
):
    result = bookings_controller.get_tickets(
        limit=limit,
        offset=offset,
        passenger_id=passenger_id,
        booking_id=booking_id,
        ticket_id=ticket_id,
    )

    return result

@app.get("/bookings")
async def get_bookings(
    limit: int = 10,
    offset: int = 0,
    booking_id: str = None,
    book_date: datetime = None,
):
    result = bookings_controller.get_bookings(
        limit=limit,
        offset=offset,
        booking_id=booking_id,
        book_date=book_date,
    )

    return result

@app.post("/bookings")
async def add_booking(
    aircraft_code: str,
    passenger_id: int,
    flight_ids: list[int],
    seat_nos: list[str],
):
    return bookings_controller.add_booking(aircraft_code, passenger_id, flight_ids, seat_nos)