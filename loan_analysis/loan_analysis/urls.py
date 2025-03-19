# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("", include("loan.urls")),  # Your main loan application
#     path("auth/", include("authentication.urls")),  # Include authentication routes
# ]





# //////////////////////////////////////////////////////








from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("loan.urls")),  # Your main loan application
    path("auth/", include("authentication.urls")),  # Include authentication routes
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
]
