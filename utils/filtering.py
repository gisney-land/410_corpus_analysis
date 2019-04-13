from nltk.collocations import *
import nltk
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
import numpy as np

doc_dir = "/Users/fenyiye/Documents/uiuc/sem2/CS410/BioNLP-ST_2011_genia_train_data_rev1/"
files = os.listdir(doc_dir)

docs = []
for file in files:
    if (file.endswith('txt')):
        docs.append(open(doc_dir + file, 'r').read())


def gen_association_dict(docs, window_size=4, min_freq=2, method=nltk.collocations.BigramAssocMeasures().chi_sq):
    doc = "".join()
    finder = BigramCollocationFinder.from_words(doc.split(), window_size=4)
    finder.apply_freq_filter(min_freq)
    lookup = dict(finder.score_ngrams(method))
    return lookup


def get_tfidf_vectorizer(docs):
    vectorizer = TfidfVectorizer()
    return vectorizer.fit(docs)


def gen_tfidf_dict(new_docs, corpora):
        # new_docs is list of strings
        # corpora is list of string
    docs = new_docs + corpora
    vectorizer = get_tfidf_vectorizer(docs)
    vect = vectorizer.transform(docs)
    new_doc_cnt = len(new_docs)

    vectorized_docs = [vec.toarray() for vec in vect[:new_doc_cnt]]
    tfidf_vecs = np.array(vectorized_docs)
    reduced_tfidf_vec = np.amax(tfidf_vecs, axis=0).flatten()
    for i in range(len(reduced_tfidf_vec)):
        if reduced_tfidf_vec[i] > 0:
            print(vectorizer.get_feature_names()[i], reduced_tfidf_vec[i])


'''
for (indice, value) in zip(v.indices, v.data):
    print(vectorizer.get_feature_names()[indice], value)
'''


def lemma_stem(word):
    # word is token
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(stemmer.stem(word))


def get_stemmed_sent(sent):
    # sent is string
    return " ".join([lemma_stem(word) for word in nltk.word_tokenize(sent)])


def get_stemmed_crpora(docs):
    # doc is list of string
    return ["".join([get_stemmed_sent(sent) for sent in nltk.sent_tokenize(doc)]) for doc in docs]


def phrase_adapt_modifier(phrase, assoc_lookup, tfidf_lookup, assoc_thres, tfidf_thres):
    tokens = nltk.word_tokenize(phrase)
    tags = nltk.pos_tag(tokens)
    print(tags)


docs = get_stemmed_crpora(docs)
gen_tfidf_dict(docs[:1], docs[1:])
