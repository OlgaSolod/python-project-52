migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

start_server:
	python manage.py runserver