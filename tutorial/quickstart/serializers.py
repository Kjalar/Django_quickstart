from django.contrib.auth.models import User
from rest_framework import serializers
from quickstart.models import Tweet, Follow


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'url': {'lookup_field': 'username'}}


class TweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['url', 'id', 'text', 'photo', 'author', 'created']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = []  # ничего не возращаем клиенту


class FollowsSerializer(serializers.HyperlinkedModelSerializer):
    follows = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['follows', 'followed']


class FollowerSerializer(serializers.HyperlinkedModelSerializer):
    follower = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['follower', 'followed']
