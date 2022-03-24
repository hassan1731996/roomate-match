from rest_framework import serializers
from mainweb.models import UserPosts


class UserPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPosts
        fields = ('title', 'city', 'university', 'looking_for', 'role', 'id')
