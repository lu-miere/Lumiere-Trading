from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
from core.security import hash_password


class UserManager(BaseUserManager):
    use_in_migrations= True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Must be an email')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        hashPassword = hash_password(password)
        user.set_password(hashPassword)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,password, **extra_fields)
    
    def create_staff_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("is_staff is not set to True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser is not set to True')
        
        return self._create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    id = models.UUIDField(primary_key= True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True, null = False, blank = False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20, blank=True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    has_news_sub = models.BooleanField(default=False)
    news_sub_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    news_sub_exp = models.DateTimeField()
    has_trading_sub = models.BooleanField(default=False)
    trading_sub_exp = models.DateTimeField()
    trader_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_has_news_sub(self):
        return self.has_news_sub
    
    def get_news_uuid(self):
        return self.news_sub_uid
    
    def get_has_trading_sub(self):
        return self.has_trading_sub
    
    def get_trading_uuid(self):
        return self.trading_uuid
    
    def is_news_sub_active():
        pass
    
    def is_trading_sub_axtive():
        pass
    
   


