# Generated by Django 4.2.6 on 2023-11-01 20:04

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(
                    max_length=3,
                    unique=True,
                    validators=[
                        django.core.validators.MinLengthValidator(
                            limit_value=3,
                            message='The currency code has to be exactly 3 characters long'
                        ),
                        django.core.validators.RegexValidator(
                            '[a-zA-Z]*',
                            'The currency code can only contain letters')
                    ],
                    verbose_name='currency'
                )),
            ],
            options={
                'db_table': 'currency',
            },
        ),
        migrations.CreateModel(
            name='CurrencyExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(default=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('fst_currency', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='currency_rate_fst',
                    to='currency_exchange.currency'
                )),
                ('snd_currency', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='currency_rate_snd',
                    to='currency_exchange.currency'
                )),
            ],
            options={
                'db_table': 'currency_exchange_rate',
                'ordering': ['-created'],
            },
        ),
    ]