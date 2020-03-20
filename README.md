# Secrets Manager - Django GSoC
A gist about the crux of this prototype is available <a href='https://gist.github.com/abhiravredox/cfb9fd5e8f9af6a1274a2cb68d7de05a'>here</a> as the Djnago community may not have the
time to look at all the code.

## About this Prototype
This is a prototype for my own sanity check that my approach works. Consequently, things like exception handling and some edge
cases have been overlooked.
The prototype consists of 2 projects:
  1. secrets_manager_prototype
  2. http_secrets_server (a project to act as a secrets store for testing HTTPSecrets)
  
The <a href='https://github.com/abhiravredox/secrets-manager-POC/tree/master/secrets_manager_prototype/secrets_manager'> secrets_manager package</a> is the real deal here. <a href='https://github.com/abhiravredox/secrets-manager-POC/tree/master/secrets_manager_prototype/secrets_manager_prototype/env'>env.py</a> and <a href='https://github.com/abhiravredox/secrets-manager-POC/blob/master/secrets_manager_prototype/secrets_manager_prototype/settings.py'>settings.py</a> also play a vital role. Rest of the code serves demonstration purpose.

## Deploying the prototype
1. use requirements.txt to install dependencies in both projects
2. run http_secrets_server on port 8080 using `python manage.py runserver 8080` (Port 8080 is required as the end points registered with the SecretsManager are pointing to localhost:8080. You may change that if you want in env.py.
3. run secrets_manager_prototype using `python manage.py runserver`
4. Visit http://127.0.0.1:8000/ and play

<b>Note: I've commented the sources that require authentication so that the <a href='https://github.com/abhiravredox/secrets-manager-POC/tree/master/secrets_manager_prototype/secrets_viewer'>secrets_viewer</a> app can work smoothly. However, the viewer is only for demonstration purposes. You can uncomment authentication based sources in env.py. Depending on the lazy_load parameter, you will required to input parameters required by the authentication. This might even happen while using secrets_viewer You can enter garbage values there as the http_secrets_server doesn't really authenticate. However, the authentication objects are actually sent with the request. 

## Using different registered environments
With the current code, the registered environments have names: module_base, dot_env_dev, dot_env_prod, dot_env_test, module_dev, module_prod, module_test, http_get_dev, http_get_prod, http_get_test, http_post_dev, http_post_prod, http_post_test. You can also view them in the aforementioned secrets_viewer.
There are 2 ways to deploy the app with registered environments (otherwise default environment, as defined in env.py, is used)
1. Pass --env to manage.py like this: `python manage.py runserver --env=http_get_test`
2. Pass env_name to get_secrets() in settings.py. If you do this, the server will always run with env_name secrets even if you    
   pass --env to manage.py.
   
## <a href='https://github.com/abhiravredox/secrets-manager-POC/tree/master/secrets_manager_prototype/secrets_viewer'>secrets_viewer</a>
* This app is only for demonstration purposes and tries to demonstrate what functionalities can be exploited by the developer.
* The app will allow you to view the registered environment secrets sources. 
* The table on the left lists the registrations.
* On the right, the secrets of the selected environment will be displayed. 
  * Everytime you click on a row, the get_secrets(env_name) is called. If auto_reload=True, the secrets will reload    
    automatically.
  * You can also force a reload, even if auto_reload is false.
* You can view the secrets that were used to deploy the app using the navbar on top. Again, as get_secrets() is called,   
  auto_reload may entail
  
