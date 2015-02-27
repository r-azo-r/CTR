import math
class User:
    age = -1
    gender = -1
    queryCount=-1

    def __init__(self,gender,age):
        self.age=age
        self.gender=gender
        self.queryCount = -1

    #Higher the value the more similar they ares
    def similarity(self,other):
        gamma = 3#2
        sigma = 1.5
        offset = 0#1

        sim =-1
        if self.age == other.age and self.gender == other.gender:
            sim =  sigma
        else:
            g_self = (self.gender + offset) * gamma;
            g_oth = (other.gender + offset) * gamma;
            sim = 1/math.sqrt((g_self - g_oth)^2 + (self.age - other.age)^2)

        return sim