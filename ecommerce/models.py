from django.db import models;
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

class EmailorUsernameModelBackend(ModelBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
    

class Cart(models.Model):

    product_name = models.CharField(max_length=200, blank=False, null=False)
    price = models.IntegerField()
    image = models.TextField()
    account = models.ForeignKey(User, on_delete=models.CASCADE)

    

class Bought(models.Model):

    product_name = models.CharField(max_length=200)
    image = models.TextField()
    account = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):

        return f'{self.product_name} | {self.account.username}'