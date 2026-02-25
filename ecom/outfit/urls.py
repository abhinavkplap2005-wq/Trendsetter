from django.urls import path
from .import views

urlpatterns = [
    path ('',views.home,name="home"),
    path('login/',views.login_view,name="login"),
    path('register/',views.register_view,name="register"),
    path('logout/',views.logout_view,name="logout"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path("products/", views.products, name="products"),
    path('category/', views.category, name='category'),
    path('cloth/<int:id>/', views.cloth_detail, name='cloth_detail'),
    path('my-orders/', views.my_orders, name='my_orders'),
]
