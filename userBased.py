import numpy as np
import scipy.stats
import scipy.spatial
# from sklearn.model_selection import KFold
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

def similarity_user(data,mode='default',bots=30):
	# print("Hello User")
	if mode == 'attack':
		users = 943 + bots
	else: 
		users = 943
	#f_i_d = open("sim_user_based.txt","w")
	user_similarity_cosine = np.zeros((users,users))
	user_similarity_jaccard = np.zeros((users,users))
	user_similarity_pearson = np.zeros((users,users))
	for user1 in range(users):
		# print(user1)
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

def crossValidation(data,mode='default',bots=30):
	# k_fold = KFold(n=len(data), n_folds=10)
	# k_fold = KFold(n_splits=10)
	if mode == 'attack':
		# print("here")
		users = 943 + bots
	else:
		users = 943

	Mat = np.zeros((users,items))
	for e in data:
		Mat[e[0]-1][e[1]-1] = e[2]

	sim_user_cosine, sim_user_jaccard, sim_user_pearson = similarity_user(Mat,mode=mode,bots=bots)
	#sim_user_cosine, sim_user_jaccard, sim_user_pearson = np.random.rand(users,users), np.random.rand(users,users), np.random.rand(users,users)

	return Mat, sim_user_cosine


def predictRating(recommend_data,resultfile='result_user_based_before_attack.csv',mode='default',bots=30):

	M, sim_user = crossValidation(recommend_data,mode=mode,bots=bots)

	#f = open("toBeRated.csv","r")
	f = open(sys.argv[2],"r")   #toberated file
	toBeRated = {"user":[], "item":[]}
	for row in f:
		r = row.split(',')	
		toBeRated["item"].append(int(r[1]))
		toBeRated["user"].append(int(r[0]))

	f.close()

	pred_rate = []

	#fw = open('result1.csv','w')
	fw_w = open(resultfile,'w')  #resultfile --predicted rating
	csvwriter = csv.writer(fw_w)
    # csvwriter.writerows(tobeupdated_data)

	l = len(toBeRated["user"])
	for e in range(l):
		user = toBeRated["user"][e]
		item = toBeRated["item"][e]

		pred = 3.0

		#user-based
		if np.count_nonzero(M[user-1]):
			sim = sim_user[user-1]
			ind = (M[:,item-1] > 0)
			#ind[user-1] = False
			normal = np.sum(np.absolute(sim[ind]))
			if normal > 0:
				pred = np.dot(sim,M[:,item-1])/normal

		if pred < 0:
			pred = 0.0

		if pred > 5:
			pred = 5.0

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

	
