from django.db import connection
from django.utils import timezone
from typing import Dict, Optional, Any
from .logger import logger

class UserV2Service:
    @staticmethod
    def create_user(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new user with the provided data"""
        logger.debug("Creating new user with data: %s", data)
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO user (
                        login, password_sha256, first_name, last_name, 
                        created_at, changed_at, created_from, changed_from,
                        strBool, isActive
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    RETURNING id, login, first_name, last_name, created_at, isActive, strBool
                """, [
                    data['login'],
                    data['password_sha256'],
                    data['first_name'],
                    data['last_name'],
                    timezone.now(),  # created_at
                    timezone.now(),  # changed_at
                    data['created_from'],
                    data['created_from'],  # Initial changed_from same as created_from
                    data.get('str_bool'),  # Optional field
                    True  # isActive
                ])
                
                row = cursor.fetchone()
                if not row:
                    logger.error("Failed to create user: No row returned")
                    return None

                return {
                    'id': row[0],
                    'login': row[1],
                    'first_name': row[2],
                    'last_name': row[3],
                    'created_at': row[4],
                    'is_active': row[5],
                    'str_bool': row[6]
                }
                
        except Exception as e:
            logger.fatal("Fatal error creating user: %s", str(e), exc_info=True)
            raise

    @staticmethod
    def get_user(user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        logger.debug("Fetching user with ID: %s", user_id)
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, login, first_name, last_name, created_at, isActive, strBool 
                    FROM user 
                    WHERE id = %s AND isActive = 1
                """, [user_id])
                row = cursor.fetchone()
                
                if not row:
                    logger.info("No active user found with ID: %s", user_id)
                    return None

                return {
                    'id': row[0],
                    'login': row[1],
                    'first_name': row[2],
                    'last_name': row[3],
                    'created_at': row[4],
                    'is_active': row[5],
                    'str_bool': row[6]
                }
                
        except Exception as e:
            logger.fatal("Fatal error fetching user: %s", str(e), exc_info=True)
            raise

    @staticmethod
    def update_user(user_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user with the provided data"""
        logger.debug("Updating user %s with data: %s", user_id, data)
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE user 
                    SET login = %s,
                        password_sha256 = %s,
                        first_name = %s,
                        last_name = %s,
                        strBool = %s,
                        changed_at = %s,
                        changed_from = %s
                    WHERE id = %s AND isActive = 1
                    RETURNING id, login, first_name, last_name, created_at, isActive, strBool
                """, [
                    data['login'],
                    data['password_sha256'],
                    data['first_name'],
                    data['last_name'],
                    data.get('str_bool'),
                    timezone.now(),
                    data['changed_from'],
                    user_id
                ])
                
                row = cursor.fetchone()
                if not row:
                    logger.info("No user found to update with ID: %s", user_id)
                    return None

                return {
                    'id': row[0],
                    'login': row[1],
                    'first_name': row[2],
                    'last_name': row[3],
                    'created_at': row[4],
                    'is_active': row[5],
                    'str_bool': row[6]
                }
                
        except Exception as e:
            logger.fatal("Fatal error updating user: %s", str(e), exc_info=True)
            raise

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """delete a user from the database"""
        logger.debug("deleting user %s", user_id)
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM user 
                    WHERE id = %s
                """, [user_id])
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.fatal("Fatal error deleting user: %s", str(e), exc_info=True)
            raise 