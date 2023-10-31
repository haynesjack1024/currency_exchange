import os
import django
from celery import Celery
import yfinance as yf

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "currency_exchange.settings")
django.setup()

from currency_exchange.models import Currency

app = Celery("currency_exchange")
app.config_from_object("django.conf:settings", namespace="CELERY")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        300.0, get_currency_exchange_rates.s(), name="get currency exchange rates"
    )


@app.task
def get_currency_exchange_rates():
    currencies = list(map(
        lambda elem: elem[0],
        Currency.objects.all().values_list("symbol")
    ))

    tickers = yf.Tickers(" ".join(currencies)).tickers
    ticker_data = {}
    for symbol, ticker in tickers.items():
        ticker_data[symbol] = ticker.fast_info["lastPrice"]
    return ticker_data
