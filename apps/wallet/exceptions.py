class CustomizedException(Exception):
    """
    A customized exception that stores message text in itself.
    """
    message = None

    def __init__(self, message=None, *args, **kwargs):
        super().__init__(message if message else self.message, *args, **kwargs)


class InvalidTransactionType(CustomizedException):
    message = ('Invalid transaction type, please provide '
               'a valid value like "inflow" or "outflow"')


class InflowTransactionHasANegativeAmount(Exception):
    message = ('Inflow transactions can not have negative values '
               'in the "amount" field, please provide a positive value.')


class OutflowTransactionHasAPositiveAmount(Exception):
    message = ('Outflow transactions can not have positive values '
               'in the "amount" field, please provide a negative value.')
