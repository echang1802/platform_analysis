from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

class model_trainer:

    def __init__(self, data, target):
        self._target = data.loc[1:, target]
        self._data = data.drop(columns = target)[:-1]

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

class simulator:

    def __init__(self, data, **kwargv):

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

    def simulate_one_day(self, campaigns):
