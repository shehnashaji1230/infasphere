from rest_framework import serializers
from infa.models import User,Post,Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password','phone']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CommentSerializer(serializers.ModelSerializer):
    owner=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Comment
        fields="__all__"
        read_only_fields=["id","owner","post_object","created_date"]
class PostSerializer(serializers.ModelSerializer):
    owner=serializers.StringRelatedField(read_only=True)

    comment_count=serializers.SerializerMethodField(method_name='get_comment_count',read_only=True)
    comments=serializers.SerializerMethodField(method_name='get_comments',read_only=True)
    likes=serializers.SerializerMethodField(method_name='get_likes_count',read_only=True)
    liked_by=serializers.StringRelatedField(read_only=True,many=True)
    class Meta:
        model=Post
        fields="__all__"
        read_only_fields=['id','liked_by','created_date','owner']
    
    def get_comment_count(self,object):
        return object.comments.count()
    
    def get_comments(self,object):
        qs=object.comments.all()
        serializer_instance=CommentSerializer(qs,many=True)
        return serializer_instance.data
    
    def get_likes_count(self,object):
        return object.liked_by.count()

