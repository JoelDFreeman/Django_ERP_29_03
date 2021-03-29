from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),
    path('upload/', views.upload, name="upload"),
    path('account/', views.accountSettings, name="account"),

    path('products/', views.products, name='products'),
    path('product_create/', views.product_create, name='product_create'),
    path('update_product/<str:pk>/', views.updateProduct, name="update_product"),
    path('delete_product/<str:pk>/', views.deleteProduct, name="delete_product"),
    
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('customers/', views.customers, name="customers"),
    path('update_customer/<str:pk>/', views.updateCustomer, name="update_customer"),
    path('customer_create/', views.customer_create, name='customer_create'),
    path('delete_customer/<str:pk>/', views.deleteCustomer, name="delete_customer"),

    path('orders/', views.Orders, name="orders"),
    path('order_create/', views.order_create, name='order_create'),


    path('tag_create/', views.tag_create, name='tag_create'),

    path('visualisations/', views.visualisations, name='visualisations'),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    path('create_address/', views.createAddress, name="create_address"),
    path('update_address/<str:pk>/', views.updateAddress, name="update_address"),
    path('delete_address/<str:pk>/', views.deleteAddress, name="delete_address"),

    path('export/',views.download_csv,name='export'),
    
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)