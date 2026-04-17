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
        try:
            name = request.data.get('name')

            if not name or not isinstance(name, str):
                return Response(
                    {"status": "error", "message": "Invalid name"},
                    status=400
                )

            name = name.strip()

            existing = Profile.objects.filter(name__iexact=name).first()
            if existing:
                return Response(
                    {
                        "status": "success",
                        "message": "Profile already exists",
                        "data": ProfileSerializer(existing).data
                    },
                    status=200
                )

            # 🔥 Fetch external data
            try:
                data = get_name_data(name)
            except Exception as e:
                print("API ERROR:", str(e))
                return Response(
                    {"status": "error", "message": "External API failed"},
                    status=502
                )

            # 🔥 Normalize data (CRITICAL FIX)
            age = data.get("age") if data.get("age") is not None else 0
            payload = {
                "name": name,
                "gender": data.get("gender") or "unknown",
                "gender_probability": data.get("gender_probability") or 0.0,
                "sample_size": data.get("sample_size") or 0,
                "age": age,
                "age_group": (
                    "child" if age < 18 else
                    "adult" if age < 60 else
                    "elder"
                ),
                "country_id": data.get("country_id") or "N/A",
                "country_probability": data.get("country_probability") or 0.0,
            }

            serializer = ProfileSerializer(data=payload)

            if not serializer.is_valid():
                print("SERIALIZER ERROR:", serializer.errors)
                return Response(
                    {"status": "error", "errors": serializer.errors},
                    status=400
                )

            profile = serializer.save()

            return Response(
                {"status": "success", "data": ProfileSerializer(profile).data},
                status=201
            )

        except Exception as e:
            print("CRITICAL ERROR:", str(e))
            return Response(
                {"status": "error", "message": "Server error"},
                status=500
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