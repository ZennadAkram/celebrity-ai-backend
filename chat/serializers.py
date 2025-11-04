from rest_framework import serializers
from .models import Category, User,ChatSession,Message,Celebrity
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'user_avatar', 'email']

    def create(self, validated_data):
        avatar = validated_data.pop('user_avatar', None)
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email"),
        )
        user.set_password(validated_data["password"])
        user.save()

        if avatar:
            user.user_avatar.save(avatar.name, avatar, save=True)  # ✅ triggers GCS upload

        return user
    def update(self, instance, validated_data):
     avatar = validated_data.pop('user_avatar', None)
     instance.username = validated_data.get('username', instance.username)
     instance.email = validated_data.get('email', instance.email)
     password = validated_data.get('password', None)
     if password:
        instance.set_password(password)
     instance.save()

     if avatar:
        instance.user_avatar.save(avatar.name, avatar, save=True)  # ✅ triggers GCS upload

     return instance


class CelebritySerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Celebrity
        fields = '__all__'
        extra_kwargs = {
            'creator': {'write_only': True},
    
            
        }

    

class ChatSessionSerializer(serializers.ModelSerializer):
    celebrity_image = serializers.SerializerMethodField()
    celebrity_name = serializers.CharField(source='celebrity.name', read_only=True)

    class Meta:
        model = ChatSession
        fields = ["id", "celebrity", "time_stamp", "celebrity_image", "celebrity_name"]
        read_only_fields = ["time_stamp"]

    def get_celebrity_image(self, obj):
        request = self.context.get('request')
        if obj.celebrity.avatar and hasattr(obj.celebrity.avatar, 'url'):
            return request.build_absolute_uri(obj.celebrity.avatar.url)
        return None
    
        
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "session", "text", "sender", "created_at"]
        read_only_fields = ["created_at"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'        

        