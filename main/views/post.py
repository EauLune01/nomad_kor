# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from ..models import Post, Comment, Position, FTF, Anonymous  # 경로를 수정
from ..serializers.post import PostSerializer  # PostSerializer import
from ..serializers.comment import CommentSerializer  # CommentSerializer import
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Swagger 요청 및 응답 스키마 정의
post_create_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='게시글 제목'),
        'content': openapi.Schema(type=openapi.TYPE_STRING, description='게시글 내용'),
    },
    required=['title', 'content']
)

post_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='게시글 ID'),
        'author_name': openapi.Schema(type=openapi.TYPE_STRING, description='작성자 이름'),
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='게시글 제목'),
        'content': openapi.Schema(type=openapi.TYPE_STRING, description='게시글 내용'),
        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime', description='작성일시'),
        'comments': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='댓글 ID'),
                'author_name': openapi.Schema(type=openapi.TYPE_STRING, description='댓글 작성자'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='댓글 내용'),
                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime', description='댓글 작성일'),
                'replies': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='대댓글 ID'),
                        'author_name': openapi.Schema(type=openapi.TYPE_STRING, description='대댓글 작성자'),
                        'content': openapi.Schema(type=openapi.TYPE_STRING, description='대댓글 내용'),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime', description='대댓글 작성일')
                    }
                ))
            }
        ))
    }
)

class PostListView(generics.ListCreateAPIView):
    """
    게시글 목록 조회 및 생성
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        게시판 유형별로 게시글을 필터링합니다.
        """
        path = self.request.path
        if 'position' in path:
            position_id = self.kwargs.get('position_id')
            return Post.objects.filter(position_id=position_id)
        elif 'ftf' in path:
            ftf_id = self.kwargs.get('ftf_id')
            return Post.objects.filter(ftf_id=ftf_id)
        elif 'anonymous' in path:
            anonymous_id = self.kwargs.get('anonymous_id')
            return Post.objects.filter(anonymous_id=anonymous_id)
        return Post.objects.none()  # 잘못된 URL에 대해서는 빈 쿼리셋 반환

    @swagger_auto_schema(
        operation_summary="게시글 목록 조회",
        operation_description="특정 게시판의 게시글 목록을 반환합니다.",
        responses={
            200: openapi.Response(description="목록 조회 성공", schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=post_response_schema
            )),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="게시글 생성",
        operation_description="특정 게시판에 새로운 게시글을 생성합니다.",
        request_body=post_create_request_schema,
        responses={
            201: openapi.Response(description="게시글 생성 성공", schema=post_response_schema),
            400: openapi.Response(description="잘못된 요청"),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        path = self.request.path

        if 'position' in path:
            position_id = self.kwargs.get('position_id')
            if not position_id:
                raise ValidationError({"position": "Position ID is missing from the request URL."})
            try:
                position = Position.objects.get(id=position_id)
            except Position.DoesNotExist:
                raise ValidationError({"position": f"Position with the given ID {position_id} does not exist."})

            serializer.save(position=position, author=self.request.user.profile, author_name=self.request.user.profile.nickname)

        elif 'ftf' in path:
            ftf_id = self.kwargs.get('ftf_id')
            if not ftf_id:
                raise ValidationError({"ftf": "FTF ID is missing from the request URL."})
            try:
                ftf = FTF.objects.get(id=ftf_id)
            except FTF.DoesNotExist:
                raise ValidationError({"ftf": f"FTF with the given ID {ftf_id} does not exist."})

            serializer.save(ftf=ftf, author=self.request.user.profile, author_name=self.request.user.profile.nickname)

        elif 'anonymous' in path:
            anonymous_id = self.kwargs.get('anonymous_id')
            if not anonymous_id:
                raise ValidationError({"anonymous": "Anonymous ID is missing from the request URL."})
            try:
                anonymous = Anonymous.objects.get(id=anonymous_id)
            except Anonymous.DoesNotExist:
                raise ValidationError({"anonymous": f"Anonymous group with the given ID {anonymous_id} does not exist."})

            serializer.save(anonymous=anonymous, author=self.request.user.profile, author_name=self.request.user.profile.nickname)

class PostDetailView(generics.RetrieveAPIView):
    """
    게시글 상세 조회 (댓글 및 대댓글 포함)
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        """
        게시글의 상세 정보와 댓글 및 대댓글 포함하여 반환
        """
        post = self.get_object()  # 게시글 객체 가져오기
        post_data = self.get_serializer(post).data
        # 댓글 및 대댓글 목록 추가
        post_data['comments'] = CommentSerializer(Comment.objects.filter(post=post), many=True).data
        return Response(post_data)


