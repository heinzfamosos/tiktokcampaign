""" import requests
import json

url = "https://api.tikapi.io/public/hashtag?name=palabrascomoamuletos"

payload={}
headers = {
  'X-API-KEY': '56ONwxSEmceiI9b27WsP8Ai3bfRPSlqD'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
 """

import http.client
import json 


def get_data(hashtag):
    conn = http.client.HTTPSConnection("api.tikapi.io")
    payload = ''
    headers = {
    'X-API-KEY': '56ONwxSEmceiI9b27WsP8Ai3bfRPSlqD'
    }
    req_text = "/public/hashtag?name=" + hashtag
    conn.request("GET", req_text, payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_string = data.decode("utf-8")
    tiktok_data = json.loads(json_string)
    return tiktok_data