import random
import pickle
import csv 
import sys

users_count = 943
items_count = 1682


# to be rated file compute -- which is same for before and after attack
def evaluation(attackfilename = 'ratings_updated_rand_attack.csv',target_item_set=[],target_user_set=[]):
    orig_file = 'ratings_updated.csv'
    attacked_ratings_file = attackfilename
    orig_data = []
    with open(orig_file,'r') as f:
        lines = f.readlines()
        for line in lines:
            lst = line.split(',')
            # print(len(lst))
            orig_data.append([int(lst[0]),int(lst[1]),float(lst[2])])

    # attacked_ratings_data = []
    # with open(attacked_ratings_file,'r') as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         lst = line.split(',')
    #         # print(len(lst))
    #         attacked_ratings_data.append([int(lst[0]),int(lst[1]),int(lst[2])])

    to_be_rated_list = []  # for prediction

    users_map = {}

    for row in orig_data:
        if row[0] not in users_map:
            users_map[row[0]] = [row[1]]
            # users_map[row[0]].append(row[1])
        else:
            users_map[row[0]].append(row[1])

    for user in target_user_set:
        for item in target_item_set:
            if item not in users_map[user]:
                to_be_rated_list.append([int(user),int(item)])

    filename = 'toberated_attack.csv'
    with open(filename,'w',newline='') as csvfile2:
        csvwriter = csv.writer(csvfile2)
        csvwriter.writerows(to_be_rated_list)


def prediction_shift(resultfile1,resultfile2):
    
    result1_map = {}
    with open(resultfile1,'r') as f:
        lines = f.readlines()
        for line in lines:
            lst = line.split(',')
            # print(len(lst))
            # data.append([int(lst[0]),int(lst[1]),float(lst[2])])
            user_id = int(lst[0])
            item_id = int(lst[1])
            rating = float(lst[2])
            if user_id not in result1_map:
                result1_map[user_id] = {}
                result1_map[user_id][item_id] = rating

            else:
                result1_map[user_id][item_id] = rating

    
    result2_map = {}
    with open(resultfile2,'r') as f:
        lines = f.readlines()
        for line in lines:
            lst = line.split(',')
            # print(len(lst))
            # data.append([int(lst[0]),int(lst[1]),float(lst[2])])
            user_id = int(lst[0])
            item_id = int(lst[1])
            rating = float(lst[2])
            if user_id not in result2_map:
                result2_map[user_id] = {}
                result2_map[user_id][item_id] = rating

            else:
                result2_map[user_id][item_id] = rating

    
    delta_map = {}

    for user_id in result1_map:
        for item_id in result1_map[user_id]:
            if user_id not in delta_map:
                delta_map[user_id] = {}
                delta_map[user_id][item_id] = result2_map[user_id][item_id]-result1_map[user_id][item_id]
            else:
                delta_map[user_id][item_id] = result2_map[user_id][item_id]-result1_map[user_id][item_id]

    # delta item calc
    delta_item_map = {}

    for user_id in delta_map:
        for item_id in delta_map[user_id]:
            if item_id not in delta_item_map:
                delta_item_map[item_id] = (delta_map[user_id][item_id],1)
            else:
                delta_item_map[item_id] = (delta_item_map[item_id][0]+delta_map[user_id][item_id],delta_item_map[item_id][1]+1)

    total_sum = 0.0
    total_count = 0

    for item_id in delta_item_map:
        delta_item_map[item_id] = float(delta_item_map[item_id][0])/float(delta_item_map[item_id][1])
        total_sum = total_sum + delta_item_map[item_id]
        total_count = total_count + 1

    total_sum = total_sum

    
    print("Prediction shift for {} and {} is {}".format(resultfile1,resultfile2,float(total_sum)/float(total_count)))
    



    


if __name__ == "__main__":
    # target_user_set = random.sample(range(1,users_count+1), 63) #63 target users -id

    # with open('target_user_set.pkl', 'wb') as f:
    #     pickle.dump(target_user_set, f)

    with open('target_user_set.pkl', 'rb') as f:
        target_user_set = pickle.load(f)

    with open('target_item_set.pkl', 'rb') as f:
        target_item_set = pickle.load(f)
    
    # evaluation(attackfilename='ratings_updated_rand_attack.csv',target_item_set=target_item_set,target_user_set=target_user_set)

    # prediction_shift('result_item_based_before_attack.csv','result_item_based_after_avg_attack.csv')
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    prediction_shift(file1,file2)

