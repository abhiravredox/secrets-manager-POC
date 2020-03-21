# Secrets Manager - Django GSoC
A gist about the crux of this prototype is available <a href='https://gist.github.com/abhiravredox/cfb9fd5e8f9af6a1274a2cb68d7de05a'>here</a> as the Django community may not have the
time to look at all the code. The part explaing important files is available in this README as well.

## About this POC
This is a prototype for my own sanity check that my approach works. Consequently, things like exception handling and some edge
cases have been overlooked.
The POC consists of 2 projects:
  1. secrets_manager_prototype
  2. http_secrets_server (a project to act as a secrets store for testing HTTPSecrets)
  
The <a href='https://github.com/abhiravredox/secrets-manager-POC/tree/master/secrets_manager_prototype/secrets_manager'> secrets_manager package</a> is the real deal here. <a href='https://github.com/abhiravredox/secrets-manager-POC/blob/master/secrets_manager_prototype/secrets_manager_prototype/env/env.py'>env.py</a> and <a href='https://github.com/abhiravredox/secrets-manager-POC/blob/master/secrets_manager_prototype/secrets_manager_prototype/settings.py'>settings.py</a> also play a vital role. Rest of the code serves demonstration purpose.

## Deploying the POC
1. Use requirements.txt to install dependencies in both projects
2. Run http_secrets_server on port 8080 using `python manage.py runserver 8080` (Port 8080 is required as the end points registered with the SecretsManager are pointing to localhost:8080. You may change that if you want in env.py.
3. Run secrets_manager_prototype using `python manage.py runserver`
4. Visit http://127.0.0.1:8000/ and play

<b>Note: I've commented the sources that require authentication so that the <a href='https://github.com/abhiravredox/secrets-manager-POC/tree/master/secrets_manager_prototype/secrets_viewer'>secrets_viewer</a> app can work smoothly. However, the viewer is only for demonstration purposes. You can uncomment authentication based sources in env.py. Depending on the lazy_load parameter, you will required to input parameters required by the authentication. This might even happen while using secrets_viewer when loading an authenticated source for the first time. You can enter garbage values there as the http_secrets_server doesn't really authenticate. However, the authentication objects are actually sent with the request. </b>

## Using different registered environments
With the current code, the registered environments have names: module_base, dot_env_dev, dot_env_prod, dot_env_test, module_dev, module_prod, module_test, http_get_dev, http_get_prod, http_get_test, http_post_dev, http_post_prod, http_post_test. You can also view them in the aforementioned secrets_viewer.
<br>There are 2 ways to deploy the app with registered environments (otherwise default environment, as defined in env.py, is used):
1. Pass --env to manage.py like this: `python manage.py runserver --env=http_get_test`
2. Pass env_name to get_secrets() in settings.py. <br>If you do this, the server will always run with env_name secrets (even if you pass --env to manage.py)
   
## <a href='https://github.com/abhiravredox/secrets-manager-POC/tree/master/secrets_manager_prototype/secrets_viewer'>secrets_viewer</a>
* This app is only for demonstration purposes and tries to demonstrate what functionalities can be exploited by the developer.
* The app will allow you to view the registered environment secrets sources and their secrets. 
* The table on the left lists the registrations.
* On the right, the secrets of the selected environment will be displayed. 
  * Everytime you click on a row, the get_secrets(env_name) is called. If auto_reload=True, the secrets will reload    
    automatically.
  * You can also force a reload, even if auto_reload is false.
* You can view the secrets that were used to deploy the app using the navbar on top. Again, as get_secrets() is called,   
  auto_reload may entail
  
  
## Design
![class](https://user-images.githubusercontent.com/8560430/77208339-80e04500-6af3-11ea-87ba-75ce8bb2f2d8.png)

## Important Files

### <a href='https://github.com/abhiravredox/secrets-manager-POC/tree/master/secrets_manager_prototype/secrets_manager_prototype/env'>env.py</a>
env.py resides in the env/ folder in the Django root, the directory where settings.py resides in a new project.
<br>This is the entry point for a developer to register secrets sources with the SecretsManager. An object of class
SecretsManager is instantiated here. Any environment secrets sources can be registered here to be used later anywhere
in the project.

### <a href='https://github.com/abhiravredox/secrets-manager-POC/blob/master/secrets_manager_prototype/secrets_manager_prototype/settings.py'>settings.py</a> 
The developer will retrieve the created SecretsManager object (singleton, so developer doesn't have to do much).
get_secrets()/get_secrets(env_name) is triggered as per requirement to get secrets from the appropriate source as a dict.
       
### <a href='https://github.com/abhiravredox/secrets-manager-POC/blob/master/secrets_manager_prototype/secrets_manager/secrets_manager.py'>secrets_manager.py</a> 
In this prototype, secrets_manager.py resides in secrets_manager package. However, it will reside in the Django codebase 
later.<br>
The SecretsManager class is an instance of Singleton. Singleton is a design pattern that ensures that only one object is 
created throughout the project life cycle. This pattern facilitates the use of a SecretsManager instantiated once, to be used throughout the project in any other module.<br>
The SecretsManager's instantiating parameters define how the SecretsManager is constructed:
  1. default_env_name defines the default environment secrets source to be returned by default.
       * --env=$env_name passed to manage.py can override this
       * env_name passed to get_secrets(env_name) can override this
  2. lazy_loading defines if secrets sources are read when registered or when requested. (True by default)
  3. auto_register defines if SecretsManager should automatically register .env and python module secrets sources present 
     in the env/ directory (False by default)
       * The naming convention for auto registered environment sources in the prototype can be viewed in SecretsManager's 
          instance method auto_register(). This convention is only for demonstration purposes and will be perfected later.
       * during automatic registration, if there is a source file that contains 'base' in it's name, that source will 
          be set as the base.

The SecretsManager's instance methods allow the developer work the required magic:
  1. register(env_name, src, auto_reload=False, payload=None, headers=None, Auth=None) allows registration of a secrets
     source with the secrets manager.
  2. set_base(env_name) allows the developer to set base environment secrets, pulling from a registered source.
  3. auto_register() can be triggered by the developer in case (s)he wants to trigger automatic registration inspite of
     setting auto_register=False while instantiating SecretsManager.
  4. get_secrets(env_name=None) returns secrets of the specified environment, if env_name is passed. It env_name is not 
     passed, Returns secrets of environment name passed to manage.py using --env argument. If --env is not passed, 
     SecretsManager's default environment's secrets are returned. A dict is returned to the calling module.
  5. reload_secrets(env_name) allows developer to force reload/re-read of secrets associated with env_name even if the
     source was registered with auto_reload=False
  6. unregister(env_name) allows the developer to unregister a previously registered secrets source.

### <a href='https://github.com/abhiravredox/secrets-manager-POC/blob/master/secrets_manager_prototype/secrets_manager/secrets.py'>secrets.py</a>
In this prototype, secrets.py resides in secrets_manager module. However, it will reside in the Django codebase 
later.<br>
The SecretsAbstract class is an instance of SingletonByArgument. SingletonByArgument is a design pattern that ensures that 
only one object is created for a particular combination of registration parameters. 
DotEnvSecrets, ModuleSecrets, HTTPSecrets implement SecretsAbstract and implement the abstract method read_secrets() and 
read corresponding types of secret sources.<br>
HTTPSecrets in particular needs more parameters, payload, headers and Auth. 
  1. Auth is the type of authentication, if required, for an API based secrets source. HTTPSecrets will inspect this 
     authentication type's constructor and request CLI input for the required parameters.
