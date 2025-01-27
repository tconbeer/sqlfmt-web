.PHONY: serve
serve:
	pkill python || true
	python -m sqlfmt_web &
	echo "run pkill python to kill the server"

.PHONY: check
check:
	pkill python || true
	python -m sqlfmt_web &
	MOZ_HEADLESS=1 pytest --driver Firefox
	pkill python
	isort .
	black .
	flake8 .
	mypy
