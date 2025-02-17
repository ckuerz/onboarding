from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from django.utils import timezone
from .serializers import UserV2Serializer
from .services import UserV2Service
from .logger import logger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

@swagger_auto_schema(
    method='post',
    request_body=UserV2Serializer,
    request_body_properties={
        'str_bool': openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description='Boolean value that will be stored as yes/no'
        )
    },
    operation_description="Create a new user",
    responses={
        201: openapi.Response(
            description="User created successfully",
            schema=UserV2Serializer
        ),
        400: openapi.Response(
            description="Bad Request"
        ),
        500: openapi.Response(
            description="Internal Server Error"
        )
    }
)
@api_view(['POST'])
def create_user(request):
    """Create a new user"""
    try:
        serializer = UserV2Serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = UserV2Service.create_user(serializer.validated_data)
                if user:
                    return Response(user, status=status.HTTP_201_CREATED)
                return Response(
                    {'error': 'Failed to create user'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                logger.error("Error in create_user view: %s", str(e), exc_info=True)
                return Response(
                    {'error': 'Internal server error'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error("Unexpected error in create_user view: %s", str(e), exc_info=True)
        return Response(
            {'error': 'Internal server error'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@swagger_auto_schema(
    method='get',
    operation_description="Get user details",
    responses={
        200: UserV2Serializer,
        404: openapi.Response(
            description="User not found"
        ),
        500: openapi.Response(
            description="Internal Server Error"
        )
    }
)
@swagger_auto_schema(
    method='patch',
    request_body=UserV2Serializer(partial=True),
    operation_description="Partially update user",
    responses={
        200: UserV2Serializer,
        400: openapi.Response(
            description="Bad Request",
            examples={"application/json": {"error": "No valid fields to update"}}
        ),
        404: openapi.Response(
            description="User not found",
            examples={"application/json": {"error": "User not found"}}
        )
    }
)
@swagger_auto_schema(
    method='delete',
    operation_description="Delete user",
    responses={
        204: openapi.Response(description="User deleted successfully"),
        404: openapi.Response(
            description="User not found",
            examples={"application/json": {"error": "User not found"}}
        )
    }
)
@api_view(['GET', 'PATCH', 'DELETE'])
def user_detail(request, user_id):
    """Handle GET, PATCH, and DELETE requests for a user"""
    try:
        # First check if user exists
        user = UserV2Service.get_user(user_id)
        if not user:
            logger.info("User not found: %s", user_id)
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        if request.method == 'GET':
            serializer = UserV2Serializer(user)
            return Response(serializer.data)

        elif request.method == 'DELETE':
            if UserV2Service.delete_user(user_id):
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': 'Failed to delete user'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        elif request.method == 'PATCH':
            # Get current user data first
            current_user = UserV2Service.get_user(user_id)
            serializer = UserV2Serializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(
                    serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Merge current data with updates
            update_data = current_user.copy()
            update_data.update(serializer.validated_data)
            
            updated_user = UserV2Service.update_user(user_id, update_data)
            if updated_user:
                return Response(updated_user)
            return Response(
                {'error': 'Failed to update user'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        logger.error("Error in user_detail view: %s", str(e), exc_info=True)
        return Response(
            {'error': 'Internal server error'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
