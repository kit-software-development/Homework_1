import io
from collections import defaultdict
from surprise import KNNBaseline
from surprise import Dataset
from surprise import get_dataset_dir


def get_rid_to_item_mapping():
    """Read the u.item file from MovieLens 100-k dataset and return two
    mappings to convert raw ids into movie names and movie names into raw ids.
    """
    file_name = get_dataset_dir() + '/ml-100k/ml-100k/u.item'
    rid_to_name = {}
    with io.open(file_name, 'r', encoding='ISO-8859-1') as f:
        for line in f:
            line = line.split('|')
            rid_to_name[line[0]] = (line[1], line[2])

    return rid_to_name

def get_top_n(predictions, n=5):
    '''Return the top-N recommendation for each user from a set of predictions.
    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.
    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, round(est, 3)))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:5]

    return top_n

uid = str(19)
k = 4
n = 5

# First train an SVD algorithm on the movielens dataset.
data = Dataset.load_builtin('ml-100k')
trainset = data.build_full_trainset()
sim_options = {'name': 'cosine', 'user_based': True, 'min_support': 5}
algo = KNNBaseline(k=4, sim_options=sim_options)
algo.fit(trainset)

testset = trainset.build_anti_testset()
testset = filter(lambda x: x[0] == uid, testset)
predictions = algo.test(testset)
top_n = get_top_n(predictions, n=5)
rid_to_item_mapping = get_rid_to_item_mapping()

print('User '+ str(uid))
for movie_rid, rating in top_n[uid]:
    print(movie_rid, str(rid_to_item_mapping[movie_rid]), rating)