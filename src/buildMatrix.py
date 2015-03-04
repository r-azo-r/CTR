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

userAd_file = '../data/track2/msync-training.txt'
user_file = '../data/track2/msync-users.txt'
(userAdDf,userDf)=readData(userAd_file,user_file)

#(userAdList,userList)=build(userAdDf,userDf)

plotUserAd(userAdDf.iloc[:,[-1,3]])