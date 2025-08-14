TODO
=====

Product:

1. Plug in some data into the mock **Volatility Analyser** dashboard
2. Plug in some data into the mock **System Headroom** dashboard
3. Plug in some data into the mock **Live Plant Status board** dashboard

Shared app setup/infra:

1. Set up simple settings loading with `pydantic-settings`
    - Configure Postgres settings
    - Configure Celery settings
2. Set up Celery broker container
3. Set up simple Celery app and add a healthcheck task
