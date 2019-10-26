import csv
import math
import json
import numpy as np

class MovieRating:

    def __init__(self):
        self.array=[]
        self.context_place=[]
        self.context_day=[]
        self.userA=19
        self.sim=[]
        self.matrix=[]

    def reader(self):
        if __name__ == "__main__":
             csv_path = "data.csv"
             with open(csv_path, "rU") as file_obj:
                 self.array = list(csv.reader(file_obj))
                 self.secdat = list(csv.reader(file_obj))
        
        if __name__ == "__main__":
            csv_path = "context_place.csv"
            with open(csv_path, "rU") as file_obj:
                self.context_place = list(csv.reader(file_obj))

        if __name__ == "__main__":
            csv_path = "context_day.csv"
            with open(csv_path, "rU") as file_obj:
                self.context_day = list(csv.reader(file_obj))

        self.find_similarity()
        self.place_day_array()
        self.json_writer()


    def json_writer(self):
        dictionary ={ "user": self.userA,
                     "1":self.mov,
                     "2":self.film}
        with open("data_file.json", "w") as write_file:
            json.dump(dictionary, write_file)
        print(dictionary)


    def film_average_mark(self, mov):
        """ Расчет средней оценки фильма"""
        mark=0
        n=0
        j=self.array[0].index(mov)
        for i in range(1, len(self.array)):
            if(int(self.array[i][j])!=-1):
                mark+=float(self.array[i][j])
                n+=1
        return round(float(mark/n), 3)


    def averageMark(self, i):
        """ Расчет средней оценки пользователя """
        mark=0
        n=0
        for j in range(1,len(self.array[0])):
                if(int(self.array[i][j])!=-1):
                   mark+=float(self.array[i][j])
                   n+=1
        return round(float(mark/n),3)
                

    def calculated_mark(self):
        """Расчет оценок для всех фильмов, которые не смотрел пользователь """
        up=0
        down=0
        res=[]
        self.mov={}
        for j in range(1,len(self.array[0])):
                if (int(self.array[self.userA][j])==-1):
                    
                    k=self.matrix[0][2]
                    for i in range(1,5):
                        if(int(self.array[self.matrix[i][0]][j])!=-1):
                            up=float(self.matrix[i][1])*(float(self.array[self.matrix[i][0]][j])-float(self.matrix[i][2]))
                            down+=float(self.matrix[i][1])
                            
                    res.append([j, round(k+up/down,3)])
                    
        for i in range(0, len(res)):
            self.mov.update({self.array[0][res[i][0]]:res[i][1]})
        

    def find_similarity(self):
        """ Поиск одинаковых пользователей """
        for i in range(1,len(self.array)):
            top=0
            down=0
            downA=0
            for j in range(1,len(self.array[0])):
                if(int(self.array[i][j])!=-1 and int(self.array[self.userA][j])!=-1):
                    downA+=float(self.array[self.userA][j])**2
                    down+=float(self.array[i][j])**2
                    top+=float(self.array[self.userA][j])*(float(self.array[i][j]))
                    
                    
            self.sim.append(round(top/(math.sqrt(downA)*math.sqrt(down)),3))

        for val in sorted(self.sim, reverse = True)[0:5]:
            r=self.averageMark(int(self.sim.index(val)+1))
            self.matrix.append([self.sim.index(val)+1, val, r])
        self.calculated_mark()


    def place_day_array(self):
        """ Выработка контекстных рекомендаций """
        self.film={}
        a=[]

        for i in range(1,len(self.array)):
            for j in range(1,len(self.array[0])):
                if(self.context_place[i][j]==' h' and (self.context_day[i][j]==' Sun' or self.context_day[i][j]==' Sat') 
                   and self.context_place[self.userA][j]==' -1'):
                    a.append([self.context_place[0][j], self.context_place[i][0], self.array[i][j], self.sim[i-1]])
                    
        for val in sorted(a,  key=lambda a_entry: a_entry[3], reverse = True):
            if(val[2]==' 5' or val[2]==' 4'):
                r=self.film_average_mark(val[0])
                self.film[val[0]]=r
                break



userRating=MovieRating()
userRating.reader()
