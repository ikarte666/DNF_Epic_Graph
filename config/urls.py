from django.contrib import admin
from django.urls import path
from mainapps import views as main_views
from django.conf.urls import url, handler404, handler500

handler404 = "mainapps.views.error404"
handler500 = "mainapps.views.error500"

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("", main_views.main_view, name="main"),
    path("graph", main_views.search_view, name="search"),
]
