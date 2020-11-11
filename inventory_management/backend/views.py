# from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, Character, Item
from .serializers import (
    UserCreationSerializer,
    CharacterCreationSerializer,
    ItemCreationSerializer,
    ItemInfoSerializer,
    CharacterInventorySerializer,
    UserDataSerializer,
)

# Create your views here.
class UserVisit(APIView):
    def get(self, request, format=None):
        username = request.data.get("user")
        try:
            client = User.objects.prefetch_related(
                "character_set__item_set",
            ).get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "mesasge": "User must be valid."
            })
        
        serializer = UserDataSerializer(client, read_only=True)
        return Response(serializer.data["character_inventories"])

class CharacterInventory(APIView):
    def post(self, request, format=None):
        queryset = Character.objects.get(character_name=request.data.get("character")).item_set.all()
        serializer = ItemInfoSerializer(queryset, many=True, read_only=True)

        return Response(serializer.data)