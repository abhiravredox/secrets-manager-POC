from django.http import HttpResponse
from django.template import loader

from secrets_manager.secrets_manager import SecretsManager

secrets_manager = SecretsManager()


def index(request):
    secrets = secrets_manager.get_secrets()
    env_name = secrets_manager.deploy_env
    base = secrets_manager.base
    template = loader.get_template('test_app/show_detail.html')
    context = {
        'secrets': secrets,
        'env_name': env_name,
        'heading': 'Deployed Environment Settings',
        'display_env': secrets_manager.env_secrets[env_name],
        'base': base,
        'base_env': secrets_manager.env_secrets[base],
        'deployed_page': 'active',
        'display_details': True
    }
    return HttpResponse(template.render(context, request))


def detail(request, env_name):
    secrets = secrets_manager.get_secrets(env_name)
    template = loader.get_template('test_app/show_detail.html')
    base = secrets_manager.base
    context = {
        'secrets': secrets,
        'env_name': env_name,
        'heading': 'Registered Environment Settings',
        'display_env': secrets_manager.env_secrets[env_name],
        'base': base,
        'base_env': secrets_manager.env_secrets[base],
        'registered_page': 'active'
    }
    return HttpResponse(template.render(context, request))


# def loaded(request):
#     secrets = secrets_manager.get_secrets(env_name)
#     template = loader.get_template('test_app/detail.html')
#     base = secrets_manager.base
#     context = {
#         'secrets': secrets,
#         'env_name': env_name,
#         'heading': 'Registered Environment Settings',
#         'display_env': secrets_manager.env_secrets[env_name],
#         'secrets_manager': secrets_manager,
#         'base': base,
#         'base_env': secrets_manager.env_secrets[base]
#     }
#     return HttpResponse(template.render(context, request))

def registred(request, env_name=None, action=None):
    print(action)
    template = loader.get_template('test_app/registered.html')
    if env_name is None:
        context = {
            'registered_env_details': zip(secrets_manager.env_configs.keys(), [config[1] for config in secrets_manager.env_configs.values()]),
            'registered_page': 'active',
            'loaded_env_names': secrets_manager.env_secrets.keys(),
            'auto_reload': [config[1] for config in secrets_manager.env_configs.values()],
            'display_details': False
        }
    else:
        secrets = secrets_manager.get_secrets(env_name)
        if action == 'reload':
            secrets_manager.env_secrets[env_name].reload()
        base = secrets_manager.base
        context = {
            'secrets': secrets,
            'env_name': env_name,
            'heading': 'Registered Environment Settings',
            'display_env': secrets_manager.env_secrets[env_name],
            'base': base,
            'base_env': secrets_manager.env_secrets[base],
            'registered_env_details': zip(secrets_manager.env_configs.keys(), [config[1] for config in secrets_manager.env_configs.values()]),
            'registered_page': 'active',
            'loaded_env_names': secrets_manager.env_secrets.keys(),
            'display_details': True
        }

    return HttpResponse(template.render(context, request))


def loaded(request, env_name=None):
    template = loader.get_template('test_app/loaded.html')
    if env_name is None:
        context = {
            'loaded_env_names': secrets_manager.env_secrets.keys(),
            'loaded_page': 'active',
            'loaded_envs': secrets_manager.env_secrets
        }
    else:
        secrets = secrets_manager.get_secrets(env_name)
        base = secrets_manager.base
        context = {
            'secrets': secrets,
            'env_name': env_name,
            'heading': 'Registered Environment Settings',
            'display_env': secrets_manager.env_secrets[env_name],
            'base': base,
            'base_env': secrets_manager.env_secrets[base],
            'loaded_page': 'active',
            'loaded_env_names': secrets_manager.env_secrets.keys(),
            'loaded_envs': secrets_manager.env_secrets
        }

    return HttpResponse(template.render(context, request))
