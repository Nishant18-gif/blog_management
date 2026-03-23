from rest_framework import serializers
from .models import Blog, Comment, Like


# -----------------------------
# Blog Serializer
# -----------------------------
class BlogSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    # LIKE FIELDS
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id',
            'title',
            'content',
            'author',
            'image',

            'created_at',
            'updated_at',
            'deleted_at',
            'status',

            'likes_count',
            'is_liked'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request', None)

        if request and request.user.is_authenticated:
            # optimized check
            return obj.likes.filter(user=request.user).exists()

        return False


# -----------------------------
# Comment Serializer
# -----------------------------
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    blog = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'blog',
            'author',
            'text',
            'created_at'
        ]