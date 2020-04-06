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

def userData(mode='default'):
	filename = sys.argv[3]
	if mode == 'attack':
		users = 943 + 30
	else:
		users = 943
	f = open(filename,"r")
	data = np.zeros((users,3))
	for row in f:
		r = row.strip().split(',')
		if r[1] == "M" or r[1] == "m":
			data[int(r[0])-1] = [1,(int(r[2])/56.0),((int(r[3])+1.0)/21.0)]
		else:
			data[int(r[0])-1] = [0,(int(r[2])/56.0),((int(r[3])+1)/21.0)]

	return data


def itemData():
	filename = sys.argv[4]
	f = open(filename,"r")
	data = np.zeros((items,18))
	genre = {"Action":0, "Adventure":1, "Animation":2, "Children's":3, "Comedy":4, "Crime":5, "Documentary":6, "Drama":7, "Fantasy":8, "Film-Noir":9, "Horror":10, "Musical":11, "Mystery":12, "Romance":13, "Sci-Fi":14, "Thriller":15, "War":16, "Western":17 }
	for row in f:
		r = row.split(',')
		g = r[len(r)-1].split('|')
		for e in g:
			if e.strip() not in genre.keys():
				continue
			else:
				data[int(r[0])-1][genre[e.strip()]] = 1

	return data

def similarity_item(data,mode='default'):
	# print("Hello Item")
	#f_i_d = open("sim_item_hybrid.txt","w")
	item_similarity_cosine = np.zeros((items,items))
	item_similarity_jaccard = np.zeros((items,items))
	item_similarity_pearson = np.zeros((items,items))
	for item1 in range(items):
		print(item1)
		for item2 in range(items):
			if np.count_nonzero(data[item1]) and np.count_nonzero(data[item2]):
				item_similarity_cosine[item1][item2] = 1-scipy.spatial.distance.cosine(data[item1],data[item2])
				# item_similarity_jaccard[item1][item2] = 1-scipy.spatial.distance.jaccard(data[item1],data[item2])
				# try:
				# 	if not math.isnan(scipy.stats.pearsonr(data[item1],data[item2])[0]):
				# 		item_similarity_pearson[item1][item2] = scipy.stats.pearsonr(data[item1],data[item2])[0]
				# 	else:
				# 		item_similarity_pearson[item1][item2] = 0
				# except:
				# 	item_similarity_pearson[item1][item2] = 0

			#f_i_d.write(str(item1) + "," + str(item2) + "," + str(item_similarity_cosine[item1][item2]) + "," + str(item_similarity_jaccard[item1][item2]) + "," + str(item_similarity_pearson[item1][item2]) + "\n")
	#f_i_d.close()
	return item_similarity_cosine, item_similarity_jaccard, item_similarity_pearson


def similarity_user(data,mode='default'):
	# print("Hello User")
	if mode == 'attack':
		users = 943 + 30
	else:
		users = 943
	#f_i_d = open("sim_user_hybrid.txt","w")
	user_similarity_cosine = np.zeros((users,users))
	user_similarity_jaccard = np.zeros((users,users))
	user_similarity_pearson = np.zeros((users,users))
	for user1 in range(users):
		print(user1)
		for user2 in range(users):
			if np.count_nonzero(data[user1]) and np.count_nonzero(data[user2]):
				user_similarity_cosine[user1][user2] = 1-scipy.spatial.distance.cosine(data[user1],data[user2])
				# user_similarity_jaccard[user1][user2] = 1-scipy.spatial.distance.jaccard(data[user1],data[user2])
				# try:
				# 	if not math.isnan(scipy.stats.pearsonr(data[user1],data[user2])[0]):
				# 		user_similarity_pearson[user1][user2] = scipy.stats.pearsonr(data[user1],data[user2])[0]
				# 	else:
				# 		user_similarity_pearson[user1][user2] = 0
				# except:
				# 	user_similarity_pearson[user1][user2] = 0

			#f_i_d.write(str(user1) + "," + str(user2) + "," + str(user_similarity_cosine[user1][user2]) + "," + str(user_similarity_jaccard[user1][user2]) + "," + str(user_similarity_pearson[user1][user2]) + "\n")
	#f_i_d.close()
	return user_similarity_cosine, user_similarity_jaccard, user_similarity_pearson

def crossValidation(data, user_data, item_data,mode='default'):
	# k_fold = KFold(n=len(data), n_folds=10)

	sim_user_cosine, sim_user_jaccard, sim_user_pearson = similarity_user(user_data,mode=mode)
	sim_item_cosine, sim_item_jaccard, sim_item_pearson = similarity_item(item_data,mode=mode)
	#sim_user_cosine, sim_user_jaccard, sim_user_pearson = np.random.rand(users,users), np.random.rand(users,users), np.random.rand(users,users)
	#sim_item_cosine, sim_item_jaccard, sim_item_pearson = np.random.rand(items,items), np.random.rand(items,items), np.random.rand(items,items) 

	return sim_user_cosine, sim_item_cosine


def predictRating(data, user_data, item_data,mode='default'):

	sim_user, sim_item = crossValidation(data, user_data, item_data)
	if mode=='attack':
		users = 943+ 30
	else:
		users = 943

	M = np.zeros((users,items))
	for e in data:
		M[e[0]-1][e[1]-1] = e[2]

	#f = open("toBeRated.csv","r")
	f = open(sys.argv[2],"r")	
	toBeRated = {"user":[], "item":[]}
	for row in f:
		r = row.split(',')	
		toBeRated["item"].append(int(r[1]))
		toBeRated["user"].append(int(r[0]))

	f.close()

	pred_rate = []

	#fw = open('result3.csv','w')
	# fw_w = open('result3.csv','w')
  fw_w = open(resultfile,'w')  #resultfile --predicted rating
	csvwriter = csv.writer(fw_w)

	l = len(toBeRated["user"])
	for e in range(l):
		user = toBeRated["user"][e]
		item = toBeRated["item"][e]

		user_pred = 3.0
		item_pred = 3.0

		#item-based
		if np.count_nonzero(M[:,item-1]):
			sim = sim_item[item-1]
			ind = (M[user-1] > 0)
			#ind[item-1] = False
			normal = np.sum(np.absolute(sim[ind]))
			if normal > 0:
				item_pred = np.dot(sim,M[user-1])/normal

		if item_pred < 0:
			item_pred = 0

		if item_pred > 5:
			item_pred = 5

		#user-based
		if np.count_nonzero(M[user-1]):
			sim = sim_user[user-1]
			ind = (M[:,item-1] > 0)
			#ind[user-1] = False
			normal = np.sum(np.absolute(sim[ind]))
			if normal > 0:
				user_pred = np.dot(sim,M[:,item-1])/normal

		if user_pred < 0:
			user_pred = 0

		if user_pred > 5:
			user_pred = 5

		if (user_pred != 0 and user_pred != 5) and (item_pred != 0 and item_pred != 5):
				pred = (user_pred + item_pred)/2
		else:
			if (user_pred == 0 or user_pred == 5):
				if (item_pred != 0 and item_pred != 5):
					pred = item_pred
				else:
					pred = 3.0
			else:
				if (user_pred != 0 and user_pred != 5):
					pred = user_pred
				else:
					pred = 3.0

		#pred = (user_pred + item_pred)/2
		pred_rate.append(pred)
		csvwriter.writerow([int(user),int(item),float(pred)])

	#fw.close()
	fw_w.close()

#recommend_data = readingFile("ratings.csv")
# recommend_data = readingFile(sys.argv[1])

# predictRating(recommend_data, user_data, item_data,mode='default')
#crossValidation(recommend_data, user_data, item_data)


if __name__ == "__main__":
	#recommend_data = readingFile("ratings.csv")
	recommend_data = readingFile(sys.argv[1])
	#crossValidation(recommend_data)
	mode = sys.argv[3] #attack or default
	resultfile = sys.argv[4]
  	user_data = userData(mode=mode)
  	item_data = itemData(mode=mode)
	predictRating(recommend_data,resultfile=resultfile,mode=mode)
