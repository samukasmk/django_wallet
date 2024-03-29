from django.db import models
from django.db.models import Q, Sum


class FinancialTransactionManager(models.Manager):
    def summarize_all_transactions_by_user_email(self):
        """
        Aggregate total inflow and outflow by user email for all users
        SQL Query:
            SELECT user_email, COALESCE(
                                   SUM(amount) FILTER (WHERE type = 'inflow'),
                                   0.0
                               ) AS "total_inflow",
                               COALESCE(
                                   SUM(amount) FILTER (WHERE type = 'outflow'),
                                   0.0
                               ) AS "total_outflow"
            FROM wallet_financialtransaction
            GROUP BY user_email
        """
        return self.values(
            'user_email').annotate(total_inflow=Sum('amount',
                                                    filter=Q(type='inflow'),
                                                    default=0.0),
                                   total_outflow=Sum('amount',
                                                     filter=Q(type='outflow'),
                                                     default=0.0))

    def summarize_user_transactions_by_category(self, user_email: str):
        """
        Aggregate total inflow and outflow by categories for a specific user
        SQL Query:
            SELECT type, category, SUM(amount) as total
            FROM wallet_financialtransaction
            WHERE user_email = 'janedoe@email.com'
            GROUP BY type, category
        """
        return self.filter(
            user_email=user_email
        ).values('type', 'category').annotate(total=Sum('amount'))
