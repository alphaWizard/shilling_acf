# shilling_acf
Shilling Attack Models in Recommender System and their Effectiveness Analysis

This repository contains an unofficial implementation of the paper [Shilling Recommender Systems for Fun and Profit.](https://wwwconference.org/proceedings/www2004/docs/1p393.pdf)

Steps to run:
1. python attack.py
1. python itemBased.py ratings_updated.csv toberated_attack.csv default result_before.csv
1. python itemBased.py ratings_updated_avg_attack.csv toberated_attack.csv attack result_after.csv
1. python evaluation.py result_after.csv result_before.csv

Note that above steps run the code for evalauting average attack with push intent on item-based cf algorithm. Last step gives the prediction shift value for the attack.
