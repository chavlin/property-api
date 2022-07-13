env:
	pipenv sync --dev

test:
	pipenv run python -m pytest

clean:
	pipenv --rm
