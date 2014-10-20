# -*- coding: utf-8 -*-

# @version 1.0
# @author Nayelli Valeria Pérez Corona
# @date 20/10/2014
# This module allows to train a ner from a text file with a corpus of annotated sentences.
# Tested with Python 2.7 and Windows 7




from mitie.mitie import *
import codecs
import re

##Regular expression to find class in a token
cl_ptn = r"(?P<clase>]?\\[a-zA-Z]+)"



##Must call this function for train with a corpus
# @param corpus is the directory to the corpus file. Ex:"C:\\corpus_example.txt"
# @param model file name to saving the model
def train_from_corpus(corpus,model):
    trainer = ner_trainer("MITIE-models\\english\\total_word_feature_extractor.dat")
    with codecs.open(corpus, "rU", encoding='utf-8') as f:
        for line in f:
            print( line)
            sample = __getSample(line, trainer)
            trainer.add(sample)
    f.close()
    trainer.num_threads = 4
    ner = trainer.train()
    ner.save_to_disk(model)
    printInfo(ner)


## Print the info and results for a test
def printInfo(ner):
    print "tags:", ner.get_possible_ner_tags()
    # Now let's make up a test sentence and ask the ner object to find the entities.
    tokens = ["I", "met", "with", "John", "Becker", "at", "HBU", "."]
    entities = ner.extract_entities(tokens)
    # Happily, it found the correct answers, "John Becker" and "HBU" in this case which we
    # print out below.
    print "\nEntities found:", entities
    print "\nNumber of entities detected:", len(entities)
    for e in entities:
        range = e[0]
        tag = e[1]
        entity_text = " ".join(tokens[i] for i in range)
        print "    " + tag + ": " + entity_text


##Line must be annotated as word\CLASS or [word1 word2 ... wordn]\ORG for multi word.
# Example:
# My name is [Davis King]\PER and I-PER work for MIT\ORG.
# @param line annotated sentence to add
def __getSample(line, trainer):
    clean, words = __chunkSentence(line)
    sample = ner_training_instance(clean)
    i=0
    fl = False
    for w in words:
        if "[" in w:
            i = words.index(w)
            fl= True
        m = re.search(cl_ptn, w)
        if m!=None:
            j = words.index(w)
            cl= (m.group("clase").replace("\\","")).replace("]","")
            if fl:
                sample.add_entity(xrange(i,j+1),cl)
                print(cl+":"+str(i)+","+str(j+1))
            else:
                sample.add_entity(xrange(j,j+1),cl)
                print(cl+":"+str(j)+","+str(j+1))
            fl = False
    return sample

##tokenize the sentence
# @param line sentence to be tokenized
# @return li list with tokens
def __chunkSentence(line):
    w =""
    li = []
    cl = []
    punctuation = [u'?',u'¿',u'!',u'¡',u'.',u',',u';',u':']
    for c in line:
        if c == " ":
            li.append(w)
            cl.append(__scapeWord(w))
            w=""
        elif c in punctuation:
            li.append(w)
            cl.append(__scapeWord(w))
            w=""
            li.append(c)
            cl.append(c)
        else:
            w+=c
    return cl,li

## Remove meta-language for
def __scapeWord(w):
    if "[" in w:
        w = w.replace("[","")
    if "\\" in w:
        w = w.replace("]","")
        w = w.replace(re.search(cl_ptn,w).group("clase"),"")
    return w
