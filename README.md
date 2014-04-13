
# HLCS Presence

Remote Web control for Hacklab Cosenza doors

## Setup

0. Install virtualenv. In debian derivates just run

	sudo apt-get install python-virtualenv
	
1. Create a virtualenv inside project's directory and activate it

	virtualenv venv
	source venv/bin/activate
	
2. Install the required modules

	pip install -r requirements.txt
	
3. Create the db. Default is sqlite, you will be asked to create a superuser

	python manage.py syncdb
	
4. You are now able to run the app. The webserver will be available at the specified port.

	python manage.py runserver 8080
	
## urls

+ */*	checks door status
+ */open/*	opens the door
+ */admin/*	administration dashboard