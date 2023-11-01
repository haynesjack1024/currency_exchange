from django.db import models


class Currency(models.Model):
    symbol = models.CharField(
        verbose_name="currency's yfinance compatible symbol",
        help_text="Only insert values which correspond to symbols supported by yfinance",
        max_length=8,
        unique=True,
    )

    class Meta:
        db_table = "currency"


class CurrencyExchangeInfo(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    exchange_rate = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "currency_exchange_info"
        ordering = ["-created"]
