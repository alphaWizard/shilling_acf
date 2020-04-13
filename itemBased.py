import numpy as np
import scipy.stats
import scipy.spatial
# from sklearn.cross_validation import KFold
import random
from sklearn.metrics import mean_squared_error
from math import sqrt
import math
import warnings
import sys 
import csv
#from sklearn.utils.extmath import np.dot

warnings.simplefilter("ignore")

# users = 943
items = 1682

def readingFile(filename):
	f = open(filename,"r")
	data = []
	for row in f:
		r = row.split(',')
		e = [int(r[0]), int(r[1]), float(r[2])]
		data.append(e)
	return data

def similarity_item(data,mode='default',bots=30):
	# print("Hello")
	#f_i_d = open("sim_item_based.txt","w")
	item_similarity_cosine = np.zeros((items,items))
	item_similarity_jaccard = np.zeros((items,items))
	item_similarity_pearson = np.zeros((items,items))
	for item1 in range(items):
		# print(item1)
		for item2 in range(items):
			if np.count_nonzero(data[:,item1]) and np.count_nonzero(data[:,item2]):
				item_similarity_cosine[item1][item2] = 1-scipy.spatial.distance.cosine(data[:,item1],data[:,item2])
				# item_similarity_jaccard[item1][item2] = 1-scipy.spatial.distance.jaccard(data[:,item1],data[:,item2])
				# try:
				# 	if not math.isnan(scipy.stats.pearsonr(data[:,item1],data[:,item2])[0]):
				# 		item_similarity_pearson[item1][item2] = scipy.stats.pearsonr(data[:,item1],data[:,item2])[0]
				# 	else:
				# 		item_similarity_pearson[item1][item2] = 0
				# except:
				# 	item_similarity_pearson[item1][item2] = 0

			#f_i_d.write(str(item1) + "," + str(item2) + "," + str(item_similarity_cosine[item1][item2]) + "," + str(item_similarity_jaccard[item1][item2]) + "," + str(item_similarity_pearson[item1][item2]) + "\n")
	#f_i_d.close()
	return item_similarity_cosine, item_similarity_jaccard, item_similarity_pearson

def crossValidation(data,mode='default',bots=30):
	# k_fold = KFold(n=len(data), n_folds=10)
	if mode == 'attack':
		users = 943 + bots
	else:
		users = 943

	Mat = np.zeros((users,items))
	for e in data:
		Mat[e[0]-1][e[1]-1] = e[2]

	sim_item_cosine, sim_item_jaccard, sim_item_pearson = similarity_item(Mat,mode=mode,bots=bots)
	#sim_item_cosine, sim_item_jaccard, sim_item_pearson = np.random.rand(items,items), np.random.rand(items,items), np.random.rand(items,items) 

	return Mat, sim_item_cosine


def predictRating(recommend_data,resultfile='result_item_based_before_attack.csv',mode='default',bots=30):

	M, sim_item = crossValidation(recommend_data,mode=mode,bots=bots)

	#f = open("toBeRated.csv","r")
	f = open(sys.argv[2],"r")
	toBeRated = {"user":[], "item":[]}
	for row in f:
		r = row.split(',')	
		toBeRated["item"].append(int(r[1]))
		toBeRated["user"].append(int(r[0]))

	f.close()

	pred_rate = []

	#fw = open('result2.csv','w')
	fw_w = open(resultfile,'w')  #resultfile --predicted rating
	csvwriter = csv.writer(fw_w)

	l = len(toBeRated["user"])
	for e in range(l):
		user = toBeRated["user"][e]
		item = toBeRated["item"][e]

		pred = 3.0

		#item-based
		if np.count_nonzero(M[:,item-1]):
			sim = sim_item[item-1]
			ind = (M[user-1] > 0)
			#ind[item-1] = False
			normal = np.sum(np.absolute(sim[ind]))
			if normal > 0:
				pred = np.dot(sim,M[user-1])/normal

		if pred < 0:
			pred = 0

		if pred > 5:
			pred = 5

		pred_rate.append(pred)
		# print(str(user) + "," + str(item) + "," + str(pred))
		#fw.write(str(user) + "," + str(item) + "," + str(pred) + "\n")
		# fw_w.write(str(pred) + "\n")
		csvwriter.writerow([int(user),int(item),float(pred)])

	#fw.close()
	fw_w.close()

if __name__ == "__main__":

	#recommend_data = readingFile("ratings.csv")
	recommend_data = readingFile(sys.argv[1])
	#crossValidation(recommend_data)
	mode = sys.argv[3] #attack or default
	resultfile = sys.argv[4]
	if len(sys.argv) > 5:
		bots=int(sys.argv[5])
	else:
		bots = 30
	predictRating(recommend_data,resultfile=resultfile,mode=mode,bots=bots)

	if mode == 'attack':
		print('Applied prediction on the attacked database...')
	else:
		print('Applied prediction on normal database...')
