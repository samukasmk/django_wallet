class InflowTransactionHasANegativeAmount(Exception):
    message = 'Inflow transactions can not have negative values in the "amount" field, please provide a positive value.'

    def __init__(self, message: str = None, *args, **kwargs) -> None:
        super().__init__(message if message else self.message, *args, **kwargs)


class OutflowTransactionHasAPositiveAmount(Exception):
    message = 'Outflow transactions can not have positive values in the "amount" field, please provide a negative value.'

    def __init__(self, message: str = None, *args, **kwargs) -> None:
        super().__init__(message if message else self.message, *args, **kwargs)
