import userAdEntry as ua
import Session

def updateUserAdEntry(obj,entry):
    session= Session.Session()
    session.click = entry[0]
    session.depth = entry[5]
    session.impression = entry[1]
    session.position = entry[6]
    session.queryId = entry[7]
    obj.sessionList.append(session)

def addNewUserAdEntry(userAdList,entry):
    session= Session.Session()
    session.click = entry[0]
    session.depth = entry[5]
    session.impression = entry[1]
    session.position = entry[6]
    session.queryId = entry[7]

    userObj = ua.UserAdEntry(entry[-1],entry[3])
    userObj.sessionList.append(session)
    userAdList[(entry[-1],entry[3])] = userObj


#storage
userAdlist={}
#read from input
input_file='../data/track2/train-small.txt'
fh=open(input_file,'r')
for line in fh:
    entry= line.split()

    if (entry[-1], entry[3]) in userAdlist.keys():
        updateUserAdEntry(userAdlist[(entry[-1],entry[3])],entry)
        # obj = userAdlist[(c[-1][3])]
        # obj.click +=c[0]
        # obj.queryCount +=1

    addNewUserAdEntry(userAdlist,entry)
    #userAdlist[(c[-1],c[3])]= ua.UserAdEntry(c[-1],c[3],c[0])


print userAdlist