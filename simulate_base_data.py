
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Auxiliar functions
def campaign_new_users(campaign):
    return np.round(np.max([np.power(campaign / 100, 2) + np.random.uniform(-10,10,1)[0], 0]))

def network_new_users(users):
    return np.round((users / 200) + np.random.uniform(-10,10,1)[0])

def camapign_variation(campaign):
    return campaign * (1 + np.random.uniform(-0.1,0.1,1)[0])

# Time handle values
today = datetime.now()
date = today - timedelta(days = 700)
period = 7 # number of days
# Base values
data = pd.DataFrame()
money_users = 0
sudsidy_users = 0
campaign = 1000
# Auxiliari settings
np.random.seed(0)
ready = False
while not ready:
    # ------ Period Simulation -------
    # In this case, money size increase by network effects based on sudsidy size
    money_size_campaign = campaign_new_users(campaign)
    sudsidy_size_campaign = campaign_new_users(campaign)
    money_size_network = network_new_users(sudsidy_users)
    sudsidy_size_network = network_new_users(sudsidy_users)
    data = data.append(pd.DataFrame({
        "date" : date,
        "money_size_users" : money_users + money_size_campaign + money_size_network,
        "subsidy_size_users" : sudsidy_users + sudsidy_size_campaign + sudsidy_size_network,
        "money_size_new_users_by_campaign" : money_size_campaign,
        "money_size_new_users_by_network" : money_size_network,
        "subsidy_size_new_users_by_campaign" : sudsidy_size_campaign,
        "subsidy_size_new_users_by_network" : sudsidy_size_network,
        "investement_in_money_size_campaigns" : campaign,
        "investement_in_sudsidy_size_campaigns" : campaign
    }, index = {date}))

    # ------- Variables update --------
    money_users += money_size_campaign + money_size_network
    sudsidy_users += sudsidy_size_campaign + sudsidy_size_network
    campaign = camapign_variation(campaign)
    date += timedelta(days = period)

    ready = date >= today

print(data.tail())
print(data.shape)
data.to_csv("data/test_data.csv", index = False)
