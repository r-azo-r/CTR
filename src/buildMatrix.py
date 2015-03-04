from __future__ import division
import pandas as pd
import userAdEntry as ua
import User as u
import Session
import matplotlib.pyplot as plt


def readData(userAd_file,user_file):
    # read from input
    userAd_col = ['click','imps','dUrl','adId','advId','depth','pos','qId','keyId','titleId','descId','userId']
    user_col = ['userId','gender','age']
    userAdDf=pd.read_csv(userAd_file,sep='\t',engine='c')
    userAdDf.columns = userAd_col
    userAdDf = userAdDf[userAdDf.userId != 0]

    userDf=pd.read_csv(user_file,sep='\t',engine='c')
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

def computeAggregateSimilarity(test_user,test_adid,userAdDf,userDf):
    simUsers=userAdDf[userAdDf.adId == testad]['userId']
    simUsers = simUsers.where(simUsers != test_user).dropna().unique()

    scores_userAd=[]
    user_sim=[]
    similarityScore=[]
    testU=userDf[userDf.userId == test_user]
    testUserObj = u.User(testU.gender.values[0],testU.age.values[0])
    for x in simUsers:
        #Perform user similarity
        xU=userDf[userDf.userId == x]
        #TODO Fix for users not in userDF , not sure why this is happening
        if not xU.empty:
            xUserObj = u.User(xU.gender.values[0],xU.age.values[0])
            score_userSim=testUserObj.similarity(xUserObj)
            user_sim.append(score_userSim)
            # #TODO change this to use a different metric to score user-ad association
            #Build UserAd object from data frame
            (testUserAdObj,qc) = buildUserAdObj(x,test_adid,userAdDf)
            score_userAd=testUserAdObj.score(testUserAdObj.scoreMetric1_fix2(qc))

            user_sim.append(score_userSim)
            scores_userAd.append(score_userAd)
            similarityScore.append(score_userSim*score_userAd)
    print user_sim
    print scores_userAd
    print similarityScore

def computeCTR(test_user,test_adid,userAdDf,userDf):
    #remove a datapoint
    temp=userAdDf[(UserAdDf.userId != test_user) & (userAdDf.adId != test_adid)]
    score=computeAggregateSimilarity(test_user,test_adid,temp,userDf)
    return score

#TODO need to complete this
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

userAd_file = '../data/track2/ksync-training.txt'
user_file = '../data/track2/ksync-users.txt'
(userAdDf,userDf)=readData(userAd_file,user_file)
testad=20172874
testuser=userAdDf[userAdDf.adId == testad]['userId'].values[0]

print computeAggregateSimilarity(testuser,testad,userAdDf,userDf)
#result_set = testCTR(userAdList,userList,10)
#computeAccuracy(result_set,2)

