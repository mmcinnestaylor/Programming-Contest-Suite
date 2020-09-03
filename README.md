# ACM at FSU Programming Contest Suite v2
### Production began on 2/17/2020

## Resources
- [Django](https://www.djangoproject.com/) - Python Web Framework
- [MariaDB](https://mariadb.com) -  Relational Database Management System
- [Redis](https://redis.io) -  Cache broker
- [Bootstrap 4](https://getbootstrap.com) -  CSS Framework
- [Font Awesome](https://fontawesome.com) -  Site Icons  
- [DomJudge](https://www.domjudge.org/) - Contest judging platform
- [Pipenv](https://pipenv.kennethreitz.org/en/latest/) - Environment virtualization
- [Docker](https://www.docker.com/) - Software containerization
- [Kubernetes](https://kubernetes.io/) - Container orchestration
- [rpi-mariadb](https://hub.docker.com/r/jsurf/rpi-mariadb/) - MariaDB container for raspberrypi
- [Contest Server v1](https://github.com/FSU-ACM/Contest-Server) - Flask implementation developed by [Andrew Sosa](https://github.com/andrewsosa)
- [Contest Server v1.1](https://github.com/FSU-ACM/Programming-Contest-Suite-v1.1) - First Django implementation for CEN4020 SP'19

# Database setup (dev only)
	sudo apt install mariadb-server
	sudo apt install libmariadbclient-dev

	sudo mysql -u root -p

	CREATE DATABASE contestsuite CHARACTER SET utf8mb4;
	CREATE USER dev@localhost IDENTIFIED BY 'seminoles';
	GRANT ALL PRIVILEGES ON contestsuite.* TO dev@localhost;
	FLUSH PRIVILEGES;

# Reset DB
	DROP DATABASE contestsuite;
	
# Useful commands
	//run testserver
	python3 manage.py runserver 0:8000
	//register new static files to serve 
	python3 manage.py collectstatic
	//interactive shell
	python3 manage.py shell

	redis-server --daemonize yes
	celery -A contestsuite beat -l info
	celery -A contestsuite worker -l info

# Test DB Users
	python3 manage.py createsuperuser

	dev seminoles1!
	rflack softly1!
	dsummer hotstuff1!
	hsolo hyperfuel1!
	lvandross	myfather1!

# Clear migrations
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete

# Migraitons
	python3 manage.py makemigrations
	python3 manage.py migrate

# Updating requirements
	pipenv lock -r > requirements.txt
	pipenv lock -r --dev > dev-requirements.txt