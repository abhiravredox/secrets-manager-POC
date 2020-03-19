import json
from django.http import HttpResponse
from django.core import serializers
from secrets_api.models import Secret
import random
import string
from django.views.decorators.csrf import csrf_exempt

def get_secrets(request, env_name):
    return env_settings(env_name)

@csrf_exempt
def post_secrets(request):
    env_name = json.loads(request.body)["env_name"]
    return env_settings(env_name)

def genrate_random_key(len):
    return ''.join(random.choice(string.hexdigits + string.punctuation) for _ in range(len))

def env_settings(env_name):
    secrets = Secret.objects.get(pk=env_name)
    data = serializers.serialize('json', [secrets])
    json_data = json.loads(data[1:-1])['fields']
    json_data['API_KEY'] = genrate_random_key(40) + "/" + env_name + "_API"
    json_data = json.dumps(json_data)
    return HttpResponse(json_data, content_type='application/json')