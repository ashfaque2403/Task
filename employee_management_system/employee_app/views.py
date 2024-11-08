from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import Profile, Employee, CustomField
from .serializers import EmployeeSerializer

# Home page
def index(request):
    return render(request, 'index.html')

# Login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

# Registration view
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, 'Registration successful')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'register.html')

# Change password view
@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if request.user.check_password(current_password):
            if new_password == confirm_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully')
                return redirect('profile')
            else:
                messages.error(request, 'New passwords do not match')
        else:
            messages.error(request, 'Incorrect current password')
    return render(request, 'change_password.html')

# Profile view
@login_required
def profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.name = name
        profile.phone = phone
        profile.address = address
        profile.save()
        messages.success(request, 'Profile updated successfully')
    return render(request, 'profile.html', {'profile': request.user.profile})

# Create employee view
@login_required
def create_employees(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        position = request.POST.get('position')
        
        if name and email and position:
            employee = Employee.objects.create(name=name, email=email, position=position)
            messages.success(request, f"Employee {employee.name} created successfully.")
            return redirect('employee_details', employee_id=employee.id)
        else:
            messages.error(request, "All fields are required.")
    
    return render(request, 'create_employee.html')

# Employee list view
@login_required
def employee_lists(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

# Employee detail view
@login_required
def employee_details(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'employee_detail.html', {'employee': employee})

# Add custom field view
@login_required
def add_custom_field(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        field_name = request.POST.get('field_name')
        field_value = request.POST.get('field_value')
        
        if field_name and field_value:
            # Add or update custom field
            custom_field, created = CustomField.objects.update_or_create(
                employee=employee, field_name=field_name,
                defaults={'field_value': field_value}
            )
            if created:
                messages.success(request, f"Custom field '{field_name}' added.")
            else:
                messages.success(request, f"Custom field '{field_name}' updated.")
            return redirect('employee_details', employee_id=employee.id)
        else:
            messages.error(request, "Field name and value are required.")
    
    return render(request, 'add_custom_field.html', {'employee': employee})

# Logout view
def logout_view(request):
    logout(request)
    return redirect(index)
from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Employee API viewset for CRUD operations
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def perform_create(self, serializer):
        serializer.save()

# Login view for JWT authentication
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Refresh token view to get a new access token using a refresh token
@api_view(['POST'])
def refresh_token_view(request):
    refresh = request.data.get('refresh')
    try:
        token = RefreshToken(refresh)
        return Response({'access': str(token.access_token)})
    except Exception:
        return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

# API endpoint to list all employees
@api_view(['GET'])
def employee_list(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)

# API endpoint to get details of a specific employee
@api_view(['GET'])
def employee_detail(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = EmployeeSerializer(employee)
    return Response(serializer.data)

# API endpoint to create a new employee
@api_view(['POST'])
def create_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
