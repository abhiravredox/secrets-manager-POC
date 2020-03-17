import abc
import importlib

import requests
from dotenv import dotenv_values


class SingletonByArgument(type, metaclass=abc.ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if (args, tuple(kwargs.keys()), tuple(kwargs.values())) not in cls._instances:
            cls._instances[(args, tuple(kwargs.keys()), tuple(kwargs.values()))] = super(SingletonByArgument,
                                                                                         cls).__call__(*args, **kwargs)
        return cls._instances[(args, tuple(kwargs.keys()), tuple(kwargs.values()))]


class SecretAbstract(metaclass=SingletonByArgument):

    def __init__(self, src=None, auto_reload=False, payload=None, headers=None):
        self.secrets = None
        self.src = src
        self.auto_reload = auto_reload
        self.payload = payload
        self.headers = headers
        self.reload()

    def reload(self):
        self.secrets = self.read_secrets()

    @abc.abstractmethod
    def read_secrets(self):
        """implement in subclass"""


class DotEnvSecret(SecretAbstract):

    def read_secrets(self):
        env = dotenv_values(self.src)
        return env


class ModuleSecret(SecretAbstract):

    def read_secrets(self):
        print(self.src)
        spec = importlib.util.spec_from_file_location(self.src.split('/')[-1][:-3], self.src)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        env = {key: vars(mod)[key] for key in vars(mod).keys() if not key.startswith("__")}
        return env


class URLSecret(SecretAbstract):

    def read_secrets(self):
        if self.payload is None:
            r = requests.get(self.src)
        else:
            r = requests.post(self.src, data=self.payload, headers=self.headers)
        env = r.json()
        return env
