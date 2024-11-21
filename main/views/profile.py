from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from ..models.profile import Profile
from ..serializers.profile import ProfileSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_profile(request):
    """
    프로필 생성 (nickname, age, gender 필수)
    """
    user = request.user
    if Profile.objects.filter(user=user).exists():
        return Response({"error": "프로필이 이미 존재합니다."}, status=400)

    data = request.data
    serializer = ProfileSerializer(data=data)
    if serializer.is_valid():
        profile = serializer.save(user=user)
        return Response(ProfileSerializer(profile).data, status=201)
    return Response(serializer.errors, status=400)


class ProfileDetailView(RetrieveAPIView):
    """
    프로필 조회
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        현재 로그인된 유저의 프로필 반환
        """
        return Profile.objects.get(user=self.request.user)


class ProfileUpdateView(RetrieveUpdateAPIView):
    """
    프로필 조회 및 업데이트
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        현재 로그인된 유저의 프로필 반환
        """
        return Profile.objects.get(user=self.request.user)