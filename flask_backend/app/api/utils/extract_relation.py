from gensim.models import Word2Vec
from . import justeson_extractor_another as je
from . import preprocessing as p
import nltk
import re
import sys
import logging
import os

logging.disable(logging.INFO)


def knowledge_graph(text_to_parse):
    print("=========" + os.getcwd() + "===============")
    model = Word2Vec.load("./app/api/utils/word2vec.model")
    documents = p.text_cleaning(text_to_parse)

    term_list_cand = list(je.get_all_terms_in_doc(documents, 1))
    term1 = []
    for term in term_list_cand:
        term = "-".join(term.split())
        try:
            vec = model.wv[term]
            if (len(term.split("-")) > 1):
                term1.append(term)
        except:
            pass

    term_list = list(je.get_all_terms_in_doc(documents, 5))

    for idx, term in enumerate(term_list):
        reg_term = re.sub("\.", "\.", term)
        documents = re.sub(reg_term, "-".join(term.split()), documents)

    for idx, term in enumerate(term_list):
        term_list[idx] = "-".join(term.split())

    term_list = list(set(term1).union(set(term_list)))
    sents = nltk.sent_tokenize(documents)
    tokens = [nltk.word_tokenize(sent) for sent in sents]

    model.build_vocab(tokens, update=True)
    model.train(tokens, total_examples=len(tokens), epochs=1000)

    # for term in term_list:
    #     term_file.write(term + "\n")
    # term_file.close()
    graph_list = []
    uses_list = []
    for idx, term in enumerate(term_list):
        for term_ in term_list:
            sim = model.wv.n_similarity([term], [term_, "tools", "applications"])
            if (sim > 0.2 and term != term_):
                uses_list.append(term + " -[:uses]-> " + term_)
                graph_list.append([term, term_])

    relates_list = []
    print("<<<")
    for idx, term in enumerate(term_list):
        for term_ in term_list:
            sim = model.wv.n_similarity([term, "topics"], [term_])
            if (sim > 0.15 and term != term_):
                relates_list.append(term + " -[:related to]-> " + term_)
                graph_list.append([term, term_])

    console_str = "".join(uses_list) + "\n" + "".join(relates_list)
    # print(console_str)
    uses_list.extend(relates_list)
    result_dict = {"console": uses_list, "graph": graph_list}
    return result_dict


if __name__ == "__main__":
    file_name = sys.argv[1]
    model = Word2Vec.load("word2vec.model")

    file = open(file_name, 'rb')
    lines = file.readlines()
    lines = [line.decode('utf-8') for line in lines]
    documents = p.text_cleaning("".join(lines)).lower()
    print(type(documents))

    term_list_cand = list(je.get_all_terms_in_doc(documents, 1))
    term1 = []
    for term in term_list_cand:
        term = "-".join(term.split())
        try:
            vec = model.wv[term]
            if (len(term.split("-")) > 1):
                term1.append(term)
        except:
            pass

    term_list = list(je.get_all_terms_in_doc(documents, 5))

    for idx, term in enumerate(term_list):
        reg_term = re.sub("\.", "\.", term)
        documents = re.sub(reg_term, "-".join(term.split()), documents)

    for idx, term in enumerate(term_list):
        term_list[idx] = "-".join(term.split())

    term_list = list(set(term1).union(set(term_list)))
    sents = nltk.sent_tokenize(documents)
    tokens = [nltk.word_tokenize(sent) for sent in sents]

    model.build_vocab(tokens, update=True)
    model.train(tokens, total_examples=len(tokens), epochs=1000)

    term_file = open("term_list.txt", "w")
    use_file = open("use_list.txt", "w")
    relate_file = open("relate_list.txt", "w")

    for term in term_list:
        term_file.write(term + "\n")
    term_file.close()

    for idx, term in enumerate(term_list):
        for term_ in term_list:
            sim = model.wv.n_similarity([term], [term_, "tools", "applications"])
            if (sim > 0.2 and term != term_):
                print(term + " -[:uses]-> " + term_)
                use_file.write(term + " | " + term_ + "\n")

    print("<<<")
    for idx, term in enumerate(term_list):
        for term_ in term_list:
            sim = model.wv.n_similarity([term, "topics"], [term_])
            if (sim > 0.15 and term != term_):
                print(term + " -[:related to]-> " + term_)
                relate_file.write(term + " | " + term_ + "\n")

    use_file.close()
    relate_file.close()
