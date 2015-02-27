import pickle
import User
def populateUserMatrix(userList,line):
    entry = line.split()

    #Build list of unique users
    # if int(entry[0]) not in userList:
    #     userList[int(entry[0])]= u.User(int(entry[1]),int(entry[2]))
    userList[int(entry[0])]= User.User(int(entry[1]),int(entry[2]))

fh_training=open('../data/track2/userid_profile.txt','r')
userList={}

for line in fh_training:
    populateUserMatrix(userList, line)

pickle.dump(userList,open("userProf.p","wb"))
# fh_uid=open('../data/track2/uids.txt','r')
# fh_sync=open('../data/track2/tsync.txt','wa')
#
# uids = fh_uid.read().splitlines()
#
# print len(uids)
# #uids = map(uids,)
#
# count=0
# for line in fh_training :
#     if line.split()[0] in uids:
#         count+=1
#         if count % 1000 == 0:
#             print count
#         fh_sync.write(line)
# fh_sync.close()
