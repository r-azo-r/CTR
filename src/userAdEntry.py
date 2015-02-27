class UserAdEntry:
    'Common base class for all UserAdEntry'
    userid=-1
    adid=-1
    sessionList=[]

    def __init__(self, userid,adid):
        self.userid = userid
        self.adid = adid
