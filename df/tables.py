from sqlalchemy import Integer, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Bookings(Base):
    __tablename__ = 'bookings'

    hotel: Mapped[str] = mapped_column(String(256))
    is_canceled: Mapped[int] = mapped_column(Integer())
    lead_time: Mapped[int] = mapped_column(Integer())
    arrival_date_year: Mapped[int] = mapped_column(Integer())
    arrival_date_month: Mapped[str] = mapped_column(String(256))
    arrival_date_week_number: Mapped[int] = mapped_column(Integer())
    arrival_date_day_of_month: Mapped[int] = mapped_column(Integer())
    stays_in_weekend_nights: Mapped[int] = mapped_column(Integer())
    stays_in_week_nights: Mapped[int] = mapped_column(Integer())
    adults: Mapped[int] = mapped_column(Integer())
    children: Mapped[int] = mapped_column(Integer(), nullable=True)
    babies: Mapped[int] = mapped_column(Integer())
    meal: Mapped[str] = mapped_column(String(256))
    country: Mapped[str] = mapped_column(String(256))
    market_segment: Mapped[str] = mapped_column(String(256))
    distribution_channel: Mapped[str] = mapped_column(String(256))
    is_repeated_guest: Mapped[int] = mapped_column(Integer())
    previous_cancellations: Mapped[int] = mapped_column(Integer())
    previous_bookings_not_canceled: Mapped[int] = mapped_column(Integer())
    reserved_room_type: Mapped[str] = mapped_column(String(256))
    assigned_room_type: Mapped[str] = mapped_column(String(256))
    booking_changes: Mapped[int] = mapped_column(Integer())
    deposit_type: Mapped[str] = mapped_column(String(256))
    agent: Mapped[int] = mapped_column(Integer(), nullable=True)
    company: Mapped[int] = mapped_column(Integer(), nullable=True)
    days_in_waiting_list: Mapped[int] = mapped_column(Integer())
    customer_type: Mapped[str] = mapped_column(String(256))
    adr: Mapped[float] = mapped_column(Float(), nullable=True, default=0)
    required_car_parking_spaces: Mapped[int] = mapped_column(Integer())
    total_of_special_requests: Mapped[int] = mapped_column(Integer())
    reservation_status: Mapped[str] = mapped_column(String(256))
    reservation_status_date: Mapped[str] = mapped_column(String(256))
    name: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String(256))
    phone_number: Mapped[str] = mapped_column(String(256))
    credit_card: Mapped[str] = mapped_column(String(256))
