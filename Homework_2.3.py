import io
from collections import defaultdict
from surprise import KNNWithMeans
from surprise import Dataset
from surprise import get_dataset_dir
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas 


def get_rid_to_item_mapping():
    file_name = get_dataset_dir() + '/ml-100k/ml-100k/u.item'
    rid_to_name = {}
    with io.open(file_name, 'r', encoding='ISO-8859-1') as f:
        for line in f:
            line = line.split('|')
            rid_to_name[line[0]] = (line[1], line[2])
    return rid_to_name


def get_top_n(predictions, n=5):
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, round(est, 3)))
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]
    return top_n

uid = str(8)
k = 4
n = 5

data = Dataset.load_builtin('ml-100k')
trainset = data.build_full_trainset()
sim_options = {'name': 'cosine', 'user_based': True, 'min_support': n}
algo = KNNWithMeans(k, sim_options=sim_options)
algo.fit(trainset)
testset = trainset.build_anti_testset()
testset = filter(lambda x: x[0] == uid, testset)
predictions = algo.test(testset)

top_n = get_top_n(predictions)
rid_to_name = get_rid_to_item_mapping()


chosen_movies=[]
for movie_rid, rating in top_n[uid]:
    print('{:4s} {:<60s} {}'.format(movie_rid, str(rid_to_name[movie_rid]), rating))
    chosen_movies.append(rid_to_name[movie_rid][0])
    
print(chosen_movies)

    
for k,_ in enumerate(chosen_movies):
    chosen_movies[k]=chosen_movies[k][:-6]
    if(',' in chosen_movies[k]):
        temp=chosen_movies[k].split(',')
        chosen_movies[k]=temp[1]+temp[0]
    chosen_movies[k]=chosen_movies[k].strip()


API_ENDPOINT = "https://www.wikidata.org/w/api.php"

films_arr=[]

for name_film in chosen_movies:
    params = {
        'action' : 'wbsearchentities',
        'format' : 'json',
        'language' : 'en',
        'search': name_film
    }
    res = requests.get(API_ENDPOINT, params = params)
    if res.json()['search']:
        for item in res.json()['search']:
            if('film' in item['description']):
                films_arr.append((name_film, item['id']))
                break


sparql = SPARQLWrapper("https://query.wikidata.org/sparql")


for film in films_arr:
    query = """
SELECT DISTINCT ?personLabel ?awardLabel WHERE {
wd:"""+film[1]+""" wdt:P57 ?person .
?person wdt:P166 ?award .
SERVICE wikibase:label { bd:serviceParam wikibase:language "ru,en". }
}
"""
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = (sparql.query().convert())
    for result in results["results"]["bindings"]:
        director = result['personLabel']['value']
        award = result['awardLabel']['value']
        print("{}: {}  -  {}".format(film[0], director ,award))
        
