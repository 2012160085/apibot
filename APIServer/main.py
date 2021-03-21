from zipgapbot import apirequest,configmaker,dbwork,jobs
from zipgapbot import logger
import time




def work(job,page,jobConfiguration):
    job["pageNo"] = str(page) 
    job["numOfRows"] = '50'
    job["ServiceKey"] = jobConfiguration["apikey"]
    resultCode, totalCount, itemlist = apirequest.get_response(jobConfiguration["apiurl"],job)
    while resultCode != "00":
        time.sleep(1)
        resultCode, totalCount, itemlist = apirequest.get_response(jobConfiguration["apiurl"],job)
    return totalCount, itemlist

def getitemlist(joblist,columnMapper):
    result = {}
    for job in joblist:
        indb = dbwork.sel_pk(job['DEAL_YMD'],job['LAWD_CD'])
        totalCount, itemlist = work(job,1,jobConfiguration)
        result.update(insertdata(totalCount,itemlist,indb,columnMapper))
        for i in range(1,int(totalCount)//50):
            totalCount, itemlist = work(job,1+i,jobConfiguration)
            result.update(insertdata(totalCount,itemlist,indb,columnMapper))
    return result   


def insertdata(totalCount,itemlist,indb,columnMapper):
    result = {}
    for item in itemlist:
        if '일련번호' not in item:
            continue
        pk = '+'.join([item['년'],item['월'],item['일'],item['일련번호']])
        if pk in indb:
            result[pk] = 'already exist'
        else:
            sql = dbwork.makequery("tb_api00",item,columnMapper)
            dbwork.execute_commit(sql)
            result[pk] = 'insert'
    return result



if __name__ == "__main__":
    jobConfiguration = (configmaker.readconf("jobConfiguration.json"))
    regnCodes = (configmaker.readconf("regnCodes.json"))
    columnMapper = (configmaker.readconf("columnMapper.json"))
    
    logger.setconfigure(jobConfiguration)
    dbwork.setconfigure(jobConfiguration)
    jobs.setconfigure(jobConfiguration)

    apiurl = jobConfiguration["apiurl"]
    joblist = jobs.createjob(regnCodes)
    result = getitemlist(joblist,columnMapper)



    


