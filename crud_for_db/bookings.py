from typing import List, Type, Any

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from db.base import get_session
from db.tables import Booking
from models.booking_db import BookingIn


class BookingCRUD:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def read_all(self, limit, offset) -> List[Type[Booking]]:
        return self.session.query(Booking).limit(limit).offset(offset).all()

    def read_one(self, id: int) -> Booking | None:
        booking = self.session.query(Booking).filter(Booking.id == id).first()
        if booking is not None:
            return booking
        raise HTTPException(status_code=404, detail="Booking not found")

    def create(self, data: dict):
        obj = Booking(**data)
        self.session.add(obj)
        self.session.commit()
        return obj

    def delete(self, obj: Booking):
        self.session.delete(obj)
        self.session.commit()

    def read_by_params(self, booking_date: str | None, length_of_stay: int | None, guest_name: str | None,
                       daily_rate: float | None) -> Booking:
        if booking_date:
            result = self.session.query(Booking).filter(Booking.booking_date == booking_date).all()
        if length_of_stay:
            result = self.session.query(Booking).filter(Booking.length_of_stay == length_of_stay).all()
        if guest_name:
            result = self.session.query(Booking).filter(Booking.guest_name == guest_name).all()
        if daily_rate:
            result = self.session.query(Booking).filter(Booking.daily_rate == daily_rate).all()
        return result

    def __del__(self):
        self.session.close()
