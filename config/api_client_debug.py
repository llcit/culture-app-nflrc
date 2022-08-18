# config/api_client.py
import requests


key = '396820f0-8a41-46b9-a488-3d4d9b838d17'
ip = '127.0.0.1'
token = 'srgxkitbvj4j2l5wb.tcxognqctbp1!u9c8z2uwck4jn#q!adtwpwhxfpnz'
user_id = 'rmedina@hawaii.edu'
last_record = '2021-07-08 02:49:00.879897+00:00'
module_url = 'http://localhost:8000/mod/L/'

endpoint = 'http://localhost:8000/api/get-activity/'
payload = {
	'ip': ip, 
	'key': key, 
	'token': token, 
	'user_id': user_id, 
	'last_rec': last_record,
}
r = requests.post(endpoint, data=payload)
print(r.text)

payload = {
	'ip': ip, 
	'key': key, 
	'token': token, 
	'module_url': module_url,
}

endpoint = 'http://localhost:8000/api/get-module-info/'
r = requests.post(endpoint, data=payload)
print(r.text)

# Sample Usage (Python/Requests)
"""
endpoint: /api/get-activity/
last_rec is determined by statement attribute: "https://languageflagshipdashboard.com/response_time" from the most recently stored statement

endpoint = 'http://localhost:8000/api/get-activity/'
payload {
  "ip": "127.0.0.1",
  "key": "396820f0-8a41-46b9-a488-3d4d9b838d17",
  "token": "ixni4#dsmna#492rgvopxsk4drc7e0#dgwl7ppq75vn!5lk2wwj751bt.ns",
  "user_id": "rmedina@hawaii.edu",
  "last_rec": "2022-08-08 02:49:00.879897+00:00" # (empty string retrieves all records)
}
response = requests.post(endpoint, data=payload)
print(response.text)

endpoint: /api/get-module-info/
last_rec is determined by statement attribute: "https://languageflagshipdashboard.com/response_time" from the most recently stored statement

endpoint = 'http://localhost:8000/api/get-module-info/'
module_url = 'http://localhost:8000/mod/L/'
payload = {
	'ip': ip, 
	'key': key, 
	'token': token, 
	'module_url': module_url,
}
response = requests.post(endpoint, data=payload)
print(response.text)

"""