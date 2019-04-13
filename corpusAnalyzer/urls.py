from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index_page),
    path("ajax/handle_extract_file_term/<int:queryid>", views.handle_extract_file_term, name="handle_extract_file_term"),
    # path("ajax/<str:receiver>/all", views.all_msg_ajax),
]
