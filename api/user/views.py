from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import UserService
from .models import User

# Create your views here.

class UserRegistrationView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        operation_description="Create a new user",
        responses={
            201: UserSerializer,
            400: "Bad Request"
        }
    )
    def post(self, request):
        """
        Create a new user with the provided data.
        
        Parameters:
            - login: username for the new user
            - password: user's password
            - first_name: user's first name
            - last_name: user's last name
        
        Returns:
            - 201: Successfully created user data
            - 400: Bad request with error details
        """
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Create User instance from validated data
                user_data = User(**serializer.validated_data)
                user = UserService.create_user(user_data)
                # Serialize the User instance for response
                response_serializer = UserSerializer(user)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                    
            except Exception as e:
                return Response({
                    'error': 'Database error occurred',
                    'detail': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    @swagger_auto_schema(
        operation_description="Get list of all users",
        responses={
            200: UserSerializer(many=True)
        }
    )
    def get(self, request):
        """
        Retrieve a list of all users.
        
        Returns:
            - 200: List of users with their details (excluding passwords)
        """
        users = UserService.get_all_users()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
