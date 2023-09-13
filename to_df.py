import pandas as pd
import numpy as np
from datetime import datetime, timedelta



def import_data_to_df():
    df = pd.read_csv("hotel_booking_data.csv")

    df["arrival_date"] = df["arrival_date_year"].apply(lambda x: str(x)) + "-" + df["arrival_date_month"]\
                         + "-" + df["arrival_date_day_of_month"].apply(lambda x: str(x))
    print(df["lead_time"])

    df["arrival_date"] = df["arrival_date_year"].apply(lambda x: str(x)) + "-" + df["arrival_date_month"]\
                         + "-" + df["arrival_date_day_of_month"].apply(lambda x: str(x))

    df["arrival_date"] = pd.to_datetime(df["arrival_date"], format='mixed', errors="ignore")

    df["booking_date"] = df["arrival_date"] - df["lead_time"].apply(lambda x: timedelta(days=x))

    return df
