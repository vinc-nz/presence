
# Presence

Home automation system for controlling doors electronically and logging accesses

## Setup

0. Install virtualenv. In debian derivates just run

	    sudo apt-get install python-virtualenv
	
1. Create a python3.4 virtualenv inside project's directory and activate it

	    virtualenv -p /usr/bin/python3 venv
	    source venv/bin/activate
	
2. Install the required modules

	    pip install -r requirements-dev.txt
	
3. Create the db. Default is sqlite, you will be asked to create a superuser

	    python manage.py syncdb
	
4. You are now able to run the app. The webserver will be available at the specified port.

	    python manage.py runserver 8080
	
## Modules

+ `gatecontrol`	Provides abstract interface and REST API for doors control and logging
+ `hlcs`	Implementation based on the hardware used at Hacklab Cosenza 

## Usage

1. Extend the `gatecontrol.gatecontrol.Gate` class in order to support your hardware

2. Include it in the GATES dictionary in settings.py

		GATES = {<unique-name> : <Instance of your Gate>}

3. You can then list your doors by running the server and querying it

		python manage.py runserver 8080
		curl http://localhost:8080/gates/

4. To issue the `open_gate` command send and authenticated POST request at the relative endpoint

		http://localhost:8080/gates/<unique-name>/
