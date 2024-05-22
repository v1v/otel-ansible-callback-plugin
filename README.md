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