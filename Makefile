.PHONY: syncdbschema test

syncdbschema:
	dropdb fcc-opif --if-exists
	createdb fcc-opif
	rm -f -r fcc_opif/migrations
	python manage.py makemigrations fcc_opif
	python manage.py migrate

test:
	python manage.py test
