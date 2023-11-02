from django.contrib import admin

from .models import Currency, CurrencyExchangeRate

admin.site.register(Currency)
admin.site.register(CurrencyExchangeRate)
