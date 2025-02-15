from django.db import connection
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from typing import List, Optional
from .models import User

class UserService:
    @staticmethod
    def create_user(user_data: dict) -> User:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO user (
                    login, password, first_name, last_name, 
                    createdAt, isActive, testBool
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id, login, first_name, last_name, createdAt, isActive, testBool
            """, [
                user_data['login'],
                user_data['password'],
                user_data['first_name'],
                user_data['last_name'],
                timezone.now(),
                user_data.get('is_active', True),
                user_data.get('test_bool')
            ])
            return UserService._create_user_from_row(cursor.fetchone())

    @staticmethod
    def get_user(user_id: int) -> Optional[User]:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, login, first_name, last_name, createdAt, isActive, testBool 
                FROM user WHERE id = %s AND isActive = 1
            """, [user_id])
            row = cursor.fetchone()
            return UserService._create_user_from_row(row) if row else None

    @staticmethod
    def get_all_users() -> List[User]:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, login, first_name, last_name, createdAt, isActive, testBool 
                FROM user WHERE isActive = 1
            """)
            return [UserService._create_user_from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def update_user(user_id: int, user_data: dict) -> Optional[User]:
        fields = []
        values = []
        for key, value in user_data.items():
            if key in ['login', 'password', 'first_name', 'last_name', 'test_bool']:
                fields.append(f"{key if key != 'test_bool' else 'testBool'} = %s")
                values.append(value)

        if not fields:
            return None

        with connection.cursor() as cursor:
            values.append(user_id)
            cursor.execute(f"""
                UPDATE user 
                SET {', '.join(fields)}
                WHERE id = %s AND isActive = 1
                RETURNING id, login, first_name, last_name, createdAt, isActive, testBool
            """, values)
            row = cursor.fetchone()
            return UserService._create_user_from_row(row) if row else None

    @staticmethod
    def delete_user(user_id: int) -> bool:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE user 
                SET isActive = 0 
                WHERE id = %s AND isActive = 1
            """, [user_id])
            return cursor.rowcount > 0

    @staticmethod
    def _create_user_from_row(row) -> User:
        return User(
            id=row[0],
            login=row[1],
            first_name=row[2],
            last_name=row[3],
            created_at=row[4],
            is_active=row[5],
            test_bool=row[6]
        ) 