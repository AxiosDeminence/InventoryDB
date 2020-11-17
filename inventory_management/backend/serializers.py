from rest_framework import serializers
from .models import User, Character, Item

class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class CharacterCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"

class ItemCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

class ItemDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ["id", "owner"]

class ItemInfoSerializer(serializers.ModelSerializer):
    data = ItemDataSerializer(source="*", read_only=True)

    class Meta:
        model = Item
        fields = ["id", "data"]
        read_only_fields = fields

class CharacterInventorySerializer(serializers.ModelSerializer):
    inventory = ItemInfoSerializer(source="item_set", many=True, read_only=True)

    class Meta:
        model = Character
        fields = ["name", "inventory"]
        read_only_fields = fields

class UserDataSerializer(serializers.ModelSerializer):
    character_inventories = CharacterInventorySerializer(source="character_set", many=True, read_only=True)

    class Meta:
        model = User
        fields = ["character_inventories"]
        read_only_fields = fields