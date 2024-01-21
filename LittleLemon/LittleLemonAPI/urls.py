from django.urls import path
from . import views

urlpatterns = [
    path('api/menu-items/',views.MenuItemsView.as_view(),name = 'menu-items'),
    path('api/menu-items/<int:pk>/',views.SingleMenuItemsView.as_view(),name = 'single-menu-items'),
    path('api/groups/<str:group_name>/users/', views.GroupUserApiView.as_view(), name='group-user-list'),
    path('api/groups/<str:group_name>/users/<int:user_id>/', views.RemoveUserFromGroup.as_view(), name='remove-user-from-group'),
    path('api/cart/menu-items', views.CartView.as_view(), name='Cart'),
    path('api/orders',views.OrderView.as_view(),name='order_view'),
    path('api/orders/<int:pk>/',views.SingleOrderView.as_view(),name='single_order_view'),
#    path('api/orders/<int:pk>/',views.DeleteSingleOrderView.as_view(),name='delete_single_order_view'),
]