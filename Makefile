run:
	python manage.py runserver

migrations:
	python manage.py makemigrations app

migrate:
	python manage.py migrate

test:
	python manage.py test --keepdb