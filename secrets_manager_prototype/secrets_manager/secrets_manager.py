import os
from pathlib import Path

from django.core.validators import URLValidator
from secrets_manager.secrets import DotEnvSecrets, ModuleSecrets, HTTPSecrets


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SecretsManager(metaclass=Singleton):
    def __init__(self, default_env_name=None, lazy_loading=True, auto_register=False):
        self.env = {}
        self.env_configs = {}
        try:
            self.deploy_env = os.environ["env"]
        except KeyError:
            self.deploy_env = default_env_name

        root_path = str(Path(__file__).resolve(strict=True).parents[1])
        project_name = os.path.basename(root_path)
        self.env_dir = root_path + "/" + project_name + "/env/"
        self.is_base_set = False
        self.lazy_loading = lazy_loading
        self.env_secrets = {}
        self.base_env_name = None
        if auto_register:
            self.auto_register()

    def auto_register(self):
        file_names = list(os.walk(self.env_dir))[0][2]
        file_names = [
            file_name
            for file_name in file_names
            if file_name not in ["env.py", "__init__.py"]
        ]
        for file_name in file_names:
            env_name = "dot_env_" + file_name[1:]
            if file_name.endswith(".py"):
                env_name = "module_" + file_name[:-3]
            self.register(env_name, file_name)
            if "base" in env_name:
                self.set_base(env_name)

    def set_base(self, env_name):
        if env_name in self.env_configs:
            self.is_base_set = True
            self.base_env_name = env_name

    def register(
        self, env_name, src, auto_reload=False, payload=None, headers=None, Auth=None
    ):
        if self.deploy_env is None:
            self.deploy_env = env_name
        self.env_configs[env_name] = (
            env_name,
            src,
            auto_reload,
            payload,
            headers,
            Auth,
        )
        if not self.lazy_loading:
            self.load_secrets(env_name)

    def load_secrets(self, env_name):
        if env_name not in self.env_secrets:
            _, src, auto_reload, _, _, _ = self.env_configs[env_name]
            try:
                validate_url = URLValidator()
                validate_url(src)
            except:
                if src.endswith(".py"):
                    self.env_secrets[env_name] = ModuleSecrets(
                        env_name, self.env_dir + src, auto_reload
                    )
                else:
                    self.env_secrets[env_name] = DotEnvSecrets(
                        env_name, self.env_dir + src, auto_reload
                    )
            else:
                self.env_secrets[env_name] = HTTPSecrets(*self.env_configs[env_name])

        return self.env_secrets[env_name]

    def get_secrets(self, env_name=None):
        env_name = self.deploy_env if env_name is None else env_name
        env = self.load_secrets(env_name)
        if env.auto_reload:
            self.reload_secrets(env=env)
        secrets = env.secrets
        if self.is_base_set and env_name is not self.base_env_name:
            all_secrets = self.get_secrets(self.base_env_name)
            all_secrets.update(secrets)
            return all_secrets
        return secrets

    def reload_secrets(self, env_name=None, env=None):
        if env_name is not None and env_name in self.env_configs:
            env = self.load_secrets(env_name)
        if env is not None:
            env.reload()

    def unregister(self, env_name):
        if env_name in self.env_configs:
            env = self.env_secrets.pop(env_name, None)
            if env is not None:
                del env
            del self.env_configs[env_name]
        if env_name == self.base_env_name:
            self.base_env_name = None
            self.is_base_set = False
