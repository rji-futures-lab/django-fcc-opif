.PHONY: syncdbschema test encryptsecrets

syncdbschema:
	dropdb fcc-opif --if-exists
	createdb fcc-opif
	rm -f -r fcc_opif/migrations
	python manage.py makemigrations fcc_opif
	python manage.py migrate

test:
	python manage.py test

encryptsecrets:
	rm -f secrets.tar.enc
	tar cvf secrets.tar zappa_settings.json secrets.cfg
	travis encrypt-file secrets.tar --add --pro
	rm secrets.tar