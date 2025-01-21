from multiprocessing import Pool
import requests
import data_agent_post
import pandas as pd
import json
from datetime import datetime as dt


probabilities = {}
truth = {}
n_workers = 4
p = Pool(n_workers)


base_url = "http://localhost:8000/get_svc?"
symbol_list = []
jobs = []
for symbol in symbol_list:
    path = "worker_data/" + symbol + ".csv"
    # df = featureset[featureset['symbol'] == symbol]
    # dates = [y for y in df['date'] if dt.strptime(y, '%Y-%m-%d').year >= 2022]
    # df.to_csv(path, index=False)

    print(symbol)
    some_variable = ""
    data_list = []
    url = ""
    jobs.append(
        {
            "url": base_url + url.format(path, some_variable),
            "data": ",".join(data_list),
        }
    )
    results = p.map(data_agent_post.wrech_mach, jobs)
    probabilities[symbol] = [json.loads(r.content.decode("utf-8")) for r in results]
    break
p.close()
