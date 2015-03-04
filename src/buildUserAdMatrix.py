from __future__ import division
import userAdEntry as ua
import User as u
import Session
import math
import random

def score(clk,imp,p_ctr):
    mse = lambda clicks, impressions, p_ctr: math.pow(clicks/impressions-p_ctr,2.0)
    return mse(clk,imp,p_ctr)

def updateUserAdEntry(obj,entry):
    session= Session.Session()
    session.click = int(entry[0])
    session.depth = int(entry[5])
    session.impression = int(entry[1])
    session.position = int(entry[6])
    session.queryId = int(entry[7])
    obj.sessionList.append(session)

def addNewUserAdEntry(userAdList,entry):
    userObj = ua.UserAdEntry(int(entry[-1]),int(entry[3]))
    session= Session.Session()
    session.click = int(entry[0])
    session.depth = int(entry[5])
    session.impression = int(entry[1])
    session.position = int(entry[6])
    session.queryId = int(entry[7])

    userObj.sessionList.append(session)
    userAdList[(int(entry[-1]),int(entry[3]))] = userObj

def populateUserAdMatrix(userAdList,userList,line):
    entry = line.split()

    #Fix to not add user 0
    if int(entry[-1]) != 0:
        #increment query count for the user
        if int(entry[-1]) in userList:
            userList[int(entry[-1])].queryCount+=int(entry[1])

        #Add entry to user-ad matrix
        if (int(entry[-1]), int(entry[3])) in userAdList.keys():
            updateUserAdEntry(userAdList[(int(entry[-1]), int(entry[3]))], entry)
        else:
            addNewUserAdEntry(userAdList, entry)

def populateUserMatrix(userList,line):
    entry = line.split()

    #Build list of unique users
    # if int(entry[0]) not in userList:
    #     userList[int(entry[0])]= u.User(int(entry[1]),int(entry[2]))
    userList[int(entry[0])]= u.User(int(entry[1]),int(entry[2]))

def readData(userAd_file,user_file):

    #storage
    userAdList={}
    userList={}

    # read from input
    fh = open(user_file, 'r')
    for line in fh:
        populateUserMatrix(userList, line)

    fh = open(userAd_file, 'r')
    for line in fh:
        populateUserAdMatrix(userAdList,userList,line)

    return (userAdList,userList)

def getAudienceForAd(adid,userAdList):
    #TODO Add threshold based on user-ad score to limit the number of users
    tmpUserList = [userAdList[x].userid for x in userAdList.keys() if x[1]==adid ]
    return list(set(tmpUserList))

#Logic to identify ads with multiple users
def getAdsWithMultipleUsers(userAdList):
    testAd = []
    dup = []
    for key in userAdList.keys():
        if key[1] in testAd: #if adid in testad list
            dup.append(key[1])
        else:
            testAd.append(key[1])
    return list(set(dup))

def computeAggregateSimilarity(test_user,test_adid,userAdList,userList):
    simUsers=getAudienceForAd(test_adid,userAdList)

    #Fix to remove 0 user as it is unknown
    #simUsers=filter(lambda a: a != 0, simUsers)

    scores_userAd=[]
    user_sim=[]
    similarityScore=[]
    for x in simUsers:
        tempTuple=(x,test_adid)
        score_userSim=userList[test_user].similarity(userList[x])

        #TODO change this to use a different metric to score user-ad association
        score_userAd=userAdList[tempTuple].score(userAdList[tempTuple].scoreMetric1_fix(userList))

        user_sim.append(score_userSim)
        scores_userAd.append(score_userAd)
        similarityScore.append(score_userSim*score_userAd)

    # print scores_userAd
    # print user_sim
    # print similarityScore
    # print len(scores_userAd)
    # print len(user_sim)
    # print len(similarityScore)
    return sum(similarityScore)/len(similarityScore) if len(similarityScore) > 0 else 0

def computeCTR(test_user,test_adid,userAdList,userList):
    #remove a datapoint
    temp=userAdList.pop((test_user,test_adid))
    score=computeAggregateSimilarity(test_user,test_adid,userAdList,userList)
    #put back
    if temp is not None:
        userAdList[(test_user,test_adid)]=temp
    return score

def testCTR(userAdList,userList,n):
    if n == 0:
        testSet=[ (5276025, 7409307), (654889, 10396332), (1544886, 20549646), (2853641, 21162426), (58791, 9025386),(1307537, 20183684), (677596, 8676724), (3336229, 4345226), (13903553, 8676728), (2990599, 9584595),(9459266, 6960975)]
    else:
        testSet = pickNRandomValues(10,userAdList)
    #testSet = pickNRandomValues(5,userAdList)
    #testSet=[(getAudienceForAd(20172874)[0],20172874),(getAudienceForAd(21522776)[0],21522776)]
    scores=[]
    #repeat n times
    for i in range(0,len(testSet)):
        p_ctr = computeCTR(testSet[i][0],testSet[i][1],userAdList,userList)
        tuple = (testSet[i][0],testSet[i][1])
        click_impList = [(x.click,x.impression) for x in userAdList[tuple].sessionList]
        click_sum=sum([x[0] for x in click_impList])
        imp_sum = sum([x[1] for x in click_impList])
        scores.append((click_sum,imp_sum,p_ctr))
    return scores

def pickNRandomValues(n,userAdList):
    keyList=[]
    keys=userAdList.keys()
    for i in range(0,n):
        r_val = random.randint(0,len(keys))
        keyList.append(keys[r_val])
    return keyList

# userAd_file = '../data/track2/msync-training.txt'
# user_file = '../data/track2/msync-users.txt'
# (userAdList,userList)=readData(userAd_file,user_file)