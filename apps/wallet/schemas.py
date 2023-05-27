from drf_spectacular.utils import OpenApiParameter, OpenApiExample

# Many transactions schema
list_many_transactions_schema = {
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
                                       "amount": "-77.77",
                                       "type": "outflow",
                                       "category": "candies",
                                       "user_email": "janedoe@email.com"}),
                 OpenApiExample('2.) Return the summary with aggregated total_inflow and total_outflows per user',
                                value={"user_email": "janedoe@email.com",
                                       "total_inflow": "3254.32",
                                       "total_outflow": "-761.85"})]}

create_many_transactions_schema = {
    'examples': [
        OpenApiExample('Create multiple financial transactions records in bulk operation',
                       value=[{"reference": "000051",
                               "date": "2020-01-03",
                               "amount": "-51.13",
                               "type": "outflow",
                               "category": "groceries",
                               "user_email": "janedoe@email.com"},
                              {"reference": "000052",
                               "date": "2020-01-10",
                               "amount": "2500.72",
                               "type": "inflow",
                               "category": "salary",
                               "user_email": "janedoe@email.com"},
                              {"reference": "000053",
                               "date": "2020-01-10",
                               "amount": "-150.72",
                               "type": "outflow",
                               "category": "transfer",
                               "user_email": "janedoe@email.com"},
                              {"reference": "000054",
                               "date": "2020-01-13",
                               "amount": "-560.00",
                               "type": "outflow",
                               "category": "rent",
                               "user_email": "janedoe@email.com"},
                              {"reference": "000055",
                               "date": "2020-01-04",
                               "amount": "-51.13",
                               "type": "outflow",
                               "category": "other",
                               "user_email": "johndoe@email.com"},
                              {"reference": "000689",
                               "date": "2020-01-10",
                               "amount": "150.72",
                               "type": "inflow",
                               "category": "savings",
                               "user_email": "janedoe@email.com"}]),
    ]}

summary_user_transactions_by_category_schema = {
    'examples': [OpenApiExample('janedoe@email.com',
                                value={"inflow": {"salary": "2500.72",
                                                  "savings": "150.72"},
                                       "outflow": {"groceries": "-51.13",
                                                   "rent": "-560.00",
                                                   "transfer": "-150.72"}}),
                 OpenApiExample('johndoe@email.com',
                                value={"inflow": {},
                                       "outflow": {"other": "-51.13"}})]}

# Single transactions schema
create_single_transaction_schema = {
    'examples': [
        OpenApiExample('Create an inflow transaction record',
                       value={"reference": "000001",
                              "date": "2023-05-27",
                              "amount": "38.00",
                              "type": "inflow",
                              "category": "investiment",
                              "user_email": "janedoe@email.com"}),
        OpenApiExample('Create an outflow transaction record',
                       value={"reference": "000002",
                              "date": "2023-05-27",
                              "amount": "-77.77",
                              "type": "outflow",
                              "category": "candies",
                              "user_email": "janedoe@email.com"})]}

retrieve_single_transaction_schema = {
    'examples': [
        OpenApiExample('Get an inflow transaction record',
                       value={"reference": "000001",
                              "date": "2023-05-27",
                              "amount": "38.00",
                              "type": "inflow",
                              "category": "investiment",
                              "user_email": "janedoe@email.com"}),
        OpenApiExample('Get an outflow transaction record',
                       value={"reference": "000002",
                              "date": "2023-05-27",
                              "amount": "-77.77",
                              "type": "outflow",
                              "category": "candies",
                              "user_email": "janedoe@email.com"})]}

update_single_transaction_schema = {
    'examples': [   
        OpenApiExample('Update an inflow transaction record',
                       value={"reference": "000001",
                              "date": "2023-05-27",
                              "amount": "1000000.10",
                              "type": "inflow",
                              "category": "investiment",
                              "user_email": "janedoe@email.com"}),
        OpenApiExample('Update an outflow transaction record',
                       value={"reference": "000002",
                              "date": "2023-05-27",
                              "amount": "-50000000.50",
                              "type": "outflow",
                              "category": "candies",
                              "user_email": "janedoe@email.com"})]}
