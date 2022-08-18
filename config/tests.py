from django.test import TestCase
# from unittest import TestCase
import json
import requests
from culture.settings import DASHBOARD_CULTUREAPP_ENDPOINT, DASHBOARD_LRS_ENDPOINT, DASHBOARD_TOKEN


class APITestCase(TestCase):
    def setUp(self):
        self.key = 'f1daa5be-42e9-4dae-8f39-6d22764cfb80'
        self.ip = '127.0.0.1'
        self.token = 'jbxwzih#!otw7kourqdohu2ccg1kimq25r72f#umopxy4g.9kvzfov60l5t'

    def test_authentication_denied(self):
        """Verify authentication token is inited or renewed (uses get-module-info call)
            Sends an invalid key with empty token.
        """
        module_url = DASHBOARD_CULTUREAPP_ENDPOINT+'/mod/L/'
        endpoint = DASHBOARD_CULTUREAPP_ENDPOINT+'/api/get-module-info/'
        payload = {
            'ip': self.ip, 
            'key': 'f1daa5be-42e9-4dae-8f39-6d22764cfb89', 
            'token': '', 
            'module_url': module_url,
        }
        r = requests.post(endpoint, data=payload)
        data = json.loads(r.text[16:])
        self.assertIn(data['message'], ['KO'])

    def test_authentication_renewed(self):
        """Verify authentication token renewed (uses get-module-info call)"""
        module_url = DASHBOARD_CULTUREAPP_ENDPOINT+'/mod/L/'
        endpoint = DASHBOARD_CULTUREAPP_ENDPOINT+'/api/get-module-info/'
        payload = {
            'ip': self.ip, 
            'key': self.key, 
            'token': self.token, 
            'module_url': module_url,
        }
        r = requests.post(endpoint, data=payload)
        data = json.loads(r.text[16:])
        self.assertIn(data['message'], ['OK', 'RENEWED'])

    def test_sync_judgment_task_activity(self):
        """Verify LRS record push 
            should return records only after login date.
        """
        user_id = 'rmedina@hawaii.edu'
        last_record = '2022-07-08 02:49:00.879897+00:00'
        endpoint = DASHBOARD_CULTUREAPP_ENDPOINT+'/api/get-activity/'
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
        """Verify LRS record push with null login date 
         should return all records for user.
        """
        user_id = 'rmedina@hawaii.edu'
        last_record = ''
        endpoint = DASHBOARD_CULTUREAPP_ENDPOINT+'/api/get-activity/'
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
        """ Verify detection of non registered user id in Culture App"""
        user_id = 'exampleuser@example.edu'
        last_record = '2021-07-08 02:49:00.879897+00:00'
        endpoint = DASHBOARD_CULTUREAPP_ENDPOINT+'/api/get-activity/'
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
        """ Verify detection of module information for a given module url"""
        module_url = DASHBOARD_CULTUREAPP_ENDPOINT+'/mod/L/'
        endpoint = DASHBOARD_CULTUREAPP_ENDPOINT+'/api/get-module-info/'
        payload = {
            'ip': self.ip, 
            'key': self.key, 
            'token': self.token, 
            'module_url': module_url,
        }
        r = requests.post(endpoint, data=payload)
        data = json.loads(r.text[16:])
        resp = data['RESULT_LOG']
        self.assertEqual(resp['RESULT_DATA']['Culture App Language'], 'All')
