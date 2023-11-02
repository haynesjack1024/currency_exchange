from django.conf import settings
from django.db import migrations


def insert_def_currencies(apps, schema_editor):
    currency_codes = settings.INIT_CURRENCIES
    Currency = apps.get_model("currency_exchange", "Currency")
    for currency_code in currency_codes:
        Currency(code=currency_code).save()


def delete_def_currencies(apps, schema_editor):
    currency_codes = settings.INIT_CURRENCIES
    Currency = apps.get_model("currency_exchange", "Currency")
    Currency.objects.filter(symbol__in=currency_codes).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("currency_exchange", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(insert_def_currencies, delete_def_currencies)
    ]
