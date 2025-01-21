from sklearn.svm import SVC
import pandas as pd
from flask import Flask, request
from sklearn.preprocessing import RobustScaler
import requests

print("version 0.3")

app = Flask(__name__)


@app.route("/get_svc", methods=["GET", "POST"])
def get_svc():
    scaler = RobustScaler()
    file_path = request.args.get("file_path")
    target_name = request.args.get("target_name")
    predict_date = request.args.get("predict_date")

    predictors = request.data.decode("utf-8").split(",")
    df = pd.read_csv(file_path)
    target = df[df["date"] < predict_date][target_name]
    pdf = df[df["date"] < predict_date][predictors]
    pdf[predictors] = scaler.fit_transform(pdf[predictors])
    #    clf = SVC(C = 2, probability=True)
    clf = SVC(C=2, probability=False)
    try:
        clf.fit(pdf.iloc[:-1], target.iloc[1:])
        return (
            '{"Status": "OK", "prediction":'
            + str(clf.predict(pdf.iloc[-1:])[0])
            + ', "probability": '
            + str(clf.decision_function(pdf.iloc[-1:])[0])
            + ', "date": "'
            + predict_date
            + '"}'
        )
    except Exception as e:
        print(file_path)
        print(e)
        print(pdf.shape)
        print(predict_date)
        return '{"Status":, "' + str(e) + '"}'
