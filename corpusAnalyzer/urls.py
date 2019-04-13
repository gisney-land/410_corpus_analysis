from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index_page),
    path("ajax/handle_extract_file_term/<int:queryid>", views.handle_extract_file_term,
         name="handle_extract_file_term"),
    path("ajax/return_extracted_file/<int:queryid>", views.return_extracted_file, name="return_extracted_file"),
]
