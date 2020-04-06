import numpy as np
import random
import pandas as pd 
import scipy.stats
import matplotlib.pyplot as plt
import csv
import pickle
import sys

def my_distribution(min_val, max_val, mean, std, size):
    lower = min_val
    upper = max_val
    mu = mean
    sigma = std
    N = size

    samples = scipy.stats.truncnorm.rvs(
            (lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=N)
    return samples

users = 943
items = 1682

def readingFile(filename):
	f = open(filename,"r")
	data = []
	for row in f:
		r = row.split(',')
		e = [int(r[0]), int(r[1]), int(r[2])]
		data.append(e)
        
	return data

def readFile(filename):
    f = open(filename,"r")
    data = {"user":[],"item":[]}
    for row in f:
        r = row.split(',')	
        data["item"].append(int(r[1]))
        data["user"].append(int(r[0]))
    f.close()



def randomAttack(n_new_users=30,intent="push",target_item_set=[]):

    def copy_csv():
        df = pd.read_csv('ratings_updated.csv')
        df.to_csv('ratings_updated_rand_attack.csv',index=False)

    copy_csv()
    lines_to_be_added = []

    for iters in range(n_new_users):
        new_user_id = users+iters+1  #944,945,....973
        # filler_items = 
        filler_items_size = items-len(target_item_set)  #1682 - target items
        filler_ratings = my_distribution(1.0,5.0,3.6,1.1,filler_items_size)
        start = 0
        for item_id in range(1,items+1):
            if item_id in target_item_set:
                if intent == "push":
                    lines_to_be_added.append([new_user_id,item_id,5.0])
                else:
                    lines_to_be_added.append([new_user_id,item_id,1.0])
                    
            else:
                lines_to_be_added.append([new_user_id,item_id,filler_ratings[start]])
                start = start + 1

    with open('ratings_updated_rand_attack.csv','a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(lines_to_be_added)


def items_avg_rating():
    data = []
    with open('u_data.txt','r') as f:
        lines = f.readlines()
        for line in lines:
            lst = line.split('\t')
            # print(len(lst))
            data.append([int(lst[0]),int(lst[1]),int(lst[2])])

    items_ratings_dict = {}  # dict[item_id] = (sum,count)
    for row in data:
        if row[1] not in items_ratings_dict:
            items_ratings_dict[row[1]] = (row[2],1)
        else:
            sums = items_ratings_dict[row[1]][0]
            count = items_ratings_dict[row[1]][1]
            items_ratings_dict[row[1]] = (sums+row[2],count+1)

    return items_ratings_dict


def averageAttack(n_new_users=30,intent="push",target_item_set=[]):
    items_ratings_dict = items_avg_rating()

    def copy_csv():
        df = pd.read_csv('ratings_updated.csv')
        df.to_csv('ratings_updated_avg_attack.csv',index=False)

    copy_csv()
    lines_to_be_added = []


    for item_id in range(1,items+1):
        if item_id not in target_item_set:
            mean = float(items_ratings_dict[item_id][0])/float(items_ratings_dict[item_id][1])
            filler_ratings = my_distribution(1.0,5.0,mean,1.1,n_new_users)
            start = 0
            for iters in range(n_new_users):
                new_user_id = users+iters+1 
                lines_to_be_added.append([new_user_id,item_id,filler_ratings[start]])
                start = start + 1
        
        else:
            for iters in range(n_new_users):
                new_user_id = users+iters+1 
                if intent == "push":
                    lines_to_be_added.append([new_user_id,item_id,5.0])
                else:
                    lines_to_be_added.append([new_user_id,item_id,1.0])



    with open('ratings_updated_avg_attack.csv','a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(lines_to_be_added)



    



if __name__ == "__main__":
    # recommendation_data = readingFile("ratings.csv")
    # toberated_data = readFile("toBeRated.csv")
    # rec_mat = np.zeros((users,items))
    # target_item_set = random.sample(range(1,items+1), 50) #50 target items -id
    # target_user_set = random.sample(range(1,users+1), 63) #63 target users -id

    # with open('target_item_set.pkl', 'wb') as f:
    #     pickle.dump(target_item_set, f)

    with open('target_item_set.pkl', 'rb') as f:
        target_item_set = pickle.load(f)

    with open('target_user_set.pkl', 'rb') as f:
        target_user_set = pickle.load(f)

    # with open('target_user_set.pkl', 'wb') as f:
    #     pickle.dump(target_user_set, f)

    # for e in recommendation_data:
	# 	rec_matat[e[0]-1][e[1]-1] = e[2]

    # filler_ratings = my_distribution(1.0,5.0,3.6,1.1,10)
    # print(filler_ratings)
    no_of_bots = int(sys.argv[1])
    intent = sys.argv[2]

    randomAttack(n_new_users=no_of_bots,intent=intent,target_item_set=target_item_set)
    averageAttack(n_new_users=no_of_bots,intent=intent,target_item_set=target_item_set)
    