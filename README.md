Multithreading financial datapull

User story: As a financial analyst I want to pull multiple tickers' data so that I have a cache of data for use in subsequent preprocessing for analysis.

This repo will allow for a client code app to assemble a json "jobs" list to send to gunicorn, which then multithreads the data calls.  In this case I am using 6 cores.

data_pull.py contains an abstract base data class and one contrete data class; yahoo
missing: settings.toml and keys.toml which contain my s3 keys and file save settings - I can email on request
data_agent_client_code.py shows how to run the data pull
- assuming gunicorn is running
- for one symbol (for now)
- create a jobs map for multiprocessing
- send to flask
data_agent_flask_worker.py is the flask worker which reads the jobs url and creates the associated data class from a case statement
- saves file to s3
data_agent_post.py is the post file for flask

usage:
gunicorn --timeout 600 -w 6 'data_agent_flask_worker:app' in the same directory
run data_agent_client_code.py

<img width="551" alt="image" src="https://github.com/user-attachments/assets/f91560df-80c1-4815-9c23-4f96dd5e4c3f" />
