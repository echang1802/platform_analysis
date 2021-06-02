# Platform Analysis

### Input

CSV file with the columns:
 * date: date of data colection.
 * money_size_users: total users on the money size of the platform (at the end of the day).
 * subsidy_size_users: total users on the subsify size of the platform (at the end of the day).
 * money_size_new_users_by_campaign: new users adquired on money size by performing comercial / marketing actions.
 * money_size_new_users_by_network: new users adquired on money size by network behaviour.
 * subsidy_size_new_users_by_campaign: new users adquired on sudsidy size by performing comercial / marketing actions.
 * subsidy_size_new_users_by_network: new users adquired on sudsidy size by network behaviour.
 * investement_in_money_size_campaigns: total money invested in the growth of money size.
 * investement_in_sudsidy_size_campaigns: total money invested in the growth of sudsidy size.

A example CSV simulated data could be created with the ´simulate_base_data.py´ file.

### Pipeline

1. Create data file.
2. Create a campaign_control object based on campaigns investement.
3. Create a simulator object.
4. Use the ´simulate´ method, which return two values
  * The number of periods simulated.
  * If the critical mass was reached in the simulated periods.

### Objects:

* Simulator.
* model_trainer.
* campaign_control.
