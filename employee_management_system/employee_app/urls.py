from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Router for Employee API CRUD
router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('change_password/', views.change_password, name='change_password'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),

    # Employee Management URLs
    path('employee/create/', views.create_employees, name='create_employees'),
    path('employee/<int:employee_id>/', views.employee_details, name='employee_details'),
    path('employee/<int:employee_id>/add_field/', views.add_custom_field, name='add_custom_field'),
    path('employee/list/', views.employee_lists, name='employee_lists'),

    # JWT Authentication URLs
    path('api/token/', views.login_view, name='login_api'),
    path('api/token/refresh/', views.refresh_token_view, name='refresh_token_api'),

    path('api/employees/create/', views.create_employee, name='create_employee'),

    path('api/employees/', views.employee_list, name='employee_list'),

    # URL to get details of a specific employee
    path('api/employees/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    # Include the API router for Employee endpoints
    path('api/', include(router.urls)),
]
