"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from .settings import OUTPUT_MOCKUPS, OUTPUT_MOCKUPS_URL, DEBUG

from mockups_api.views import MockupTaskGenerateView
from mockups_api.views import MockupTaskDetailView
from mockups_api.views import MockupListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/mockups/generate/", MockupTaskGenerateView.as_view()),
    path("api/v1/tasks/<uuid:task_id>/", MockupTaskDetailView.as_view()),
    path("api/mockups/", MockupListView.as_view()),
    # Swagger URLs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
]

if DEBUG:
    # TODO: Make images available via url.
    urlpatterns += static(OUTPUT_MOCKUPS_URL, document_root=OUTPUT_MOCKUPS)
