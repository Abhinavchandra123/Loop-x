from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework.authtoken.views import obtain_auth_token


# urlpatterns = [
#     path("", views.hotel_list_view, name="home"),  # Frontend home
#     # web upload
#     # path('upload/', views.upload_page, name='upload_page'),
#     path("upload/", views.upload_xlsx_view, name="upload"),


#     # API token obtain
#     path('api-token-auth/', obtain_auth_token, name='api_token_auth'),


#     # upload api
#     path('api/upload-menu/', views.UploadMenuAPI.as_view(), name='api_upload_menu'),


#     # mobile APIs
#     path('api/hotels/', views.HotelListAPI.as_view(), name='api_hotels'),
#     path('api/hotel/<int:pk>/menu/', views.HotelMenuAPI.as_view(), name='api_hotel_menu'),
#     path('api/menu/all/', views.MenuAllAPI.as_view(), name='api_menu_all'),
#     path('api/menu/random/', views.MenuRandomAPI.as_view(), name='api_menu_random'),
#     ]


# # Serve media in development
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
urlpatterns = [
    # Web pages
    # path("", views.hotel_list_view, name="home"),
    path("", views.dashboard_view, name="dashboard"),
    path("hotel/<int:pk>/", views.hotel_menu_view, name="hotel_menu"),  # <-- this name must exist
    path("upload/", views.upload_xlsx_view, name="upload"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # path("dashboard/", views.dashboard_view, name="dashboard"),
    path("api/menu/<int:pk>/toggle_visibility/", views.ToggleVisibilityAPI.as_view(), name="toggle_visibility"),
    path("hotel/add/", views.add_hotel_view, name="add_hotel"),
    path("hotel/<int:hotel_id>/menu/add/", views.add_menu_item_view, name="add_menu_item"),
    path("hotel/<int:hotel_id>/menu/<int:item_id>/edit/", views.edit_menu_item_view, name="edit_menu_item"),
    path("hotel/<int:pk>/edit/", views.edit_hotel_view, name="edit_hotel"),
    path("api/manual-category/create/", views.create_manual_category, name="create_manual_category"),
    # APIs
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("api/menu/all/", views.UnifiedMenuAPI.as_view(), name="unified_menu_api"),
    path("api/upload-menu/", views.UploadMenuAPI.as_view(), name="api_upload"),
    path("api/hotels/", views.HotelListAPI.as_view(), name="api_hotels"),
    path("api/hotel/<int:pk>/menu/", views.HotelMenuAPI.as_view(), name="api_hotel_menu"),
    path("api/menu/random/", views.MenuRandomAPI.as_view(), name="api_random_menu"),
    path("api/menu/<int:pk>/update_category/", views.UpdateMenuCategoryAPI.as_view(), name="update_menu_category"),
    
    path("api/menu/<int:pk>/delete/", views.DeleteMenuItemAPI.as_view(), name="delete_menu_item"),
    path("api/menu/bulk_delete/", views.BulkDeleteMenuItemsAPI.as_view(), name="bulk_delete_menu_items"),
    # path("api/menu/all/", views.MenuAllAPI.as_view(), name="api_all_menu"),
]