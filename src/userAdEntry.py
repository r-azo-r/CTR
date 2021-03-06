from __future__ import division
import math

class UserAdEntry:
    'Common base class for all UserAdEntry'
    userid=-1
    adid=-1

    sessionList=None

    def __init__(self, userid,adid):
        self.userid = userid
        self.adid = adid
        self.sessionList=list()

    def score(self,f=lambda x : 1 if x.click > 0 else 0):
        #return sum(1 for x in self.sessionList if f(x))
        return f

    def scoreMetric1(self):
        alpha =1
        beta = 1
        s = sum([(x.click/x.impression) * (x.position/x.depth) for x in self.sessionList]) * alpha \
        + sum([x.impression/(x.impression+len(self.sessionList)) for x in self.sessionList]) * beta
        #sum([alpha*((x.click*x.position)/(x.impression*x.depth))+((x.impression/len(self.sessionList))*beta) for x in self.sessionList])
        return s

    def scoreMetric1_norm(self):
        alpha =1
        beta = 1
        s = sum([(x.click/x.impression) * (x.position/x.depth) for x in self.sessionList])/len(self.sessionList) * alpha \
            + sum([x.impression/(x.impression+len(self.sessionList)) for x in self.sessionList]) * beta
        #sum([alpha*((x.click*x.position)/(x.impression*x.depth))+((x.impression/len(self.sessionList))*beta) for x in self.sessionList])
        return s

    def scoreMetric1_fix(self,userList):
        alpha =0.7
        beta = 0.3
        s = sum([(x.click/x.impression) * (x.position + math.log(x.depth))/x.depth for x in self.sessionList]) * alpha \
            + sum([x.impression for x in self.sessionList])/userList[self.userid].queryCount * beta
        #sum([alpha*((x.click*x.position)/(x.impression*x.depth))+((x.impression/len(self.sessionList))*beta) for x in self.sessionList])
        return s

    def scoreMetric1_fix2(self,queryCount):
        alpha =0.7
        beta = 0.3
        s = sum([(x.click/x.impression) * (x.position + math.log(x.depth))/x.depth for x in self.sessionList]) * alpha \
            + sum([x.impression for x in self.sessionList])/queryCount * beta
        #sum([alpha*((x.click*x.position)/(x.impression*x.depth))+((x.impression/len(self.sessionList))*beta) for x in self.sessionList])
        return s


    def scoreMetric2(self,userList):
        alpha =0.5
        beta = 0.5
        #gamma = 1
        f1 = sum([1 for x in self.sessionList if x.click > 0])/len(self.sessionList)
        f2 = len(self.sessionList)/userList[self.userid].queryCount if self.userid in userList  else 0
        return alpha*f1 + beta*f2
