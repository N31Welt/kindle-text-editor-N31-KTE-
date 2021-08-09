#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os import path as osp
from codecs import open as cds_open

from math import log
from cPickle import load as mrsh_load
from cPickle import dump as mrsh_dump
from itertools import product
sys.setcheckinterval(1287)

class PY_IME:    #
    __slot__ = ('py_freq', 'p2c', 'chn_freq', 'min_freq')
    def __init__(self):        #
        self.py_freq= {}
        self.p2c = {}
        self.chn_freq = {}
        self.min_freq = None
        DATA_PATH = osp.join(osp.dirname(osp.abspath(__file__)),    'data/pinyin_final.txt')        #
        CACHE_PATH = osp.join(osp.dirname(osp.abspath(__file__)),   'data/pinyin.cache')            #
        try:        # t_start = time.time()
            with file(CACHE_PATH,'rb') as cache_file:  self.p2c,self.chn_freq,self.py_freq,self.min_freq = mrsh_load(cache_file)       #marshal.load(cache_file)
        except IOError: #lines = []
            with cds_open(DATA_PATH,encoding='utf-8') as txt: lines = txt.readlines()
            for line in lines:
                #
                word,py,freq = line.rstrip().split('\t')
                freq = int(freq)
                plain_py = py.replace(" ","")
                self.chn_freq[word] = self.chn_freq.get(word,0)+freq
                self.py_freq[plain_py] = self.py_freq.get(plain_py,0)+freq
                if not plain_py in self.p2c: self.p2c[plain_py] = []
                self.p2c[plain_py].append((freq,word))
                py_array = py.split(" ")
                py_short = [x[0] for x in py_array]
                if len(py_array)<=6:
                    for ip in product(*zip(py_array,py_short)):
                        initial_py = "".join(ip)
                        self.py_freq[initial_py] = self.py_freq.get(initial_py,0) + max(int(log(freq)),1)
                        if not initial_py in self.p2c: self.p2c[initial_py] = []
                        self.p2c[initial_py].append((freq,word))        #lines = None
            self.p2c  = dict( ( k,tuple( w[1] for w in sorted(v,reverse=1) ) ) for k,v in self.p2c.iteritems())
            total = sum(self.chn_freq.itervalues())
            self.chn_freq = dict( (k,log(float(v)/total)) for k,v in self.chn_freq.iteritems() )
            self.py_freq  = dict( (k,log(float(v)/total)) for k,v in self.py_freq.iteritems()  )
            self.min_freq = min(self.py_freq.values())
            with file(CACHE_PATH,'wb') as cache_file: mrsh_dump((self.p2c,self.chn_freq,self.py_freq,self.min_freq),cache_file, protocol=2)       #marshal.dump((self.p2c,self.chn_freq,self.py_freq,self.min_freq),cache_file)

    def word_rank(self, word):        #
        single_letters = frozenset(['a', 'c', 'b', 'e', 'd', 'g', 'f', 'i', 'h', 'k', 'j', 'm', 'l', 'o', 'n', 'q', 'p', 's', 'r', 'u', 't', 'w', 'v', 'y', 'x', 'z'])
        if word in single_letters: return self.min_freq-1.0
        elif len(word)==1: return 0.0
        return self.py_freq.get(word,self.min_freq*20.0)

    def dp_cut(self, sentence,topK=3):
        max_word_len=20
        path = {}
        N = len(sentence)
        path[N] = [ [] ]
        for i in xrange(N-1,-1,-1):
            path[i] = []
            for hop in xrange(i+1,min(i+max_word_len+1,N+1)):
                if (hop-i==1) or (sentence[i:hop] in self.py_freq):
                    for pt in path[hop]: path[i].append([sentence[i:hop]] + pt)
                path[i] = sorted(path[i],key=lambda L:sum(self.word_rank(x) for x in L), reverse=1)[:topK]
        return path[0]

    def all_combine_idx(self, m,idx,tb):
        if idx==len(m)-1:
            for i in xrange(0,len(m[idx])):
                if tb['n']>1500: return          #
                yield [i]
                tb['n']=tb.get('n',0)+1
        else:
            for w in xrange(0,len(m[idx])):
                if tb['n']>1500: return             #
                for sub in self.all_combine_idx(m,idx+1,tb):
                    if tb['n']>1500: return         #
                    yield [w]+sub

    def chn_rank(self, word):
        q = self.chn_freq.get(word,self.min_freq*20)
        return q

    def all_combine(self, m,idx):
        tb = {'n':0}
        all_index_list = sorted(self.all_combine_idx(m,idx,tb),key=lambda L: sum(self.chn_rank(m[i][j]) for i,j in enumerate(L) ) ,reverse=1)
        if len(m)>1: all_index_list = all_index_list[:16]        #
        for column in all_index_list: yield "\n".join(m[i][column[i]] for i in xrange(len(m)))

    def guess_words_no_sort(self, sentence):
        if len(sentence)>0:
            bucket = {}
            showed = 0
            for py_list in self.dp_cut(sentence):
                sub_showed = 0
                if showed>=16: break                            #
                m=[]
                for p in py_list:
                    if len(p)<6:
                        if len(py_list)==1: span = 1500         #
                        else:    span = 6
                    else:    span = 3
                    m.append( self.p2c.get(p,[p])[:span] )
                for c in self.all_combine(m,0):
                    stripped = c.replace("\n","")
                    if sub_showed>=16/2: break                  #
                    if not stripped in bucket:
                        yield c
                        bucket[stripped]=1
                        if len(c)>1:
                            showed+=1
                            sub_showed+=1
                        if sub_showed>=16/2: break              #
            del bucket

    def guess_words(self, sentence):
        result = self.guess_words_no_sort(sentence)
        st_list = sorted( [(sum(self.chn_rank(word) for word in s.split('\n')),s) for s in result], reverse=1)
        return [x[1].replace("\n",'') for x in st_list]
