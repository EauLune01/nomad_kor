# serializers/post.py
from rest_framework import serializers
from ..models import Post, Comment  # 모델 임포트
from .comment import CommentSerializer  # CommentSerializer 임포트

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    comments = CommentSerializer(many=True, read_only=True)  # 댓글 목록 포함

    class Meta:
        model = Post
        fields = ['id', 'author_name', 'title', 'content', 'created_at', 'comments']

