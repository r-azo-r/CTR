from __future__ import division
import userAdEntry as ua
import User as u
import Session

def updateUserAdEntry(obj,entry):
    session= Session.Session()
    session.click = int(entry[0])
    session.depth = int(entry[5])
    session.impression = int(entry[1])
    session.position = int(entry[6])
    session.queryId = int(entry[7])
    obj.sessionList.append(session)

def addNewUserAdEntry(userAdList,entry):
    userObj = ua.UserAdEntry(entry[-1],entry[3])
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

    #increment query count for the user
    if int(entry[-1]) in userList:
        userList[int(entry[-1])].queryCount+=1

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

def readData():

    #storage
    userAdList={}
    userList={}

    # read from input
    userAd_file = '../data/track2/msync-training.txt'
    user_file = '../data/track2/msync-users.txt'
    fh = open(user_file, 'r')
    for line in fh:
        populateUserMatrix(userList, line)

    fh = open(userAd_file, 'r')
    for line in fh:
        populateUserAdMatrix(userAdList,userList,line)

    return (userAdList,userList)

(userAdList,userList)=readData()
tempScores = [userAdList[x].score(userAdList[x].scoreMetric1()) for x in userAdList.keys()]

# percentage who never click on an ad
print sum([1 for x in tempScores if x > 0.5])/len(tempScores)

print min(tempScores)
print max(tempScores)
print len(userAdList)
print len(userList)

