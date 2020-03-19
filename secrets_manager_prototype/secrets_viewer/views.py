from django.http import HttpResponse
from django.template import loader
from secrets_manager.secrets_manager import SecretsManager

secrets_manager = SecretsManager()


def registred(request, env_name=None):
    if env_name is None:
        env_name = secrets_manager.deploy_env
    template = loader.get_template("secrets_viewer/registered.html")
    secrets = secrets_manager.get_secrets(env_name)
    base = secrets_manager.base_env_name
    secrets_object = secrets_manager.env_secrets[env_name]
    secrets_types = [
        "Object yet to be instantiated"
        if env not in secrets_manager.env_secrets
        else type(secrets_manager.env_secrets[env]).__name__
        for env in secrets_manager.env_configs
    ]
    context = {
        "secrets": secrets,
        "env_name": env_name,
        "display_env": secrets_manager.env_secrets[env_name],
        "base_env_name": base,
        "base_env": secrets_manager.env_secrets[base],
        "registered_env_details": zip(
            secrets_manager.env_configs.keys(),
            [config[2] for config in secrets_manager.env_configs.values()],
            secrets_types,
        ),
        "registered_page": "active",
        "loaded_env_names": secrets_manager.env_secrets.keys(),
        "display_details": True,
        "deployed_env_name": secrets_manager.deploy_env,
        "env_config": {
            "Source": secrets_object.src,
            "Payload": secrets_object.payload,
            "Headers": secrets_object.headers,
            "Auto Reload": secrets_object.auto_reload,
            "Authentication": secrets_object.Auth.__name__ if secrets_object.Auth is not None else None,
        },
        "env_secrets_type": type(secrets_object).__name__,
    }

    return HttpResponse(template.render(context, request))


def reload_registered(request, env_name):
    secrets_manager.env_secrets[env_name].reload()
    return registred(request, env_name)


def deployed(request):
    env_name = secrets_manager.deploy_env
    template = loader.get_template("secrets_viewer/deployed.html")
    secrets = secrets_manager.get_secrets(env_name)
    base = secrets_manager.base_env_name
    secrets_object = secrets_manager.env_secrets[env_name]
    context = {
        "secrets": secrets,
        "env_name": env_name,
        "display_env": secrets_manager.env_secrets[env_name],
        "base_env_name": base,
        "base_env": secrets_manager.env_secrets[base],
        "deployed_page": "active",
        "display_details": True,
        "env_config": {
            "Source": secrets_object.src,
            "Payload": secrets_object.payload,
            "Headers": secrets_object.headers,
            "Auto Reload": secrets_object.auto_reload,
            "Authentication": secrets_object.Auth.__name__ if secrets_object.Auth is not None else None,
        },
        "env_secrets_type": type(secrets_object).__name__,
    }

    return HttpResponse(template.render(context, request))


def reload_deployed(request):
    secrets_manager.env_secrets[secrets_manager.deploy_env].reload()
    return deployed(request)
