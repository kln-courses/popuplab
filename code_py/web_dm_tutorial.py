#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
tutorial in web data mining for Frontiers in DH March 30, 2017

@author: kln
"""
### preamble - some practical stuff
# import module ("collections of functions that as helpful")
import os
# make a working directory
os.mkdir('/home/kln/Desktop/web_dm')
# change to working directory
os.chdir('/home/kln/Desktop/web_dm')
pwd

### basic objects that we need in this tutorial
## variables: data types
# numerical
# intergers
a = 2
print a
# sequences
# strings
s = 'this is a text'
print s
print s[1]
# lists
l = [a,s]
print l, l[0]
# iterateables
for c in s:
    print c*a
# function
def add(x,y):
    result = x+y
    return result
print add(a,3)
print add('foo','bar') # polymorphism

### web pages are identified through address (i.e., uniform resource locator)
import io, urllib2
url = 'http://www.gutenberg.org/files/16/16-0.txt'
response = urllib2.urlopen(url) 
text = response.read()

# write text to file
with open("Pan.txt", "w") as text_file:
    text_file.write(text)

# load text
file = 'Pan.txt'
f = io.open(file,'r',encoding = 'utf8')
text = f.read()

# inspect the text
len(text)
print text[0:10]

# extract content through brute force
strt = '*** START OF THIS PROJECT GUTENBERG EBOOK PETER PAN ***'
end = 'End of the Project Gutenberg EBook of Peter Pan, by James M. Barrie'
idx = text.find(strt)
idx1 = idx+len(strt)+1
idx2 = text.find(end)
content = text[idx1:idx2]

# preprocess
import re
content = re.sub(r'\W+', ' ',content)
content = re.sub(r'\d','',content)
content = content.lower()
tokens = content.split()
print tokens[0:100]

# chunkize text
c_size = 500
idx = range(0,len(tokens)+1,c_size)
chunk_list = [] 
for i in idx:
    if i == len(idx):
        chunk_list.append(tokens[i:-1])
    else:
        chunk_list.append(tokens[i:i+c_size])

# sentiment plot analysis
from afinn import Afinn
import numpy as np

afinn = Afinn(language='en')
sent_vec = []
for chunk in chunk_list:
    c_vec = []
    for s in chunk:
        c_vec.append(afinn.score(s))
    sent_vec.append(np.sum(c_vec))

idx = range(1,len(sent_vec)+1)
import matplotlib.pyplot as plt
plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
plt.bar(idx,sent_vec,color='r')
plt.axhline(y=np.mean(sent_vec), linewidth=1, color = 'k')
plt.axvline(x=sent_vec.index(max(sent_vec))+1, linewidth=1, color='k')
plt.axvline(x=sent_vec.index(min(sent_vec))+1, linewidth=1, color='k')
plt.xlabel('Narrative time')
plt.ylabel('Sentiment score')
plt.title('Peter Pan')
plt.tight_layout()
plt.savefig('pan_sentiment.png')

# explore signal to text
idx = sent_vec.index(min(sent_vec))
print ' '.join(chunk_list[idx])
idx = sent_vec.index(max(sent_vec))
print ' '.join(chunk_list[idx])

# scale signal to text to n values
import heapq
sent_arr = np.array(sent_vec).astype(int)
minval = heapq.nsmallest(5,sent_arr)
minidx = []
for i in minval:
    minidx.append(sent_vec.index(i))    
print ' '.join(chunk_list[minidx[1]])

### scale solution using functions & build your own module
import re
def pp_token(s):
    tmp = re.sub(r'\W+',' ',s)
    tmp = re.sub(r'\d','',tmp)
    tmp = tmp.lower()
    res = tmp.split()
    return res

def chunkize(t,n):
    idx = range(0,len(t)+1,n)
    res = []
    for i in idx:
        if i == len(idx):
            res.append(t[i:-1])
        else:
            res.append(t[i:i+n])
    return res

from afinn import Afinn
from numpy import sum
def sent_list(textl):
    afinn = Afinn(language='en')
    sent_vec = []
    for t in textl:
        t_vec = []
        for s in t:
            t_vec.append(afinn.score(s))
        sent_vec.append(sum(t_vec))
    return sent_vec
        

file = 'Pan.txt'
f = io.open(file,'r',encoding = 'utf8')
text = f.read()
strt = '*** START OF THIS PROJECT GUTENBERG EBOOK PETER PAN ***'
end = 'End of the Project Gutenberg EBook of Peter Pan, by James M. Barrie'
idx = text.find(strt)
idx1 = idx+len(strt)+1
idx2 = text.find(end)
content = text[idx1:idx2]

tokens = pp_token(content)
chunks = chunkize(tokens,500)
sent_scr = sent_list(chunks)
plt.bar(range(1,len(sent_scr)+1),sent_scr)

### scale to multiple documents
import re
file = '/home/kln/Desktop/http:_www.gutenberg.org_ebooks_search_?query=peter+pan.html'
text = open(file, "rw+").read()
pat = r'http://www.gutenberg.org/ebooks/+\d+'
s = 'http://www.gutenberg.org/files/'
s2 = 'http://www.gutenberg.org/cache/epub/'
urls = []
urls_alt = []
for m in re.finditer(pat,text):
    tmp = text[m.start():m.end()]
    d = re.search('\d+',tmp)
    #urls.append(tmp+'/'+d.group()+'-0.txt')
    urls.append(s+d.group()+'/'+d.group()+'-0.txt')
    #urls.append(text[m.start():m.end()])
    urls_alt.append(s2+d.group()+'/pg'+d.group()+'.txt')

def download_corpus(urls):
    res = []
    title = []
    for i in range(len(urls)):
        try:
            call = urllib2.urlopen(urls[i])
        except:
            pass
            print 'HTTPerror'
        else:
            res.append(call.read())
            #title.append(urls[i])
            title.append(urls[i][urls[i].find('pg'):len(urls[i])])
    return res, title

corpus, title = download_corpus(urls_alt)

# write to folder
os.mkdir('corpus')
os.chdir('/home/kln/Desktop/web_dm/corpus')
for i in range(len(corpus)):
    with open(title[i], "w") as text_file:
        text_file.write(corpus[i])
    

    
# randomize interval
import random, time
print("download file 0")
time.sleep(random.random()*10)
print("download file 1")

for i in range(5):
    print 'download file: '+str(i)
    time.sleep(random.random()*10)