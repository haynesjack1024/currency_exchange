from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from currency_exchange.models import Currency


class CurrencyTestCase(TestCase):
    def assert_test_code_not_in_db_currency_codes(self, test_code):
        db_currency_codes = list(map(
            lambda elem: elem[0],
            Currency.objects.all().values_list("code")
        ))

        self.assertNotIn(
            test_code,
            db_currency_codes,
            f'Test currency code "{test_code}" conflicts with settings'
        )

    def test_db_contains_default_currencies(self):
        db_currency_codes = set(Currency.objects.all().values_list("code"))

        default_currency_codes = set(map(
            lambda elem: (elem,),
            getattr(settings, "INIT_CURRENCIES", [])
        ))

        self.assertEqual(
            db_currency_codes,
            default_currency_codes,
            "Default currencies have not been inserted"
        )

    def test_currency_insert(self):
        code = "TTT"
        self.assert_test_code_not_in_db_currency_codes(code)

        currency = Currency(code=code)
        currency.save()
        db_currencies = Currency.objects.all()

        self.assertIn(currency, db_currencies, "Currency was not inserted")

    def test_currencies_are_unique(self):
        code = "DUP"
        self.assert_test_code_not_in_db_currency_codes(code)

        Currency(code=code).save()
        with self.assertRaises(
                IntegrityError,
                msg="Currency's code uniqueness is not enforced"
        ):
            Currency(code=code).save()

    def test_currency_code_max_len(self):
        too_long_code = "LONG"

        with self.assertRaises(
                ValidationError,
                msg="Currency's code max length is not enforced"
        ):
            Currency(code=too_long_code).full_clean()

    def test_currency_code_min_len(self):
        too_short_code = "SH"

        with self.assertRaises(
                ValidationError,
                msg="Currency's code min length is not enforced"
        ):
            Currency(code=too_short_code).full_clean()

    def test_currency_symbol_not_null(self):
        empty_code = ""

        with self.assertRaises(
                ValidationError,
                msg="Empty codes shouldn't be allowed"
        ):
            Currency(code=empty_code).full_clean()

    def test_code_valid_characters(self):
        invalid_code = "H4T"

        with self.assertRaises(
                ValidationError,
                msg="Only letters should be allowed in currency codes"
        ):
            Currency(code=invalid_code).full_clean()

    def test_to_string(self):
        code = "TTT"
        currency = Currency(code=code)

        self.assertEqual(
            code,
            str(currency),
            "Currency's string representation should be equal to it's code"
        )
