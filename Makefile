.PHONY: test test-cov test-e2e run

test:
	pytest tests/unit/ tests/integration/

test-cov:
	pytest --cov=src

test-e2e:
	pytest tests/e2e/ -v

run:
	python -m src.web.app
