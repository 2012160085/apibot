#job
from datetime import datetime,timedelta

__configure__ = None
def setconfigure(conf):
    global __configure__
    __configure__ = conf
    for key in ["range_from","range_to"]:
        if key not in conf.keys():
            raise Exception(key + " key not exist in config")
    return __configure__

def createjob(codes):
    yyyymm = set()
    yyyymm.add(datetime.today().strftime('%Y%m'))
    yyyymm.add((datetime.now() - timedelta(1)).strftime('%Y%m'))
    joblist=[]
    for date in yyyymm:
        for code in codes:
            if code < __configure__["range_to"] and code >= __configure__["range_from"]:
                joblist.append({
                    'LAWD_CD': code,
                    'DEAL_YMD': date
                })
    return joblist
