.PHONY: start
start:
	@mkdir -p output
	@touch output/logs.txt
	@env docker compose --env-file .env --file docker-compose.yml up --detach --no-recreate

.PHONY: stop
stop:
	@env docker compose --file docker-compose.yml stop

.PHONY: clean
clean:
	@env docker compose --file docker-compose.yml down -v
