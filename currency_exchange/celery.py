import os

import django
import yfinance as yf
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "currency_exchange.settings")
django.setup()

from currency_exchange.models import Currency
from currency_exchange.models import CurrencyExchangeInfo

app = Celery("currency_exchange")
app.config_from_object("django.conf:settings", namespace="CELERY")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        10.0,
        get_currency_exchange_info.s(),
        name="get currency exchange info"
    )


@app.task
def get_currency_exchange_info():
    currencies = list(map(
        lambda elem: elem[0],
        Currency.objects.all().values_list("symbol")
    ))

    tickers = yf.Tickers(" ".join(currencies)).tickers
    for symbol, ticker in tickers.items():
        last_price = ticker.fast_info["lastPrice"]

        if last_price is not None:
            CurrencyExchangeInfo(
                currency=Currency.objects.get(symbol=symbol),
                exchange_rate=last_price
            ).save()
