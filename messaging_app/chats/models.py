from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
import uuid

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone_number, role, password=None, **extra_fields):
        if not all([first_name, last_name, email]):
            return ValueError("This field may not be blank!")
        email = self.normalize_email(email)
        user = self.model(first_name, last_name, email, phone_number, role, **extra_fields)
        user.set_pasword(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, phone_number, role="admin", password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            return ValueError("Superuser must have is_staff set to True")
        if not extra_fields.get("is_superuser"):
            return ValueError("Superuser must have is_superuser set to True")
        
        return self.create_user(first_name, last_name, email, phone_number, role, password, **extra_fields)

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True, editable=False, max_length=36)
    username = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    role = models.CharField(max_length=6, default="user", choices=
                            [('guest', 'Guest'),
                            ('user', 'User'), 
                            ('admin', 'Admin')]
                            )

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.first_name:
            self.first_name=self.first_name.strip().title()
        if self.last_name:
            self.last_name=self.last_name.strip().title()
        if self.email:
            self.email=self.email.strip().lower()
        if self.phone_number:
            self.phone_number=self.phone_number.strip()
        super().save(*args, **kwargs)

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.message_body:
            self.message_body.strip()
        super().save(*args, **kwargs)

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='conversation')
    participants = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now=True)

   
