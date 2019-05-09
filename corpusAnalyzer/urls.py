from django.urls import path, re_path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.index_page),
    path("testgraph", views.show_graph),
    path("api/confirmData",views.handle_text),
    path("home", views.portal),
    path("ajax/handle_extract_file_term/<int:queryid>", views.handle_extract_file_term,
         name="handle_extract_file_term"),
    path("ajax/return_extracted_file/<int:queryid>", views.return_extracted_file, name="return_extracted_file"),
]
