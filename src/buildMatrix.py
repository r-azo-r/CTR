from __future__ import division
import pandas as pd
import userAdEntry as ua
import User as u
import Session
import matplotlib.pyplot as plt
import random


def readData(userAd_file,user_file):
    # read from input
    userAd_col = ['click','imps','dUrl','adId','advId','depth','pos','qId','keyId','titleId','descId','userId']
    user_col = ['userId','gender','age']
    #userAdDf=pd.io.parsers.read_table(userAd_file)
    userAdDf=pd.read_csv(userAd_file,sep='\t',lineterminator ='\n',engine='c')
    userAdDf.columns = userAd_col
    userAdDf = userAdDf[userAdDf.userId != 0]

    userDf=pd.read_csv(user_file,sep='\t',lineterminator ='\n',engine='c')
    userDf.columns = user_col
    return (userAdDf,userDf)

def build(userAd_Df,user_Df):

    #storage
    userAdList={}
    userList={}

    # read from input
    for line,row in user_Df.iterrows():
        populateUserMatrix(userList, row)

    for line,row in userAd_Df.iterrows():
        populateUserAdMatrix(userAdList,userList,row)

    return (userAdList,userList)

def populateUserAdMatrix(userAdList,userList,line):
    entry = line
    #increment query count for the user
    if int(entry[-1]) in userList:
        userList[int(entry[-1])].queryCount+=int(entry[1])

    #Add entry to user-ad matrix
    if (int(entry[-1]), int(entry[3])) in userAdList.keys():
        updateUserAdEntry(userAdList[(int(entry[-1]), int(entry[3]))], entry)
    else:
        addNewUserAdEntry(userAdList, entry)

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

def populateUserMatrix(userList,line):
    entry = line

    #Build list of unique users
    # if int(entry[0]) not in userList:
    #     userList[int(entry[0])]= u.User(int(entry[1]),int(entry[2]))
    userList[int(entry[0])]= u.User(int(entry[1]),int(entry[2]))

def plotUserAd(df):
    min_adId=min(df['adId'])
    min_userId=min(df['userId'])
    print "Scatter"
    plt.scatter(map(lambda x: x - min_adId,df['adId']),map(lambda x: x - min_userId,df['userId']),marker='.')
    plt.ylabel('Users')
    plt.xlabel('Ads')
    plt.xlim(0,max(df['adId']))
    plt.ylim(0,max(df['userId']))
    # # plt.title('2 most popular hashtags')
    plt.show()

def getAudienceForAd(adid,userAdList):
    #TODO Add threshold based on user-ad score to limit the number of users
    tmpUserList = [userAdList[x].userid for x in userAdList.keys() if x[1]==adid ]
    return list(set(tmpUserList))

def buildUserAdObj(user,ad,userAdDf):
    #get userAdFrame
    userAdFrame = userAdDf[(userAdDf.userId == user) & (userAdDf.adId == ad)]
    userObj = ua.UserAdEntry(user,ad)
    imps = 0
    for row in userAdFrame.values:
        session= Session.Session()
        session.click = int(row[0])
        session.depth = int(row[5])
        session.impression = int(row[1])
        imps += session.impression
        session.position = int(row[6])
        session.queryId = int(row[7])
        userObj.sessionList.append(session)
    return (userObj,imps)

def computeAggregateSimilarity(test_user,test_adid,userAdDf,userDf,SimUserthreshold):# = 40
    simUsers=userAdDf[userAdDf.adId == test_adid]['userId']
    simUsers = simUsers.where(simUsers != test_user).dropna().unique()
    if len(simUsers) > SimUserthreshold:
        simUsers=random.sample(simUsers,SimUserthreshold)
    scores_userAd=[]
    user_sim=[]
    similarityScore=[]
    testU=userDf[userDf.userId == test_user]
    testUserObj = u.User(testU.iloc[0,-2],testU.iloc[0,-1])#.gender.values[0],testU.age.values[0])
    for x in simUsers:
        #Perform user similarity
        xU=userDf[userDf.userId == x]
        #TODO Fix for users not in userDF , not sure why this is happening
        #if not xU.empty:
        #xUserObj = u.User(xU.gender.values[0],xU.age.values[0])
        if len(xU) > 0:
            xUserObj = u.User(xU.iloc[0,-2],xU.iloc[0,-1])
            score_userSim=testUserObj.similarity(xUserObj)

            # #TODO change this to use a different metric to score user-ad association
            #Build UserAd object from data frame
            (testUserAdObj,qc) = buildUserAdObj(x,test_adid,userAdDf)
            score_userAd=testUserAdObj.score(testUserAdObj.scoreMetric1_fix2(qc))

            user_sim.append(score_userSim)
            scores_userAd.append(score_userAd)
            similarityScore.append(score_userSim*score_userAd)
    # print user_sim
    # print scores_userAd
    # print similarityScore
    return sum(similarityScore)/len(similarityScore) if len(similarityScore) > 0 else 0

def computeCTR(test_user,test_adid,userAdDf,userDf):
    #remove a datapoint
    temp=userAdDf[(userAdDf.userId != test_user) & (userAdDf.adId != test_adid)]
    score=computeAggregateSimilarity(test_user,test_adid,temp,userDf)
    return score

#TODO need to complete this
def testCTR(userAdDf,userDf,n):
    if n == 0:
        testSet=[ (5276025, 7409307), (654889, 10396332), (1544886, 20549646), (2853641, 21162426), (58791, 9025386),(1307537, 20183684), (677596, 8676724), (3336229, 4345226), (13903553, 8676728), (2990599, 9584595),(9459266, 6960975)]
    else:
        testSet = pickNRandomValues(n,userAdDf)
    scores=[]
    #repeat n times
    for i in testSet:
        p_ctr = computeCTR(i[0],i[1],userAdDf,userDf)
        # obj=buildUserAdObj(testSet[i][0],testSet[i][1],userAdDf)
        # click_impList = [(x.click,x.impression) for x in obj[0].sessionList]
        # click_sum=sum([x[0] for x in click_impList])
        # imp_sum = sum([x[1] for x in click_impList])
        #scores.append((click_sum,imp_sum,p_ctr))
        scores.append(p_ctr)
    return scores

def getRandomRows(x, n):
    return x.ix[random.sample(x.index, n)]

def pickNRandomValues(n,userAdDf):
    keyList=[]
    keys=userAdDf[['userId','adId']]
    userRandomMat = getRandomRows(keys,n)
    return [tuple(x) for x in userRandomMat.values]
    # for i in range(0,n):
    #     r_val = random.randint(0,len(keys))
    #     keyList.append(keys[r_val])
    # return keyList

def repeatNtimes(userAdDf,userDf,n,thres=40):
    robj = getRandomRows(userAdDf,n)
    print "Got Random Rows"
    results = []
    for i in range(0,n):
        if len(userDf[userDf.userId == robj['userId'].values[i]]) > 0:
            #dataObj=buildUserAdObj(robj['userId'].values[i],robj['adId'].values[i],userAdDf)
            (clk,imps)=calculateNormalClickImpressions(robj['userId'].values[i],robj['adId'].values[i],userAdDf)
            print clk,imps
            pctr=computeAggregateSimilarity(robj['userId'].values[i],robj['adId'].values[i],userAdDf,userDf,thres) #userAdDf[(userAdDf.userId != robj['userId'].values[i]) & (userAdDf.adId != robj['adId'].values[i])]
            print pctr
            results.append((clk,imps,pctr))
    return results
    #print i
    #print

#returns clicks and impressions
def calculateNormalClickImpressions(user,ad,userAdDf):
    temp = userAdDf[(userAdDf.userId == user) & (userAdDf.adId == ad)]
    return(sum(temp.iloc[:,0].values),sum(temp.iloc[:,1].values))

def computeAccuracy(result_set,num):
    fh_p = open('submission'+`num`+'.csv','wa')
    fh_s = open('solution'+`num`+'.csv','wa')
    for tuple in result_set:
        fh_p.write(`tuple[-1]`+"\n")
        fh_s.write(`tuple[0]`+","+`tuple[1]`+"\n")
    fh_p.close()
    fh_s.close()


userAd_file = '../data/track2/k4sync-training.txt'
user_file = '../data/track2/k4sync-users.txt'
(userAdDf,userDf)=readData(userAd_file,user_file)
print 'Data set read'

#testad=20172874
#testuser=userAdDf[userAdDf.adId == testad]['userId'].values[0]
#tmp = buildUserAdObj(23459935,20083853,userAdDf)
#print computeAggregateSimilarity(testuser,testad,userAdDf,userDf)
#pickNRandomValues(10,userAdDf)
# robj = getRandomRows(userAdDf,1)
# print computeAggregateSimilarity(robj['userId'].values[0],robj['adId'].values[0],userAdDf,userDf)

#print res
#result_set = testCTR(userAdDf,userDf,0)
#print result_set
#computeAccuracy(result_set,2)

#computeAccuracy(repeatNtimes(userAdDf,userDf,100,80),7)
# computeAccuracy(repeatNtimes(userAdDf,userDf,100,10),11)
# computeAccuracy(repeatNtimes(userAdDf,userDf,100,20),12)
# computeAccuracy(repeatNtimes(userAdDf,userDf,100,40),13)
# computeAccuracy(repeatNtimes(userAdDf,userDf,100,80),14)
# computeAccuracy(repeatNtimes(userAdDf,userDf,100,100),15)
# computeAccuracy(repeatNtimes(userAdDf,userDf,400,10),21)
# computeAccuracy(repeatNtimes(userAdDf,userDf,400,20),22)
# computeAccuracy(repeatNtimes(userAdDf,userDf,400,40),23)
# computeAccuracy(repeatNtimes(userAdDf,userDf,400,80),24)
# computeAccuracy(repeatNtimes(userAdDf,userDf,400,100),25)

#plotUserAd(userAdDf)
#plotUserAd(userAdDf[userAdDf.click > 0])