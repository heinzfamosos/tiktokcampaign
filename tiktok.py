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
import numpy
 
 
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        if isinstance(obj, numpy.floating):
            return float(obj)
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


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

def get_data_search(keywords):
    conn = http.client.HTTPSConnection("api.tikapi.io")
    payload = ''
    headers = {
    'X-API-KEY': '56ONwxSEmceiI9b27WsP8Ai3bfRPSlqD'
    }
    req_text = "/public/search/general?query=" + keywords
    conn.request("GET", req_text, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    json_string = data.decode("utf-8")
    tiktok_data = json.loads(json_string)
    return tiktok_data

def get_data_search_users(keywords):
    conn = http.client.HTTPSConnection("api.tikapi.io")
    payload = ''
    headers = {
    'X-API-KEY': '56ONwxSEmceiI9b27WsP8Ai3bfRPSlqD'
    }
    req_text = "/public/search/users?query=" + keywords
    conn.request("GET", req_text, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    json_string = data.decode("utf-8")
    tiktok_data = json.loads(json_string)
    return tiktok_data

def get_data_search_videos(keywords):
    conn = http.client.HTTPSConnection("api.tikapi.io")
    payload = ''
    headers = {
    'X-API-KEY': '56ONwxSEmceiI9b27WsP8Ai3bfRPSlqD'
    }
    req_text = "/public/search/videos?query=" + keywords
    conn.request("GET", req_text, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
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
  try:
    maximum_value = int(views)*0.15
    minimum_value = int(views)*0.01
  except:
    maximum_value = 0
    minimum_value = 0

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
  payload = json.dumps(data, cls=NpEncoder)
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

def post_data_campaign(data):
  conn = http.client.HTTPSConnection("hooks.zapier.com")
  payload = json.dumps(data, cls=NpEncoder)
  headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
  conn.request("POST", "/hooks/catch/7655196/bfhgb15/", payload, headers)
  res = conn.getresponse()
  data = res.read()
  json_string = data.decode("utf-8")
  tiktok_data = json.loads(json_string)
  return tiktok_data

def post_data_create_campaign(data):
  conn = http.client.HTTPSConnection("hooks.zapier.com")
  payload = json.dumps(data, cls=NpEncoder)
  headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
  conn.request("POST", "/hooks/catch/7655196/bfjzjpn/", payload, headers)
  res = conn.getresponse()
  data = res.read()
  json_string = data.decode("utf-8")
  tiktok_data = json.loads(json_string)
  return tiktok_data