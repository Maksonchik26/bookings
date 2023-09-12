from pydantic import BaseModel


class BookingIn(BaseModel):
    # id: int
    booking_date: str
    length_of_stay: int
    guest_name: str
    daily_rate: float


class BookingOut(BaseModel):
    id: int | None
    booking_date: str
    length_of_stay: int
    guest_name: str
    daily_rate: float

