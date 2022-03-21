import requests
import time

while True:
    params = {}
    headers = {}
    url = 'http://42.192.50.232:8002/fansile'
    requests.request('get', url, json=params, headers=headers)
    time.sleep(60*60)