from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models.ftf import FTF
from ..serializers.ftf import FTFSerializer

# Swagger 요청 및 응답 스키마 정의
ftf_create_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='FTF 게시판 이름'),
    },
    required=['name']
)

ftf_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='FTF 게시판 ID'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='FTF 게시판 이름'),
    }
)


class FTFListView(generics.ListCreateAPIView):
    """
    FTF 게시판 목록 조회 및 생성
    """
    serializer_class = FTFSerializer
    queryset = FTF.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="FTF 게시판 목록 조회",
        operation_description="모든 FTF 게시판의 목록을 반환합니다.",
        responses={
            200: openapi.Response(description="성공", schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=ftf_response_schema
            ))
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="FTF 게시판 생성",
        operation_description="새로운 FTF 게시판을 생성합니다.",
        request_body=ftf_create_request_schema,
        responses={
            201: openapi.Response(description="생성 성공", schema=ftf_response_schema),
            400: openapi.Response(description="잘못된 요청")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class FTFDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    FTF 게시판 상세 조회, 수정 및 삭제
    """
    serializer_class = FTFSerializer
    queryset = FTF.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'  # 기본 키를 사용하도록 설정

    @swagger_auto_schema(
        operation_summary="FTF 게시판 상세 조회",
        operation_description="특정 FTF 게시판의 상세 정보를 반환합니다.",
        responses={
            200: openapi.Response(description="성공", schema=ftf_response_schema),
            404: openapi.Response(description="게시판을 찾을 수 없습니다."),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="FTF 게시판 수정",
        operation_description="특정 FTF 게시판의 정보를 수정합니다.",
        request_body=ftf_create_request_schema,
        responses={
            200: openapi.Response(description="수정 성공", schema=ftf_response_schema),
            400: openapi.Response(description="잘못된 요청"),
            404: openapi.Response(description="게시판을 찾을 수 없습니다."),
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="FTF 게시판 삭제",
        operation_description="특정 FTF 게시판을 삭제합니다.",
        responses={
            204: openapi.Response(description="삭제 성공"),
            404: openapi.Response(description="게시판을 찾을 수 없습니다."),
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)



