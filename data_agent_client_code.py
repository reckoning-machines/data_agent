from multiprocessing import Pool
import requests
import data_agent_post
import pandas as pd
import json
from datetime import datetime as dt
import toml
import os


if __name__ == "__main__":
    script_path = os.path.dirname(os.path.realpath(__file__))

    SETTINGS = toml.load(f"{script_path}/settings.toml")
    symbol_list = SETTINGS["symbols"]
    macro_list = SETTINGS["macros"]

    probabilities = {}
    truth = {}
    n_workers = 4
    p = Pool(n_workers)

    base_url = "http://localhost:8000/get_svc?symbol={}&data_agent={}"
    jobs = []
    for symbol in symbol_list:
        path = "worker_data/" + symbol + ".csv"
        """
        jobs:
        1. data agent type
        2. ticker list
        """

        print(symbol)
        some_variable = ""
        data_list = []
        url = ""
        agent_type = "yahoo"
        jobs.append({"url": base_url.format(symbol, agent_type)})

    for symbol in macro_list:
        path = "worker_data/" + symbol + ".csv"
        """
        jobs:
        1. data agent type
        2. ticker list
        """

        print(symbol)
        some_variable = ""
        data_list = []
        url = ""
        agent_type = "yahoo"
        jobs.append({"url": base_url.format(symbol, agent_type)})

    print(jobs)
    results = p.map(data_agent_post.wrech_mach, jobs)
    print(results)
    p.close()
