from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models


class Currency(models.Model):
    code = models.CharField(
        verbose_name="currency",
        max_length=3,
        unique=True,
        validators=[
            MinLengthValidator(
                limit_value=3,
                message="The currency code has to be exactly 3 characters long"
            ),
            RegexValidator(
                r"[a-zA-Z]{3}",
                "The currency code can only contain letters"
            )
        ]
    )

    def __str__(self):
        return self.code

    class Meta:
        db_table = "currency"


class CurrencyExchangeRate(models.Model):
    fst_currency = models.ForeignKey(Currency, related_name="currency_rate_fst", on_delete=models.PROTECT)
    snd_currency = models.ForeignKey(Currency, related_name="currency_rate_snd", on_delete=models.PROTECT)
    rate = models.FloatField(default=None)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def symbol(self):
        return f"{self.fst_currency.code}{self.snd_currency.code}"

    def __str__(self):
        return f"{self.symbol} {self.rate:.6f}"

    class Meta:
        db_table = "currency_exchange_rate"
        ordering = ["-created"]
