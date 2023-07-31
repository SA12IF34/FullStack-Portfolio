from django.db import models
from django.contrib.auth.models import User



class Cart(models.Model):
    
    perfume_name = models.CharField(max_length=200)
    perfume_company = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.perfume_name + " | " + self.user.username
    
    class Meta:
        ordering = ['perfume_name']

class Buy(models.Model):
    
    perfume_name = models.CharField(max_length=200)
    perfume_company = models.CharField(max_length=200)
    perfume_cost = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.perfume_name + " | " + self.user.username
    
    class Meta:
        ordering = ['perfume_name']