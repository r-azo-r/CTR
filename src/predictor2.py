import buildUserAdMatrix as model
import subprocess

def computeAccuracy(result_set,num):
    fh_p = open('submission'+`num`+'.csv','wa')
    fh_s = open('solution'+`num`+'.csv','wa')
    for tuple in result_set:
        fh_p.write(`tuple[-1]`+"\n")
        fh_s.write(`tuple[0]`+","+`tuple[1]`+"\n")
    fh_p.close()
    fh_s.close()
    #execfile("scoreKDD.py","solution.csv","submission.csv")


userAd_file = '../data/track2/k2sync-training.txt'
user_file = '../data/track2/k2sync-users.txt'
(userAdList,userList)=model.readData(userAd_file,user_file)


#TODO Testing
#test_adid=20172874 #21522776
#test_user=getAudienceForAd(test_adid)[0]

result_set = model.testCTR(userAdList,userList)
computeAccuracy(result_set,3)

