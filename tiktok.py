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

def get_username_profile(username):
    conn = http.client.HTTPSConnection("api.tikapi.io")
    payload = ''
    headers = {
    'X-API-KEY': '56ONwxSEmceiI9b27WsP8Ai3bfRPSlqD'
    }
    req_text = "/public/check?username=" + username
    conn.request("GET", req_text, payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_string = data.decode("utf-8")
    tiktok_data = json.loads(json_string)
    return tiktok_data

def get_username_posts(secUid):
    conn = http.client.HTTPSConnection("api.tikapi.io")
    payload = ''
    headers = {
    'X-API-KEY': '56ONwxSEmceiI9b27WsP8Ai3bfRPSlqD'
    }
    req_text = "/public/posts?count=12&secUid=" + secUid
    conn.request("GET", req_text, payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_string = data.decode("utf-8")
    tiktok_data = json.loads(json_string)
    return tiktok_data

def get_socialmedia_value(reach, likes, comments, shares):
  conn = http.client.HTTPSConnection("api.socialmediavalue.io")
  payload = json.dumps({
    "impressions": int(reach),
    "likes": int(likes),
    "comments": int(comments),
    "savedPosts": int(shares)
  })
  headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
  conn.request("POST", "/instagram", payload, headers)
  res = conn.getresponse()
  data = res.read()
  json_string = data.decode("utf-8")
  tiktok_data = json.loads(json_string)
  return tiktok_data

def get_socialvalue_cpv(views):
  maximum_value = int(views)*0.15
  minimum_value = int(views)*0.01
  result_data = json.dumps({
    "maximum_value": maximum_value,
    "minimum_value": minimum_value
  })
  tiktok_data = json.loads(result_data)
  return tiktok_data

def get_socialvalue_cpl(likes):
  maximum_value = int(likes)*0.16
  minimum_value = int(likes)*0.05
  result_data = json.dumps({
    "maximum_value": maximum_value,
    "minimum_value": minimum_value
  })
  tiktok_data = json.loads(result_data)
  return tiktok_data

def get_socialvalue_cpm(impressions):
  maximum_value = int(impressions)/1000*12
  minimum_value = int(impressions)/1000*0.16
  average_value = int(impressions)/1000*6.37
  result_data = json.dumps({
    "maximum_value": maximum_value,
    "minimum_value": minimum_value,
    "average_value":average_value
  })
  tiktok_data = json.loads(result_data)
  return tiktok_data

def get_socialvalue(views,likes,impressions):
  cpv = get_socialvalue_cpv(views)
  cpl = get_socialvalue_cpl(likes)
  cpm = get_socialvalue_cpm(impressions)
  result_data = json.dumps({
    "max_val_cpv": cpv['maximum_value'],
    "min_val_cpv": cpv['minimum_value'],
    "max_val_cpl": cpl['maximum_value'],
    "min_val_cpl": cpl['minimum_value'],
    "max_val_cpm": cpm['maximum_value'],
    "min_val_cpm": cpm['minimum_value'],
    "avg_val_cpm": cpm['average_value'],
    "maximum_value": cpl['maximum_value'] + cpv['maximum_value'] + cpm['maximum_value'],
    "minimum_value": cpl['minimum_value'] + cpv['minimum_value']+ cpm['minimum_value']
  })
  tiktok_data = json.loads(result_data)
  return tiktok_data

def post_data(data):
  conn = http.client.HTTPSConnection("hooks.zapier.com")
  payload = json.dumps(data)
  headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
  conn.request("POST", "/hooks/catch/7655196/bfterek", payload, headers)
  res = conn.getresponse()
  data = res.read()
  json_string = data.decode("utf-8")
  tiktok_data = json.loads(json_string)
  return tiktok_data
