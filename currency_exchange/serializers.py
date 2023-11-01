from rest_framework import serializers

from currency_exchange.models import CurrencyExchangeInfo


class CurrencyExchangeInfoSerializer(serializers.ModelSerializer):
    currency = serializers.SlugRelatedField(
        slug_field='symbol',
        read_only=True
    )

    class Meta:
        model = CurrencyExchangeInfo
        fields = ['currency', 'exchange_rate']
