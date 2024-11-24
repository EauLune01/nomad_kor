from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models.anonymous import Anonymous
from ..serializers.anonymous import AnonymousSerializer

# Swagger 요청 및 응답 스키마 정의
anonymous_create_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='익명 게시판 이름'),
    },
    required=['name']
)

anonymous_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='익명 게시판 ID'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='익명 게시판 이름'),
    }
)

class AnonymousListView(generics.ListCreateAPIView):
    """
    익명 게시판 목록 조회 및 생성
    """
    queryset = Anonymous.objects.all()
    serializer_class = AnonymousSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="익명 게시판 목록 조회",
        operation_description="모든 익명 게시판의 목록을 반환합니다.",
        responses={
            200: openapi.Response(description="성공", schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=anonymous_response_schema
            ))
        }
    )
    @swagger_auto_schema(
        operation_summary="익명 게시판 생성",
        operation_description="새로운 익명 게시판을 생성합니다.",
        request_body=anonymous_create_request_schema,
        responses={
            201: openapi.Response(description="익명 게시판 생성 성공", schema=anonymous_response_schema),
            400: openapi.Response(description="잘못된 요청")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



class AnonymousDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    익명 게시판 상세 조회, 수정 및 삭제
    """
    queryset = Anonymous.objects.all()
    serializer_class = AnonymousSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
