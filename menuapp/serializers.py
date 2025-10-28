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

        # ✅ Case 1: If local image exists
        if obj.image_local:
            # Convert ImageFieldFile to string before concatenation
            image_path = str(obj.image_local)
            url = f"{settings.MEDIA_URL}{image_path}"
            return request.build_absolute_uri(url) if request else url

        # ✅ Case 2: Remote image URL fallback
        if obj.image_url:
            return obj.image_url

        # ✅ Case 3: Default placeholder (optional)
        return request.build_absolute_uri(f"{settings.MEDIA_URL}no_image.jpg") if request else f"{settings.MEDIA_URL}no_image.jpg"

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