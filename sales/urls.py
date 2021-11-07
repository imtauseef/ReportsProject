from django.urls import path
from .views import home_view, SalesListView, SalesDetailView

app_name = 'sales'

urlpatterns = [
    path('', home_view, name='home'),
    path('sales', SalesListView.as_view(), name='saleslist'),
    path('sales/<pk>/', SalesDetailView.as_view(), name='salesdetail'),
]
