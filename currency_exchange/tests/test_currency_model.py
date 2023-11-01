from django.conf import settings
from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from currency_exchange.models import Currency


class CurrencyTestCase(TestCase):
    def assert_invalid_symbol_not_in_init_currencies(self, invalid_symbol):
        db_currencies = list(map(
            lambda elem: elem[0],
            Currency.objects.all().values_list("symbol")
        ))

        self.assertNotIn(
            invalid_symbol,
            db_currencies,
            f'Symbol "{invalid_symbol}" is not a valid currency symbol, '
            'remove it from settings.INIT_CURRENCIES and '
            're-run migration 0002'
        )

    def test_db_contains_default_currencies(self):
        db_currencies = set(Currency.objects.all().values_list("symbol"))

        default_currencies = set(map(
            lambda elem: (elem,),
            getattr(settings, "INIT_CURRENCIES", [])
        ))

        self.assertEqual(
            db_currencies,
            default_currencies,
            "Default currencies have not been inserted"
        )

    def test_currency_insert(self):
        symbol = "TEST"
        self.assert_invalid_symbol_not_in_init_currencies(symbol)

        currency = Currency(symbol=symbol)
        currency.save()
        db_currencies = Currency.objects.all()

        self.assertIn(currency, db_currencies, "Currency was not inserted")

    def test_currencies_are_unique(self):
        symbol = "DUPLICAT"
        self.assert_invalid_symbol_not_in_init_currencies(symbol)

        Currency(symbol=symbol).save()
        with self.assertRaises(
                IntegrityError,
                msg="Currency's uniqueness is not enforced"
        ):
            Currency(symbol=symbol).save()

    def test_currency_symbol_max_len(self):
        too_long_symbol = "TOO_LONG_"

        with self.assertRaises(
                ValidationError,
                msg="Currency's length is not enforced"
        ):
            Currency(symbol=too_long_symbol).full_clean()

    def test_currency_symbol_not_null(self):
        empty_symbol = ""

        with self.assertRaises(
                ValidationError,
                msg="Empty symbols shouldn't be allowed"
        ):
            Currency(symbol=empty_symbol).full_clean()
