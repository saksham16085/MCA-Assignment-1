# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17vBVYwC_SLjRY8LIgdWqQIGvMOSs07PD
"""

#from google.colab import drive
#drive.mount('/gdrive')

#%cd /gdrive/My\ Drive/MCA\ Ass\ 1/

from PIL import Image
from google.colab.patches import cv2_imshow
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin
from sklearn.datasets import load_sample_image
from sklearn.utils import shuffle
import os
import pickle as pkl
import datetime
from operator import itemgetter

def getNeighbours(x,y,dist,h,w):
  neighbours = []
  final = []
  for i in range(-dist+1,dist):
    if(valid([x-dist,y+i],h,w)):
      neighbours.append([x-dist,y+i])
    if(valid([x+dist,y+i],h,w)):
      neighbours.append([x+dist,y+i])
    if(valid([x+i,y-dist],h,w)):
      neighbours.append([x+i,y-dist])
    if(valid([x+i,y+dist],h,w)):
      neighbours.append([x+i,y+dist])
  if(valid([x-dist,y-dist],h,w)):
    neighbours.append([x-dist,y-dist])
  if(valid([x-dist,y+dist],h,w)):
    neighbours.append([x-dist,y+dist])
  if(valid([x+dist,y-dist],h,w)):
    neighbours.append([x+dist,y-dist])
  if(valid([x+dist,y+dist],h,w)):
    neighbours.append([x+dist,y+dist])
  return neighbours
def valid(i,h,w):
  if i[0]<0 or i[0]>h-1:
    return False
  if i[1]<0 or i[1]>w-1:
    return False
  return True

directory = 'HW-1/images/'
count = 0
# a = datetime.datetime.now()
# for filename in os.listdir(directory):
#   count +=1
#     b = datetime.datetime.now()
#     img = cv2.imread(directory+filename)
#     h = int(img.shape[0]*0.15)
#     w = int(img.shape[1]*0.15)
#     img = cv2.resize(img,(w,h))
#     cm = np.unique(img.reshape(-1, img.shape[2]), axis=0)
#     k = [1,3,5,7]
#     correlogram = {}
#     for m in cm:
#       tupl = (m[0],m[1],m[2])
#       correlogram[tupl] =[]
#     for dist in k:
#       color = {}
#       map = {}
#       for m in cm:
#         tupl = (m[0],m[1],m[2])
#         map[tupl] =0
#         color[tupl] = 0
#       for i in range(img.shape[0]):
#         for j in range(img.shape[1]):
#           ci = img[i][j]
#           image_tuple = (ci[0],ci[1],ci[2])
#           Cn = getNeighbours(i,j,dist,h,w)
#           color[(ci[0],ci[1],ci[2])]+=1
#           for neighbour_point in Cn:
#             neighbour_pixel = img[neighbour_point[0]][neighbour_point[1]]
#             ntuple = (neighbour_pixel[0],neighbour_pixel[1],neighbour_pixel[2])
#             if (image_tuple== ntuple):
#               map[image_tuple]+=1
#       for m in cm:
#         tup = (m[0],m[1],m[2])
#         correlogram[tup].append(float(map[tup])/(color[tup]*8*dist))
#     megaCorrelogram[filename] = correlogram
#     c = datetime.datetime.now()
#     delta1 = c-a
#     delta2 = c-b
#     print('Current image no: '+str(count)+"\t time for image "+str(count)+" : "+str(delta2)+"\t Total time elapsed : "+str(delta1)+"\t size : "+str(len(megaCorrelogram)))
#     if(count%500 == 0):
#       print('saving features ' +str(count-500)+'-'+str(count)+' Correlogram')
#       pkl.dump(megaCorrelogram,open('features ' +str(count-500)+'-'+str(count)+' Correlogram','wb'))
#       megaCorrelogram = {}

# pkl.dump(megaCorrelogram,open('features 5000-5063 Correlogram','wb'))



features = pkl.load(open('images_pkl_file_name','rb'))
directory_query = 'HW-1/train/query/'
directory_feature = 'question_1_features/'
count = 0
query_count = 0
similarity = {}
avg_precision = [0.0,0.0,0.0]
avg_recall =[0.0,0.0,0.0]

directory_ground_truth = 'HW-1/train/ground_truth/'
filers = ['ok.txt','good.txt','junk.txt']
filers_trim = ['ok','good','junk']
files_read = {}

for i in os.listdir(directory_query):
  precision = [0.0,0.0,0.0]
  recall = [0.0,0.0,0.0]
  query = ''
  query_count+=1
  files_read[i] = {}
  abc = i.split('_')[:-1]
  filename = ''
  value = 0
  for v in abc:
    filename+=v+'_'
  for a in range(len(filers)):
    files_read[i][filers_trim[a]] = []
    file_txt = open(directory_ground_truth+filename+filers[a],'r')
    text_text = file_txt.read().split('\n')
    text = len(text_text)-1
    for f in text_text:
      files_read[i][filers_trim[a]].append(f+'.jpg')

    value+=text
    file_txt.close()
  files_read[i]['total'] = value

  file = open(directory_query+i,'r')
  line = file.readline().split(' ')[0].split('_')
  for n in line[1:]:
    query += n+'_'
  query = query[:-1]+'.jpg'
  similarity[query] = {}
  feature = pkl.load(open(directory_feature+features[query],'rb'))
  feature_query = feature[query]
  for j in os.listdir(directory_feature):
    feature_each = pkl.load(open(directory_feature+j,'rb'))
    for q in feature_each:
      count+=1
      if(count%500 == 0):
        print(query_count,count)
      k = feature_each[q]
      lista = {}
      for l in feature_query:
        if(l not in lista):
          lista[l] = [feature_query[l]]
        else:
          lista[l].append(feature_query[l])
      for l in k:
        if(l not in lista):
          lista[l] = [k[l]]
        else:
          lista[l].append(feature_query[l])

      dist = 0
      for l in lista:
        if(len(lista[l])==2):
          val1 = lista[l][0]
          val2 = lista[l][1]
          for m in range(4):
            dist+= (abs(val1[m]-val2[m])/(val1[m]+val2[m]+1))
        else:
          val1 = lista[l][0]
          for m in range(4):
            dist+= (abs(val1[m])/(val1[m]+1))
      similarity[query][q] = dist/len(lista)
  res = dict(sorted(similarity[query].items(), key = itemgetter(1), reverse = True)[:value]).keys()
  for t in range(len(filers_trim)):
    for c in files_read[i][filers_trim[t]]:
      if c in res:
        precision[t]+=1/value
        recall[t]+=1/len(files_read[i][filers_trim[t]])
    avg_precision[t]+=precision[t]
    avg_recall[t]+=avg_recall[t]

  print(avg_precision/query_cohdunt,avg_recall/query_count)
  print(precision,recall)
  print(value)
  print(similarity)
  file.close()