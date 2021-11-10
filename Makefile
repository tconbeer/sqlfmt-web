.PHONY: check
check:
	sqlfmt-web &
	MOZ_HEADLESS=1 pytest --driver Firefox
	pkill sqlfmt-web
	isort .
	black .
	flake8 .
	mypy