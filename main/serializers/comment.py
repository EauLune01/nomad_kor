from rest_framework import serializers
from ..models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.nickname')  # 'nickname' 필드를 사용
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # 댓글 작성일
    parent_id = serializers.IntegerField(source='parent.id', allow_null=True)  # 대댓글 부모 ID

    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'content', 'is_private', 'created_at', 'parent_id']


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(read_only=True)  # 작성자 이름
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # 게시글 작성일
    comments = serializers.SerializerMethodField()  # 댓글과 대댓글을 병렬로 가져오기

    class Meta:
        model = Post
        fields = ['id', 'author_name', 'title', 'content', 'created_at', 'comments']

    def get_comments(self, obj):
        # 모든 댓글을 가져옵니다.
        comments = Comment.objects.filter(post=obj)  # 현재 게시글에 대한 모든 댓글을 가져옵니다.

        # 대댓글도 같은 방식으로 포함시킵니다.
        return CommentSerializer(comments, many=True).data
