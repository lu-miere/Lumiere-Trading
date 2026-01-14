from rest_framework import serializers
from authentication.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)


    class Meta:
        model =  User
        fields = ('email', 'first_name',  'last_name', 'password')

        
    def create(self, validated_data):

        password = validated_data.pop('password')

        user = User.objects.create_user(
                email=validated_data['email'],
                password= password, 
                **validated_data)
        
        return user
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =('email', 'first_name', 'last_name', 'news_sub_uuid', 'trader_uuid' ,)
            


            