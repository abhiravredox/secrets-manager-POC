from pathlib import Path

from requests.auth import HTTPDigestAuth
from requests_oauthlib import OAuth1, OAuth2

from secrets_manager.secrets_manager import SecretsManager

ENV_DIR = Path(__file__).resolve(strict=True).parents[0]
secrets_manager = SecretsManager(ENV_DIR, default_env="http_get_test")
secrets_manager.register("base", "base.py")
secrets_manager.set_base("base")
secrets_manager.register("dot_env_dev", ".DEV")
secrets_manager.register("dot_env_prod", ".PROD")
secrets_manager.register("dot_env_test", ".TEST")
secrets_manager.register("module_dev", "DEV.py")
secrets_manager.register("module_prod", "PROD.py")
secrets_manager.register("module_test", "TEST.py")
secrets_manager.register(
    "http_get_dev", "http://127.0.0.1:8080/secrets/DEV/", auto_reload=True
)
secrets_manager.register(
    "http_get_prod", "http://127.0.0.1:8080/secrets/PROD/", auto_reload=True
)
secrets_manager.register(
    "http_get_test", "http://127.0.0.1:8080/secrets/TEST/", auto_reload=False
)
secrets_manager.register(
    "http_prod_dev",
    "http://127.0.0.1:8080/secrets/",
    payload='{"env_name":"DEV"}',
    auto_reload=True,
)
secrets_manager.register(
    "http_prod_prod",
    "http://127.0.0.1:8080/secrets/",
    payload='{"env_name":"PROD"}',
    auto_reload=True,
)
secrets_manager.register(
    "http_prod_test",
    "http://127.0.0.1:8080/secrets/",
    payload='{"env_name":"TEST"}',
    auto_reload=False,
)
