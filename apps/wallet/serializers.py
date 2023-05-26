from typing import Sequence
from rest_framework import serializers
from apps.wallet.models import FinancialTransaction
from apps.wallet.validators import validate_amount_flow_value
from apps.wallet.exceptions import InflowTransactionHasANegativeAmount, OutflowTransactionHasAPositiveAmount


class FloatFieldTwoDecimalPoints(serializers.Field):
    def to_internal_value(self, data):
        """ Convert str to float value to save on db"""
        try:
            return float(data)
        except (TypeError, ValueError):
            raise serializers.ValidationError("Invalid float value")

    def to_representation(self, value):
        """ Convert float value to str with two decimal points to export """
        return '{:.2f}'.format(value)


class FinancialTransactionSerializer(serializers.ModelSerializer):
    amount = FloatFieldTwoDecimalPoints()

    class Meta:
        model = FinancialTransaction
        fields = ['reference', 'date', 'amount', 'type', 'category', 'user_email']

    def validate(self, data: dict) -> dict:
        """ Validate input values """

        # check signal of amount value before call save method.
        try:
            validate_amount_flow_value(data['type'], float(data['amount']))
        except InflowTransactionHasANegativeAmount as exc:
            raise serializers.ValidationError(
                {'amount': InflowTransactionHasANegativeAmount.message}) from exc
        except OutflowTransactionHasAPositiveAmount as exc:
            raise serializers.ValidationError(
                {'amount': OutflowTransactionHasAPositiveAmount.message}) from exc
        except Exception as exc:
            raise serializers.ValidationError({'amount': 'error on validation'}) from exc

        # call other validations of inheritance
        return super().validate(data)


class SummaryAllTransactionsByUser(serializers.Serializer):
    user_email = serializers.EmailField()
    total_inflow = FloatFieldTwoDecimalPoints()
    total_outflow = FloatFieldTwoDecimalPoints()


class SummaryUserTransactionByCategory(serializers.Serializer):
    inflow = serializers.DictField()
    outflow = serializers.DictField()

    def to_representation(self, queryset_result: Sequence[FinancialTransaction]) -> dict:
        """ Format QuerySet result into json response """

        response_dict = {'inflow': {}, 'outflow': {}}
        for summary_category in queryset_result:
            flow_type = summary_category['type']
            category_name = summary_category['category']
            total_category = summary_category['total']
            response_dict[flow_type][category_name] = total_category

        return response_dict
