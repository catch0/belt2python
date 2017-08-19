from __future__ import unicode_literals
import bcrypt
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]*$')

class UserManager(models.Manager):
    def register(self, name, alias, email, password, password_confirmation, birthday):
        errors = {}
        if (len(name) < 2):
            errors['name'] = "could we please get your first name"

        if (len(alias) < 2):
            errors['alias'] = "get yourself an alias!!"

        if (len(password) < 8):
            errors['password'] = "we need a password please"

        if (password != password_confirmation):
            errors['password'] = "uh oh, the passwords don't match"
        #try:
        #    existingUser = self.get(email__iexact=email)
        #except:
         #   existingUser = None
        #if (existingUser):
         #   errors['email'] = 'That email is already registered'

        if (not EMAIL_REGEX.match(email)):
            errors['email'] = 'Invalid email.'

        if (birthday == None):
            error['birthday'] = 'we gotta be born to login!'
            
        if (errors):
            return (False, errors)
        else:
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            self.create(email=email, name=name, alias=alias, password=password, birthday=birthday)

            return (True, self.get(email=email))

    def login(self, email, password):
        try:
            user = self.get(email__iexact=email)
        except:
            user = None
        if user and bcrypt.hashpw(password.encode('utf-8'), user.password.encode('utf-8')) == user.password.encode('utf-8'):
            return (True, user)

        return(False, "aww snap, did you forget your password?")
    def addFriend(self, user_id, friend_id):
        user = self.get(id=user_id)
        friend = self.get(id=friend_id)
        Friend.objects.create(user_friend=user, second_friend=friend)
        Friend.objects.create(user_friend=friend, second_friend=user)

    def unfriend(self, user_id, friend_id):
        user = self.get(id=user_id)
        friend = self.get(id=friend_id)
        friendship1 = Friend.objects.get(user_friend=user, second_friend=friend)
        friendship2 = Friend.objects.get(user_friend=friend, second_friend=user)
        friendship1.delete()
        friendship2.delete()


class User(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    userManager = UserManager()
    objects = models.Manager()

class Friend(models.Model):
    user_friend = models.ForeignKey(User, related_name='requester')
    second_friend = models.ForeignKey(User, related_name='accepter')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

