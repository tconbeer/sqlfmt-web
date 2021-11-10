.PHONY: check
check:
	sqlfmt-web &
	pytest --driver Firefox
	pkill sqlfmt-web
	isort .
	black .
	flake8 .
	mypy