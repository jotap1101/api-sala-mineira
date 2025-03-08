from collections import OrderedDict
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'first_name', 'last_name', 'username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'profile_picture', 'last_login', 'date_joined']
        read_only_fields = ['id', 'url', 'last_login', 'date_joined']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'write_only': True},
        }
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        ordered_representation = OrderedDict()

        for key, value in representation.items():
            ordered_representation[key] = value

            if key == 'last_name' and instance.get_full_name():
                ordered_representation['full_name'] = instance.get_full_name()

        return ordered_representation
    
    def validate_password(self, value):
        try:
            validate_password(value)
        except serializers.ValidationError as error:
            raise serializers.ValidationError(error.detail)
        
        return value
    
    def create(self, validated_data):
        # return User.objects.create_user(**validated_data)

        password = validated_data.pop('password')
        instance = User(**validated_data)

        instance.set_password(password)
        instance.save()

        return instance
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        
        instance.save()

        return instance