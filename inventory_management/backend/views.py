# from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.utils.datastructures import MultiValueDictKeyError as MissingParamError

from .models import User, Character, Item
from .serializers import (
    UserCreationSerializer,
    CharacterCreationSerializer,
    ItemCreationSerializer,
    UserDataSerializer,
)

# Create your views here.
class UserVisit(APIView):
    def get(self, request, format=None):
        try:
            client = User.objects.prefetch_related("character_set__item_set").get(username=request.user.username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "User must be valid."
            })
        
        serializer = UserDataSerializer(client, read_only=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data["character_inventories"])

class ItemManagement(APIView):
    # Item Creation
    def post(self, request, format=None):
        try:
            data = {
                "name": request.data["name"],
                "type": request.data["type"],
                "enhancements": request.data["enhancements"],
                "quantity": request.data["quantity"],
                "owner": request.data["owner"],
            }
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "Missing parameters.",
            })
        
        serializer = ItemCreationSerializer(data=data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "Incorrect form usage."
            })
        
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data={
            "message": "Object created.",
        })

    # Item Edits
    def patch(self, request, format=None):
        try:
            data = {
                "id": request.data["id"],
                "name": request.data["name"],
                "type": request.data["type"],
                "enhancements": request.data["enhancements"],
                "quantity": request.data["quantity"],
                "owner": request.data["owner"],
            }
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "Missing parameters.",
            })
        
        serializer = ItemCreationSerializer(data=data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "Incorrect form usage."
            })
        
        item = Item.objects.get(id=data["id"])
        serializer.update(item, serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED, data={
            "message": "Object updated.",
        })


    # Item Deletion
    def delete(self, request, format=None):
        try:
            data = {
                "id": request.data["id"],
            }
            item = Item.objects.select_related("owner__owner").get(id=data["id"])
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "Missing parameters.",
            })
        except Item.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "Item must be valid.",
            })

        if item.owner.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={
                "message": "Cannot delete item that is not yours."
            })

        item.delete()
        return Response(status=status.HTTP_202_ACCEPTED, data={
            "message": "Item deleted.",
        })

class CharacterManagement(APIView):
    def post(self, request, form=None):
        try:
            data = {
                "name": request.data["name"],
            }
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "Missing parameters.",
            })
        
        serializer = CharacterCreationSerializer(data=data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "Incorrect form usage or character already exists."
            })
        
        serializer.save(owner=request.user)
        return Response(status=status.HTTP_201_CREATED, data={
            "message": "Character created."
        })
    
    def delete(self, request, form=None):
        try:
            data = {
                "name": request.data["name"],
            }
            char = Character.objects.select_related("owner").get(name=data["name"])
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "Missing parameters.",
            })
        except Character.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "Character must be valid.",
            })
        
        if char.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={
                "message": "Cannot delete character that is not yours."
            })
        
        char.delete()
        return Response(status=status.HTTP_202_ACCEPTED, data={
            "message": "Character deleted.",
        })