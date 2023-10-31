from django.db import migrations
from django.conf import settings


def insert_init_currencies(apps, schema_editor):
    currencies = settings.INIT_CURRENCIES
    Currency = apps.get_model("currency_exchange", "Currency")
    for currency in currencies:
        Currency(symbol=currency).save()


def delete_init_currencies(apps, schema_editor):
    currencies = settings.INIT_CURRENCIES
    Currency = apps.get_model("currency_exchange", "Currency")
    Currency.objects.filter(symbol__in=currencies).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("currency_exchange", "0001_currency_model"),
    ]

    operations = [
        migrations.RunPython(insert_init_currencies, delete_init_currencies)
    ]
