import pandas as pd
from flask import Flask, request
import requests

print("version 0.0.1")

app = Flask(__name__)


@app.route("/get_svc", methods=["GET", "POST"])
def get_svc():
    try:
        pass
    except Exception as e:
        pass
        return '{"Status":, "' + str(e) + '"}'
