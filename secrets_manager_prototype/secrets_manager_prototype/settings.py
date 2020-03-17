"""
Django settings for secrets_manager_test_app project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import json
from pathlib import Path

from secrets_manager.secrets_manager import SecretsManager

BASE_DIR = Path(__file__).resolve(strict=True).parents[1]
ENV_DIR = Path(__file__).resolve(strict=True).parents[0]
secrets_manager = SecretsManager(ENV_DIR, "dev_api_post")
secrets_manager.register("base", 'base.py')
secrets_manager.set_base("base")
secrets_manager.register("dev_env", '.DEV')
secrets_manager.register("prod_env", '.PROD')
secrets_manager.register("test_env", '.TEST')
secrets_manager.register("dev_mod", 'DEV.py')
secrets_manager.register("prod_mod", 'PROD.py')
secrets_manager.register("test_mod", 'TEST.py')
secrets_manager.register("dev_api_get", 'http://127.0.0.1:8000/secrets/DEV/', auto_reload=True)
secrets_manager.register("prod_api_get", 'http://127.0.0.1:8000/secrets/PROD/', auto_reload=True)
secrets_manager.register("test_api_get", 'http://127.0.0.1:8000/secrets/TEST/', auto_reload=True)
secrets_manager.register("dev_api_post", 'http://127.0.0.1:8000/secrets/', payload='{"env_name":"DEV"}',
                         auto_reload=True)
secrets_manager.register("prod_api_post", 'http://127.0.0.1:8000/secrets/', payload='{"env_name":"PROD"}',
                         auto_reload=True)
secrets_manager.register("test_api_post", 'http://127.0.0.1:8000/secrets/', payload='{"env_name":"TEST"}',
                         auto_reload=True)
SECRETS = secrets_manager.get_secrets()
SECRET_KEY = SECRETS['SECRET_KEY']
print(SECRET_KEY)

for i in range(5):
    SECRETS = secrets_manager.get_secrets("prod_api_post")
    SECRET_KEY = SECRETS['SECRET_KEY']
    print(SECRET_KEY)
    API_KEY = SECRETS['API_KEY']
    print(API_KEY)

DEBUG = SECRETS['DEBUG']
print(DEBUG)

DATABASES = {
    'default': {
        'ENGINE': SECRETS['DB_DEFAULT_ENGINE'],
        'NAME': BASE_DIR / SECRETS['DB_DEFAULT_NAME'],
    }
}
