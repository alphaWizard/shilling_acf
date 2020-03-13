import csv
import random

users_count = 943
items_count = 1682
 

if __name__ == "__main__":

    data = []
    with open('u_data.txt','r') as f:
        lines = f.readlines()
        for line in lines:
            lst = line.split('\t')
            # print(len(lst))
            data.append([int(lst[0]),int(lst[1]),float(lst[2])])
            # print([int(lst[0]),int(lst[1]),int(lst[2])])

    filename = 'ratings_updated.csv'

    with open(filename,'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(data)

    users_map = {}

    # for row in data:
    #     if row[0] not in users_map:
    #         users_map[row[0]] = [row[1]]
    #         # users_map[row[0]].append(row[1])
    #     else:
    #         users_map[row[0]].append(row[1])


    tobeupdated_data = []
    filename2 = 'toberated_updated.csv'
    target_item_set = random.sample(range(1,items_count+1), 50) #50 target items -id
    target_user_set = random.sample(range(1,users_count+1), 63) #63 target users -id
    # for user in range(1,users_count+1):
    #     for item in range(1,items_count+1):
    #         if item not in users_map[user]:
    #             tobeupdated_data.append([user,item])




    # print(len(tobeupdated_data))


    # with open(filename2,'w') as csvfile2:
    #     csvwriter = csv.writer(csvfile2)
    #     csvwriter.writerows(tobeupdated_data)








    

