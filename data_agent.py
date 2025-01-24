"""
data agents for use by flask worker
"""

"""
imports
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
import yfinance as yf
import pandas as pd
import boto3
import toml
import os
from datetime import datetime
from skimpy import clean_columns
from fredapi import Fred


"""
globals
"""
script_path = os.path.dirname(os.path.realpath(__file__))
KEYS = toml.load(f"{script_path}/keys.toml")
RUN_TYPE = ""
API_KEY = KEYS["fmp"]
SETTINGS = toml.load(f"{script_path}/settings.toml")
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}
today = datetime.now()
DATE_DIR = today.strftime("%Y%m%d")
DATE_STR = today.strftime("%Y-%m-%d")
TICKER_LIST = SETTINGS["symbols"]
BUCKET_NAME = "reckoning-machines-datapull"

"""
s3 session
"""
session = boto3.Session(
    aws_access_key_id=KEYS["key"],
    aws_secret_access_key=KEYS["secret"],
)

S3 = boto3.resource("s3")

"""
helper functions
"""


def upload_to_s3(filename, bucket, key):
    try:
        S3 = session.resource("s3")
        S3 = boto3.resource(
            "s3",
            region_name="us-east-2",
            aws_access_key_id=KEYS["key"],
            aws_secret_access_key=KEYS["secret"],
        )
        response = S3.Object(bucket, key).put(Body=open(filename, "rb"))
        print(response)
        return response
    except Exception as error:
        print(error)


def save_file(
    df, end_point, symbol="", put_to_s3=SETTINGS["put_to_s3"], clean_cols=True
):
    df = df.loc[:, ~df.columns.duplicated()]

    folder_name = f"data-agent-datapull"
    if clean_cols:
        df = clean_columns(df)
    df["datapull_date"] = DATE_STR

    os.makedirs(folder_name, exist_ok=True)
    file_name = f"{folder_name}/{end_point}"

    if df is not None:
        df = df.astype(str)
        if symbol != "":
            if "symbol" not in df.columns:
                df["symbol"] = symbol

        if SETTINGS["file_type"] == "csv":
            file_name = f"{file_name}.csv"
            df.to_csv(file_name, index=False)

        if SETTINGS["file_type"] == "parquet":
            try:
                file_name = f"{file_name}.pq"
                df.to_parquet(file_name, index=False)
            except:
                print("df save to parquet error")
                print(type(df))
                print(df)

    if put_to_s3 == "True":
        upload_to_s3(file_name, BUCKET_NAME, file_name)

    return


@dataclass
class DataAgent(ABC):
    _symbol: str
    _data: pd.DataFrame = None

    @abstractmethod
    def get_data(self, *args, **kwargs):
        # create json jobs
        pass


@dataclass
class YahooDataAgent(DataAgent):
    """
    class to retrieve yahoo finance data
    """

    _symbol: str
    name: str = "YahooDataAgent"

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        if not isinstance(value, str):
            raise TypeError("symbol must be a string")
        self._symbol = value

    def get_data(self):
        print("get data")
        self._data = yf.download([self._symbol], "2015-1-1")["Close"].reset_index()

    def save(self):
        save_file(self._data, end_point="yahoo-prices", symbol=self._symbol)


@dataclass
class FREDDataAgent(DataAgent):
    """
    class to retrieve yahoo finance data
    """

    _symbol: str
    name: str = "FREDDataAgent"

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        if not isinstance(value, str):
            raise TypeError("symbol must be a string")
        self._symbol = value

    def get_data(self, symbol):
        from datetime import date

        today = date.today()
        today = today.strftime("%Y-%m-%d")

        FRED = Fred(KEYS["fred"])

        fred_list = []
        s = pd.DataFrame(
            FRED.get_series(
                symbol,
                observation_start="2018-01-01",
            )
        ).reset_index()
        s.dropna(inplace=True)
        s.columns = ["date", "value"]
        s["series"] = symbol
        fred_list.append(s)
        df_fred = pd.concat(fred_list)

        self._data = df_fred.dropna()

        return

    def save(self):
        save_file(self._data, end_point="fred-prices", symbol=self._symbol)
