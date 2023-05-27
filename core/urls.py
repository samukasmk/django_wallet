"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from apps.wallet.viewsets import (FinancialTransactionsViewSet,
                                  FinancialTransactionViewSet)

# wallet routes
router_many_transactions = routers.DefaultRouter(trailing_slash=False)
router_many_transactions.register(r'transactions', FinancialTransactionsViewSet)

router_each_transaction = routers.DefaultRouter(trailing_slash=False)
router_each_transaction.register(r'transaction', FinancialTransactionViewSet)

urlpatterns = [
    # Redirection from / to /api/docs
    path(r'', RedirectView.as_view(url='/api/docs')),

    # API docs by swagger
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Inclusion of rest framework viewsets
    path('', include(router_many_transactions.urls)),
    path('', include(router_each_transaction.urls)),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
