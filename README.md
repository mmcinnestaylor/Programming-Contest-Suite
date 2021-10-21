# ACM at FSU Programming Contest Suite

The Programming Contest Suite is a set of tools for running [ICPC](https://icpc.global) style programming competitions hosted by the [Association for Computing Machinery Florida State University Student Chapter](https://fsu.acm.org). The PCS is a [Django](https://www.djangoproject.com/) powered contest account registration &  management application working alongside the [DOMJudge](https://www.domjudge.org/) jury system.

## Getting Started
Ensure the target development or production machine has a functioning installiation of [Docker](https://www.docker.com) with `docker-compose` and `docker-swarm`.
### Development Deployment  
From the project root, navigate to the development folder:  

	cd deploy/dev

If you are running the development deployment for the first time, or have made any changes to the project's Celery tasks run this:  

	docker-compose build  

Launch the project in dev mode:  

	docker-compose up

NOTE: In order to monitor the debug logs, as well as view any emails the suite sends while in debug, it is suggested to NOT use the `-d` flag with the `docker-compose up` command.
### Production Deployment
The following steps are intended for deploying the suite on the Chapter's server, Agon.   

Initialize the swarm:  

	docker swarm init
	
From the project root, navigate to the production folder:  

	cd deploy/prod


Deploy the services needed to run both registration (contestsuite) and judging (DOMjudge) platforms. Deployment of services uses the Docker stacks, and will utilize the following format:  

	docker stack deploy -c path/to/compose-file.yaml service_name

NOTE: The `service_name` above is the stack service name, and does not need to match the name of the app being deployed. Picking good service names aids in monitoring running stacks in the swarm.

Deploy nginx-proxy, which routes traffic between the registration platform and the judging platform:  

	docker stack deploy -c ./nginx-proxy/docker-compose.yaml nginxproxy

Next, deploy the registration platform.  

	docker stack deploy -c ./contestsuite/docker-compose.yaml contestsuite

* The `MAIL` environment variables in the Compose file should be updated in order to connect to a valid smtp email account.  
* The `SECRET_KEY` environment variable in the Compose file should be updated as well. Django secret key generators are easily found with a Google search.  
* The `MARIADB` and `SQL` environment variables in the Compose file should be updated to properly secure the service. The credentils should match, as Django uses them to connect to MariaDB.  
* If the suite it being initialized (i.e. an empty database with no users), the default Django superuser's password should be updated from it's default of `seminoles1!` This should be performed in Django Admin. 

Then deploy DOMjudge:  

	docker stack deploy -c ./domjudge/docker-compose.yaml domjudge

* Similar to the registration platform, the `MARIADB` and `MYSQL` in the Compose file should be updated to secure the service.  
* The default admin password should be updated from `adminpw` This can be done by navigating to the DOMjudge site, logging in as admin, and nagivating to the Users section.  
* The Judgehost user's password should also be updated, as this is randomly initialized.

Lastly, deploy the Judgehosts:

	cd ./judgehosts

	docker-compose up -d --scale judgehost=<an_integer>

* The `JUDGEDAEMON_PASSWORD` environment variable in the Compose file should be updated to what was set in the step above. 

#### Teardown  
Docker stacks:  

	docker stack rm service_name

Judgehosts:  

	docker-dompose down
