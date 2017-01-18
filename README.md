
# Presence [![Build Status](https://travis-ci.org/sp4x/presence.svg?branch=master)](https://travis-ci.org/sp4x/presence)

Home automation system for controlling doors electronically and logging accesses.

Presence is a web application based on Django and tornado web server.
Client applications can interact with Presence using websockets

----
## Development


### Setup development environment

0. Install virtualenv. In debian derivates just run

	    sudo apt-get install python-virtualenv

1. Create a python3.4 virtualenv inside project's directory and activate it

	    virtualenv -p /usr/bin/python3.4 venv
	    source venv/bin/activate

2. Install the required modules

	    pip install -r requirements.txt

3. Create the db. Default is sqlite

	    python manage.py migrate

4. Create the directory for static files

        python manage.py collectstatic

5. Create super user so you can login do Django admin

        python manage.py createsuperuser

6. You are now able to run the app, the development server will listen at http://localhost:8000

	    python runserver.py

#### Modules

+ `gatecontrol`	Provides abstract interface and web handlers for doors control and logging
+ `hlcs`	Implementation based on the hardware used at [Hacklab Cosenza](http://hlcs.it)

#### Customizing

Extend the `gatecontrol.models.GateController` class in order to support your hardware and create the relative record in the database,
you can use the django shell:

	python manage.py shell
	>>> from gatecontrol.models import Gate
	>>> Gate.objects.create(name='Test Gate', controller_class=<your-class-fullname>)    

----
## API

Presence API are exposed via Websocket, except the authentication process which is done via plain HTTP.

#### Websocket

Connect to the socket endpoint `/socket`

The server accepts json messages of the form:

	{"method": <string>, "args": <json-object>}

Currently supported methods are `list_gates`, `authenticate` and `open`.

##### list_gates

Requests the list of doors (gates), does not require authentication.

*args:* `<empty>`

*response:*

	{
		type: "list_gates",
		content: [
			{
			id : <numeric: id of the gate>,
			name : <string: gate name>,
			state : <string: current state of the gate>,
			managed: <boolean: whether or not the user is able to open the gate>
			},
			...
		]
	}

##### authenticate

*args:* `token` (see below)

##### open

requests to open the door identified by `gate_id`, may require authentication.

*args:* `gate_id`

*response:*

		{type: "open", content: "success"}

if success, otherwise

		{type: "error", content: <error message>}

#### Obtaining the token

In order to perform actions that require authentication (e.g. open a door) a user must first request a JWT access token by sending an HTTP POST request to the `/token` endpoint
Request format:

	{"username": <username>, "password": <password>}

Response:

	{"type": "token", "content": <the-token>}

----
## Administration

The administration web interface is provided by django at the endpoint `/admin`.

----
## Running in production

Same step as development, but you can skip the virtualenv and install the requirements system wide

    sudo pip install -r requirements.txt

If you are using the module `hlcs` you need to setup presence on a RPi, as it uses the GPIO python library you may need to install it:

    pip install -r requirements-rpi.txt

It is recommended to set up and HTTP server to proxy requests to presence and serve static files.
By default Django looks for static files under the HTTP path `/static/`, so that path should be served by the server.
You can change location of static files and static URL by modifying the settings STATIC_ROOT and STATIC_URL.

### Configuration

The configuration file in presence/settings.py.
As this file is under version control, the recommended way to customize application settings is by creating a file called `local_settings.py` under the directory `presence`.
In local_settings.py place the settings variable you want to override (e.g. DATABASES, SECRET_KEY).
It is important that you set DEBUG = False.
Check Django documentation for inscructions.


### Serving static files

It is recommended that static files are served by an HTTP server (e.g. apache, nginx).
You can use the setting STATIC_ROOT to change the directory where static file are copied after running `collectstatic`.
By default Django looks for static files under the HTTP path `/static/`, you can change the HTTP path modifying the setting STATIC_URL.
You can setup the HTTP server to serve STATIC_URL directly and proxy every other URL.
