import abc
import importlib
import inspect

import requests
from dotenv import dotenv_values


class SingletonByArgument(type, metaclass=abc.ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if (args, tuple(kwargs.keys()), tuple(kwargs.values())) not in cls._instances:
            cls._instances[
                (args, tuple(kwargs.keys()), tuple(kwargs.values()))
            ] = super(SingletonByArgument, cls).__call__(*args, **kwargs)
        return cls._instances[(args, tuple(kwargs.keys()), tuple(kwargs.values()))]


class SecretsAbstract(metaclass=SingletonByArgument):
    def __init__(
        self,
        env_name=None,
        src=None,
        auto_reload=False,
        payload=None,
        headers=None,
        Auth=None,
    ):
        self.env_name = env_name
        self.src = src
        self.auto_reload = auto_reload
        self.payload = payload
        self.headers = headers
        self.Auth = Auth
        self.secrets = None
        self.auth_parameters = None
        self.reload()

    def reload(self):
        self.secrets = self.read_secrets()

    @abc.abstractmethod
    def read_secrets(self):
        """implement in subclass"""


class DotEnvSecrets(SecretsAbstract):
    def read_secrets(self):
        secrets = dotenv_values(self.src)
        return secrets


class ModuleSecrets(SecretsAbstract):
    def read_secrets(self):
        spec = importlib.util.spec_from_file_location(
            self.src.split("/")[-1][:-3], self.src
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        secrets = {
            key: vars(mod)[key] for key in vars(mod).keys() if not key.startswith("__")
        }
        return secrets


class HTTPSecrets(SecretsAbstract):
    def auth_parameters_CLI(self):
        parameters = list(inspect.signature(self.Auth.__init__).parameters)
        parameters.remove("self")
        print(
            self.Auth.__name__
            + " Authentication defined for environment '"
            + self.env_name
            + "'.\n"
            + "Secrets Source Endpoint: "
            + self.src
        )
        kwargs = {}
        for parameter in parameters:
            value = input("Enter " + parameter + ":")
            kwargs[parameter] = value
        return kwargs

    def read_secrets(self):
        if self.auth_parameters is None and self.Auth is not None:
            self.auth_parameters = self.auth_parameters_CLI()
            print()
        if self.payload is None:
            response = requests.get(
                self.src,
                auth=self.Auth(**self.auth_parameters)
                if self.auth_parameters is not None
                else None,
            )
        else:
            response = requests.post(
                self.src,
                data=self.payload,
                headers=self.headers,
                auth=self.Auth(**self.auth_parameters)
                if self.auth_parameters is not None
                else None,
            )
        secrets = response.json()
        return secrets
