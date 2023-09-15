from time import strftime

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def import_data_to_df():
    df = pd.read_csv("hotel_booking_data.csv")
    df.rename(columns = {"phone-number":"phone_number"}, inplace=True)
    df["arrival_date"] = df["arrival_date_year"].apply(lambda x: str(x)) + "-" + df["arrival_date_month"]\
                         + "-" + df["arrival_date_day_of_month"].apply(lambda x: str(x))

    df["arrival_date"] = pd.to_datetime(df["arrival_date"], format='mixed', errors="ignore")

    df["booking_date"] = df["arrival_date"] - df["lead_time"].apply(lambda x: timedelta(days=x))
    df["arrival_date"] = df["arrival_date"].dt.strftime("%Y-%m-%d")
    df["booking_date"] = df["booking_date"].dt.strftime("%Y-%m-%d")
    df["length_of_stay"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    df.drop(columns=["arrival_date_day_of_month",
                     "arrival_date_week_number",
                     "stays_in_weekend_nights",
                     "stays_in_week_nights"
                     ],
            inplace=True)

    return df
