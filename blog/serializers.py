from rest_framework import serializers
from .models import Blog, Comment


# -----------------------------
# Blog Serializer
# -----------------------------
class BlogSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author', 'image']


# -----------------------------
# Comment Serializer
# -----------------------------
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    blog = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'blog', 'author', 'text', 'created_at']