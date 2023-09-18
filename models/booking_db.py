from pydantic import BaseModel


class BookingIn(BaseModel):
    booking_date: str
    length_of_stay: int
    guest_name: str
    daily_rate: float

    class Config:
        json_schema_extra = {
            "example": {
                "booking_date": "18-08-2023",
                "length_of_stay": 32,
                "guest_name": "Max",
                "daily_rate": 30.2
            }
        }


class BookingOut(BookingIn):
    id: int | None
    booking_date: str
    length_of_stay: int
    guest_name: str
    daily_rate: float
