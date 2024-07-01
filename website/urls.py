from django.urls import path
from . import views
from . import views_dwms

urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    ###########################################
    path('producto/', views_dwms.producto, name='producto'),
    path('add_producto/', views_dwms.add_producto, name='add_producto'),
    path('DWMScodigoBarra/', views_dwms.DWMScodigoBarra, name='DWMScodigoBarra'),
    #path('DWMS_add_codigoBarra/', views_dwms.DWMS_add_codigoBarra, name='DWMS_add_codigoBarra'),
]
