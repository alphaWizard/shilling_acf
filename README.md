# shilling_acf
Shilling Attack Models in Recommender System and their Effectiveness Analysis

This repository contains an unofficial implementation of the paper [Shilling Recommender Systems for Fun and Profit.](https://wwwconference.org/proceedings/www2004/docs/1p393.pdf)

Steps to run:
1. python attack.py 30 push
1. python userBased.py ratings_updated.csv toberated_attack.csv default result_before.csv
1. python userBased.py ratings_updated_avg_attack.csv toberated_attack.csv attack result_after.csv 30
1. python evaluation.py result_before.csv result_after.csv

Note that above steps run the code for evalauting average attack of 30 new users with push intent on user-based cf algorithm. Last step gives the prediction shift value for the attack.
Also, these steps run will give the evaluation result for a single data point.
These steps were run for 24 data points for (push,nuke), (random,average)  attacks with (15,30,50) bots on (user-based.item-based) acf algorithms. 
