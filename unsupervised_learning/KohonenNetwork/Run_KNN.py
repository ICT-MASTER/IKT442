from Database import Model
from Unsupervised_Learning.KohonenNetwork.Train import TrainKohonenNetwork
from Supervised_Learning.KNearestNeighbour.Algorithm import TrainKNearestNeighbour

include_ties = True

m = 50
n = 50
iterations = 100

db_teams = [x for x in Model.Team.select()]
for team in db_teams:
    # Kohonen Network
    som = TrainKohonenNetwork(team=team, include_ties=include_ties)
    som.prep_data()
    som.train_som(m, n, iterations)

    # K-Nearest Neighbour
    knn = TrainKNearestNeighbour(team.name, include_ties)
    knn.prep_data(som.training, som.predictions)
    knn.train_knn()
    knn.print_results()
