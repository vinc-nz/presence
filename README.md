
# Presence

Home automation system for controlling doors electronically and logging accesses.

Presence is a web application based on Django and tornado web server.
Client applications can interact with Presence using websockets


## Setup

0. Install virtualenv. In debian derivates just run

	    sudo apt-get install python-virtualenv
	
1. Create a python3.4 virtualenv inside project's directory and activate it

	    virtualenv -p /usr/bin/python3.4 venv
	    source venv/bin/activate
	
2. Install the required modules

	    pip install -r requirements.txt
	
3. Create the db. Default is sqlite

	    python manage.py migrate
	
4. You are now able to run the app.

	    python runserver.py
	
## Modules

+ `gatecontrol`	Provides abstract interface and web handlers for doors control and logging
+ `hlcs`	Implementation based on the hardware used at Hacklab Cosenza 

## Customizing

Extend the `gatecontrol.models.GateController` class in order to support your hardware and create the relative record in the database,
you can use the django shell:

	python manage.py shell
	>>> from gatecontrol.models import Gate
	>>> Gate.objects.create(name='Test Gate', controller_class=<your-class-fullname>)
		
## Usage


		
### Websocket

Connect to the socket endpoint `/socket`

The server accepts json messages of the form:

	{"method": <string>, "args": <json-object>}
		
Currently supported methods are:

1. **list_gates**
	
    args: empty

    Requests the list of doors (gates), does not require authentication
	
2. **authenticate**
	
    args: `token` (see below)

3. **open**
	
    args: `gate_id`

    requests to open the door identified by `gate_id`, may require authentication
	

	
The server returns messages of the form

	{"type": <string>, "content": <json-object>}
		
Currently supported message types are:

1. **list_gates**
	sent as reply to `list_gates`
	
    content:
	
		[
			{
			'id' : <numeric: id of the gate>,
			'name' : <string: gate name>,
			'state' : <string: current state of the gate>,
			'managed': <boolean: whether or not the user is able to open the gate> 
			},
			...
		]
    
        	
2. **open**
	
    content: "success"
	
    sent as reply to `open` in case of success
	
3. **error**
	
    content: <string: error message>
	
    sent in case of errors

### Obtaining the token

In order to perform actions that require authentication (e.g. open a door) a user must first request a JWT access token by sending an HTTP POST request to the `/token` endpoint
Request format:

	{"username": <username>, "password": <password>}
		
Response:

	{"type": "token", "content": <the-token>}
		
## Administration

The administration web interface is provided by django at the endpoint `/admin`
You must first create the superuser:

	python manage.py createsuperuser
