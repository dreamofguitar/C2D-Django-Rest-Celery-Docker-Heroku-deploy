from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'password','name','first_name','last_name','birthday','client_type','phone','gender','is_active')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','email','name','last_name','first_name','client_type','is_active')

class BasicUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'first_name',)