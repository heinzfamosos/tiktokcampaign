import http.client
import json 

base_url = "/v1.1/instagram/profile/"
params = "/update?analyze_demography=1&load_feed_posts=1&max_posts=10&from_date=2022-05-01&load_comments=0&callback_url="
access_token = "ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6STFOaUo5LmV5SnpkV0lpT2lKR1lXMXZjMjl6SWl3aWFXRjBJam94TmpVeU9UYzBOREl5TGpFMk5ETTVOREY5LkZfM0wyMEdTSlhvRVVfdGZTaGZZVWZlM1BLWnp0aUVSSFk0RzB5Zm5fOW8="
params2 = "&access_token="

def create_update_task_ig(username):
    callback_url = "https://hooks.zapier.com/hooks/catch/7655196/bfm8axq/"
    conn = http.client.HTTPSConnection("api.data365.co")
    payload = ''
    request_str= base_url + username + params + callback_url+ params2 + access_token 
    headers = {}
    conn.request("POST", request_str, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    json_string = data.decode("utf-8")
    response_data = json.loads(json_string)
    return response_data

def get_profile_data_ig(username):
    request_str = base_url + username + "?access_token="+access_token
    conn = http.client.HTTPSConnection("api.data365.co")
    payload = ''
    headers = {}
    conn.request("GET", request_str, payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_string = data.decode("utf-8")
    response_data = json.loads(json_string)
    return response_data

def get_feed_posts_data_ig(username):
    request_str = base_url + username + "/feed/posts?from_date=2022-03-01&access_token="+access_token
    conn = http.client.HTTPSConnection("api.data365.co")
    payload = ''
    headers = {}
    conn.request("GET", request_str, payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_string = data.decode("utf-8")
    response_data = json.loads(json_string)
    return response_data




def get_task_update_profile_data_ig(username):
    request_str = base_url + username + "/update?access_token="+access_token
    conn = http.client.HTTPSConnection("api.data365.co")
    payload = ''
    headers = {}
    conn.request("GET", request_str, payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_string = data.decode("utf-8")
    response_data = json.loads(json_string)
    return response_data

def create_update_task_location(location_id):
    base_url_loc = "/v1.1/instagram/location/"
    params = "/update?&callback_url=https://hooks.zapier.com/hooks/catch/7655196/bfmfnj7/&access_token=ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6STFOaUo5LmV5SnpkV0lpT2lKR1lXMXZjMjl6SWl3aWFXRjBJam94TmpVeU9UYzBOREl5TGpFMk5ETTVOREY5LkZfM0wyMEdTSlhvRVVfdGZTaGZZVWZlM1BLWnp0aUVSSFk0RzB5Zm5fOW8="
    request_str = base_url_loc + location_id + params
    conn = http.client.HTTPSConnection("api.data365.co")
    payload = ''
    headers = {}
    conn.request("POST", request_str , payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    json_string = data.decode("utf-8")
    response_data = json.loads(json_string)
    return response_data

def get_task_update_location_data_ig(location):
    base_url_loc = "/v1.1/instagram/location/"
    request_str = base_url_loc + location + "/update?access_token="+access_token
    conn = http.client.HTTPSConnection("api.data365.co")
    payload = ''
    headers = {}
    conn.request("GET", request_str, payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_string = data.decode("utf-8")
    response_data = json.loads(json_string)
    return response_data

def get_location_data_ig(location):
    base_url_loc = "/v1.1/instagram/location/"
    request_str = base_url_loc + location + "?access_token="+access_token
    conn = http.client.HTTPSConnection("api.data365.co")
    payload = ''
    headers = {}
    conn.request("GET", request_str, payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_string = data.decode("utf-8")
    response_data = json.loads(json_string)
    return response_data