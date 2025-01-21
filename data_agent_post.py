import requests


def wrech_mach(p):
    return requests.post(p["url"])
