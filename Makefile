migrate:
	uv run python manage.py makemigrations
	uv run python manage.py migrate

start-server:
	python manage.py runserver

test:
	uv run python ./manage.py test 