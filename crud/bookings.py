from typing import List, Type, Any

from fastapi import Depends
from sqlalchemy.orm import Session

from db.base import get_session
from db.tables import Booking


class BookingCRUD:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def read_all(self) -> List[Type[Booking]]:
        return self.session.query(Booking).all()

    def read_one(self, id: int) -> Booking | None:
        return self.session.query(Booking).filter(Booking.id == id).first()

    def create(self, data: dict):
        obj = Booking(**data)
        self.session.add(obj)
        self.session.commit()
        return obj

    def update(self, obj: Booking, name: str, value: Any):
        setattr(obj, name, value)
        self.session.commit()

    def delete(self, obj: Booking):
        self.session.delete(obj)
        self.session.commit()

    def __del__(self):
        self.session.close()