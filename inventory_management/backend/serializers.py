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

class ItemDataSerializer(serializers.Serializer):
    id           = serializers.CharField()
    item_type    = serializers.CharField()
    enhancements = serializers.ListField()

class ItemInfoSerializer(serializers.ModelSerializer):
    # item_name = serializers.CharField()
    item_data = ItemDataSerializer(source="*", read_only=True)

    class Meta:
        model = Item
        fields = ["item_name", "item_data"]
        read_only_fields = fields

class CharacterInventorySerializer(serializers.ModelSerializer):
    inventory = ItemInfoSerializer(source="item_set", many=True, read_only=True)

    class Meta:
        model = Character
        fields = ["character_name", "inventory"]
        read_only_fields = fields

class UserDataSerializer(serializers.ModelSerializer):
    character_inventories = CharacterInventorySerializer(source="character_set", many=True, read_only=True)

    class Meta:
        model = User
        fields = ["character_inventories"]
        read_only_fields = fields