from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from currency_exchange.models import Currency, CurrencyExchangeRate
from currency_exchange.serializers import CurrencySerializer, CurrencyExchangeRateSerializer


class CurrenciesList(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CurrencyPairExchangeRate(APIView):
    def get(self, request, fst_currency_code, snd_currency_code):
        fst_currency_id = get_object_or_404(Currency, code=fst_currency_code)
        snd_currency_id = get_object_or_404(Currency, code=snd_currency_code)

        currency_exchange_rate = (
            CurrencyExchangeRate.objects
            .filter(fst_currency_id=fst_currency_id)
            .filter(snd_currency_id=snd_currency_id)
            .last()
        )

        serialized_currency_exchange_rate = (
            CurrencyExchangeRateSerializer(currency_exchange_rate)
        )

        return Response(serialized_currency_exchange_rate.data)
