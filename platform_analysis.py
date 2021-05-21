from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np

class model_trainer:

    def __init__(self, data, target, size = None):
        self.campaign = "campaign" in target
        if self.campaign:
            self._data = data.iloc[:-1][f"investement_in_{size}_size_campaigns"]
            self._target = data.loc[1:, target]
        else:
            self._target = data.loc[1:, target]
            self._data = data.iloc[:-1][["money_size_users", "subsidy_size_users"]]

    def train(self, model, params, **kwargv):
        # model:
        #   - if str: train sklearn model of type [model]
        #   - if model. use itself.
        #   - if None: train several sklearn model.
        # self._load_model(model)
        # MVP: model is a sklearn model
        # TO DO: add model class usage. <--------------------------

        self._train_test_split({
            "test_size": kwargv["test_size"] if "test_size" in kwargv.keys() else 0.33,
            "random_state": kwargv["random_state"] if "random_state" in kwargv.keys() else 42,
        })

        self._model = model()
        # TODO: Add hyper params optimization <---------------------------
        self._model.fit(self.X_train, self.y_train)

    def _train_test_split(self, params):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self._data, self._target, test_size=params["test_size"], random_state=params["random_state"])
        if self.campaign:
            self.X_train = np.asarray(self.X_train).reshape(-1,1)

    def predict(self, data):
        return self._model.predict(data)

class campaign_control:

    def __init__(self, value_to_invest, add_random = True):
        self._value_to_invest = value_to_invest
        self._add_random = add_random

    def get_investement(self):
        # TODO: make a investement based on actual state of platform
        return self._value_to_invest * ((1 + np.random.uniform(-0.1,0.1,1)[0]) if self._add_random else 0)

class simulator:

    def __init__(self, data, tol = 1, **kwargv):
        # Set tol
        self._tol = tol

        # Train regression model for money side
        self._model_money_size_campaign = model_trainer(data, "money_size_new_users_by_campaign", "money")
        self._model_money_size_campaign.train(RandomForestRegressor , {"random_state" : 0}, **kwargv)
        self._model_money_size_network = model_trainer(data, "money_size_new_users_by_network")
        self._model_money_size_network.train(LinearRegression , {}, **kwargv)
        # Train regression models for sudsidy side
        self._model_subsidy_size_campaign = model_trainer(data, "subsidy_size_new_users_by_campaign", "sudsidy")
        self._model_subsidy_size_campaign.train(RandomForestRegressor , {"randon_state": 0}, **kwargv)
        self._model_subsidy_size_network = model_trainer(data, "subsidy_size_new_users_by_network")
        self._model_subsidy_size_network.train(LinearRegression , {}, **kwargv)

    def _simulate_one_period(self, campaigns):
        # Make predictions
        money_size_new_users_by_campaign = self._model_money_size_campaign.predict(self._campaigns) # What is data?
        money_size_new_users_by_network = self._model_money_size_network.predict(self._data)
        subsidy_size_new_users_by_campaign = self._model_subsidy_size_campaign.predict(self._campaigns)
        subsidy_size_new_users_by_network = self._model_subsidy_size_network.predict(self._data)

        self.money_size += (money_size_new_users_by_network + money_size_new_users_by_campaign)
        self.subsidy_size += (subsidy_size_new_users_by_network + subsidy_size_new_users_by_campaign)

        return (money_size_new_users_by_network + subsidy_size_new_users_by_network) > self._tol * (money_size_new_users_by_campaign + subsidy_size_new_users_by_campaign)

    def _get_data(self, campaigns):
        self._data = pd.DataFrame({
            "money_size_users" : self.money_size,
            "subsidy_size_users" : self.subsidy_size
        }, index = {0})
        self._campaigns = pd.DataFrame({
            "investement" : campaigns.get_investement()
        }, index = {0})

    def simulate(self, users, campaigns, periods_to_evolve = 1, max_periods = 1000):
        self.money_size = users["money_size"]
        self.subsidy_size = users["subsidy_size"]
        periods = 0
        periods_count = 0
        ready = False
        while not ready:
            self._get_data(campaigns)
            good_period = self._simulate_one_period(campaigns)
            if good_period:
                periods_count += 1
            else:
                periods_count = 0
            periods += 1
            ready = periods_count >= periods_to_evolve or periods >= max_periods
        return periods, periods_count >= periods_to_evolve
