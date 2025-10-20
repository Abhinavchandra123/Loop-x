from django.contrib import admin
from .models import Hotel, ManualCategory, MenuItem, AllowedApp, Category


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_at')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'hotel', 'get_categories', 'get_manual_categories', 'price', 'is_visible')
    list_filter = ('hotel', 'categories', 'manual_categories')
    search_fields = ('item_name',)

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])
    get_categories.short_description = 'Auto Categories'

    def get_manual_categories(self, obj):
        return ", ".join([c.name for c in obj.manual_categories.all()])
    get_manual_categories.short_description = 'Manual Categories'


@admin.register(AllowedApp)
class AllowedAppAdmin(admin.ModelAdmin):
    list_display = ('app_name', 'api_key', 'is_active', 'created_at')
    readonly_fields = ('api_key',)
    
@admin.register(ManualCategory)
class ManualCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)