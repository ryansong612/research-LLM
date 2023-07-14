#!/usr/bin/env python
# coding: utf-8

# In[39]:


# Import Modules#
import pandas as pd
import numpy as np
import tensorflow_hub as hub
import matplotlib.pyplot as plt

# In[55]:


# Read Chemistry abstract title data from desktop#
# Input txt file#
with open('C:/Users/13122/Desktop/data/Crawled Articles.txt', 'r') as file:
    text = file.read()
lines = text.split('\n\n')
lines.pop(-1)
# convert txt file into readable json form#
documents = []
for i in range(0, len(lines), 3):
    title_parts = lines[i].split(': ')
    title = ': '.join(title_parts[1:]).strip()
    title = title.replace("\n", "")
    abstract_parts = lines[i + 1].split(': ')
    abstract = ': '.join(abstract_parts[1:]).strip()
    abstract = abstract.replace("\n", " ")
    document = {"title": title,
                "abstract": abstract
                }
    documents.append(document)


# output: [dict{"title":, "abstract":}] length is number of articles#

# define embedding calculation function#
# Input: list ["Tom is a good boy.", "Diana is a bad girl."]#
def embed_sentences(sentences):
    # Load the Universal Sentence Encoder module
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(module_url)
    # Generate embeddings for the sentences
    embeddings = model(sentences)
    return embeddings


# Output number of numpy arrays(2 in this case) of shape(1,512) dtype=float32#


# define similarity calculation function based on dot product#
# Input two numpy array output from embed_sentences#
def compute_similarity(embedding1, embedding2):
    # Compute cosine similarity between two embeddings
    similarity = np.dot(embedding1, embedding2)
    return similarity


# convert documents into sentence split form for more convenient data analyzing#
documents_split_sentence = [{"title": i["title"].split(". "), "abstract": i["abstract"].split(". ")}
                            for i in documents]

# In[56]:


# code in last meeting#
query = str(input('Enter query: '))
query_vec = embed_sentences([query])
test = [documents[i]["title"] + " " + documents[i]["abstract"] for i in
        range(len(documents))]  # combine all of #
embed = embed_sentences(test)
simi1 = {i: compute_similarity(query_vec, embed[i]) for i in range(len(embed))}

# In[ ]:


# find the max simi value#
maximum = 0
idx = 0
counter = 0

for sim in simi1.values():
    if sim[0] > maximum:
        maximum = sim[0]
        idx = counter
    counter += 1


# In[ ]:


def SearchPaper(keySentence):
    global documents
    results = []
    no = 0
    while no < len(documents):
        content = documents[no]["abstract"] + documents[no]["title"]
        search = content.find(keySentence)
        if search != -1:
            results.append(no)
        no += 1

    print("Identified these papers (id):")
    msg = "id: {id}\ntitle: {title}\nabstract:\n{abstract}"
    for id in results:
        title = documents[id]['title']
        abstract = documents[id]['abstract']
        print(msg.format(id=id, title=title, abstract=abstract))


# Example: SearchPaper("Deep-symphysis")#


# In[ ]:


# Code Tony wrote on the plane about compare title_embedding with average embedding of the first article#
# data analysis on the first data: compute embedding vectors#
test_1 = documents_split_sentence[0]
title_1 = test_1["title"]
abstract_1 = test_1["abstract"]
input_1 = title_1 + abstract_1
embed_test1 = embed_sentences(input_1)

# get average vector of test1#
embed_test1 = np.array(embed_test1)
average_vec1 = embed_test1.sum(axis=0) / embed_test1.shape[0]

# compare with title#
simi1_1 = compute_similarity(embed_test1[0], average_vec1)
simi1_1

# In[57]:


# Code Tony wrote on the plane about kmeans#
# convert every sentence in data to be embedding vectors#
data_list = []
for index in range(len(documents_split_sentence)):
    data_list.append([index, documents_split_sentence[index]["title"][0]])
    sentence_index = 0
    while sentence_index < len(documents_split_sentence[index]["abstract"]):
        data_list.append([index, documents_split_sentence[index]["abstract"][sentence_index]])
        sentence_index += 1

data_array = np.array(data_list)
data_array_content = data_array[:, 1]
data_embed = embed_sentences(list(data_array_content))
data_embed_array = np.array(data_embed)
data_embed_list = list(data_embed_array)
for i in range(data_array.shape[0]):
    data_list[i][1] = list(data_embed_list[i])
data_list_array = np.array(data_list)


def article_embed_find(index):
    list = []
    for i in range(len(data_list)):
        if data_list[i][0] == index:
            list.append(data_list[i][1])
    return list


test4 = article_embed_find(0)
test4 = np.array(test4)
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans.fit(test4)
label_pred = kmeans.labels_
centeroid = kmeans.cluster_centers_
print(centeroid)
print(label_pred)


# In[12]:


# Code Tony wrote on the plane#
def compare_title_mean(index):
    test = documents_split_sentence[index]
    title = test["title"]
    abstract = test["abstract"]
    input_ = title + abstract
    embed_test = embed_sentences(input_)
    embed_test = np.array(embed_test)
    average_vec = embed_test.sum(axis=0) / embed_test.shape[0]
    simi = compute_similarity(embed_test[0], average_vec)
    return simi


result = []
for i in range(len(documents)):
    input_ = [j[1] for j in data_list if j[0] == i]
    input_arr = np.array(input_)
    m = input_arr.sum(axis=0)
    vec_ave = m / input_arr.shape[0]
    simi = compute_similarity(input_[0], list(vec_ave))
    result.append(simi)
plt.plot(result)


# In[ ]:


# Code Tony wrote at home #
def kmeans_analysis(index):
    list = []
    for i in range(len(data_list)):
        if data_list[i][0] == index:
            list.append(data_list[i][1])
    test = np.array(list)
    for j in [2, 3, 4, 5, 6]:
        kmeans = KMeans(n_clusters=j, random_state=42, n_init=10)
        kmeans.fit(test)
        label_pred = kmeans.labels_
        print("cluster is {}; label is {}".format(j, label_pred))
