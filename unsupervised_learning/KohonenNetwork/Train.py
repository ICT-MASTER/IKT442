import random
import pickle
import Database.Dataset as Dataset
from sklearn import preprocessing
from Unsupervised_Learning.KohonenNetwork.Network import SOM

# For plotting the images
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


class TrainKohonenNetwork:
    def __init__(self, features=None, team=None, data_processing="Normalize", shuffle_data=True, include_ties=True):
        self.team = team
        self.data_processing = data_processing
        self.shuffle_data = shuffle_data
        self.include_ties = include_ties
        self.features = [
            "is_home",
            "wins",
            "loss",
            "tie",
            "team_place",
            "team_place_other",
            "rain",
            "wind",
            "temp",
            "month",
            "day",
            "hour",
            "vg_scoring",
            "vg_scoring_other"
        ] if features is None else features

    def prep_data(self):

        training, testing = Dataset.kohonen_dataset(in_features=self.features, team=self.team)

        self.training_0 = [x[:-1] for x in training if x[-1] is 0]  # Extract Home-Win matches
        self.training_1 = [x[:-1] for x in training if x[-1] is 1]  # Extract Away-Win matches
        self.training_2 = [x[:-1] for x in training if x[-1] is 2] if self.include_ties else []  # Extract Tie Matches

        self.testing_0 = [x[:-1] for x in testing if x[-1] is 0]  # Extract Home-Win matches
        self.testing_1 = [x[:-1] for x in testing if x[-1] is 1]  # Extract Away-Win matches
        self.testing_2 = [x[:-1] for x in testing if x[-1] is 2] if self.include_ties else []  # Extract Tie Matches

        self.training_data = self.training_0 + self.training_1 + self.training_2

        if self.data_processing == "Normalize":
            # Normalize data
            self.training_data = preprocessing.normalize(self.training_data)
            self.testing_0 = preprocessing.normalize(self.testing_0)
            self.testing_1 = preprocessing.normalize(self.testing_1)
            self.testing_2 = preprocessing.normalize(self.testing_2)

        elif self.data_processing is "Standardize":
            # Standardize data
            self.training_data = preprocessing.scale(self.training_data)
            self.testing_0 = preprocessing.scale(self.testing_0)
            self.testing_1 = preprocessing.scale(self.testing_1)
            self.testing_2 = preprocessing.scale(self.testing_2)

        else:
            # Keep the data as-is
            pass

        if self.shuffle_data:
            random.shuffle(self.training_data)

    def train_som(self, m, n, n_iterations=100, alpha=None, sigma=None):
        """
        :param m: Dimension 1 of the SOM
        :param n: Dimension 2 of the SOM
        :param n_iterations: Number of training iterations
        :param alpha: Initial time(iteration no)-based learning rate. Default: 0.3
        :param sigma: Initial neighbourhood value. Default: max(m, n) / 2
        :return: None
        """
        self.som = SOM(m, n, len(self.training_data[0]), n_iterations, alpha, sigma)
        self.som.train(self.training_data)

    def map_som(self):
        self.mapped_wins = [[], []]
        self.mapped_loss = [[], []]
        self.mapped_ties = [[], []]

        for x in self.som.map_vects(self.training_0,):
            self.mapped_wins[0].append(x[0])
            self.mapped_wins[1].append(x[1])

        for x in self.som.map_vects(self.training_1):
            self.mapped_loss[0].append(x[0])
            self.mapped_loss[1].append(x[1])

        for x in self.som.map_vects(self.training_2):
            self.mapped_ties[0].append(x[0])
            self.mapped_ties[1].append(x[1])

        self.training = {
            'wins': self.mapped_wins,
            'loss': self.mapped_loss,
            'ties': self.mapped_ties
        }

        self.predictions = []
        for x in self.som.map_vects(self.testing_0):
            x = list(x)
            x.append(0)
            self.predictions.append(x)

        for x in self.som.map_vects(self.testing_1):
            x = list(x)
            x.append(1)
            self.predictions.append(x)

        for x in self.som.map_vects(self.testing_2):
            x = list(x)
            x.append(2)
            self.predictions.append(x)

    def graph_som(self):
        plt.plot(
            self.mapped_wins[0], self.mapped_wins[1], 'ro',
            self.mapped_loss[0], self.mapped_loss[1], 'bo'
        )
        plt.title('Rosenborg')
        plt.savefig('Kohonen_1.png')

        plt.plot(self.mapped_ties[0], self.mapped_ties[1], 'go')
        plt.savefig('Kohonen_2.png')

    def save_som(self, som=True, training=False, predictions=False):
        if som:
            with open('{0}_som.pkl'.format(self.team.name), 'wb') as f:
                pickle.dump(self.som, f)

        if training:
            with open('{0}_training.pkl'.format(self.team.name), 'wb') as f:
                pickle.dump(self.training, f)

        if predictions:
            with open('{0}_predictions.pkl'.format(self.team.name), 'wb') as f:
                pickle.dump(self.predictions, f)
