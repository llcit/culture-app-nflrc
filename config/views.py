from django.contrib.auth.decorators import login_required
from .models import Config, TokenApi
import hashlib
import random
import datetime


def verify_device(config):
	if Config.objects.filter(ipaddress=config['ip'], key=config['key']).exists():
		obj = Config.objects.get(ipaddress=config['ip'], key=config['key'])
		s = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz!.#') for i in range(59))
		try:
			hash = hashlib.sha256(s.encode('utf-8'))
			TokenApi.objects.create(device=obj, token=hash, valid_until=datetime.datetime.now()+datetime.timedelta(days=2))
			return {'message': 'OK', 'token': s}
		except:
			return {'message': 'KO'}
	else:
		return {'message': 'KO'}


def token_is_valid(token):
	hash = hashlib.sha256(token.encode('utf-8'))
	try:
		tk = TokenApi.objects.get(token= hash)
		if tk.valid_until > datetime.datetime.now():
			return True
		else:
			return False
	except:
		return False



