import pickle
import User
# def populateUserMatrix(userList,line):
#     entry = line.split()
#
#     #Build list of unique users
#     # if int(entry[0]) not in userList:
#     #     userList[int(entry[0])]= u.User(int(entry[1]),int(entry[2]))
#     userList[int(entry[0])]= User.User(int(entry[1]),int(entry[2]))
#
# fh_training=open('../data/track2/userid_profile.txt','r')
# userList={}
#
# for line in fh_training:
#     populateUserMatrix(userList, line)
#
# pickle.dump(userList,open("userProf.p","wb"))
fh_user=open('../data/track2/userid_profile.txt','r')
fh_uid=open('../data/track2/k4uids.txt','r')
user_sync=open('../data/track2/k4sync-users.txt','wa')

uids = fh_uid.read().splitlines()
uids=set(uids)

print len(uids)
#uids = map(uids,)

count=0
for line in fh_user :
    if line.split()[0] in uids:
        count+=1
        if count % 10 == 0:
            print count
        user_sync.write(line)
user_sync.close()
