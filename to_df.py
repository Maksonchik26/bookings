import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def import_data_to_df():
    df = pd.read_csv("hotel_booking_data.csv")
    return df
    # df["arrival_date"] = df["arrival_date_year"].apply(lambda x: str(x)) + "-" + df["arrival_date_month"]\
    #                      + "-" + df["arrival_date_day_of_month"].apply(lambda x: str(x))
    # print(df["arrival_date"])
    #
    #
    # df['arrival_date'] = pd.to_datetime(df['arrival_date'])
    # df["booking_date"] = df['arrival_date'] - df['lead_time']
    # print(df['arrival_date'])
    # print("")
    # print("booking_date")

