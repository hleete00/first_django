from django.urls import path



# Import any views you plan on using from the views.py file 
from .views import home_view, SaleListView, SaleDetailView

app_name = 'sales'

urlpatterns = [
    # If url is blank, call home_view method in sales/views.py
    path('', home_view, name='home'),
    # If url is ./list/, then call the SaleListView class view in sales/views.py
    path('list/', SaleListView.as_view(), name='list'),
    # If url is .sales/<Primary Key of Sales record>, call the SaleDetailView class view in sales/views.py
    path('sales/<pk>/', SaleDetailView.as_view(), name='detail')
]