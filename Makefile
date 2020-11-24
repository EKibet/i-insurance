install:
	pip install

migrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

superuser:
	python manage.py createsuperuser

collectstatic:
	python manage.py collectstatic

shell:
	python3 manage.py shell

set_env_vars:
	@[ -f .env ] && source .env

serve:
	python3.8 manage.py runserver

.PHONY: set_env_vars