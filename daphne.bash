$env:DJANGO_SETTINGS_MODULE="mediplant.settings.dev"
daphne -b 0.0.0.0 -p 8000 mediplant.asgi:application
