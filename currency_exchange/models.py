from django.db import models
from django.core.validators import MinLengthValidator


class Currency(models.Model):
    symbol = models.CharField(
        verbose_name="currency's yfinance compatible symbol",
        help_text="Only insert values which correspond to symbols supported by yfinance",
        max_length=8,
        unique=True,
    )
