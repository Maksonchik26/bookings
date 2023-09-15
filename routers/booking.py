import json
from typing import List

from fastapi import APIRouter, Depends, Path
from pydantic import Field
from starlette import status
from starlette.responses import Response

from crud_for_db.bookings import BookingCRUD
from models import booking_db, booking_df
from to_df import import_data_to_df

bookings = APIRouter(
    prefix='/bookings',
    tags=['bookings']
)

stats = APIRouter(
    prefix='/bookings/stats',
    tags=['/bookings/stats']
)


@bookings.get('/', response_model=List[booking_db.BookingOut], status_code=status.HTTP_200_OK)
def get_all(test_crud: BookingCRUD = Depends()):
    data = test_crud.read_all()
    return data


@bookings.post('/', response_model=booking_db.BookingOut, status_code=status.HTTP_201_CREATED)
def create(test_data: booking_db.BookingIn,
           test_crud: BookingCRUD = Depends()):
    data = test_crud.create(test_data.__dict__)
    return data


@bookings.delete('/{id}', response_model=booking_db.BookingOut)
def delete(id: int,
           test_crud: BookingCRUD = Depends()):
    data = test_crud.read_one(id)
    test_crud.delete(data)
    return Response()


@bookings.get("/nationality",
              response_model=List[booking_df.BookingOut],
              status_code=status.HTTP_200_OK)
def get_by_nationality(country: str, df=Depends(import_data_to_df)):
    filter_data = df[df["country"] == country].head(2)
    data = [json.loads(filter_data.iloc[i].to_json()) for i in range(len(filter_data))]
    return data


@bookings.get("/popular_meal_package", status_code=status.HTTP_200_OK)
def get_popular_meal_package(df=Depends(import_data_to_df)):
    data = df["meal"].value_counts().idxmax()
    return {"popular_meal_package": data}


@bookings.get("/total_revenue", status_code=status.HTTP_200_OK)
def get_total_revenue(df=Depends(import_data_to_df)):
    df["revenue"] = df["adr"] * df["length_of_stay"]
    revenues = df.groupby(["hotel", "arrival_date_month"])[["revenue"]].sum()
    city_hotels_rev = revenues.xs("City Hotel").rename(columns={"revenue": "City Hotel"}).to_dict()
    resort_hotels_rev = revenues.xs("Resort Hotel").rename(columns={"revenue": "Resort Hotel"}).to_dict()
    data = city_hotels_rev | resort_hotels_rev
    return data






@bookings.get('/search', status_code=status.HTTP_200_OK)
def get_by_param(booking_date: str | None = None,
                 length_of_stay: str | None = None,
                 daily_rate: str | None = None,
                 guest_name: str | None = None,
                 test_crud: BookingCRUD = Depends()):
    data = test_crud.read_by_params(booking_date, length_of_stay, guest_name, daily_rate)
    return data


@bookings.get("/avg_length_of_stay", status_code=status.HTTP_200_OK)
def get_avg_length_of_stay(df=Depends(import_data_to_df)):
    df["length_of_stay"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    return {"avg_length_of_stay": df["length_of_stay"].mean()}


@bookings.get('/{id}', response_model=List[booking_db.BookingOut] | booking_db.BookingOut,
              status_code=status.HTTP_200_OK)
def get_one(id: int = Path(ge=0),
            test_crud: BookingCRUD = Depends()):
    data = test_crud.read_one(id)
    return data


@bookings.get("/avg_daily_rate/{id}", status_code=status.HTTP_200_OK)
def get_avg_daily_rate(id: int, df=Depends(import_data_to_df)):
    return {"avg_daily_rate": df.iloc[id]["adr"]}


@stats.get("/total_number_of_bookings", status_code=status.HTTP_200_OK)
def get_total_number_of_bookings(df=Depends(import_data_to_df)):
    return {"total_number_of_bookings": len(df)}


@stats.get("/avg_length_of_stay", status_code=status.HTTP_200_OK)
def get_avg_length_of_stay(df=Depends(import_data_to_df)):
    df["length_of_stay"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    return {"avg_length_of_stay": df["length_of_stay"].mean()}

