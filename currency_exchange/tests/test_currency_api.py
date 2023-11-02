import io

from rest_framework.parsers import JSONParser
from rest_framework.test import APITestCase

from currency_exchange.models import Currency, CurrencyExchangeRate
from currency_exchange.serializers import CurrencySerializer, CurrencyExchangeRateSerializer


class CurrencyApiTestCase(APITestCase):
    def get_parsed_json(self, endpoint):
        response = self.client.get(endpoint)
        stream = io.BytesIO(response.content)
        return JSONParser().parse(stream)

    def assert_equal_db_api_currencies(self):
        api_currencies = self.get_parsed_json('/currency/')
        db_currencies = CurrencySerializer(
            Currency.objects.all(),
            many=True
        ).data

        self.assertEqual(
            api_currencies,
            db_currencies,
            "Currencies returned by the db "
            "don't match the ones returned by the api"
        )

    def test_currency_list(self):
        Currency(code="TTT").save()

        self.assert_equal_db_api_currencies()

    def test_empty_currency_list(self):
        Currency.objects.all().delete()

        self.assert_equal_db_api_currencies()

    def test_currency_exchange_rate(self):
        fst_currency = Currency(code="TTT")
        fst_currency.save()

        snd_currency = Currency(code="EEE")
        snd_currency.save()

        db_currency_exchange_rate = CurrencyExchangeRate(
            fst_currency=fst_currency,
            snd_currency=snd_currency,
            rate=1.234
        )
        db_currency_exchange_rate.save()
        serialized_db_currency_exchange_rate = CurrencyExchangeRateSerializer(db_currency_exchange_rate).data

        api_currency_exchange_rate = self.get_parsed_json(f'/currency/{fst_currency.code}/{snd_currency.code}/')

        self.assertEqual(
            serialized_db_currency_exchange_rate,
            api_currency_exchange_rate,
            "Currency exchange rates returned by the db "
            "don't match the ones returned by the api"
        )

    def assert_not_found(self, endpoint):
        response = self.client.get(endpoint)
        self.assertEqual(
            response.status_code,
            404,
            f"Endpoint {endpoint} should return a 404 status code"
        )

    def test_not_found_currency_exchange_rate(self):
        fst_currency_code = "TTT"
        snd_currency_code = "EEE"

        Currency(code=snd_currency_code).save()

        db_currency_codes = list(map(
            lambda elem: elem[0],
            Currency.objects.all().values_list("code")
        ))

        self.assertNotIn(fst_currency_code, db_currency_codes)

        self.assert_not_found('/currency/TTT/TTT/')
        self.assert_not_found('/currency/TTT/EEE/')
        self.assert_not_found('/currency/EEE/TTT/')
