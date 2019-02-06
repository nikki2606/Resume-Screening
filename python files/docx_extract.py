# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 21:39:23 2019

@author: suman
"""
import docx
import csv
import os
import spacy 
import re
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd

import sklearn 
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
text = ""
def extract_name(string):
    r1 = string
    nlp = spacy.load('en')
    doc = nlp(r1)
    for ent in doc.ents:
        if(ent.label_ == 'PERSON'):
            print(ent.text)
            break
    
def docx_to_text(name):
    doc = docx.Document(name)
    texts ='' 
    for para in doc.paragraphs: 
        texts += para.text
        texts += '\n'
        
    return texts

def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)

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

#Sets are used as it has a a constant time for lookup hence the overall the time for the total code will not exceed O(n)
s = set(your_list[0])
s1 = your_list
s2 = your_listatt
skillindex = []
skills = []
skillsatt = []
print('\n')



text = docx_to_text('shellsujitresume1.docx')

text_lo = text.lower()
text_lo = text_lo.replace(',', '')
text_lo = text_lo.replace(':', '')
#print(text)
extract_name(text)

phone_no = extract_phone_numbers(text)
print(phone_no)
emails = extract_email_addresses(text)
print(emails)


for word in text_lo.split(" "):
    if word in s:
        skills.append(word)
skills1 = list(set(skills))
print('\n')
print("Following are his/her Technical Skills")
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

#Sets are used as it has a a constant time for lookup hence the overall the time for the total code will not exceed O(n)
s1 = set(your_list1[0])
nontechskills = []
for word in text_lo.split(" "):
    if word in s1:
        nontechskills.append(word)
nontechskills = set(nontechskills)
print('\n')

print("Following are his/her Non Technical Skills")
list5 = list(nontechskills)
print('\n')
for i in range(len(list5)):
    print(list5[i])
print('\n \n')

#Save in text file 
file1 = open("res1.txt", "w")
res = ''
for sk in skills1:
    res = res + sk;
    res = res + " ";
file1.write(res)
file1.close()

