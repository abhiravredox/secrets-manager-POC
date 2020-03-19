from pathlib import Path
from requests.auth import HTTPDigestAuth
from requests_oauthlib import OAuth1, OAuth2
from secrets_manager.secrets_manager import SecretsManager

ENV_DIR = Path(__file__).resolve(strict=True).parents[0]
secrets_manager = SecretsManager(ENV_DIR, default_env='dev_api_get')
secrets_manager.register("base", 'base.py')
secrets_manager.set_base("base")
secrets_manager.register("dev_env", '.DEV')
secrets_manager.unregister("dev_env")
secrets_manager.register("dev_env", '.DEV')
secrets_manager.register("prod_env", '.PROD')
secrets_manager.register("test_env", '.TEST')
secrets_manager.register("dev_mod", 'DEV.py')
secrets_manager.register("prod_mod", 'PROD.py')
secrets_manager.register("test_mod", 'TEST.py')
secrets_manager.register("dev_api_get", 'http://127.0.0.1:8000/secrets/DEV/', auto_reload=True)
secrets_manager.register("prod_api_get", 'http://127.0.0.1:8000/secrets/PROD/', auto_reload=True)
secrets_manager.register("test_api_get", 'http://127.0.0.1:8000/secrets/TEST/', auto_reload=False)
secrets_manager.register("dev_api_post", 'http://127.0.0.1:8000/secrets/', payload='{"env_name":"DEV"}',
                         auto_reload=True)
secrets_manager.register("prod_api_post", 'http://127.0.0.1:8000/secrets/', payload='{"env_name":"PROD"}',
                         auto_reload=True)
secrets_manager.register("test_api_post", 'http://127.0.0.1:8000/secrets/', payload='{"env_name":"TEST"}',
                         auto_reload=False)