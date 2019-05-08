import nltk
import re
from collections import Counter
from nltk.tag.perceptron import PerceptronTagger
import sys
import PyPDF2
import unicodedata
import justeson_extractor as je
import os
import gensim
import logging 

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

max_count = 8000
term_min = 5
wv_min = 5

def ite_directories(dir):
    count = 0
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            filepath = subdir + os.sep + file
            count += 1
            if count>max_count:
                break
            if filepath.endswith(".pdf"):
                text = pdf_read(filepath)
                text = text_cleaning(text)
                yield text


def text_cleaning(pages):
    pages = re.sub(r"(?<=\-)(\s)*", "", pages)
    pages = re.sub(r"b\'\'", '', pages)
    pages = re.sub(r"\.+", '.', pages)
    pages = re.sub(r"((?<=\s)b(\'|\"))|(^b\')|(\"$)", '', pages)
    pages = re.sub(r"(?<=[\W])([0-9]+.)?[0-9]+(?=[\W])", '0', pages)
    pages = re.sub(r"[^a-zA-Z0-9.,;?!-\'\"\s]+", '', pages)
    pages = re.sub(r"\s\'\s", ' ', pages)
    pages = re.sub(r"%+", " ", pages)
    return pages


def pdf_read(file_dir):
    try:
        print(file_dir)
        pdfFileObj = open(file_dir, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pages = ' '.join([str(pdfReader.getPage(i).extractText().encode('utf-8').lower()) for i in range(pdfReader.numPages)])
        pdfFileObj.close()
        return pages
    except:
        return ""

if __name__ == "__main__":
    documents = "".join(list(ite_directories("../acl_anthology")))

    print("getting justeson")

    term_list = list(je.get_all_terms_in_doc(documents, term_min))
    term_list.sort(key=len, reverse=True)
    for idx, term in enumerate(term_list):
        reg_term = re.sub("\.", "\.", term)
        #print(idx, "change " + reg_term + " to " + "-".join(term.split()))
        documents = re.sub(reg_term, "-".join(term.split()), documents)

    documents = nltk.sent_tokenize(documents)
    documents = [nltk.word_tokenize(line) for line in documents]

    for idx, term in enumerate(term_list):
        term_list[idx] = "-".join(term.split())

    term_file = open("term_list.txt", "w")
    for term in term_list:
        term_file.write(term + "\n")
    term_file.close()

    print("start training")
    model = gensim.models.Word2Vec(
        documents,
        size=300,
        window=10,
        min_count=wv_min,
        workers=10)
    model.train(documents, total_examples=len(documents), epochs=1000)
    model.save("word2vec.model")

    vocab_file = open("vocab_list.txt", "w")
    for vocab in model.wv.vocab:
        vocab_file.write(vocab + "\n")
    vocab_file.close()

