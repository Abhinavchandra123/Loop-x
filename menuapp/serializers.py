from rest_framework import serializers
from .models import Hotel, MenuItem
from django.conf import settings



class MenuItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    manual_categories = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ('id', 'item_name', 'price', 'categories', 'manual_categories', 'description', 'image', 'is_visible')

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image_local:
            url = settings.MEDIA_URL + obj.image_local
            return request.build_absolute_uri(url) if request else url
        return obj.image_url

    def get_categories(self, obj):
        return [cat.name for cat in obj.categories.all()]

    def get_manual_categories(self, obj):
        return [cat.name for cat in obj.manual_categories.all()]  # ✅ now reads from new model

class HotelSerializer(serializers.ModelSerializer):
    menu_count = serializers.IntegerField(source='menu_items.count', read_only=True)
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ('id', 'name', 'uploaded_at', 'menu_count', 'logo')

    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.logo:
            url = obj.logo.url
            return request.build_absolute_uri(url) if request else url
        return None


class HotelDetailSerializer(serializers.ModelSerializer):
    menu = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ('id', 'name', 'uploaded_at', 'logo', 'menu')

    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.logo:
            url = obj.logo.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_menu(self, obj):
        # ✅ Filter visible menu items only
        items = obj.menu_items.filter(is_visible=True).prefetch_related('categories', 'manual_categories')
        return MenuItemSerializer(items, many=True, context=self.context).data