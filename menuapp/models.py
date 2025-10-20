from django.db import models
from django.utils import timezone
import uuid
from slugify import slugify

class Hotel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='hotel_logos/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Separate model to hold all unique categories."""
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='menu_items')
    item_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    categories = models.ManyToManyField('Category', blank=True, related_name='menu_items')
    manual_categories = models.ManyToManyField('ManualCategory', blank=True, related_name='menu_items')  # ✅ separate table
    description = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    def hotel_image_upload_path(instance, filename):
        """Upload path: media/menu_images/<hotel-name>/<filename>"""
        
        hotel_folder = slugify(instance.hotel.name)
        return f"menu_images/{hotel_folder}/{filename}"
    image_local = models.ImageField(upload_to=hotel_image_upload_path, null=True, blank=True)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    

    class Meta:
        unique_together = ('hotel', 'item_name')
        indexes = [
            models.Index(fields=['hotel', 'item_name']),
        ]

    def __str__(self):
        return f"{self.hotel.name} - {self.item_name}"
    
class ManualCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class AllowedApp(models.Model):
    app_name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = uuid.uuid4().hex
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.app_name} ({'active' if self.is_active else 'inactive'})"
