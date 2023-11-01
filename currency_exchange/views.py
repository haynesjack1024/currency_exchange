from rest_framework.decorators import api_view
from rest_framework.response import Response

from currency_exchange.models import Currency, CurrencyExchangeInfo
from currency_exchange.serializers import CurrencyExchangeInfoSerializer


@api_view(['GET'])
def currency_exchange_rates(request):
    if request.method == 'GET':
        currencies = Currency.objects.all()
        latest_exchange_info = []
        for currency in currencies:
            latest_currency_exchange_rate = (
                CurrencyExchangeInfo.objects
                .filter(currency__exact=currency.id)
                .first()
            )

            if latest_currency_exchange_rate is not None:
                latest_exchange_info.append(latest_currency_exchange_rate)

        serialized_data = CurrencyExchangeInfoSerializer(latest_exchange_info, many=True).data
        return Response(serialized_data)
