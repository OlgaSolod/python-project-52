migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

start-server:
	python manage.py runserver