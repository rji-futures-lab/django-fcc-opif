.PHONY: syncdbschema

syncdbschema:
	dropdb fcc-opif
	createdb fcc-opif
	rm -f -r fcc_opif/migrations
	python manage.py makemigrations fcc_opif
	python manage.py migrate
