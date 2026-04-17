from rest_framework import serializers  
from .models import User 
from django.contrib.auth import authenticate 

class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User 
        fields = ['email', 'password','first_name','last_name']
        extra_kwargs = {'password': {'write_only': True}} 

    def create(self,validated_data):
        return User.objects.create_user( **validated_data)  
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials', code='authorization')
        else:
            raise serializers.ValidationError('Must include "email" and "password".', code='authorization')

        data['user'] = user
        return data 
