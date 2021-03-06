from django.urls import path, re_path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings

app_name = 'food'

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('<int:pk>/', views.shop_detail, name='shop_detail'),
    path('<int:shop_pk>/oreder/new/', views.order_new, name='order_new'),
    re_path(r'^(?P<shop_pk>\d+)/order/(?P<merchant_uid>[\da-f\-]{36})/pay/$', views.order_pay, name='order_pay'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGIN_REDIRECT_URL), name='logout'),
    path('profile/', views.profile, name='profile'),
]
