from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

def account_img(self, filename):
    return 'accounts/{name}/{filename}'.format(name=self.username, filename=filename)

class Account(models.Model):
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    email = models.EmailField() 
    profile_img = models.FileField(upload_to=account_img, blank=True, null=True)
    followers_number = models.IntegerField(default=0)
    followers = models.ManyToManyField('Follow', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self): 
        return self.username

class Follow(models.Model):
    name = models.CharField(max_length=200)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    profile_img = models.CharField(max_length=5000, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follow_accounts = models.ManyToManyField(Account, blank=True)
 
    def __str__(self):
        return self.name


def upload_to(self, filename):
    return 'posts/{id}/{filename}'.format(id=len(Post.objects.all())+1, name=self.author.username, filename=filename)

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    content = models.TextField()
    edit_content = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    file = models.FileField(upload_to=upload_to, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return 'post of '+self.author.username

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return 'comment of ' + self.author

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.account.username} | post {self.post.post_id}'

class Dislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.account.username} | post {self.post.post_id}'