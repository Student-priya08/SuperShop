from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='products'),
    path('inventory/', views.inventory_list, name='inventory'),
    path('transactions/', views.transaction_list, name='transactions'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    
    # Category Management URLs
    path('categories/', views.categories_list, name='categories'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),
    
    # Unit Management URLs
    path('units/', views.units_list, name='units'),
    path('add_unit/', views.add_unit, name='add_unit'),
    path('edit_unit/<int:id>/', views.edit_unit, name='edit_unit'),
    path('delete_unit/<int:id>/', views.delete_unit, name='delete_unit'),
]