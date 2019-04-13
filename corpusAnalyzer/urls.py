from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index_page),
    # path("ajax/<str:receiver>/unread", views.index,name="index"),
    # path("ajax/<str:receiver>/all", views.all_msg_ajax),
]
