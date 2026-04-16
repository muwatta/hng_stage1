from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from .models import Profile
from .serializers import ProfileSerializer, ProfileListSerializer
from .services import get_name_data
from rest_framework.exceptions import APIException

class ProfileListCreateView(APIView):
    def get(self, request):
        # List all profiles with filters
        queryset = Profile.objects.all()
        gender = request.query_params.get('gender')
        if gender:
            queryset = queryset.filter(gender__iexact=gender)
        country_id = request.query_params.get('country_id')
        if country_id:
            queryset = queryset.filter(country_id__iexact=country_id)
        age_group = request.query_params.get('age_group')
        if age_group:
            queryset = queryset.filter(age_group__iexact=age_group)
        serializer = ProfileListSerializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "count": queryset.count(),
                "data": serializer.data
            },
            headers={"Access-Control-Allow-Origin": "*"}
        )

    def post(self, request):
        # Create a new profile
        name = request.data.get('name', None)
        if name is None or (isinstance(name, str) and name.strip() == ""):
            return Response(
                {"status": "error", "message": "Missing or empty name"},
                status=status.HTTP_400_BAD_REQUEST,
                headers={"Access-Control-Allow-Origin": "*"}
            )
        if not isinstance(name, str):
            return Response(
                {"status": "error", "message": "Invalid type"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                headers={"Access-Control-Allow-Origin": "*"}
            )
        name = name.strip()
        # Check existing
        existing = Profile.objects.filter(name__iexact=name).first()
        if existing:
            serializer = ProfileSerializer(existing)
            return Response(
                {
                    "status": "success",
                    "message": "Profile already exists",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK,
                headers={"Access-Control-Allow-Origin": "*"}
            )
        try:
            data = get_name_data(name)
        except APIException as e:
            return Response(
                {"status": "error", "message": e.detail},
                status=e.status_code,
                headers={"Access-Control-Allow-Origin": "*"}
            )
        except Exception:
            return Response(
                {"status": "error", "message": "Upstream or server failure"},
                status=status.HTTP_502_BAD_GATEWAY,
                headers={"Access-Control-Allow-Origin": "*"}
            )
        profile = Profile.objects.create(name=name, **data)
        serializer = ProfileSerializer(profile)
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers={"Access-Control-Allow-Origin": "*"}
        )

class ProfileDetailView(APIView):
    def get(self, request, id):
        try:
            profile = Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND,
                headers={"Access-Control-Allow-Origin": "*"}
            )
        serializer = ProfileSerializer(profile)
        return Response(
            {"status": "success", "data": serializer.data},
            headers={"Access-Control-Allow-Origin": "*"}
        )

    def delete(self, request, id):
        try:
            profile = Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND,
                headers={"Access-Control-Allow-Origin": "*"}
            )
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, headers={"Access-Control-Allow-Origin": "*"})