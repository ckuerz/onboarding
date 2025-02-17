from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from django.contrib.auth.hashers import make_password
from .serializers import UserReadSerializer, UserCreateSerializer, UserUpdateSerializer
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import UserService
from .models import User

# Create your views here.

class UserListView(APIView):
    @swagger_auto_schema(
        operation_description="List all active users",
        responses={200: UserReadSerializer(many=True)}
    )
    def get(self, request):
        """List all active users"""
        try:
            users = UserService.get_all_users()
            return Response(UserReadSerializer(users, many=True).data)
        except Exception as e:
            return Response(
                {'error': 'Database error', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        request_body=UserCreateSerializer,
        operation_description="Create a new user",
        responses={
            201: UserReadSerializer,
            400: openapi.Response(
                description="Bad Request",
                examples={"application/json": {"error": "Invalid input data"}}
            ),
            409: openapi.Response(
                description="Conflict",
                examples={"application/json": {"error": "User already exists"}}
            )
        }
    )
    def post(self, request):
        """Create a new user"""
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = UserService.create_user(serializer.validated_data)
            return Response(UserReadSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    @swagger_auto_schema(
        operation_description="Get a specific user by ID",
        responses={200: UserReadSerializer}
    )
    def get(self, request, user_id):
        """Get a specific user by ID"""
        try:
            user = UserService.get_user(user_id)
            if not user:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(UserReadSerializer(user).data)
        except Exception as e:
            return Response(
                {'error': 'Database error', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        operation_description="Full update of a user",
        manual_parameters=[
            openapi.Parameter(
                'user_id', openapi.IN_PATH,
                description="User ID",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: UserReadSerializer,
            400: "Invalid input data",
            404: "User not found"
        }
    )
    def put(self, request, user_id):
        """Full update of a user"""
        serializer = UserUpdateSerializer(data=request.data)
        if serializer.is_valid():
            user = UserService.update_user(user_id, serializer.validated_data)
            if not user:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(UserReadSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=UserReadSerializer,
        operation_description="Partial update of a user",
        manual_parameters=[
            openapi.Parameter(
                'user_id', openapi.IN_PATH,
                description="User ID",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: UserReadSerializer,
            400: "Invalid input data",
            404: "User not found"
        }
    )
    def patch(self, request, user_id):
        """Partial update of a user"""
        serializer = UserReadSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid input data', 'detail': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = UserService.update_user(user_id, serializer.validated_data)
            if not user:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(UserReadSerializer(user).data)
        except Exception as e:
            return Response(
                {'error': 'Database error', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description="Delete a user",
        manual_parameters=[
            openapi.Parameter(
                'user_id', openapi.IN_PATH,
                description="User ID",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            204: "Successfully deleted",
            404: "User not found"
        }
    )
    def delete(self, request, user_id):
        """Delete a user"""
        try:
            if UserService.delete_user(user_id):
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': 'Database error', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
