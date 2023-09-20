from typing import List, Optional, Dict, Annotated

import pandas as pd
from fastapi import APIRouter, Depends, Path, status, Query

from starlette.responses import Response

import auth
from crud_for_db.bookings import BookingCRUD
from models import booking_db, booking_df
from to_df import import_data_to_df


bookings = APIRouter(
    prefix="/bookings",
    tags=["bookings"]
)

stats = APIRouter(
    prefix="/bookings/stats",
    tags=["stats"]
)

analysis = APIRouter(
    prefix="/bookings/analysis",
    tags=["analysis"]
)


@bookings.get("/", response_model=List[booking_db.BookingOut],
              status_code=status.HTTP_200_OK,
              description=" Retrieves a list of all bookings in the dataset",
              )
async def get_all(crud: BookingCRUD = Depends()):
    data = crud.read_all()
    return data


@bookings.post("/", response_model=booking_db.BookingOut,
               status_code=status.HTTP_201_CREATED,
               description="Create booking in db"
               )
async def create(data: booking_db.BookingIn,
           crud: BookingCRUD = Depends()):
    data = crud.create(data.__dict__)
    return data


@bookings.delete("/{booking_id}",
                 status_code=status.HTTP_204_NO_CONTENT,
                 description="Delete the booking by id")
async def delete(booking_id: int = Path(ge=0),
           crud: BookingCRUD = Depends()):
    data = crud.read_one(booking_id)
    crud.delete(data)
    return Response()


@bookings.get("/nationality",
              response_model=List[booking_df.BookingOut],
              status_code=status.HTTP_200_OK,
              description="Retrieves bookings based on the provided nationality")
async def get_by_nationality(country: str, df=Depends(import_data_to_df)):
    data = df[df["country"] == country.upper()].head(100)
    return Response(data.to_json(orient="records"), media_type="application/json")


@bookings.get("/popular_meal_package",
              response_model=Dict[str, str],
              status_code=status.HTTP_200_OK,
              description="Retrieves the most popular meal package among all bookings")
async def get_popular_meal_package(df=Depends(import_data_to_df)):
    data = df["meal"].value_counts().idxmax()
    return {"popular_meal_package": data}


@bookings.get("/total_revenue",
              response_model=Dict[str, Dict[str, float]],
              status_code=status.HTTP_200_OK,
              description="Retrieves the total revenue grouped by booking month and hotel type"
              )
async def get_total_revenue(df=Depends(import_data_to_df)):
    df["revenue"] = df["adr"] * df["length_of_stay"]
    revenues = df.groupby(["hotel", "arrival_date_month"])[["revenue"]].sum()
    city_hotels_rev = revenues.xs("City Hotel").rename(columns={"revenue": "City Hotel"}).to_dict()
    resort_hotels_rev = revenues.xs("Resort Hotel").rename(columns={"revenue": "Resort Hotel"}).to_dict()
    data = city_hotels_rev | resort_hotels_rev
    return data


@bookings.get("/top_countries",
              response_model=Dict[int, str],
              status_code=status.HTTP_200_OK,
              description="Retrieves the top 5 countries with the highest number of bookings"
              )
async def get_top_countries(df=Depends(import_data_to_df)):
    top_countries = df["country"].value_counts().head().index.to_list()
    data = {}
    for i, country in enumerate(top_countries):
        data[i+1] = country
    return data


@bookings.get("/search",
              response_model=List[booking_db.BookingOut] | booking_db.BookingOut,
              status_code=status.HTTP_200_OK,
              description="""Allows searching for bookings based on various parameters such as guest name,
              booking dates, length of stay, etc""")
async def get_by_param(booking_date: Optional[str] = None,
                 length_of_stay: Optional[int] = None,
                 daily_rate: Optional[float] = None,
                 guest_name: Optional[str] = None,
                 crud: BookingCRUD = Depends()):
    data = crud.read_by_params(booking_date, length_of_stay, guest_name, daily_rate)
    return data


@bookings.get("/avg_length_of_stay",
              response_model=Dict[str, Dict[str, float]],
              status_code=status.HTTP_200_OK,
              description="Retrieves the average length of stay grouped by booking year and hotel type"
              )
async def get_avg_length_of_stay(df=Depends(import_data_to_df)):
    df_without_canceled = df[df["is_canceled"] == 0]
    df_without_canceled["booking year"] = df["booking_date"].apply(lambda x: x[:4])
    avg_length_of_stay = df_without_canceled.groupby(["hotel", "booking year"])[["length_of_stay"]].mean()
    city_hotels_avg = avg_length_of_stay.xs("City Hotel").rename(columns={"length_of_stay": "City Hotel"})
    resort_hotels_avg = avg_length_of_stay.xs("Resort Hotel").rename(columns={"length_of_stay": "Resort Hotel"})
    data = city_hotels_avg.to_dict() | resort_hotels_avg.to_dict()
    return data


@bookings.get("/repeated_guests_percentage",
              response_model=Dict[str, float],
              status_code=status.HTTP_200_OK,
              description="Retrieves the percentage of repeated guests among all bookings.",
              )
async def get_repeated_guests_percentage(df=Depends(import_data_to_df)):
    repeated_guests = df[df["is_repeated_guest"] == 1]
    data = round((len(repeated_guests) / len(df) * 100), 2)
    return {"percentage_o_repeated_guests": data}


@bookings.get("/total_guests_by_year",
              response_model=Dict[int, int],
              status_code=status.HTTP_200_OK,
              description="Retrieves the total number of guests (adults, children, and babies) by booking year",
              )
async def get_total_guests_by_year(df=Depends(import_data_to_df)):
    df["guests"] = df["adults"] + df["children"] + df["babies"]
    df["booking_year"] = df["booking_date"].apply(lambda x: x[:4])
    data = df.groupby(["booking_year"])["guests"].sum()
    return Response(data.to_json(orient="index"), media_type="application/json")


@bookings.get("/avg_daily_rate_resort",
              response_model=Dict[str, Dict[str, float]],
              status_code=status.HTTP_200_OK,
              description="Retrieves the average daily rate by month for resort hotel bookings",
              )
async def get_avg_daily_rate_resort(credentials: Annotated[str, Depends(auth.verify_credentials)],
                              df=Depends(import_data_to_df)):
    df = df[df["hotel"] == "Resort Hotel"]
    data = df.groupby(["arrival_date_month"])[["adr"]].mean()
    return Response(data.to_json(orient="index"), media_type="application/json")


@bookings.get("/count_by_hotel_meal",
              response_model=Dict[str, Dict[str, int]],
              status_code=status.HTTP_200_OK,
              description="Retrieves the count of bookings grouped by hotel type and meal package",
              )
async def get_count_by_hotel_meal(credentials: Annotated[str, Depends(auth.verify_credentials)],
                            df=Depends(import_data_to_df)):
    df = df[["hotel", "meal"]].value_counts().to_frame()
    city_hotels = df.xs("City Hotel").rename(columns={"count": "City Hotel"})
    resort_hotels = df.xs("Resort Hotel").rename(columns={"count": "Resort Hotel"})
    data = city_hotels.to_dict() | resort_hotels.to_dict()
    return data


@bookings.get("/total_revenue_resort_by_country",
              response_model=Dict[str, Dict[str, float]],
              status_code=status.HTTP_200_OK,
              description="Retrieves the total revenue by country for resort hotel bookings",
              )
async def get_total_revenue_resort_by_country(credentials: Annotated[str, Depends(auth.verify_credentials)],
                                        df=Depends(import_data_to_df)):
    df = df[df["hotel"] == "Resort Hotel"]
    df["revenue"] = df["adr"] * df["length_of_stay"]
    data = df.groupby(["country"])[["revenue"]].sum()

    return Response(data.to_json(orient="index"), media_type="application/json")


@bookings.get("/most_common_arrival_day_city",
              response_model=Dict[str, str],
              status_code=status.HTTP_200_OK,
              description="Retrieves the most common arrival date day of the week for city hotel bookings",
              response_description="Number of the day of the week, where Monday = 0",
              )
async def get_most_common_arrival_day_city(credentials: Annotated[str, Depends(auth.verify_credentials)],
                                     df=Depends(import_data_to_df)):
    df = df[df["hotel"] == "City Hotel"]
    df["arrival_date_day_of_the_week"] = pd.DatetimeIndex(df["arrival_date"]).weekday
    data = df["arrival_date_day_of_the_week"].value_counts().idxmax()
    return {"most_common_arrival_day_city": int(data)}


@bookings.get("/count_by_hotel_repeated_guest",
              response_model=Dict[str, Dict[int, int]],
              status_code=status.HTTP_200_OK,
              description="Retrieves the count of bookings grouped by hotel type and repeated guest status",
              response_description="0 - guest is not repeated, 1 - guest is repeated",
              )
async def get_count_by_hotel_repeated_guest(credentials: Annotated[str, Depends(auth.verify_credentials)],
                                      df=Depends(import_data_to_df)
                                      ):
    df = df[["hotel", "is_repeated_guest"]].value_counts().to_frame()
    city_hotels = df.xs("City Hotel").rename(columns={"count": "City Hotel"})
    resort_hotels = df.xs("Resort Hotel").rename(columns={"count": "Resort Hotel"})
    data = city_hotels.to_dict() | resort_hotels.to_dict()
    return data


@bookings.get("/{booking_id}",
              response_model=List[booking_db.BookingOut] | booking_db.BookingOut,
              description="Retrieves details of a specific booking by its unique ID",
              status_code=status.HTTP_200_OK)
async def get_one(booking_id: int = Path(ge=0),
            crud: BookingCRUD = Depends()):
    data = crud.read_one(booking_id)
    return data


@stats.get("/total_number_of_bookings",
           response_model=Dict[str, int],
           description="Retrieves total number of bookings",
           status_code=status.HTTP_200_OK)
async def get_total_number_of_bookings(df=Depends(import_data_to_df)):
    return {"total_number_of_bookings": len(df)}


@stats.get("/avg_length_of_stay",
           response_model=Dict[str, float],
           description="Retrieves the average length of stay",
           status_code=status.HTTP_200_OK)
async def get_avg_length_of_stay(df=Depends(import_data_to_df)):
    df["length_of_stay"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    return {"avg_length_of_stay": df["length_of_stay"].mean()}


@stats.get("/avg_daily_rate",
           response_model=Dict[str, float],
           status_code=status.HTTP_200_OK,
           description="Retrieves the average daily rate bookings"
           )
async def get_avg_daily_rate(df=Depends(import_data_to_df)):
    data = df[["adr"]].mean()
    return Response(data.to_json(orient="index"), media_type="application/json")


@stats.get("/repeated_guests_percentage",
           response_model=Dict[str, float],
           status_code=status.HTTP_200_OK,
           description="Retrieves the percentage of repeated guests among all bookings."
           )
async def get_repeated_guests_percentage(df=Depends(import_data_to_df)):
    repeated_guests = df[df["is_repeated_guest"] == 1]
    data = round((len(repeated_guests) / len(df) * 100), 2)
    return {"percentage_o_repeated_guests": data}



@analysis.get("/total_revenue",
              status_code=status.HTTP_200_OK,
              response_model=Dict[str, Dict[str, float]],
              description="Retrieves the total revenue grouped by booking month and hotel type"
              )
async def get_total_revenue(df=Depends(import_data_to_df)):
    df["revenue"] = df["adr"] * df["length_of_stay"]
    revenues = df.groupby(["hotel", "arrival_date_month"])[["revenue"]].sum()
    city_hotels_rev = revenues.xs("City Hotel").rename(columns={"revenue": "City Hotel"}).to_dict()
    resort_hotels_rev = revenues.xs("Resort Hotel").rename(columns={"revenue": "Resort Hotel"}).to_dict()
    data = city_hotels_rev | resort_hotels_rev
    return data


@analysis.get("/top_countries_bookings",
              status_code=status.HTTP_200_OK,
              response_model=Dict[str, int],
              description="Retrieves the top 5 countries bookings with the highest number of bookings"
              )
async def get_top_countries_bookings(df=Depends(import_data_to_df)):
    data = df["country"].value_counts().head()
    return Response(data.to_json(orient="index"), media_type="application/json")


@analysis.get("/total_guests_by_year",
              status_code=status.HTTP_200_OK,
              description="Retrieves the total number of guests (adults, children, and babies) by booking year",
              response_model=Dict[int, int]
              )
async def get_total_guests_by_year(df=Depends(import_data_to_df)):
    df["guests"] = df["adults"] + df["children"] + df["babies"]
    df["booking_year"] = df["booking_date"].apply(lambda x: x[:4])
    data = df.groupby(["booking_year"])["guests"].sum()
    return Response(data.to_json(orient="index"), media_type="application/json")
