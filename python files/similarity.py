# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 05:53:40 2019

@author: suman
"""
import dateutil
import numpy as np
import pandas as pd
import csv
import spacy
from nltk.corpus import stopwords
import sklearn
import docx 
import inflect
import re, string, unicodedata
import nltk
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#load job description
res2 = 'Mobile Android Developer - Java OOPS Design Patterns 8 - 10 yrs Opening for Mobile Android Developer for IT Experience : 6 - 10 Years Function : Technology - IT & Systems Environment : Our development environment is agile. This developer must have experience in an agile development and agile testing environment which requires experience in Test Driven Development. Essential Duties and Responsibilities : Analyzes software requirements to determine the feasibility of design within time and cost constraints. Develop software features according to published requirements Consults with the engineering staff of all disciplines to evaluate interfaces between various system components in order to consider operational and performance requirements of the overall system in feature design. Consults with the Product Owners concerning feature requirements and acceptance criteria Develop automated tests for software features developed Skills, Languages, Frameworks : Android development Java Object-oriented analysis, design and programming Understanding of design patterns Web Services such as RESTful API development Android Studio Mastery of SQL Experience with Git like GitHub or gitlab'

def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words

def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems
    
def clean_text(text):
    words = nltk.word_tokenize(text)
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = replace_numbers(words)
    words = remove_stopwords(words)
    words = stem_words(words)
    return words


def docx_to_text(name):
    doc = docx.Document(name)
    texts ='' 
    for para in doc.paragraphs: 
        texts += para.text
        texts += '\n'
        
    return texts

def extract_information(string):
    string.replace (" ", "+")
    query = string
    soup = BeautifulSoup(urlopen("https://en.wikipedia.org/wiki/" + query), "html.parser")
    #creates soup and opens URL for Google. Begins search with site:wikipedia.com so only wikipedia
    #links show up. Uses html parser.
    for item in soup.find_all('div', attrs={'id' : "mw-content-text"}):
        print(item.find('p').get_text())
        print('\n')
with open('techatt.csv', 'rt') as f:
    reader = csv.reader(f)
    your_listatt = list(reader)
with open('techskill.csv', 'rt') as f:
    reader = csv.reader(f)
    your_list = list(reader)
with open('nontechnicalskills.csv', 'rt') as f:
    reader = csv.reader(f)
    your_list1 = list(reader)

s = set(your_list[0])
s1 = your_list
s2 = your_listatt
skillindex = []
skills = []
skillsatt = []

res_lo = ''
res2_lo = res2.lower()
res2_lo = res2_lo.replace(',', '')
res2_lo = res2_lo.replace(':', '')

for word in res2_lo.split(" "):
    if word in s:
        skills.append(word)
skills1 = list(set(skills))
print('\n')
print("Following are required Technical Skills")
print('\n')
np_a1 = np.array(your_list)
for i in range(len(skills1)):
    item_index = np.where(np_a1==skills1[i])
    skillindex.append(item_index[1][0])

nlen = len(skillindex)
for i in range(nlen):
    print(skills1[i])
    #print(s2[0][skillindex[i]])
    print('\n')


#Save in text file 
file2 = open("res2.txt", "w")
res = ''
for sk in skills1:
    res = res + sk;
    res = res + " ";
file2.write(res)
file2.close()

res1 = docx_to_text('YT.docx')
#res resume is cleaned
words = clean_text(res1)
my_res1 = ''
for word in words:
    my_res1 = my_res1 + word + " ";

#res job description is cleaned
words = clean_text(res2)
my_res2 = ''
for word in words:
    my_res2 = my_res2 + word + " ";

cv=CountVectorizer()
resume=[my_res1,my_res2]

word_count_vector = cv.fit_transform(resume)

tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count_vector)

arr = cosine_similarity(word_count_vector[:], word_count_vector[:])
print(arr[0][1])

#Extract Education 

# load pre-trained model
nlp = spacy.load('en')
# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))
# Education Degrees
EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S', 
            'ME', 'M.E', 'M.E.', 'MS', 'M.S', 
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
        ]
def extract_education(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.string.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education
print(extract_education(res1))
