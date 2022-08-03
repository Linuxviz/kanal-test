from django.urls import path

from deal.views import DealListView

urlpatterns = [
    path('deals/', DealListView.as_view(), name='deals'),
]
