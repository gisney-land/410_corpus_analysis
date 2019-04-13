from django.shortcuts import render
from datetime import datetime
from django.http.response import HttpResponse, JsonResponse, FileResponse, Http404
from django.views.decorators.http import require_http_methods
import os, json
from django.core.serializers import serialize


# Create your views here.
@require_http_methods(["GET", "POST"])
def index_page(request):
    return render(request, "index.html")


def handle_extract_file_term(request, queryid):
    print("hi, I am here")
