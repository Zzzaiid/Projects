from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor, StackingRegressor, VotingRegressor
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, BaggingClassifier, StackingClassifier
from sklearn.svm import SVC
import pandas as pd
import numpy as np


class Regressor:
    def __init__(self):
        self.model = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None

    def train_test(self, df, target):
        try:
            x = df.drop([target], axis=1)
            y = df[target]
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y,
                                                                                    test_size=0.2,
                                                                                    random_state=21,)
        except Exception as e:
            print(f'train_test: error {e}')

    def create_model(self, class_model, params=None):
        if params is None:
            params = {}
        try:
            self.model = class_model(**params)
        except:
            raise ValueError(f"Unknown model class: {class_model}")

    def fit_model(self):
        if self.model is None:
            raise ValueError("Model is not created. Call create_model first.")
        try:
            self.model.fit(self.x_train, self.y_train)
        except Exception as e:
            print(f'fit_model: error {e}')

    def predict_model(self, prt=True):
        print(f'==========Predict Model==========')
        if self.model is None:
            raise ValueError("Model is not created. Call create_model first.")
        try:
            predict_test = self.model.predict(self.x_test)
            mse_test = mean_squared_error(self.y_test, predict_test)
            if prt:
                predict_train = self.model.predict(self.x_train)
                mse_train = mean_squared_error(self.y_train, predict_train)
                print(f'Train: MSE = {mse_train:.5} | RMSE = {(mse_train ** 0.5):.5}')
                print(f'Test: MSE = {mse_test:.5} | RMSE = {(mse_test ** 0.5):.5}')
            else:
                return mse_test
        except Exception as e:
            print(f'predict_model: error {e}')

    def parameter_search(self, param_grid):
        print(f'==========Parameter Search==========')
        if self.model is None:
            raise ValueError("Model is not created. Call create_model first.")
        try:
            grid_search = GridSearchCV(estimator=self.model,
                                    param_grid=param_grid,
                                    scoring='neg_mean_squared_error',
                                    n_jobs=-1, cv=2)
            grid_search.fit(self.x_train, self.y_train)

            self.model.set_params(**grid_search.best_params_)
            self.fit_model()
            print(f'Best params: {grid_search.best_params_}')
            print(f'Best score: {abs(grid_search.best_score_):.5}')
        except Exception as e:
            print(f'parameter_search: error {e}')

    def cross_validation(self, n_splits=4):
        print(f'==========Cross-Validation==========')
        if self.model is None:
            raise ValueError("Model is not created. Call create_model first.")

        try:
            scores = cross_val_score(self.model, self.x_train, self.y_train, cv=n_splits, scoring='neg_mean_squared_error', n_jobs=-1)
            for score in abs(scores):
                print(f'MSE = {score:.5} | RMSE = {(score ** 0.5):.5}')
        except Exception as e:
            print(f'cross_validation: error {e}')



class Classification:
    def __init__(self):
        self.model = None
        # self.best_params = None
        self.x = None
        self.y = None
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None

    def binarization_round(self, df, target):
        try:
            df[target] = df[target].apply(round)
        except Exception as e:
            print(f'binarization_round: error {e}')

    def tr_tst_split(self, df, target):
        try:
            self.x = df.drop(columns=[target])
            self.y = df[target]
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=0.2, random_state=21)
        except Exception as e:
            print(f'tr_tst_split: error {e}')

    def model_choose(self, model_name, params):
        try:
            if model_name == 'LogisticRegression':
                self.model = LogisticRegression(**params)
            elif model_name == 'DecisionTreeClassifier':
                self.model = DecisionTreeClassifier(**params)
            elif model_name == 'RandomForestClassifier':
                self.model = RandomForestClassifier(**params)
            elif model_name == 'VotingClassifier':
                self.model = VotingClassifier(**params)
            elif model_name == 'BaggingClassifier':
                self.model = BaggingClassifier(**params)
            elif model_name == 'StackingClassifier':
                self.model = StackingClassifier(**params)
            else:
                print("Неверная модель")
                return 0
            return self.model
        except Exception as e:
            print(f'model_choose: error {e}')

    def parameter_select(self, parameters):
        try:
            grid = GridSearchCV(estimator=self.model, param_grid=parameters, n_jobs=-1)
            grid.fit(self.x_train, self.y_train)
            self.model = grid.best_estimator_
            cross_score = cross_val_score(self.model, self.x, self.y)
            y_pred = self.model.predict(self.x_test)
            acc_score = accuracy_score(self.y_test, y_pred)
            print(f"Перекрестная проверка: {cross_score.mean()}\nТочность на тестовой выборке: {acc_score}")
            return grid.best_params_
        except Exception as e:
            print(f'parameter_select: error {e}')

    def fit(self):
        try:
            self.model.fit(self.x_train, self.y_train)
        except Exception as e:
            print(f'fit: error {e}')

    def native_accuracy(self):
        try:
            most_frequent_class = pd.Series(self.y_train).mode().iloc[0]
            naive_predictions = np.full_like(self.y_test, most_frequent_class)
            return accuracy_score(self.y_test, naive_predictions)
        except Exception as e:
            print(f'native_accuracy: error {e}')

    def binarization_category(self, df, target):
        try:
            df[target] = df[target].apply(lambda x: 'great' if x >= 4 else 'so-so' if x >= 2 else 'bad')
        except Exception as e:
            print(f'binarization_category: error {e}')

    def predicting(self, x):
        try:
            return self.model.predict(x)
        except Exception as e:
            print(f'predicting: error {e}')