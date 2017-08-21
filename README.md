# Cold-Temperature
a template to create idempotent data storage

-- clone the repo

-- cd cold-temperature

-- docker-compose up

### open up a new tab
	-- docker exec -it coldtemperature_web_1 python manage.py migrate

	-- docker exec -it coldtemperature_web_1 python create_20000_data_csv.py

	### Run more than once to see eventsdump increasing and not the other tables
	-- docker exec -it cold-temperaute_web_1 python store_data_to_postgres.py


References
* https://github.com/realpython/dockerizing-django
* https://code.djangoproject.com/wiki/MultipleColumnPrimaryKeys
* https://github.com/tonywangcn/docker-cluster-with-celery-and-rabbitmq