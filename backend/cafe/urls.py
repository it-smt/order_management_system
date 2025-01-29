from django.contrib import admin
from django.urls import path, include

from ninja import NinjaAPI

from main.api.v1.router import router as main_router

api_v1 = NinjaAPI(title="Система управления заказами", version="1.0.0")
api_v1.add_router(prefix="main", router=main_router, tags=["Основное"])

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls", namespace="main")),
    path("api/v1/", api_v1.urls),
]
