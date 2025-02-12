from django.db import connection
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from typing import List
from .models import User

class UserService:
    @staticmethod
    def create_user(user_data: User) -> User:
        """
        Create a new user in the database
        
        Args:
            user_data: User model instance with required fields
                      (login, password, first_name, last_name)
        
        Returns:
            User model instance with created data
        
        Raises:
            ValueError: If required fields are missing
            Exception: If database operation fails
        """
        required_fields = {
            field.name for field in User._meta.fields 
            if not field.auto_created and field.name != 'created_at'
        }
        
        if not all(hasattr(user_data, field) for field in required_fields):
            raise ValueError(f"Missing required fields. Required: {required_fields}")
            
        hashed_password = make_password(user_data.password)
        
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO user (login, password, first_name, last_name, created_at)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, login, first_name, last_name, created_at
            """, [
                user_data.login,
                hashed_password,
                user_data.first_name,
                user_data.last_name,
                timezone.now()
            ])
            
            row = cursor.fetchone()
            
            # Create User instance from DB data
            return User(
                id=row[0],
                login=row[1],
                first_name=row[2],
                last_name=row[3],
                created_at=row[4]
            )

    @staticmethod
    def get_all_users() -> List[User]:
        """
        Retrieve all users from the database
        
        Returns:
            List of User model instances
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, login, first_name, last_name, created_at 
                FROM user
            """)
            rows = cursor.fetchall()
            
            return [
                User(
                    id=row[0],
                    login=row[1],
                    first_name=row[2],
                    last_name=row[3],
                    created_at=row[4]
                ) for row in rows
            ] 