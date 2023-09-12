import pandas as pd

from db.base import engine

def import_data():
    df = pd.read_csv("hotel_booking_data.csv")

    df_copy = pd.DataFrame(columns=["id", "booking_date", "length_of_stay", "guest_name", "daily_rate"])
    df_copy["booking_date"] = df['arrival_date_year'].astype(str) + '-' + \
                                 df['arrival_date_month'].astype(str) + '-' + \
                                 df['arrival_date_day_of_month'].astype(str)
    df_copy["length_of_stay"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    df_copy["guest_name"] = df["name"]
    df_copy["daily_rate"] = df["adr"]
    df_copy["id"] = df_copy.index

    df_copy.to_sql('bookings', con=engine, if_exists="append", index=False)
