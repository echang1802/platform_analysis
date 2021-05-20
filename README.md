# Platform Analysis

### Input

Csv file with the columns:
 * date: date of data colection.
 * money_size_users: total users on the money size of the platform (at the end of the day).
 * subsidy_size_users: total users on the subsify size of the platform (at the end of the day).
 * money_size_new_users_by_campaign: new users adquired on money size by performing comercial / marketing actions.
 * money_size_new_users_by_network: new users adquired on money size by network behaviour.
 * subsidy_size_new_users_by_campaign: new users adquired on sudsidy size by performing comercial / marketing actions.
 * subsidy_size_new_users_by_network: new users adquired on sudsidy size by network behaviour.
 * investement_in_money_size_campaigns: total money invested in the growth of money size.
 * investement_in_sudsidy_size_campaigns: total money invested in the growth of sudsidy size.


### Pipeline

1. Read the data.
2. Train a ML model to predict new users on each size by network behaviour.
3. Simulate days until the new users by network behaviour are greater than the users by campaigns in both sides.

### Objects:

* Simulator
* model_trainer
* campaign_control
