# cielo_frontend

Frontend for CIELO.

## Settings

This project uses a modular settings package located in
`cielo_frontend/settings/`.  Development runs with
`cielo_frontend.settings.dev` by default.  Production deployments should set
`DJANGO_SETTINGS_MODULE=cielo_frontend.settings.prod` and provide required
environment variables such as `DJANGO_SECRET_KEY`.
