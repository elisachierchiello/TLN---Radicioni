import pandas as pd
from nltk.corpus import wordnet
from itertools import product
import math

depthMax = 20

df = pd.read_csv("WordSim353/WordSim353.csv")

# def get_hyperonyms2(synset):
#     hyperonyms=[]
#     for hyperonym in synset.hypernyms():
#         hyperonyms.append(hyperonym)
#     return hyperonyms

def get_hyperonyms(synset_list):
    hyperonyms=[]
    for synset in synset_list:
        for hyperonym in synset.hypernyms():
            hyperonyms.append(hyperonym)
    return hyperonyms

def get_depth(w):
    depth = 0
    next_hyper = w
    while(next_hyper != w.root_hypernyms()[0] and len(next_hyper.hypernyms())!=0):
        depth += 1
        next_hyper = next_hyper.hypernyms()[0]
    return depth

# def lcs2(syns1, syns2):
#     hypers1 = [syns1]
#     hypers2 = [syns2]
#     intersection = list(set(hypers1) & set(hypers2))
#     #print(intersection)
#     supp_list1=[syns1]
#     supp_list2=[syns2]
#     while len(intersection)==0:
#         for syn1 in supp_list1:
#             supp_list1 = get_hyperonyms2(syn1)
#             hypers1.extend(supp_list1)
#         #print(hypers1)
#         for syn2 in supp_list2:
#             supp_list2= get_hyperonyms2(syn2)
#             hypers2.extend(supp_list2)
#         #print(hypers2)
#         intersection = list(set(hypers1) & set(hypers2))
#         if len(supp_list1)==0 and len(supp_list2) == 0 and len(intersection) == 0:
#             break
#     return intersection

def lcs(syns1, syns2):
    hypers1 = [syns1]
    hypers2 = [syns2]
    intersection = list(set(hypers1) & set(hypers2))
    #print(intersection)
    supp_list1=[syns1]
    supp_list2=[syns2]
    while len(intersection)==0:
        if len(supp_list1)>0:
            supp_list1 = get_hyperonyms(supp_list1)
        #print(hypers1)
        if len(supp_list2)>0:
            supp_list2 = get_hyperonyms(supp_list2)
        #print(hypers2)
        hypers1.extend(supp_list1)
        hypers2.extend(supp_list2)
        intersection = list(set(hypers1) & set(hypers2))
        if len(supp_list1)==0 and len(supp_list2) == 0 and len(intersection) == 0:
            break
    return intersection
    

#Wu & Palmer
def wu_palmer_similarity(w1, w2):
    #res = w1.lowest_common_hypernyms(w2)
    res = lcs(w1, w2)
    depth  = 0
    if len(res) != 0:
        result = res[0]
        depth = get_depth(result)

    depth1 = get_depth(w1)
    depth2 = get_depth(w2)

    if depth1 != 0 and depth2 != 0:
        similarity = 2*depth/(depth1+depth2)
    else:
        similarity=0
    
    return similarity


# def WuAndPalmer(w1, w2):
#     syn1 = wordnet.synsets(w1)
#     syn2 = wordnet.synsets(w2)
#     max = 0
#     sim = 0
#     for syn in syn1:
#         for sy in syn2:
#             sim = Similarity(syn, sy)
#             if sim>max:
#                 max = sim
#     return max
    


def get_length_lcs(s, lcs_s1_s2):
    length =0
    next_hyper = s
    while(next_hyper != lcs_s1_s2[0] and len(next_hyper.hypernyms())!=0):
        length += 1
        next_hyper = next_hyper.hypernyms()[0]
    return length

def get_length(s1, s2):
    lcs_s1_s2 = lcs(s1, s2)
    if len(lcs_s1_s2)==0:
        return 2*depthMax
    else:
        return get_length_lcs(s1, lcs_s1_s2) + get_length_lcs(s2, lcs_s1_s2) 

#Shortest Path 
def shortest_path_similarity(s1,s2):
    length=get_length(s1, s2)
    simpath=2*depthMax-length
    return simpath


#Leeckock & Chodorow
def leakcock_chodorow_similarity(w1, w2):
    len = get_length(w1, w2)
    len_wo_errors = len+1
    return -math.log(len_wo_errors/((2*depthMax)+1))


# def shorterst_path(w1,w2):
#     syn1 = wordnet.synsets(w1)
#     syn2 = wordnet.synsets(w2)
#     max = 0
#     sim = 0
#     for syn in syn1:
#         for sy in syn2:
#             sim = shorterst_path_similarity(syn, sy)
#             if sim>max:
#                 max = sim
#     return max


def terms_similarity(method, w1, w2):
    syn1 = wordnet.synsets(w1)
    syn2 = wordnet.synsets(w2)
    max = 0
    sim = 0
    for syn in syn1:
        for sy in syn2:
            sim = method(syn, sy)
            if sim>max:
                max = sim
    return max

#print(WuAndPalmer(word1, word2))
#print(shorterst_path(word1, word2))

def correlation_calculus(method):
    lista = []
    pearson = 0
    spearman = 0
    for i in range(len(df)):
        lista.append(terms_similarity(method,df.iloc[i][0], df.iloc[i][1]))

    if method == wu_palmer_similarity:
        df['wu_palmer_similarity'] = lista
        pearson = df['Human (mean)'].corr(df['wu_palmer_similarity'], method='pearson')
        spearman = df['Human (mean)'].corr(df['wu_palmer_similarity'], method='spearman')
    if method == shortest_path_similarity:
        df['shortest_path_similarity'] = lista
        pearson = df['Human (mean)'].corr(df['shortest_path_similarity'], method='pearson')
        spearman = df['Human (mean)'].corr(df['shortest_path_similarity'], method='spearman')
    if method == leakcock_chodorow_similarity:
        df['leakcock_chodorow_similarity'] = lista
        pearson = df['Human (mean)'].corr(df['leakcock_chodorow_similarity'], method='pearson')
        spearman = df['Human (mean)'].corr(df['leakcock_chodorow_similarity'], method='spearman')

    #series = pd.Series(list)
    #pearson = df['Human (mean)'].corr(series, method='pearson')
    #spearman = df['Human (mean)'].corr(series, method='spearman')
    return df, pearson, spearman

print()    
print("Wu & Palmer similarity results")
print(correlation_calculus(wu_palmer_similarity)[0])
print("Its Pearson correlation coefficient")
print(correlation_calculus(wu_palmer_similarity)[1])
print("Its Spearman's rank correlation coefficient")
print(correlation_calculus(wu_palmer_similarity)[2])

print()
print("Shortest Path similarity results")
print(correlation_calculus(shortest_path_similarity)[0])
print("Its Pearson correlation coefficient")
print(correlation_calculus(shortest_path_similarity)[1])
print("Its Spearman's rank correlation coefficient")
print(correlation_calculus(shortest_path_similarity)[2])

print()
print("Leakcock and Chodorow similarity results")
print(correlation_calculus(leakcock_chodorow_similarity)[0])
print("Its Pearson correlation coefficient")
print(correlation_calculus(leakcock_chodorow_similarity)[1])
print("Its Spearman's rank correlation coefficient")
print(correlation_calculus(leakcock_chodorow_similarity)[2])
