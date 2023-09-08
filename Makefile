CONTAINER_DEV_IMAGE=test:dev

venv:
	# Create virtual environment.
	python3 -m venv venv
	./venv/bin/pip3 install --upgrade pip setuptools wheel
	./venv/bin/pip3 install -r dev.requirements.txt

format: venv
	# Run checking and formatting sources.
	./venv/bin/pre-commit run -a

clean:
	# Reset all containers and volumes.
	docker compose -f external.compose.yml -f dev.compose.yml down --remove-orphans --volumes --timeout 1

stop:
	# Stop all containers.
	docker compose -f external.compose.yml -f dev.compose.yml down --remove-orphans --timeout 1

build: clean
	# Build image.
	docker build -q -t postgres:dev ./external/postgres
	docker build -q -t ${CONTAINER_DEV_IMAGE} .

external: stop build
	# Run containers with db`s services.
	docker compose -f external.compose.yml up -d

run: stop build
	# Run app in container.
	docker compose -f external.compose.yml -f dev.compose.yml up --abort-on-container-exit
