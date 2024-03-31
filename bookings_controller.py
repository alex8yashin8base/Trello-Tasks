from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, JSON, String, Interval
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random
import string

Base = declarative_base()

class Aircraft(Base):
    __tablename__ = 'aircrafts'
    aircraft_code = Column(String, primary_key=True)
    model = Column(String, nullable=False)
    range = Column(Integer, nullable=False)

class AircraftData(Base):
    __tablename__ = 'aircrafts_data'
    aircraft_code = Column(String, primary_key=True)
    model = Column(JSON, nullable=False)
    range = Column(Integer, nullable=False)

class Airport(Base):
    __tablename__ = 'airports'
    airport_code = Column(String, primary_key=True)
    airport_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    coordinates = Column(String, nullable=False)
    timezone = Column(String, nullable=False)

class AirportData(Base):
    __tablename__ = 'airports_data'
    airport_code = Column(String, primary_key=True)
    airport_name = Column(JSON, nullable=False)
    city = Column(JSON, nullable=False)
    coordinates = Column(String, nullable=False)
    timezone = Column(String, nullable=False)

class BoardingPass(Base):
    __tablename__ = 'boarding_passes'
    ticket_no = Column(String, primary_key=True)
    flight_id = Column(Integer, ForeignKey('flights.flight_id'), primary_key=True)
    boarding_no = Column(Integer, nullable=False)
    seat_no = Column(String, nullable=False)

class Booking(Base):
    __tablename__ = 'bookings'
    book_ref = Column(String, primary_key=True)
    book_date = Column(DateTime, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)

class Flight(Base):
    __tablename__ = 'flights'
    flight_id = Column(Integer, primary_key=True)
    flight_no = Column(String, nullable=False)
    scheduled_departure = Column(DateTime, nullable=False)
    scheduled_arrival = Column(DateTime, nullable=False)
    departure_airport = Column(String, ForeignKey('airports.airport_code'), nullable=False)
    arrival_airport = Column(String, ForeignKey('airports.airport_code'), nullable=False)
    status = Column(String, nullable=False)
    aircraft_code = Column(String, ForeignKey('aircrafts.aircraft_code'), nullable=False)
    actual_departure = Column(DateTime)
    actual_arrival = Column(DateTime)

class Seat(Base):
    __tablename__ = 'seats'
    aircraft_code = Column(String, ForeignKey('aircrafts.aircraft_code'), primary_key=True)
    seat_no = Column(String, primary_key=True)
    fare_conditions = Column(String, nullable=False)

class TicketFlight(Base):
    __tablename__ = 'ticket_flights'
    ticket_no = Column(String, ForeignKey('tickets.ticket_no'), primary_key=True)
    flight_id = Column(Integer, ForeignKey('flights.flight_id'), primary_key=True)
    fare_conditions = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)

class Ticket(Base):
    __tablename__ = 'tickets'
    ticket_no = Column(String, primary_key=True)
    book_ref = Column(String, ForeignKey('bookings.book_ref'), nullable=False)
    passenger_id = Column(String, nullable=False)
    passenger_name = Column(String, nullable=False)
    contact_data = Column(JSON)

class FlightV(Base):
    __tablename__ = 'flights_v'
    flight_id = Column(Integer, primary_key=True)
    flight_no = Column(String, nullable=False)
    scheduled_departure = Column(DateTime, nullable=False)
    scheduled_departure_local = Column(DateTime, nullable=False)
    scheduled_arrival = Column(DateTime, nullable=False)
    scheduled_arrival_local = Column(DateTime, nullable=False)
    departure_airport = Column(String, nullable=False)
    departure_airport_name = Column(String, nullable=False)
    departure_city = Column(String, nullable=False)
    arrival_airport = Column(String, nullable=False)
    arrival_airport_name = Column(String, nullable=False)
    arrival_city = Column(String, nullable=False)
    status = Column(String, nullable=False)
    aircraft_code = Column(String, nullable=False)
    actual_departure = Column(DateTime)
    actual_departure_local = Column(DateTime)
    actual_arrival = Column(DateTime)
    actual_arrival_local = Column(DateTime)
    actual_duration = Column(Interval)

engine = create_engine("postgresql://postgres:postgres@127.0.0.1/demo")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def get_dict(rows):
    result = []
    for row in rows:
        result.append({col.name: getattr(row, col.name) for col in row.__table__.columns})
    return result

def get_flights(limit=10, offset=0, flight_id=None, departure_airport=None, arrival_airport=None, actual_departure=None, actual_arrival=None):
    args = locals()
    args.pop('limit')
    args.pop('offset')

    session = Session()
    query = session.query(FlightV)

    for key, value in args.items():
        if value:
            query = query.filter(getattr(FlightV, key) == value)

    query = query.limit(limit).offset(offset)
    session.close()

    return get_dict(query.all())

def get_airports(limit=10, offset=0, airport_code=None, name_fragment=None):
    session = Session()
    query = session.query(Airport)

    if airport_code:
        query = query.filter(Airport.airport_code == airport_code)

    if name_fragment:
        query = query.filter(or_(
            Airport.airport_name.like(f'%{name_fragment}%'),
            Airport.city.like(f'%{name_fragment}%'),
        ))

    query = query.limit(limit).offset(offset)
    session.close()

    return get_dict(query.all())

def get_boarding_passes(limit=10, offset=0, ticket_id=None):
    session = Session()
    query = session.query(BoardingPass)

    if ticket_id:
        query = query.filter(BoardingPass.ticket_id == ticket_id)

    query = query.limit(limit).offset(offset)
    session.close()

    return get_dict(query.all())

def get_tickets(limit=10, offset=0, passenger_id=None, booking_id=None, ticket_id=None):
    session = Session()
    query = session.query(Ticket)

    if passenger_id:
        query = query.join(Booking).filter(Booking.passenger_id == passenger_id)

    if booking_id:
        query = query.filter(Ticket.book_ref == booking_id)

    if ticket_id:
        query = query.filter(Ticket.ticket_no == ticket_id)

    query = query.limit(limit).offset(offset)
    session.close()

    return get_dict(query.all())

def get_bookings(limit=10, offset=0, booking_id=None, book_date=None):
    session = Session()
    query = session.query(Booking)

    if booking_id:
        query = query.filter(Booking.book_ref == booking_id)

    if book_date:
        query = query.filter(Booking.book_date == book_date)

    query = query.limit(limit).offset(offset)
    session.close()

    return get_dict(query.all())

def add_booking(aircraft_code, passenger_id, flight_ids, seat_nos):
    session = Session()

    try:
        aircraft = session.query(Aircraft).filter_by(aircraft_code=aircraft_code).one()

        booking = Booking(
            book_ref=generate_booking_ref(),
            book_date=datetime.now(),
            total_amount=calculate_total_amount(),
            aircraft_code=aircraft_code,
            passenger_id=passenger_id
        )
        session.add(booking)

        for flight_id, seat_no in zip(flight_ids, seat_nos):
            ticket = Ticket(
                book_ref=booking.book_ref,
                seat_no=seat_no
            )
            session.add(ticket)

            boarding_pass = BoardingPass(
                ticket_no=ticket.ticket_no,
                seat_no=seat_no
            )
            session.add(boarding_pass)

        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        session.close()

def generate_booking_ref():
    characters = string.ascii_letters + string.digits
    booking_ref = ''.join(random.choices(characters, k=8))
    return booking_ref

def calculate_total_amount():
    return random.randint(100, 100000)