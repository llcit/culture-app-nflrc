import datetime
import json
import os
import requests
import uuid
from typing import Dict

from django.urls import reverse
from culture_content.models import Response, Scenario, Module, Topic

from culture.settings import DASHBOARD_CULTUREAPP_ENDPOINT, DASHBOARD_LRS_ENDPOINT, DASHBOARD_TOKEN


class DashboardActor:
    def __init__(self, name, mbox, object_type):
        self.name = name
        self.mbox = mbox
        self.object_type = object_type

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'mbox': 'mailto:' + self.mbox,
            'objectType': self.object_type
        }


class DashboardData:
    def __init__(self, actor, result, verb, object):
        self.actor = actor
        self.result = result
        self.verb = verb
        self.object = object

    def to_dict(self) -> Dict:
        return {
            'id': str(uuid.uuid4()),
            'actor': self.actor,
            'result': self.result,
            'verb': self.verb,
            'object': self.object,
        }


class DashboardObject:
    def __init__(self, activity_type_id='', activity_name='', url='', mod='', topic=''):
        self.activity_type_id = activity_type_id
        self.activity_name = activity_name
        self.url = url
        self.related_module = mod
        self.related_module_topic = topic

    def set_object_url(self, url):
        self.url = url

    def to_dict(self) -> Dict:
        return {
            "id": self.url,
            "definition": {
                "type": self.activity_type_id,
                "name": {
                    "en-US": self.activity_name
                },
                "extensions": {
                    "https://languageflagshipdashboard.com/culture_module_language": self.related_module,
                    "https://languageflagshipdashboard.com/culture_module_topic": self.related_module_topic,
                }
            },
            "objectType": 'Activity'
        }

class DashboardResultJudgementTask:
    def __init__(self, score, state, success, timestamp):
        self.score = score
        self.state = state
        self.success = success
        self.timestamp = str(timestamp)
        self.response = str(self.score['raw']) + ' not in range.'
        if self.success:
            self.response = str(self.score['raw']) + ' in range.'

    def to_dict(self) -> Dict:
        return {
            'response': self.response,
            'completion': self.state,
            'success': self.success,
            "extensions": {
                "https://languageflagshipdashboard.com/response_time": self.timestamp,
            }
        }

class DashboardVerb:
    def __init__(self, verb_type_id='', verb_name=''):
        self.verb_type_id = verb_type_id
        self.verb_name = verb_name

    def to_dict(self) -> Dict:
        return {
            "id": self.verb_type_id,
            "display": {
                "en-US": self.verb_name
            }
        }

class DashboardSyncTaskActivity:
    def __init__(self, request_data):
        self.response = {'RESULT_MESSAGE': '', 'RESULT_DATA': ''}
        responses = Response.objects.filter(user__pk=request_data[0].pk)
        if request_data[1]: # last record timestamp provided
            last_rec = datetime.datetime.fromisoformat(request_data[1])
            responses = responses.filter(responded__gt=last_rec)
        responses = responses.order_by('-responded')
        if not responses:
            self.response['RESULT_MESSAGE'] = 'User does not have any stored data on Culture App.'
        else:    
            for i in responses:
                score_data = {
                    'raw': float(i.response), 
                    'min': float(i.answer.rating_from), 
                    'max': float(i.answer.rating_to),
                }

                response_in_range = i.response>=i.answer.rating_from and i.response<=i.answer.rating_to
                try: 
                    scenario = Scenario.objects.filter(judgment_task__pk=i.answer.task.pk)[0]
                    scenario_url = reverse('scenario', args=[scenario.pk])

                    topic = Topic.objects.filter(scenarios=scenario)[0]
                    topic_url = reverse('topic-scenarios', args=[topic.pk])
                    module = Module.objects.filter(topics=topic)[0]
                    module_url = reverse('modules', args=[module.language])

                    result = DashboardResultJudgementTask(score_data, True, response_in_range, i.responded).to_dict()
                    verb = DashboardVerb(verb_type_id='http://adlnet.gov/expapi/verbs/completed', verb_name='Completed a Judgement Task').to_dict()
                    actor = DashboardActor('', request_data[0].email, 'Agent').to_dict()
                    xobj = DashboardObject(activity_type_id='http://adlnet.gov/expapi/activities/Activity', activity_name='Culture App Scenario', url=DASHBOARD_CULTUREAPP_ENDPOINT+scenario_url, mod=DASHBOARD_CULTUREAPP_ENDPOINT+module_url, topic=DASHBOARD_CULTUREAPP_ENDPOINT+topic_url ).to_dict()
                except:
                    pass
                

                try:
                    dashboard_data = DashboardData(actor, result, verb, xobj).to_dict()
                    endpoint = DASHBOARD_LRS_ENDPOINT+'/statements?statementId='+dashboard_data['id']
                    
                    headers = {
                        'X-Experience-API-Version' : '1.0.3',
                        'Content-Type' : 'application/json',
                        'Authorization' : DASHBOARD_TOKEN
                    }
                    print(endpoint+'\n', json.dumps(headers, indent=2), json.dumps(dashboard_data, indent=2))
                    # req = requests.put(endpoint, headers=headers, data=json.dumps(dashboard_data), timeout=2)    
                    # self.response['RESULT'] = req.text
                    
                except Exception as e:
                    print(e)
            
            self.response['RESULT_DATA'] = len(responses)



# django.core.exceptions.ImproperlyConfigured: AUTH_USER_MODEL refers to model 'user.ReaderUser' that has not been installed