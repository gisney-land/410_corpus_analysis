from django.shortcuts import render
from datetime import datetime
from django.http.response import HttpResponse, JsonResponse, FileResponse, Http404
from django.views.decorators.http import require_http_methods
import os, json
from django.core.serializers import serialize
from tika import parser
import os.path
from utils import justeson_extractor
import re


# Create your views here.
@require_http_methods(["GET", "POST"])
def index_page(request):
    return render(request, "index.html")


def handle_extract_file_term(request, queryid):
    print("hi, I am here")
    file_to_parse = request.FILES.get("selected_files")
    to_parse_filename = os.path.join("pdfs", str(queryid) + ".pdf")
    with open(to_parse_filename, 'wb') as f:
        f.write(file_to_parse.read())

    raw = parser.from_file(to_parse_filename)
    plain_text = raw['content']

    reg_exp = '((A|N)+|((A|N)*(NP)?)(A|N)*)N'
    p = re.compile(reg_exp)
    doc = str(plain_text).encode('ascii', 'ignore').decode("ascii")
    min_freq = 2

    terms = justeson_extractor.get_all_terms_in_doc(reg_exp, doc, min_freq)

    result_txt = "\n".join(list(terms))
    result_path = os.path.join("texts", str(queryid) + ".txt")

    with open(result_path, "w+") as f:
        f.write(result_txt)

    response = HttpResponse()
    response.write(f"{result_txt}")
    return response


def return_extracted_file(request, queryid):
    pass
