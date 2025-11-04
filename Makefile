.PHONY: test test-unit coverage build clean

# Build the application
build:
	docker-compose up --build

# Build the test image
build-test:
	docker build -f Dockerfile.test -t employee-search-test .

# Run all tests (doesn't start the service)
test: build-test
	docker run --rm \
		-e PYTHONPATH=/app \
		-e TESTING=true \
		employee-search-test

# Run with coverage
coverage: build-test
	mkdir -p coverage
	docker run --rm \
		-e PYTHONPATH=/app \
		-e TESTING=true \
		-v $(PWD)/coverage:/app/htmlcov \
		employee-search-test python -m pytest tests/ --cov=app --cov-report=html

# Clean up
clean:
	docker-compose down -v
	docker system prune -f
	rm -rf coverage htmlcov .coverage
