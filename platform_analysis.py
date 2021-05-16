from sklearn.model_selection import train_test_split

class model_trainer:

    def __init__(self):
        pass

    def train(self, data, model, params, **kwargv):
        # model:
        #   - if str: train sklearn model of type [model]
        #   - if model. use itself.
        #   - if None: train several sklearn model.
        # self._load_model(model)
        # MVP: model is a sklearn model.
        # TO DO: add model class usage. <--------------------------

        self._train_test_split(data, {
            "test_size": kwargv["test_size"] if "test_size" in kwargv.keys() else 0.33,
            "random_state": kwargv["random_state"] if "random_state" in kwargv.keys() else 42,
        })

        self._model = model(params)
        # TODO: Add hyper params optimization <---------------------------
        self._model.fit(self.X_train, self.y_train)

    def _train_test_split(self, data, params):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(data, test_size=params["test_size"], random_state=params["random_state"])

    def predict(self, data):
        return self._model.predict(data)

class simulator:

    def __init__(self):
        pass

    def simulate_one_day(self):
        pass
