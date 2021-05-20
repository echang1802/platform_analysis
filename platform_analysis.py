from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

class model_trainer:

    def __init__(self, data, target, size = None):
        if "campaign" in target:
            self._target = data.loc[1:, target]
            self._data = data.loc[:-1, f"investement_in_{size}_size_campaigns"]
        else:
            self._target = data.loc[1:, target]
            self._data = data.loc[:-1, ["money_size_users", "subsidy_size_users"]]

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
        }, target)

        self._model = model(params)
        # TODO: Add hyper params optimization <---------------------------
        self._model.fit(self.X_train, self.y_train)

    def _train_test_split(self, params, target):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self._data, self._target, test_size=params["test_size"], random_state=params["random_state"])

    def predict(self, data):
        return self._model.predict(data)

class campaign_control:

    def __init__(self, value_to_invest):
        self._value_to_invest = value_to_invest

    def get_investement(self):
        # TODO: make a investement based on actual state of platform
        return self._value_to_invest

class simulator:

    def __init__(self, data, tol = 1, **kwargv):
        # Set tol
        self._tol = tol

        # Train regression model for money side
        self._model_money_size_campaign = model_trainer(data, "money_size_new_users_by_campaign")
        self._model_money_size_campaign.train(RandomForestRegressor , {"random_state":0}, **kwargv)
        self._model_money_size_network = model_trainer(data, "money_size_new_users_by_network")
        self._model_money_size_network.train(RandomForestRegressor , {"random_state":0}, **kwargv)
        # Train regression models for sudsidy side
        self._model_subsidy_size_campaign = model_trainer(data, "subsidy_size_new_users_by_campaign")
        self._model_subsidy_size_campaign.train(RandomForestRegressor , {"random_state":0}, **kwargv)
        self._model_subsidy_size_network = model_trainer(data, "subsidy_size_new_users_by_network")
        self._model_subsidy_size_network.train(data, RandomForestRegressor , {"random_state":0}, **kwargv)

    def _simulate_one_period(self, campaigns):
        # Make predictions
        money_size_new_users_by_campaign = self._model_money_size_campaign.predict(self._campaigns) # What is data?
        money_size_new_users_by_network = self._model_money_size_network.predic(self._data)
        subsidy_size_new_users_by_campaign = self._model_subsidy_size_campaign.predict(self._campaigns)
        subsidy_size_new_users_by_network = self._model_subsidy_size_network.predict(self._data)

        self.money_size += (money_size_new_users_by_network + money_size_new_users_by_campaign)
        self.sudsidy_size += (subsidy_size_new_users_by_network + subsidy_size_new_users_by_campaign)

        return (money_size_new_users_by_network + subsidy_size_new_users_by_network) > self._tol * (money_size_new_users_by_campaign + subsidy_size_new_users_by_campaign)

    def _get_data(self, campaigns):
        self._data = pd.DataFrame({
            "money_size_users", : self._money_size,
            "subsidy_size_users" : self._subsidy_size
        }, index = {0})
        self._campaigns = pd.DataFrame({
            "investement" : _campaigns.get_investement()
        })

    def simulate(self, users, campaigns, periods_to_evolve = 1):
        self.money_size = users["money_size"]
        self.sudsidy_size = users["sudsidy_size"]
        periods = 0
        periods_count = 0
        ready = False
        while not ready:
            self._get_data()
            good_period = self._simulate_one_period(campaigns)
            if good_period:
                periods_count += 1
            else:
                periods_count = 0
            periods += 1
            ready = periods_count >= periods_to_evolve
        return periods
