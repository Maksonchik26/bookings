from pydantic import BaseModel, Field


class BookingIn(BaseModel):
    booking_date: str = Field(min_length=10)
    length_of_stay: int = Field(ge=0)
    guest_name: str = Field(min_length=3)
    daily_rate: float = Field(ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "booking_date": "2022-May-1",
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
