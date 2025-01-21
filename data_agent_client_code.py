probabilities = {}
truth = {}
n_workers = 4
p = Pool(n_workers)


base_url = "http://localhost:8000/get_svc?"
for symbol in featureset["symbol"].unique()[2:]:  # AAPL is corrupted

    print(symbol)
    preds = []
    truth[symbol] = []
    path = "worker_data/" + symbol + ".csv"
    df = featureset[featureset["symbol"] == symbol]
    dates = [y for y in df["date"] if dt.strptime(y, "%Y-%m-%d").year >= 2022]

    df.to_csv(path, index=False)
    jobs = []
    url = "file_path={}&predict_date={}&target_name=target"
    for predict_date in dates:
        truth[symbol].append(df[df["date"] == predict_date]["target"].iloc[0])
        jobs.append(
            {
                "url": base_url + url.format(path, predict_date),
                "data": ",".join(predictors),
            }
        )
    results = p.map(post.wrech_mach, jobs)
    probabilities[symbol] = [json.loads(r.content.decode("utf-8")) for r in results]
    break
p.close()
