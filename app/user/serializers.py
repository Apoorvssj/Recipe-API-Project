"""
Serializers for the user API view.
"""
from dataclasses import fields
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

        def create(self, validated_data):
            """
            Create and return a user with encrypted password.
            Overiding default create method fo serializer cuz we dont want to save password as clear text,
            we want it to be encypted so we need to use our custom create_user method
            create method is only called after validation, also includes min_length.
            """
            return get_user_model().objects.create_user(**validated_data)
