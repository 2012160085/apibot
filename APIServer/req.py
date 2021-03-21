import requests
import json
from datetime import datetime,timedelta
import time
import os
import xml.etree.ElementTree as ET
import xmltodict
import pymysql
#  main.py

class RequestWorker:
    def __init__(self):
        with open("workconf.json",encoding='utf-8') as json_file:
            conf_data = json.load(json_file)
            self.apiurl = conf_data['apiurl']
            self.apikey = conf_data['apikey']
            self.rangefrom = conf_data['range_from']
            self.rangeto = conf_data['range_to']
            self.dburl = conf_data['db_url']
            self.dbusr = conf_data['db_usr']
            self.dbpwd = conf_data['db_pwd']
            self.dbname = conf_data['db_name']
            self.joblogdir = conf_data['joblogdir']
            self.logfile = conf_data['logdir']
            self.retry = conf_data['retry']
        with open("lawd_cd.json",encoding='utf-8') as json_file:
            lawd_cd_data = json.load(json_file)
        between = (lambda x : x >= self.rangefrom and x < self.rangeto)
        self.code_alc = list(filter(between,list(lawd_cd_data.keys())))
        self.get_dbcursor()
    def get_dbcursor(self):
        conn = pymysql.connect(host=self.dburl, user=self.dbusr, 
                               password=self.dbpwd, db=self.dbname,
                               charset='utf8')
        self.cursor = conn.cursors()
    def write_work(self,work):
        with open(self.logfile, "a") as f:
            f.write("+".join(work))
    def get_response(self,pnum,lawd_cd,deal_ymd):
        params = {'ServiceKey': self.apikey, 
                  'pageNo': pnum,
                  'numOfRows': '50',
                  'LAWD_CD': lawd_cd,
                  'DEAL_YMD': deal_ymd
                  }
        print(params)
        res = requests.get(self.apiurl,params=params)
        return res
    def res_value(self,pnum,lawd_cd,deal_ymd):
        res = self.get_response(pnum,lawd_cd,deal_ymd)
        for _ in range(int(self.retry)):
            if res.status_code == 200:
                break
            else:
                time.sleep(3)
                res = self.get_response(pnum,lawd_cd,deal_ymd)
        return self.parseXml(res.text)
    def get_workdates(self):
        yyyymm = set()
        yyyymm.add(datetime.today().strftime('%Y%m'))
        yyyymm.add((datetime.now() - timedelta(1)).strftime('%Y%m'))
        return list(yyyymm)
    def get_jobs(self,date):
        jobs = {}
        filename = date + self.joblogdir
        if os.path.exists(filename):
            with open(filename, "r") as f:
                log = f.readlines()
            log = [x.split() for x in log]
            for job in log:
                jobs[job[0]] = job[1]
        return jobs
    def parseXml(self,xmlStr):
        info = {}
        dict_type = xmltodict.parse(xmlStr)
        json_type = json.dumps(dict_type)
        dict2_type = json.loads(json_type)
        return dict2_type
    def insert_data(self):
        return 0
    def run(self):
        dates = self.get_workdates()
        for date in dates:
            jobs = self.get_jobs(date)
            for code in self.code_alc:
                val_dict = self.res_value("1",code,date)
                time.sleep(3)          
if __name__=='__main__':
    worker = RequestWorker()
    worker.run()