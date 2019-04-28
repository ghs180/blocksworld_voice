from os import system

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import spacy
import sys
import string
from nltk.stem.porter import *


nlp = spacy.load('en_core_web_sm')

args = sys.argv
wiki_file = args[1]
questions_file = args[2]

with open(wiki_file) as f:
    doc = [line.strip() for line in f]

sentences = [sent for section in doc for sent in sent_tokenize(section)]
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)

def find_best_match(question):
    response = tfidf_vectorizer.transform([question])
    sims = cosine_similarity(response, tfidf_matrix_train)
    zip_sentences = zip(sims[0], sentences)
    return sorted(zip_sentences, key=lambda x: x[0])

def get_answer(question, data):
    qnlp = nlp(question)
    res = []
    for elem in data:
        res = res + [(elem[0])]
    sorted_sentences = [x[1] for x in data]
    zipped = zip(res, sorted_sentences)
    return sorted(zipped)

stemmer = PorterStemmer()

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def find_key_ent(q):
    if word_tokenize(q.lower())[0] == "who":
        key_ent = ["PERSON", "NORP", "ORG"]
    elif word_tokenize(q.lower())[0] == "where":
        key_ent = ["LOC", "GPE", "FAC"]
    elif word_tokenize(q.lower())[0] == "when":
        key_ent = ["DATE", "TIME"]
    else:
        key_ent = []
    return key_ent

questions = []
with open(questions_file) as f:
    questions = [line.strip() for line in f]


for q in questions:
    tfidf = find_best_match(q)
    answers = get_answer(q, tfidf)
    answers.reverse()
    answer = answers[0][1]
    has_key_ent = True
    key_ent = find_key_ent(q)
    answer_word = ""
    highest = 0
    curr_word = ""
    answer_ent_count = 0
    q_tokens = nlp(q.lower())
    stemmedq = stem_tokens(word_tokenize(q.lower()), stemmer)

    for (score, ans) in answers:
        if key_ent != []:
            has_key_ent = False
        stemmedans = " ".join(stem_tokens(word_tokenize(ans.lower()), stemmer))
        ans_tokens = nlp(ans)
        count = 0
        curr_ent_count = 0
        if not has_key_ent: #find key_ent
            for ent in ans_tokens.ents:
                if ent.label_ in key_ent:
                    has_key_ent = True
                    curr_word = ent.text
                    curr_ent_count += 1
                    if curr_ent_count > 1:
                        break

        if has_key_ent:
            for i in range(len(stemmedq)-1):
                bigram = " ".join(stemmedq[i:i+2])
                if bigram in stemmedans:
                    count += 1

            if count > highest:
                answer = ans
                highest = count
                answer_word = curr_word
                answer_ent_count = curr_ent_count

    if q_tokens[0].dep_ == "aux" or q_tokens[0].dep_ == "ROOT" or q_tokens[0].text.lower() == "is" or \
    ", was" in q or ", is" in q or ", did" in q or ", do" in q or ", does" in q or ", have" in q or ", has" in q:
        #yes-no question
        t_tokens = nlp(answer.lower())
        q_nsubj = None
        q_ROOT = None
        q_dobj = None
        q_pobj = None
        q_neg = 0

        t_nsubj = None
        t_ROOT = None
        t_dobj = None
        t_pobj = None
        t_neg = 0

        q_nouns = set(chunk.text for chunk in q_tokens.noun_chunks)
        t_nouns = set(chunk.text for chunk in t_tokens.noun_chunks)

        if not q_nouns.issubset(t_nouns):
            if len(t_nouns - q_nouns) == 1:
                #Q nouns = abc, t nouns = abd
                elem1 = list(t_nouns - q_nouns)[0]
                elem2 = list(q_nouns - t_nouns)[0]
                if nlp(elem1).similarity(nlp(elem2)) <= 0.9:
                    #Not similar
                    q_neg += 1
            elif len(t_nouns - q_nouns) > 1:
                q_neg += 1


        for token in q_tokens:
            if token.dep_ == "neg":
                q_neg += 1

        for token in t_tokens:
            if token.dep_ == "neg":
                t_neg += 1

        if (q_neg % 2 == t_neg % 2):
            print("Yes.")
        else:
            print("No.")
    else:
        #wh questions
        if answer_ent_count == 1 and answer_word.lower() not in q.lower():
            system('say {}'.format(answer_word))
        else:
            system('say {}'.format(answer))
