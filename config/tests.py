from django.test import TestCase
# from unittest import TestCase
import json
import requests


class APITestCase(TestCase):
    def setUp(self):
        self.key = '396820f0-8a41-46b9-a488-3d4d9b838d17'
        self.ip = '127.0.0.1'
        self.token = 'wfikfrlaf!vc4rdxf54r43yf3rt0ceaf3lb6g7wfqvvobpe4pvzyn##7z2h'

    def test_authentication(self):
        user_id = 'rmedina@hawaii.edu'
        last_record = '2021-07-08 02:49:00.879897+00:00'
        endpoint = 'http://localhost:8000/api/get-activity/'
        payload = {
            'ip': self.ip, 
            'key': self.key, 
            'token': self.token, 
            'user_id': user_id, 
            'last_rec': last_record,
        }
        r = requests.post(endpoint, data=payload)
        data = json.loads(r.text[16:])
        self.assertIn(data['message'], ['OK', 'RENEWED'])

    def test_sync_judgment_task_activity(self):
        """ """
        user_id = 'rmedina@hawaii.edu'
        last_record = '2022-07-08 02:49:00.879897+00:00'
        endpoint = 'http://localhost:8000/api/get-activity/'
        payload = {
            'ip': self.ip, 
            'key': self.key, 
            'token': self.token, 
            'user_id': user_id, 
            'last_rec': last_record,
        }
        r = requests.post(endpoint, data=payload)
        data = json.loads(r.text[16:])
        resp = data['RESULT_LOG']
        self.assertEqual(resp['RESULT_DATA'], 2)

    def test_sync_judgment_task_activity_null_date(self):
        """ """
        user_id = 'rmedina@hawaii.edu'
        last_record = ''
        endpoint = 'http://localhost:8000/api/get-activity/'
        payload = {
            'ip': self.ip, 
            'key': self.key, 
            'token': self.token, 
            'user_id': user_id, 
            'last_rec': last_record,
        }
        r = requests.post(endpoint, data=payload)
        data = json.loads(r.text[16:])
        resp = data['RESULT_LOG']
        self.assertEqual(resp['RESULT_DATA'], 6)

    def test_sync_judgment_task_activity_non_user(self):
        """ """
        user_id = 'fakeuser7@hawaii.edu'
        last_record = '2021-07-08 02:49:00.879897+00:00'
        endpoint = 'http://localhost:8000/api/get-activity/'
        payload = {
            'ip': self.ip, 
            'key': self.key, 
            'token': self.token, 
            'user_id': user_id, 
            'last_rec': last_record,
        }
        r = requests.post(endpoint, data=payload)
        data = json.loads(r.text[16:])
        self.assertEqual(data['ERROR_LOG'], 'User not found.')

    def test_get_module_info(self):
        """ """
        module_url = 'http://localhost:8000/mod/L/'
        endpoint = 'http://localhost:8000/api/get-module-info/'
        payload = {
            'ip': self.ip, 
            'key': self.key, 
            'token': self.token, 
            'module_url': module_url,
        }
        r = requests.post(endpoint, data=payload)
        data = json.loads(r.text[16:])
        resp = data['RESULT_LOG']
        self.assertEqual(resp['RECORD_DATA']['Culture App Language'], 'All')
