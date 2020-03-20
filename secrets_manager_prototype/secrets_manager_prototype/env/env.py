from requests.auth import HTTPDigestAuth
from requests_oauthlib import OAuth1, OAuth2

from secrets_manager.secrets_manager import SecretsManager

secrets_manager = SecretsManager(
    default_env_name="http_get_with_auth_dev", auto_register=True
)

# Not required as auto_register=True
# To manually register .env and modules as secret sources
# secrets_manager.register("module_base", "base.py")
# secrets_manager.set_base("module_base")
# secrets_manager.register("dot_env_dev", ".DEV")
# secrets_manager.register("dot_env_prod", ".PROD")
# secrets_manager.register("dot_env_test", ".TEST")
# secrets_manager.register("module_dev", "DEV.py")
# secrets_manager.register("module_prod", "PROD.py")
# secrets_manager.register("module_test", "TEST.py")

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
    "http_post_dev",
    "http://127.0.0.1:8080/secrets/",
    payload='{"env_name":"DEV"}',
    auto_reload=True,
)
secrets_manager.register(
    "http_post_prod",
    "http://127.0.0.1:8080/secrets/",
    payload='{"env_name":"PROD"}',
    auto_reload=True,
)
secrets_manager.register(
    "http_post_test",
    "http://127.0.0.1:8080/secrets/",
    payload='{"env_name":"TEST"}',
    auto_reload=False,
)

secrets_manager.register(
    "http_get_with_auth_dev",
    "http://127.0.0.1:8080/secrets/auth/DEV",
    auto_reload=True,
    Auth=HTTPDigestAuth,
)
secrets_manager.register(
    "http_get_with_auth_prod",
    "http://127.0.0.1:8080/secrets/auth/PROD",
    auto_reload=True,
    Auth=OAuth1,
)
secrets_manager.register(
    "http_get_with_auth_test",
    "http://127.0.0.1:8080/secrets/auth/TEST",
    auto_reload=False,
    Auth=OAuth2,
)
