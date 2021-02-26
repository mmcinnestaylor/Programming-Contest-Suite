# ACM at FSU Programming Contest Suite v2

The Programming Contest Suite (PCS) v2 is a set of tools for running [ICPC](https://icpc.global) style programming competitions hosted by the Association for Computing Machinery Florida State University Student Chapter. The PCS is primarily a Django powered web application working alongside a containerized version of the DOMJudge platform.

### Production began on 2/17/2020

## Resources
- [Django](https://www.djangoproject.com/) - Python Web Framework
- [MariaDB](https://mariadb.com) -  Relational Database Management System
- [Redis](https://redis.io) -  Cache broker
- [RabbitMQ](https://www.rabbitmq.com) - Message broker
- [Bootstrap 4](https://getbootstrap.com) -  CSS Framework
- [DomJudge](https://www.domjudge.org/) - Contest judging platform
- [Pipenv](https://pipenv.kennethreitz.org/en/latest/) - Environment virtualization
- [Docker](https://www.docker.com/) - Software containerization
- [Kubernetes](https://kubernetes.io/) - Container orchestration
- [rpi-mariadb](https://hub.docker.com/r/jsurf/rpi-mariadb/) - MariaDB container for raspberrypi
### Previous Implementations
- [Contest Server v1](https://github.com/FSU-ACM/Contest-Server) - Flask implementation developed by [Andrew Sosa](https://github.com/andrewsosa)
- [Contest Server v1.1](https://github.com/FSU-ACM/Programming-Contest-Suite-v1.1) - First Django implementation for CEN4020 SP'19

# Getting Started
## Installation
### As we are still in development, these steps will get the dev environment working

	/** Linux users **/
	sudo apt install mariadb-server libmariadbclient-dev redis-server rabbitmq-server
	
	sudo systemctl enable mariadb-server
	sudo systemctl start mariadb-server

	sudo systemctl enable redis-server
	sudo systemctl start redis-server

	sudo systemctl enable rabbitmq-server
	sudo systemctl start rabbitmq-server


	/** macOS users **/
	brew install mariadb redis rabbitmq
	
	brew services start mariadb
	brew services start redis
	brew services start rabbitmq


### Getting Pipenv
	pip install --user pipenv
	OR
	brew install pipenv
	OR
	curl https://raw.githubusercontent.com/pypa/pipenv/master/get-pipenv.py | python

### Get repository and download dependencies
	git clone https://github.com/FSU-ACM/Programming-Contest-Suite-v2.git
	cd Programming-Contest-Suite-v2/

	pipenv install
	pipenv install --dev
	
## Setup Database
	sudo mysql -u root -p

	CREATE DATABASE contestsuite CHARACTER SET utf8mb4;
	CREATE USER dev@localhost IDENTIFIED BY 'seminoles';
	GRANT ALL PRIVILEGES ON contestsuite.* TO dev@localhost;
	FLUSH PRIVILEGES;

## Setup .env file
### lives in /src/contestsuite/


## Run server
	cd Programming-Contest-Suite-v2/
	pipenv shell
	cd src/

	//perform initial migrations
	python3 manage.py migrate

	//collect static files
	python3 manage.py collectstatic

	//create a super user
	python3 manage.py createsuperuser

	//run testserver
	python3 manage.py runserver 127.0.0.1:8000

	//run Celery worker and beat server
	celery -A contestsuite worker -l info
	celery -A contestsuite beat -l info


# Useful commands
## Reset DB
	DROP DATABASE contestsuite;
	
## Register new static files
	python3 manage.py collectstatic

## Django interactive shell
	python3 manage.py shell

## Make new migrations
	python3 manage.py makemigrations
	python3 manage.py migrate

## Clear migrations
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete

## Updating requirements
	pipenv lock -r > requirements.txt
	pipenv lock -r --dev > dev-requirements.txt