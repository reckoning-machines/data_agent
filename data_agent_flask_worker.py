import pandas as pd
from flask import Flask, request
import requests
from data_agent import *

print("version 0.0.1")

app = Flask(__name__)


@app.route("/get_svc", methods=["GET", "POST"])
def get_svc():
    """
    run job, return dataframe, save to S3
    1. read data agent type
    2. create data agent
    3. return data agent data
    """
    data_agent = request.args.get("data_agent")
    symbol = request.args.get("symbol")
    match data_agent:
        case "yahoo":
            da = YahooDataAgent(symbol)

    da.get_data()
    return "Success"
