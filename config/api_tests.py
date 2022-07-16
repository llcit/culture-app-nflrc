# config/api_tests.py
from datetime import datetime
import requests

ep = 'http://localhost:8000/api/get-activity/'
#ep = 'http://localhost:8000/api/get-modules/'
key = '396820f0-8a41-46b9-a488-3d4d9b838d17'
ip = '127.0.0.1'
token = 'mntoyi6vx5p4y12fa!8tkh02d!qp503kbr85!vr#6nogkyzzvcid1.y4sbz'
user_id = 'rmedina@hawaii.edu'
last_record = '2022-07-07 02:49:00.879897+00:00'
payload = {'ip': ip, 'key': key, 'token': token, 'user_id': user_id, 'last_rec': last_record}

r = requests.post(ep, data=payload)
print(r.text)
