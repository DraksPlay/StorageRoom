from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="StorageRoom API",
      default_version='v 1.0',
      description="API for StorageRoom",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="draksplay@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/users/', include('applications.users.urls')),
    path('api/storages/', include('applications.storages.urls')),
]
