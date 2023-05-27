from drf_spectacular.utils import OpenApiParameter, OpenApiExample

list_all_transactions_schema = {
    'parameters': [
        OpenApiParameter(name='group_by', type=str, required=False,
                         examples=[OpenApiExample('List all',
                                                  value=None,
                                                  summary='1.) List all financial transactions records'),
                                   OpenApiExample('Example 2',
                                                  value='type',
                                                  summary=('2.) Return the summary with aggregated '
                                                           'total_inflow and total_outflows per user'))])],
    'examples': [OpenApiExample('1.) List all financial transactions records',
                                value={"reference": "000001",
                                       "date": "2023-05-27",
                                       "amount": "-51.13",
                                       "type": "outflow",
                                       "category": "groceries",
                                       "user_email": "janedoe@email.com"}),
                 OpenApiExample('2.) Return the summary with aggregated total_inflow and total_outflows per user',
                                value={"user_email": "janedoe@email.com",
                                       "total_inflow": "3254.32",
                                       "total_outflow": "-761.85"})]}

create_transactions_schema = {
    'examples': [OpenApiExample('1.) Create single financial transaction records',
                                value={"reference": "000001",
                                       "date": "2023-05-27",
                                       "amount": "-51.13",
                                       "type": "outflow",
                                       "category": "groceries",
                                       "user_email": "janedoe@email.com"}),
                 OpenApiExample('2.) Create multiple financial transactions records in bulk operation',
                                value=[{"reference": "000003",
                                        "date": "2020-01-10",
                                        "amount": "-150.72",
                                        "type": "outflow",
                                        "category": "transfer",
                                        "user_email": "janedoe@email.com"},
                                       {"reference": "000004",
                                        "date": "2020-01-13",
                                        "amount": "-560.00",
                                        "type": "outflow",
                                        "category": "rent",
                                        "user_email": "janedoe@email.com"}])]}
