from typing import List

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from crud.bookings import BookingCRUD
from models.booking import BookingOut, BookingIn
from to_df import import_data_to_df

bookings = APIRouter(
    prefix='/bookings',
    tags=['bookings']
)

stats = APIRouter(
    prefix='/bookings/stats',
    tags=['/bookings/stats']
)



@bookings.get('/', response_model=List[BookingOut], status_code=status.HTTP_200_OK)
def get_all(test_crud: BookingCRUD = Depends()):
    data = test_crud.read_all()
    return data


@bookings.post('/', response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def create(test_data: BookingIn,
           test_crud: BookingCRUD = Depends()):
    data = test_crud.create(test_data.__dict__)
    return data


@bookings.delete('/{id}', response_model=BookingOut)
def delete(id: int,
           test_crud: BookingCRUD = Depends()):
    data = test_crud.read_one(id)
    test_crud.delete(data)
    return Response()


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


@bookings.get('/{test_id}', response_model=List[BookingOut] | BookingOut, status_code=status.HTTP_200_OK)
def get_one(test_id: int,
            test_crud: BookingCRUD = Depends()):
    data = test_crud.read_one(test_id)
    return data


# @bookings.get('/stats/', status_code=status.HTTP_200_OK)
# def get_(test_id: int,
#             test_crud: BookingCRUD = Depends()):
#     data = test_crud.read_one(test_id)
#     return data




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
