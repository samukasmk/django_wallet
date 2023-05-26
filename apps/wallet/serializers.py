from typing import Sequence
from rest_framework import serializers
from apps.wallet.models import FinancialTransaction
from apps.wallet.validators import validate_flow_type, validate_amount_signal_for_type
from apps.wallet.exceptions import (InvalidTransactionType,
                                    InflowTransactionHasANegativeAmount,
                                    OutflowTransactionHasAPositiveAmount)


class FloatFieldTwoDecimalPoints(serializers.Field):
    """
    Custom serializer field for format float values

    serializing: converting from float to str with just two decimal points
    deserializing: conversion from str into float validating it
    """

    def to_internal_value(self, data):
        """
        Convert from str to float value to save on db
        """
        try:
            return float(data)
        except (TypeError, ValueError):
            raise serializers.ValidationError("Invalid float value")

    def to_representation(self, value):
        """
        Convert from float value to str with two decimal points to response serializer
        """
        return '{:.2f}'.format(value)


class FinancialTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for LIST and POST actions
    """
    amount = FloatFieldTwoDecimalPoints()

    class Meta:
        model = FinancialTransaction
        fields = ['reference', 'date', 'amount', 'type', 'category', 'user_email']

    def validate(self, data: dict) -> dict:
        """
        Validate input values from POST creations
        """
        # check transaction types
        try:
            validate_flow_type(transaction_type=data['type'])
        except InvalidTransactionType as exc:
            raise serializers.ValidationError(
                {'type': InvalidTransactionType.message}) from exc

        # check signal of amount value before call save method.
        try:
            validate_amount_signal_for_type(data['type'], float(data['amount']))
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
    """
    Serializer for json responses of aggregations by user
    """
    user_email = serializers.EmailField()
    total_inflow = FloatFieldTwoDecimalPoints()
    total_outflow = FloatFieldTwoDecimalPoints()


class SummaryUserTransactionByCategory(serializers.Serializer):
    """
    Serializer for json responses of aggregations by user
    """
    inflow = serializers.DictField()
    outflow = serializers.DictField()

    def to_representation(self, queryset_result: Sequence[FinancialTransaction]) -> dict:
        """
        Format QuerySet result into json response
        """
        response_dict = {'inflow': {}, 'outflow': {}}
        for summary_category in queryset_result:
            flow_type = summary_category['type']
            category_name = summary_category['category']
            total_category = '{:.2f}'.format(summary_category['total'])
            response_dict[flow_type][category_name] = total_category

        return response_dict
