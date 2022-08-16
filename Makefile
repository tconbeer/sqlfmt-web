.PHONY: check
check:
	heroku local &
	MOZ_HEADLESS=1 pytest --driver Firefox
	pkill python
	isort .
	black .
	flake8 .
	mypy