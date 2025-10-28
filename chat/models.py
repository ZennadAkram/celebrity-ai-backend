from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    user_avatar = models.ImageField(upload_to='user_avatars/', null=True, blank=True)
    def __str__(self):
        return self.username

class Celebrity(models.Model):
    creator = models.ForeignKey(User, related_name='celebrities',null=True,on_delete=models.SET_NULL)
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=False,null=False)
    avatar=models.ImageField(upload_to='avatar/',null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    category=models.ForeignKey('Category',on_delete=models.SET_NULL,null=True,related_name='celebrities')
    is_Private=models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name=models.CharField(max_length=50,unique=True)
    description=models.TextField(blank=True,null=True)
    image=models.ImageField(upload_to='category_images/',null=True,blank=True)
    def __str__(self):
        return self.name

class ChatSession(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sessions')
    time_stamp=models.DateTimeField(auto_now_add=True)
    celebrity=models.ForeignKey(Celebrity,on_delete=models.CASCADE,related_name='sessions')

class Message(models.Model):
    session=models.ForeignKey(ChatSession,on_delete=models.CASCADE,related_name='messages')
    text=models.TextField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    sender=models.CharField(max_length=10,choices=[("user","User"),("ai","AI")])
