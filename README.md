# Tests for the ansible opentelemetry callback

## Configuration

You need a few tools:

- `ansible`
- `python`
- `virtualenv`

Then you need to copy the `opentelemetry` ansible callback to `plugins/callback_plugins`,
or you can run the below script:

```bash
mkdir -p plugins/callback_plugins
curl -s https://raw.githubusercontent.com/ansible-collections/community.general/main/plugins/callback/opentelemetry.py > plugins/callback_plugins/opentelemetry.py
```

## UTs

```bash
$ make virtualenv
$ make unit
```

## ITs

In a follow up

## Manual testing

Pick the latest changes for the otel ansible plugin using  `make prepare-env`.

### Elastic vendor

You can now create `manual/.env` with the environment variables that are used in:
- `manual/docker-compose.yml`
- `manual/config/otel-collector-config.yaml`

```bash
$ make virtualenv
$ make test-manual
```

You can now see traces in Kibana and `its/output/logs.txt`

You can see the otel collector logs by running `docker logs -f its-otel-collector-1`
