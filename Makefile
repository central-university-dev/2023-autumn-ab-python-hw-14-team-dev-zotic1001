install:
	poetry install

update:
	poetry lock

db_upgrade:
	alembic upgrade head

db_seed:
	python -m seed

db_start: db_upgrade db_seed
