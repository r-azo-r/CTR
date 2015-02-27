from __future__ import division

class UserAdEntry:
    'Common base class for all UserAdEntry'
    userid=-1
    adid=-1

    sessionList=None

    def __init__(self, userid,adid):
        self.userid = userid
        self.adid = adid
        self.sessionList=list()

    #TODO Need to enhance this function
    def score(self,f=lambda x : 1 if x.click > 0 else 0):
        #return sum(1 for x in self.sessionList if f(x))
        return f

    def scoreMetric1(self):
        alpha =1
        beta = 1
        #sum([alpha*((x.click*x.position)/(x.impression*x.depth))+((x.impression/len(self.sessionList))*beta) for x in self.sessionList])
        return  sum([(x.click/x.impression) * (x.position/x.depth) for x in self.sessionList]) * alpha \
            + sum([x.impression for x in self.sessionList])/len(self.sessionList) * beta


    def scoreMetric2(self,userList):
        alpha =0.5
        beta = 0.5
        #gamma = 1
        f1 = sum([1 for x in self.sessionList if x.click > 0])/len(self.sessionList)
        f2 = len(self.sessionList)/userList[self.userid].queryCount if self.userid in userList  else 0
        return alpha*f1 + beta*f2
