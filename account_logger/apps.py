from django.apps import AppConfig


class AccountLoggerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account_logger'
    verbose_name='لاگ های سیستمی یوزر'