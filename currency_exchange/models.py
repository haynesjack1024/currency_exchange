from django.db import models
from django.core.validators import MinLengthValidator


class Currency(models.Model):
    symbol = models.CharField(
        max_length=8,
        help_text="Only insert values which correspond to symbols supported by yfinance",
        unique=True,
        validators=[MinLengthValidator(limit_value=0, message="The currency's symbol can't be empty")]
    )
