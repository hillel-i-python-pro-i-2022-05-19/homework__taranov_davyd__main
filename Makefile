
.PHONY: d-run
d-run:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_COMPOSE_BUILDKIT=1 docker-compose up --build

.PHONY: d-stop
d-stop:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_COMPOSE_BUILDKIT=1 docker-compose down

.PHONY: d-purge
d-purge:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_COMPOSE_BUILDKIT=1 docker-compose down --volumes --remove-orphans --rmi local

.PHONY: app-run
# Shortcut
app-run:
	@python main.py --words_count $(words_count) --word_length $(word_length)