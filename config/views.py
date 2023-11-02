import datetime
import hashlib
import random
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from culture_content.models import Response, Scenario, Module, Topic

from .xapi_messenger import DashboardSyncTaskActivity

from .models import Config, TokenApi

@csrf_exempt
def verify_device(config):
	if Config.objects.filter(ipaddress=config['ip'], key=config['key']).exists():
		obj = Config.objects.get(ipaddress=config['ip'], key=config['key'])
		s = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz!.#') for i in range(59))
		try:
			hash = hashlib.sha256(s.encode('utf-8'))
			TokenApi.objects.create(device=obj, token=hash.hexdigest(), valid_until=datetime.datetime.now(tz=datetime.timezone.utc)+datetime.timedelta(days=2))
			return {'message': 'OK', 'token': s}
		except Exception as e:
			print(e)
			return {'message': 'KO'}
	else:
		return {'message': 'KO'}

@csrf_exempt
def token_is_valid(token):
	hash = hashlib.sha256(token.encode('utf-8'))
	try:
		tk = TokenApi.objects.get(token=hash.hexdigest())
		if tk.valid_until > datetime.datetime.now(tz=datetime.timezone.utc):
			return True
		else:
			return False
	except Exception as e:
		return False

@csrf_exempt
def authenticate_request(params):
	token = params.get('token', '')
	if not token_is_valid(token):
		valid_device = verify_device(params)
		if 'token' in valid_device:
			valid_device['message'] = 'RENEWED'
		return valid_device 
	return {'message': 'OK', 'token': token}


@csrf_exempt
def get_module_info(request):
	auth = authenticate_request(request.POST)
	auth['ERROR_LOG'] = ''
	if 'token' in auth:	
		try:
			module_code = request.POST['module_url'].strip('/').split('/')[-1]
			module_objs = Module.objects.filter(language=module_code)
			module_lang = module_objs[0].get_language_display()
			module_topics = [i.topics.all() for i in module_objs]
			topic_count = 0
			scenario_count = 0
			for i in module_topics:
				topics = [j for j in i]
				topic_count = topic_count + len(topics)
				for k in topics:
					scenario_count = scenario_count + k.scenarios.all().count()
			data = {''}
			auth['RESULT_LOG'] = { \
					'RESULT_MESSAGE': '', 
					'RESULT_DATA': {
						'Culture App Language': module_lang, 
						'Modules': module_objs.count(), 
						'Topics': topic_count, 
						'Scenarios': scenario_count}
				}
		except:
			auth['ERROR_LOG'] = 'Error retrieving Module information.'
		
		return HttpResponse('AUTHENTICATION: ' + json.dumps(auth))
	else:
		return HttpResponse('AUTHENTICATION: ' + json.dumps(auth))


@csrf_exempt
def get_user_activity(request):
	auth = authenticate_request(request.POST)
	auth['ERROR_LOG'] = ''
	try:
		if 'token' in auth:
			user_obj = User.objects.filter(email=request.POST['user_id'])
			if user_obj:
				# Get activity data for user/push to LRS
				task = DashboardSyncTaskActivity((user_obj[0], request.POST['last_rec']))
				auth['RESULT_LOG'] = task.response
			else:
				auth['ERROR_LOG'] = 'User not found.'
			
			return HttpResponse('AUTHENTICATION: ' + json.dumps(auth))
		else:
			return HttpResponse('AUTHENTICATION: ' + json.dumps({'message': 'FAILED'}))
	except Exception as e:
		auth['ERROR_LOG'] = 'Bad request. ' + str(e)
		return HttpResponse('AUTHENTICATION: ' + json.dumps(auth))			

