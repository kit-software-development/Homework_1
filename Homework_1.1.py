import csv
import math
import json
import numpy as np

def init(userA):
    data, context_place, context_day = reader()
    find_similarity(data, userA)
    sim, simval =find_similarity(data, userA)
    result_ratings =calculated_mark(userA, data, sim)
    film = place_day_array(userA, data, context_place, context_day, simval)
    dictionary ={ "User": userA,
                 "1":result_ratings,
                 "2":film}
    with open("data_file.json", "w") as write_file:
        json.dump(dictionary, write_file)



def reader():
    if __name__ == "__main__":
         csv_path = "data.csv"
         with open(csv_path, "rU") as file_obj:
             data = list(csv.reader(file_obj))

    if __name__ == "__main__":
        csv_path = "context_place.csv"
        with open(csv_path, "rU") as file_obj:
            context_place = list(csv.reader(file_obj))
    
    if __name__ == "__main__":
        csv_path = "context_day.csv"
        with open(csv_path, "rU") as file_obj:
            context_day = list(csv.reader(file_obj))

    return data, context_place, context_day

def averageMark(data, i):
    """ Расчет средней оценки пользователя """
    mark = 0
    n = 0

    for j in range(1,len(data[0])):
        if(data[i][j]!=' -1'):
            mark+=float(data[i][j])
            n+=1

    return round(float(mark/n),3)


def film_average_mark(data, mov):
    """ Расчет средней оценки фильма"""
    mark=0
    n=0
    j=data[0].index(mov)

    for i in range(1, len(data)):
        if(int(data[i][j])!=-1):
            mark+=float(data[i][j])
            n+=1

    return round(float(mark/n), 3)


def find_similarity(data, userA):
    """ Поиск одинаковых пользователей """
    simval = []
    sim =[]

    for i in range(1,len(data)):
        top=0
        down=0
        downA=0

        for j in range(1,len(data[0])):
            if(int(data[i][j])!=-1 and int(data[userA][j])!=-1):
                downA+=float(data[userA][j])**2
                down+=float(data[i][j])**2
                top+=float(data[userA][j])*(float(data[i][j]))      
        simval.append(round(top/(math.sqrt(downA)*math.sqrt(down)),3))

    for val in sorted(simval, reverse = True)[0:5]:
        r = averageMark(data, int(simval.index(val)+1))
        sim.append([simval.index(val)+1, val, r])

    return sim, simval


def calculated_mark(userA, data, sim):
    """Расчет оценок для всех фильмов, которые не смотрел пользователь """
    res=[]
    result_ratings ={}
    k=sim[0][2]
  
    for j in range(1,len(data[0])):
            if (int(data[userA][j])==-1):
                up=0
                down=0

                for i in range(1,5):
                    if(int(data[sim[i][0]][j])!=-1):
                        up+=float(sim[i][1])*(float(data[sim[i][0]][j])-float(sim[i][2]))
                        down+=float(sim[i][1])
                res.append([j, round(k+up/down,3)])
                    
    for i in range(0, len(res)):
        result_ratings.update({data[0][res[i][0]]:res[i][1]})

    return result_ratings 



def place_day_array(userA, data, context_place, context_day, simval):
    """ Выработка контекстных рекомендаций """
    film={}
    info=[]

    for i in range(1,len(data)):
        for j in range(1,len(data[0])):
            if(context_place[i][j]==' h' and (context_day[i][j]==' Sun' or context_day[i][j]==' Sat') 
               and data[userA][j]==' -1'):
                info.append([context_place[0][j], context_place[i][0][5:], float(data[i][j]), simval[i-1]])
                    
    for val in sorted(info,  key=lambda a_entry: (-a_entry[3], -a_entry[2])):
        if(float(val[2])>averageMark(data, int(val[1]))):
            r=film_average_mark(data, val[0])
            film[val[0]]=r
            break

    return film

UserA = 19
init(UserA)