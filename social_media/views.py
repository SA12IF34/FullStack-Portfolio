from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.middleware.csrf import rotate_token

# Let's Get Started

class CsrfTokenAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        rotate_token(request)

        return Response(status=HTTP_200_OK)



# Authentication System

class RegisterAPI(APIView): 

    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]
    
    def post(self, request):

        data = request.data

        if not User.objects.filter(email=data['email']).exists():
            if not User.objects.filter(username=data['username']).exists():
                user = User.objects.create_user(
                    username=data['username'], 
                    email=data['email'], 
                    password=data['password'], 
                    first_name=data['first_name'], 
                    last_name=data['last_name']
                )

                account_data = { 
                    "user": user.id, 
                    "username": user.username, 
                    "email": user.email,
                    "fname": user.first_name,
                    "lname": user.last_name
                }
                if 'img' in data.keys():
                    account_data['profile_img'] = data['img']

                account = AccountSerializer(data=account_data)
                

                if account.is_valid(raise_exception=True):
                    account.save()
                    
                    follow = FollowSerializer(data={
                    "name": user.username, 
                    "fname": user.first_name,
                    "lname": user.last_name, 
                    "profile_img": account.data['profile_img'],
                    "user": user.id
                    })
                    
                    if follow.is_valid():
                        follow.save()
                    
                    
                        login(request, user)
                            
                        return Response(data=account.data, status=HTTP_201_CREATED)
                    
                    return Response(follow.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)

                return Response(account.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)
            else :
                return Response(data={'response': 'username'}, status=HTTP_400_BAD_REQUEST)
        else :

            return Response(data={"response": "email"}, status=HTTP_400_BAD_REQUEST)
        
class AuthenticationAPI(APIView):

    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        data = request.data
        user = authenticate(username=data['username'], email=data['email'], password=data['password'])
        if user is not None:
            login(request, user)

            return Response(data={"account": user.username}, status=HTTP_202_ACCEPTED)

        return Response(data={"response": "user not found"}, status=HTTP_404_NOT_FOUND)
    
class LogOutAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        logout(request=request)

        return Response(status=HTTP_202_ACCEPTED)

class CloseAPI(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        user = request.user
        logout(request)
        user.delete()

        return Response(status=HTTP_204_NO_CONTENT)




# Accounts and Following System  

class AccountsAPI(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        
        accounts = Account.objects.all()
        serializer = AccountSerializer(instance=accounts, many=True)

        return Response(data=serializer.data, status=HTTP_200_OK)


class AccountAPI(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]

    def get(self, request, id=False):
        if id:
            try:
                user = Account.objects.get(id=id).user
                
            except Account.DoesNotExist:
                user = User.objects.get(id=id)
                
            

            serializer = AccountSerializer(instance=user.account)
            serializer2 = FollowSerializer(instance=user.follow)
            data = serializer.data
            
            followers = Follow.objects.filter(id__in=serializer.data['followers'])
            followings = Account.objects.filter(id__in=serializer2.data['follow_accounts'])
            followers_serializer = FollowSerializer(instance=followers, many=True)
            followings_serializer = AccountSerializer(instance=followings, many=True)
            
            data['email'] = ''
            data['followings'] = followings_serializer.data
            data['followers'] = followers_serializer.data
            return Response(data=data, status=HTTP_200_OK)
        else:
            user = request.user
            if user.is_authenticated:
                serializer = AccountSerializer(instance=user.account)
                serializer2 = FollowSerializer(instance=user.follow)
                data = serializer.data
                data['followings'] = serializer2.data['follow_accounts']
                return Response(data=data, status=HTTP_200_OK)
        
        return Response(status=HTTP_403_FORBIDDEN)

    def patch(self, request):
        user = request.user
        if 'profile_img' in request.data.keys():
            user.account.profile_img.delete(save=True)
            serializer = AccountSerializer(instance=user.account, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=HTTP_202_ACCEPTED)
        if 'password' in request.data.keys():
            user.set_password(request.data['password'])
            user.save()

            del request.data['password']


        if len(request.data) > 0:
            serializer = UserSerializer(instance=user, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                login(request, serializer.instance)

                if ('username' in request.data.keys() or 'email' in request.data.keys()):
                    if 'username' in request.data.keys() and not 'email' in request.data.keys():
                        data = {
                            'name': request.data['username']
                        }
                        
                        serializer2 = FollowSerializer(instance=user.follow, data=data, partial=True)
                        try:
                            if serializer2.is_valid(raise_exception=True):
                                serializer2.save()
                        except:
                            return Response(serializer2.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)
                    elif not 'username' in request.data.keys() and 'email' in request.data.keys():
                        data = {
                            'email': request.data['email']
                        }
                    
                    else :
                        data = {
                            'name': request.data['username'],
                            'email': request.data['email']
                        }
                    serializer3 = AccountSerializer(instance=user.account, data=data, partial=True)
                    try:
                        if serializer3.is_valid(raise_exception=True):
                            serializer3.save()
                            return Response(data=serializer3.data, status=HTTP_202_ACCEPTED)
                    except:
                        return Response(serializer3.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(status=HTTP_400_BAD_REQUEST)
        
                    
        login(request, user)
        return Response(status=HTTP_202_ACCEPTED)
        

class SearchAPI(APIView):

    def get(self, request, term):
        accounts = Account.objects.filter(username__contains=term)
        serializer = AccountSerializer(instance=accounts, many=True)

        return Response(data=serializer.data, status=HTTP_200_OK)

class FollowersAPI(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        user = request.user
        account = user.account
        serializer = AccountSerializer(instance=account)
        followers = Follow.objects.filter(id__in=serializer.data['followers'])
        serializer2 = FollowSerializer(instance=followers, many=True)

        return Response(data=serializer2.data)




class FollowsAPI(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        user = request.user

        follow = user.follow
        follows = FollowSerializer(instance=follow).data['follow_accounts']
        accounts = Account.objects.filter(id__in=follows)

        serializer = AccountSerializer(instance=accounts, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)

    def post(self, request):
        user = request.user
        target_account = Account.objects.get(user=request.data['target'])
        try:
            follow = user.follow

        except ObjectDoesNotExist:
            serializer = FollowSerializer(data={"name": user.username, "user": user.id})
            if serializer.is_valid():
                serializer.save()
                follow = serializer.instance
        
        serializer2 = AccountSerializer(instance=target_account)
        if follow not in serializer2.data['followers']:
            follow.follow_accounts.add(target_account)
            target_account.followers.add(follow)
            target_account.followers_number += 1
            
            follow.save()
            target_account.save()

            return Response(status=HTTP_202_ACCEPTED)
        else :
            return Response(status=HTTP_208_ALREADY_REPORTED)



class UnfollowAPI(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        try:
            user = request.user
            follow = user.follow
            target_account = Account.objects.get(user=request.data['target'])
            
            follow.follow_accounts.remove(target_account)
            target_account.followers.remove(follow)
            target_account.followers_number -= 1

            follow.save()
            target_account.save()

            return Response(status=HTTP_202_ACCEPTED)
        except:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)




# Posting System 

class PostsAPI(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]

    def get(self, request, author=False, type=False, start=False, end=False):
        if type == 'latest':
            posts = Post.objects.all().order_by('-creation_date')   
        
        elif type == 'foryou':
            follow = request.user.follow
            follow_serializer = FollowSerializer(instance=follow)
            posts = Post.objects.filter(author__in=follow_serializer.data['follow_accounts']).order_by('-creation_date')   
       
        elif author:
            posts = Post.objects.filter(author=author).order_by('-creation_date')
            
        else:
            account = request.user.account
            posts = Post.objects.filter(author=account).order_by('-creation_date')
        
        serializer = PostSerializer(instance=posts, many=True)

        return Response(data=serializer.data, status=HTTP_200_OK)

    def post(self, request):
        
        account = request.user.account
        data = {
            "content": request.data['content'],
            "edit_content": request.data['edit_content'],
            "author": account.id,
            
        }
        if 'file' in request.data.keys():
            data['file'] = request.data['file']
        
        serializer = PostSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=HTTP_201_CREATED)
        
        return Response(serializer.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)
        

class PostAPI(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]

    def get(self, request, id):
        post = Post.objects.get(post_id=id)
        likes = post.like_set
        dislikes = post.dislike_set
        serializer = PostSerializer(instance=post)
        data = serializer.data
        data['likes'] = likes.count()
        data['dislikes'] = dislikes.count()
        data['liked'] = False
        data['disliked'] = False

        account = request.user.account
        try:
            like =account.like_set.get(post=post)
            if like :
                data['liked'] = True

        except ObjectDoesNotExist:
            try:
                dislike = account.dislike_set.get(post=post)
                if dislike :
                    data['disliked'] = True
            except:
                pass

        return Response(data=data, status=HTTP_200_OK)


    def delete(self, request, id):
        post = Post.objects.get(post_id=id)
        if post.file:
            post.file.delete(save=True)

        post.delete()

        return Response(status=HTTP_202_ACCEPTED)

class PostEditAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        account = request.user.account
        post = Post.objects.get(post_id=id)
        if post.author != account:
            return Response(status=HTTP_403_FORBIDDEN)
        
        serializer = PostSerializer(instance=post)

        return Response(data=serializer.data, status=HTTP_200_OK)

    def patch(self, request, id):
        account = request.user.account
        post = Post.objects.get(post_id=id)
        if post.author.id != account.id:
            return Response(status=HTTP_403_FORBIDDEN)
        serializer = PostSerializer(instance=post, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(status=HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)

# Likes System

class LikeAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def post(self, request, id):

        account = request.user.account
        post = Post.objects.get(post_id=id)
        try: 
            like_obj = Like.objects.get(post=post, account=account)
            like_obj.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            pass
        try:
            dislike_obj = Dislike.objects.get(post=post, account=account)
            dislike_obj.delete()
        except Dislike.DoesNotExist:
            pass

        like_obj = Like(post=post, account=account)
        like_obj.save()

        return Response(status=HTTP_202_ACCEPTED)


class DislikeAPI(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def post(self, request, id):

        account = request.user.account
        post = Post.objects.get(post_id=id)
        try:
            dislike_obj = Dislike.objects.get(post=post, account=account)
            dislike_obj.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except Dislike.DoesNotExist:
            pass
        try:
            like_obj = Like.objects.get(post=post, account=account)
            like_obj.delete()
        except Like.DoesNotExist:
            pass
        
        dislike_obj = Dislike(post=post, account=account)
        dislike_obj.save()
        
        return Response(status=HTTP_202_ACCEPTED)



# Commenting System

class CommentsAPI(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]

    def get(self, request, post):
        post = Post.objects.get(post_id=post)
        comments = post.comment_set.all()
        serializer = CommentSerializer(instance=comments, many=True)

        return Response(data=serializer.data, status=HTTP_200_OK)

    def post(self, request, post):
        post = Post.objects.get(post_id=post)
        data = {
            "content": request.data['content'],
            'post': post.post_id,
            'author': request.user.username
        }
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=HTTP_201_CREATED)


class CommentAPI(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def delete(self, request, pk):
        comment = Comment.objects.get(id=pk)
        comment.delete()

        return Response(status=HTTP_204_NO_CONTENT)




