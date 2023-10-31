from django.conf import settings
from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from currency_exchange.models import Currency


class CurrencyTestCase(TestCase):

    def test_db_contains_default_currencies(self):
        db_currencies = list(Currency.objects.all().values_list("symbol"))

        default_currencies = list(map(
            lambda elem: (elem,),
            getattr(settings, "INIT_CURRENCIES", [])
        ))

        self.assertEqual(db_currencies, default_currencies,
                         "Default currencies have not been loaded")

    def test_currency_insert(self):
        symbol = "EURUSD=X"
        Currency(symbol=symbol).save()

        db_currencies = list(Currency.objects.all().values_list("symbol"))

        self.assertEqual(
            db_currencies, [(symbol,)], "Currency was not inserted")

    def test_currencies_are_unique(self):
        symbol = "EURUSD=X"
        Currency(symbol=symbol).save()

        with self.assertRaises(
                IntegrityError,
                msg="Currencies uniqueness is not enforced"
        ):
            Currency(symbol=symbol).save()

    def test_currency_symbol_max_len(self):
        too_long_symbol = "EURUSD=XG"

        with self.assertRaises(
                ValidationError,
                msg="Currencies lenght is not enforced"
        ):
            Currency(symbol=too_long_symbol).full_clean()

    def test_currency_symbol_not_null(self):
        empty_symbol = ""

        with self.assertRaises(
                ValidationError,
                msg="Empty symbols shouldn't be allowed"
        ):
            Currency(symbol=empty_symbol).full_clean()
