import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import metrics, grid_search
from sklearn.neighbors import NearestNeighbors


class TrainKNearestNeighbour:
    def __init__(self, team_name, include_ties=True):
        self.include_ties = include_ties
        self.team_name = team_name

    def prep_data(self, training, testing):
        # Sort data by match result. 0 = H, 1 = B, 2 = U
        training_0 = [[x, y] for x, y in zip(training['wins'][0], training['wins'][1])]
        training_1 = [[x, y] for x, y in zip(training['loss'][0], training['loss'][1])]
        training_2 = [[x, y] for x, y in zip(training['ties'][0], training['ties'][1])] if self.include_ties else []

        testing_0 = [[x[0], x[1]] for x in testing if x[2] == 0]
        testing_1 = [[x[0], x[1]] for x in testing if x[2] == 1]
        testing_2 = [[x[0], x[1]] for x in testing if x[2] == 2] if self.include_ties else []

        # Create numpy arrays to use for training and testing.
        # X contains the features
        # Y contains the classes
        self.X = np.array\
            (
                training_0 +
                training_1 +
                training_2
            )

        self.Y = np.array\
            (
                [0 for _ in training_0] +
                [1 for _ in training_1] +
                [2 for _ in training_2]
            )

        self._X = np.array\
            (
                testing_0 +
                testing_1 +
                testing_2
            )

        self._Y = np.array \
            (
                [0 for _ in testing_0] +
                [1 for _ in testing_1] +
                [2 for _ in testing_2]
            )

    def train_knn(self):
        # Parameters to use in the K-NearestNeighbor grid search
        parameters = [
            {
                'n_neighbors': [i for i in range(1, 30)],
                'algorithm': ['ball_tree', 'kd_tree', 'brute']
              }
        ]

        print("Starting Grid Search training...")

        model = NearestNeighbors()
        self.clf = grid_search.GridSearchCV(model, parameters, n_jobs=40, scoring="accuracy")
        self.clf.fit(self.X, self.Y)

    def save_knn(self):
        with open("{0}_knn".format(self.team_name), "wb") as f:
            pickle.dump(self.clf, f)

    def graph_knn(self):

        h = .02  # step size in the mesh

        # Create color maps for plotting
        cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
        cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

        # Plot the decision boundary, assigning a color to each
        # point in the mesh [x_min, m_max]x[y_min, y_max].
        x_min, x_max = self._X[:, 0].min() - 1, self._X[:, 0].max() + 1
        y_min, y_max = self._X[:, 1].min() - 1, self._X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        Z = self.clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = self.clf.predict

        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        plt.figure()
        plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

        # Plot also the training points
        plt.scatter(self.X[:, 0], self.X[:, 1], c=self.Y, cmap=cmap_bold)
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.title("{0} 2015".format(self.team_name))

        plt.savefig('{0}_knn.png'.format(self.team_name))

    def print_results(self):
        # summarize the fit of the model
        predicted = self.clf.predict(self._X)
        print(metrics.classification_report(self._Y, predicted))
        print(metrics.confusion_matrix(self._Y, predicted))

        print("Parameters: ")
        for key, value in self.clf.best_params_.items():
            print("\t" + key + ":", value)
