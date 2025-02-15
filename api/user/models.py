# This file can be empty since we're using raw SQL queries

from django.db import models

class User(models.Model):
    # Required fields (NOT NULL in database)
    login = models.EmailField(max_length=100, null=False)
    password = models.CharField(max_length=64, null=False)  # SHA256
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True, db_column='createdAt', null=False)
    is_active = models.BooleanField(default=True, db_column='isActive', null=False)
    
    # Optional field (can be NULL in database)
    test_bool = models.BooleanField(null=True, db_column='testBool')

    class Meta:
        managed = False
        db_table = 'user'
