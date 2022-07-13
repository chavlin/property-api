env:
	pipenv sync --dev

clean:
	pipenv --rm
	rm -rf .pytest_cache

test:
	pipenv run python -m pytest

run:
	pipenv run python run.py
