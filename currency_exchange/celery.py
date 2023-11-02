import os
from itertools import permutations

import django
import yfinance as yf
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "currency_exchange.settings")
django.setup()

from currency_exchange.models import Currency, CurrencyExchangeRate

app = Celery("currency_exchange")
app.config_from_object("django.conf:settings", namespace="CELERY")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        60.0,
        get_currency_exchange_rates.s()
    )


@app.task
def get_currency_exchange_rates():
    currency_pairs = permutations(Currency.objects.all(), 2)

    currency_exchange_rates = []
    for fst_currency, snd_currency in currency_pairs:
        currency_exchange_rates.append(
            CurrencyExchangeRate(
                fst_currency=fst_currency,
                snd_currency=snd_currency
            )
        )

        ticker = yf.Ticker(f"{currency_exchange_rates[-1].symbol}=X")
        currency_exchange_rates[-1].rate = ticker.fast_info['lastPrice']

        if currency_exchange_rates[-1].rate is not None:
            currency_exchange_rates[-1].save()
