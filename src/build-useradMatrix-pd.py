from __future__ import division
import pandas as pd
import userAdEntry as ua
import User as u
import Session

def readData():

    # read from input
    userAd_file = '../data/track2/ksync-training.txt'
    user_file = '../data/track2/ksync-users.txt'
    userAd_col = ['click','imps','dUrl','adId','advId','depth','pos','qId','keyId','titleId','descId','userId']
    user_col = ['userId','gender','age']
    userAdDf=pd.read_csv(userAd_file,sep='\t',engine='c')
    userAdDf.columns = userAd_col
    userDf=pd.read_csv(user_file,sep='\t',engine='c')
    userDf.columns = user_col
    return (userAdDf,userDf)

(userAdDf,userDf)=readData()
#flatDf=pd.merge(userAdDf, userDf, left_on='userId', right_on='userId', how='inner')
#print flatDf
#got each record grouped by user,adId
#flatDFGrouped=flatDf.groupby(['userId','adId'])
print len(userAdDf)
print len(userDf)
# for name,group in flatDFGrouped:
#      print name

#selecting based on certain criterion

#criterion = flatDf[['userId','adId']]
#print flatDf[['userId','adId']]



